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

rospy.init_node("poll_sensors")

result = find_ports.findPorts()
sensor_list = []
for a_port in result:
    try:
        rospy.loginfo("Checking for sensor in port %s", a_port)
        sensor = tsa.TSWLSensor(com_port=a_port, baudrate=115200)
        rospy.logwarn("Found Sensor")
        rospy.logwarn(sensor)
        hwid = None
        panid = None
        channel = None
        att = 0
        while hwid is None or panid is None or channel is None:
            try:
                att += 1
                rospy.loginfo("Attempting to get Sensor Data attempt #%d", att)
                hwid = convertString(sensor.f7WriteRead('getSerialNumber'))
                panid = tsa.TSWLSensor.getWirelessPanID(sensor)
                channel = tsa.TSWLSensor.getWirelessChannel(sensor)
                rospy.logwarn("HW ID : %s", hwid)
                rospy.logwarn("PanID : %s", panid)
                rospy.logwarn("Channel : %s", channel)
                # tsa.TSWLSensor.switchToWiredMode(sensor)
                tsa.TSWLSensor.switchToWirelessMode(sensor)
                if att > 10:
                    break
                break
            except:
                pass
    except:
        pass
