#!/usr/bin/env python
import serial
import time
import rospy
import math
import string
import sensor_table
import threespace_api as tsa
import find_ports
from threespace_api import *
from socket import *

rospy.init_node("poll_dongles")

result = find_ports.findPorts()
dongle_list = []
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
                rospy.loginfo("Attempting to get Dongle Data attempt #%d", att)
                panid = tsa.TSDongle.getWirelessPanID(dongle)
                channel = tsa.TSDongle.getWirelessChannel(dongle)
                wa = tsa.TSDongle.getWirelessAddress(dongle)
                rospy.logwarn("HW ID : %s", hwid)
                rospy.logwarn("PanID : %s", panid)
                rospy.logwarn("Channel : %s", channel)
                rospy.logwarn("Wireless Address %s", wa)
                rospy.logwarn(dongle.wireless_table)
                dongle_list.append(dongle)
                if att > 10:
                    break
                break
            except:
                pass
    except:
        pass
for d in dongle_list:
    tsa.TSDongle.commitWirelessSettings(d)
    tsa.TSDongle.broadcastSynchronizationPulse(d)
    wl_device = d[0]
    if wl_device is None:
        ropsy.logerr("No Sensor found")
    else:
        while True:
            quat = tsa.TSWLSensor.getTaredOrientationAsQuaternion(wl_device)
            if quat is not None:
                rospy.loginfo(quat)
# rospy.loginfo(dongle_list)
exit()
for dongle in dongle_list:
    rospy.logerr(convertString(dongle.f7WriteRead('getSerialNumber')))
    rospy.loginfo(dongle)
    for entry in dongle:
        rospy.logwarn(entry)
        rospy.loginfo(convertString(entry.f7WriteRead('getSerialNumber')))
