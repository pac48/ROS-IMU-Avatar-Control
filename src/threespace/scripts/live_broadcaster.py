#!/usr/bin/env python
import roslib
import rospy
import serial
import matlab.engine
import time
import math
import collections
import StringIO as io
import numpy as np
from gait_hmm_ros.msg import imu_vector
from gait_hmm_ros.msg import ardu_msg
from threespace_ros.msg import dataVec
from  threespace_ros.msg import GenericFloatArray


def imuCallback(msg, args):
    self = args[0]
    self.refresh = True
    index = args[1]
    topic = args[2]
    startIndex = index * ((3 * self.useAccel) + (3 * self.useGyro))
    currentIndex = 0
    if self.useGyro == 1:
        self.imuVec[startIndex + currentIndex] = msg.gyroX
        currentIndex += 1
        self.imuVec[startIndex + currentIndex] = msg.gyroY
        currentIndex += 1
        self.imuVec[startIndex + currentIndex] = msg.gyroZ
        currentIndex += 1
    if self.useAccel == 1:
        self.imuVec[startIndex + currentIndex] = msg.accX
        currentIndex += 1
        self.imuVec[startIndex + currentIndex] = msg.accY
        currentIndex += 1
        self.imuVec[startIndex + currentIndex] = msg.accZ
        # print currentIndex + startIndex
        # print("---------------------------------")


def arduCallback(msg, args):
    self = args[0]
    pos = self.imuCount * (3 * self.useGyro + 3 * self.useAccel)
    # print msg
    # print('-------------')
    # print pos
    self.refresh = True
    if self.ir == 1:
        self.imuVec[pos] = msg.ir
    if self.prox == 1:
        self.imuVec[pos + self.ir] = msg.prox
    if self.fsr == 1:
        self.imuVec[pos + self.ir + self.prox] = msg.fsrfl
        self.imuVec[pos + self.ir + self.prox + 1] = msg.fsrfr
        self.imuVec[pos + self.ir + self.prox + 2] = msg.fsrbk
    pass


