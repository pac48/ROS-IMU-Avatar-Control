#!/usr/bin/env python
import serial
import time
import math
import string
import rospy
import threespace as tsa
import find_dng
from threespace import *


# CALIBRATES ALL CONNECTED IMU
rospy.init_node("calibration")
dng_list = find_dng.returnDev("dng")
for d in dng_list:
    tsa.TSDongle.broadcastSynchronizationPulse(d)
    for device in d:
        if device == None:
            rospy.logerr("No Sensor Found")
        else:
            att = 0
            res = False
            rospy.logwarn("Calibrating %s", str(device))
            while res == False:
                att += 1
                if att > 10:
                    break
                try:
                    res = tsa.TSWLSensor.beginGyroscopeAutoCalibration(device)
                    rospy.logwarn("Calibration Successful")
                except:
                    rospy.logerr("Calibration attempt #%d failed, restarting",att)

