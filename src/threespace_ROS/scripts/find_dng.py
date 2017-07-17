import serial
import time
import math
import string
import rospy
import threespace_api as tsa
import find_ports
from threespace_api import *
from socket import *
# FIND ALL CONNECTED BLUETOOTH DONGLES
def returnDev(arg):
    # rospy.init_node("detect")
    result = find_ports.findPorts()
    dng_list = []
    dev_list = []
    rospy.logwarn(result)
    if arg == "dng":
        for a_port in result:
            try:
                rospy.loginfo("Checking for dongle in port %s", a_port)
                dongle = tsa.TSDongle(com_port=a_port, baudrate=115200)
                rospy.logwarn(dongle)
                hwid = convertString(dongle.f7WriteRead('getSerialNumber'))
                panid = None
                channel = None
                wa = None
                att = 0
                while panid is None or channel is None or wa is None:
                    try:
                        att += 1
                        if att > 10:
                            break
                        rospy.loginfo("Attempting to get Dongle data from port %s, attempt #%d", a_port, att)
                        channel = tsa.TSDongle.getWirelessChannel(dongle)
                        panid = tsa.TSDongle.getWirelessPanID(dongle)
                        wa = tsa.TSDongle.getWirelessAddress(dongle)
                        rospy.logwarn("HW ID : %s", hwid)
                        rospy.logwarn("PanID : %s", panid)
                        rospy.logwarn("Channel : %s", channel)
                        rospy.logwarn("Wireless Address %s", wa)
                        rospy.logwarn(dongle.wireless_table)
                        dng_list.append(dongle)
                    except:
                        pass
            except:
                pass
        print dng_list
        return dng_list
    else:
        for a_port in result:
            try:
                rospy.loginfo("Checking for wireless sensor in port %s", a_port)
                sensor = tsa.TSWLSensor(com_port=a_port, baudrate=115200)
                rospy.logwarn(sensor)
                hwid = convertString(sensor.f7WriteRead('getSerialNumber'))
                # dev_list.append(sensor)
                panid = None
                channel = None
                wa = None
                att = 0
                while panid is None or channel is None or wa is None:
                    try:
                        att += 1
                        if att > 10:
                            break
                        rospy.loginfo("Attempting to get Wireless Sensor data from port %s, attempt #%d", a_port, att)
                        channel = tsa.TSWLSensor.getWirelessChannel(sensor)
                        # tsa.TSWLSensor.setWirelessPanID(sensor, channel)
                        panid = tsa.TSWLSensor.getWirelessPanID(sensor)
                        wa = tsa.TSWLSensor.getWirelessAddress(sensor)
                        rospy.logwarn("HW ID : %s", hwid)
                        rospy.logwarn("PanID : %s", panid)
                        rospy.logwarn("Channel : %s", channel)
                        rospy.logwarn("Wireless Address %s", wa)
                        dev_list.append(sensor)
                    except:
                        pass
            except:
                pass
        return dev_list