class LiveBroadcaster:
    def createArray(self):
        pass

    def __init__(self, acb=arduCallback, imc=imuCallback):
        rospy.init_node('liveBroadCaster')
        self.port = rospy.get_param("~port_live", "/dev/ttyACM0")
        PORT = self.port
        BAUD_RATE = 9600
        while True:
            try:
                print("Trying to bind port " + PORT)
                ser = serial.Serial(PORT, BAUD_RATE)
                break
            except:
                rospy.sleep(1)
                continue

        self.acb = acb
        self.imc = imc

        self.combinedVector = []
        self.imuVec = []
        self.arVec = []

        self.matlabMsg = GenericFloatArray()

        self.useGyro = rospy.get_param("~use_gyro_n", 0)
        self.useAccel = rospy.get_param("~use_accel_n", 0)
        self.fsr = rospy.get_param("~fsr_n", 1)
        self.ir = rospy.get_param("~ir_n", 1)
        self.prox = rospy.get_param("~prox_n", 1)

        print ('Use Gyro: ' + str(self.useGyro))
        print ('Use Accell: ' + str(self.useAccel))
        print ('Use Fsr: ' + str(self.fsr))
        print ('Use IR: ' + str(self.ir))
        print ('Use prox: ' + str(self.prox))

        self.imuCount = 0
        self.rfIndex = 0
        self.rllIndex = 0
        self.rulIndex = 0
        self.mIndex = 0
        self.imuIndexes = [-1, -1, -1, -1]

        out = io.StringIO()
        err = io.StringIO()

        self.window = rospy.get_param("~window_n", 0)
        self.thres = rospy.get_param("~thres_n", 0)

        self.rf = rospy.get_param("~rf_n", "")
        if self.rf != "":
            self.rfIndex = self.imuCount
            rfSub = rospy.Subscriber(self.rf, dataVec, self.imc, (self, self.rfIndex, self.rf))
            self.imuCount += 1

        self.rll = rospy.get_param("~rll_n", "")
        if self.rll != "":
            self.rllIndex = self.imuCount
            rllSub = rospy.Subscriber(self.rll, dataVec, self.imc, callback_args=(self, self.rllIndex, self.rll))
            self.imuCount += 1

        self.rul = rospy.get_param("~rul_n", "")
        if self.rul != "":
            self.rulIndex = self.imuCount
            rulSub = rospy.Subscriber(self.rul, dataVec, self.imc, callback_args=(self, self.rulIndex, self.rul))
            self.imuCount += 1

        self.m = rospy.get_param("~m_n", "")
        if self.m != "":
            self.mIndex = self.imuCount
            mSub = rospy.Subscriber(self.m, dataVec, self.imc, callback_args=(self, self.mIndex, self.m))
            self.imuCount += 1

        arduinoSub = rospy.Subscriber('arduino', ardu_msg, self.acb, callback_args=(self, self.mIndex))

        size = self.imuCount * (3 * self.useAccel + 3 * self.useGyro) + 3 * self.fsr + self.ir + self.prox
        self.imuVec = [-1337.1337 for i in range(0, size)]
        self.minVec = [0.0 for i in range(0, size)]
        self.maxVec = [0.0 for i in range(0, size)]
        self.avgVec = []

        print (self.rf)
        print (self.rll)
        print (self.rul_)
        print (self.m)
        print (self.imuCount)
        print (size)
        self.window = 1
        matlabInput = collections.deque(maxlen=self.window)
        gaitPhaseInput = collections.deque(maxlen=self.window)
        minMaxFound = False

        eng = matlab.engine.start_matlab()
        eng.load('~/subject1_best.mat', nargout=0)
        eng.cd('~/ros_ws/src/threespace_ros/scripts')
        print('Starting in 3 seconds')
        rospy.sleep(3)

        startTime = rospy.Time.now()
        r = rospy.Rate(100)
        d = rospy.Duration(0.1, 0)
        self.refresh = False
        trainDuration = 60
        totalDuration = 180
        while not rospy.is_shutdown():
            # print self.imuVec[18], self.imuVec[19], self.imuVec[20]
            loopTime = rospy.Time.now()
            # print(str(loopTime.to_sec()-startTime.to_sec()))
            if (loopTime.to_sec() - startTime.to_sec()) > trainDuration:
                # print self.imuVec
                if (loopTime.to_sec() - startTime.to_sec()) > totalDuration:
                    rospy.signal_shutdown("That's all folks")
                    ser.close()
                    eng.quit()
                    exit()
                # make sure we have data from every sensor
                if -1337.1337 not in self.imuVec:
                    # have we found the limits for every input so far ?
                    if minMaxFound:
                        if len(matlabInput) < self.window:
                            xx = [(self.imuVec[i] - self.minVec[i]) / (self.maxVec[i] - self.minVec[i]) for i in
                                  range(0, len(self.imuVec))]
                            matlabInput.append(xx)

                            m = np.array(matlabInput)
                            print(m)
                            mean_gait_1 = np.mean(m[:, len(matlabInput) - 2])
                            mean_gait_2 = np.mean(m[:, len(matlabInput) - 3])
                            gaitPhaseInput.append([0] if ((mean_gait_1 > 0.5) & (mean_gait_2 > 0.5))else [1])
                            # print np.array(gaitPhaseInput)
                        else:
                            xx = [(self.imuVec[i] - self.minVec[i]) / (self.maxVec[i] - self.minVec[i]) for i in
                                  range(0, len(self.imuVec))]
                            # print self.imuVec
                            # matlabInput.append(self.imuVec[:])
                            matlabInput.append(xx)
                            # print matlabInput.pop

                            m = np.array(matlabInput)
                            print(m)
                            mean_gait_1 = np.mean(m[:, len(matlabInput) - 2])
                            mean_gait_2 = np.mean(m[:, len(matlabInput) - 3])
                            gaitPhaseInput.append([0] if ((mean_gait_1 > 0.5) & (mean_gait_2 > 0.5))else [1])

                            input_vec = np.concatenate((np.array(matlabInput), np.array(gaitPhaseInput)), axis=1)
                            print('-------------')
                            ret = eng.live_classifier(input_vec.tolist(), nargout=1)
                            print (self.imuVec)
                            print (input_vec)
                            print (ret)
                            print('-------------')
                            ser.flush()
                            if ret == 0:
                                ser.write('N\n')
                            elif ret == 1:
                                ser.write('L\n')
                            elif ret == 2:
                                ser.write('S\n')
                            elif ret == 3:
                                ser.write('E\n')
                            else:
                                ser.write('O\n')
                                ser.close()
                                eng.quit()
                                return

                            print('-----###---')
                            rospy.sleep(0.5)
                            ser.flushInput()
                        continue
                    # if not find min and max values form every input
                    # so we can calculate the average (very sloppy tbh)
                    else:
                        print(self.avgVec)
                        self.maxVec = np.array(self.avgVec).max(axis=0)
                        print (self.maxVec)
                        self.minVec = np.array(self.avgVec).min(axis=0)
                        print (self.minVec)
                        minMaxFound = True
            else:
                self.avgVec.append(self.imuVec[:])
            rospy.sleep(d)
            r.sleep()
        eng.quit()


if __name__ == '__main__':
    try:
        LiveBroadcaster()
    except rospy.ROSInterruptException:
        pass
