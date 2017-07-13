#!/usr/bin/env python
import roslib
import rospy
import string
import find_dng
import threespace as tsa
from threespace import *


# PAIRS ANY CONNECTED IMU WITH
# THE CONNECTED DONGLE
rospy.init_node("pairer")

dng_list = find_dng.returnDev("dng")
dev_list = find_dng.returnDev("dev")
if len(dng_list) == 0:
    rospy.logerr("No dongles found, exiting")
    exit()

if len(dev_list) == 0:
    rospy.logerr("No device found, exiting")
    exit()

rospy.logwarn(dng_list)
rospy.logwarn(dev_list)
d = dng_list[0]
wc = None
att = 0
while wc is None:
    if att > 10:
        exit()
    att += 1
    try:
        rospy.logwarn("Getting Wireless Channel")
        wc = tsa.TSDongle.getWirelessChannel(d)
    except:
        rospy.logerr("Could not get Wireless Channel, exiting")
        exit()
rospy.logerr(wc)
rospy.logerr(d.wireless_table)
for dev in dev_list:
    rospy.logwarn("Getting Sensor ID")
    # rospy.logwarn(convertString(dev.f7WriteRead('getSerialNumber')))
    hw_id = dev.serial_number
    rospy.logwarn("%s", hw_id)
    if hw_id in d.wireless_table:
        rospy.loginfo("Device already registered with dongle")
    else:
        rospy.logwarn("Device wireless channel" + str(tsa.TSWLSensor.getWirelessChannel(dev)))
        tsa.TSWLSensor.setWirelessPanID(dev, int(wc))
        tsa.TSWLSensor.setWirelessChannel(dev, int(wc))
        rospy.logerr("Device wireless channel" + str(tsa.TSWLSensor.getWirelessChannel(dev)))
        for i in range(0, 15):
            rospy.logwarn(d.wireless_table[i])
            if (d.wireless_table[i] < 100) or ((i > 0) and (d.wireless_table[i] == d.wireless_table[i - 1])):
                rospy.loginfo("Found free spot at [%d]=%d", i, d.wireless_table[i])
                tsa.TSDongle.setSensorToDongle(d, i, hw_id)
                tsa.TSDongle.commitWirelessSettings(d)
                tsa.TSWLSensor.commitWirelessSettings(dev)
                break
for d in dng_list:
    tsa.TSDongle.close(d)
for dev in dev_list:
    tsa.TSWLSensor.close(dev)
rospy.logwarn(d.wireless_table)
