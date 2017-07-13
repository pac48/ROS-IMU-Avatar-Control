#!/usr/bin/env python
import roslib
import rospy
import tf
import tf2_ros
import geometry_msgs.msg
import serial
import time
import math
import string
import glob
import sensor_table
import find_dng
import threespace as tsa
from threespace import *
from socket import *
from threespace_ros.msg import dataVec

rospy.init_node("publisher")
r = rospy.Rate(100)
suffix = "_data_vec"
dongle_list = find_dng.returnDev("dng")
publishers = {}
dv_publishers = {}
broadcasters = {}

frame_list = []
publishers_list = []

if len(dongle_list) == 0:
    rospy.logerr("No Dongles Found, Exiting")
    exit()

for d in dongle_list:
    tsa.TSDongle.broadcastSynchronizationPulse(d)
    for device in d:
        if device is None:
            rospy.logerr("No Sensor Found")
        else:
            id_ = str(device)
            id_ = id_[id_.find('W'):-1]
            rospy.logerr(id_)
            frame = sensor_table.sensor_table.get(id_)
            rospy.logerr("Adding publisher for %s : %s", id_, frame)
            rospy.logerr("Battery at %s Percent ", tsa.TSWLSensor.getBatteryPercentRemaining(device))
            br = tf2_ros.TransformBroadcaster()
            dv_pub = rospy.Publisher(frame+suffix, dataVec, queue_size=100)
            broadcasters[frame] = br
            dv_publishers[frame] = dv_pub
            frame_list.append(frame)
            publishers_list.append(dv_pub)
            tsa.TSWLSensor.setStreamingSlots(device, slot0='getTaredOrientationAsQuaternion',
                                             slot1='getAllCorrectedComponentSensorData')

t = geometry_msgs.msg.TransformStamped()
g = geometry_msgs.msg.QuaternionStamped()
dv = dataVec()
dev_list = []

for d in dongle_list:
    for dev in d:
        # batch = tsa.TSWLSensor.getStreamingBatch(device)
        if dev is not None:
            tsa.TSWLSensor.setFilterMode(dev, mode=2)
            dev_list.append(dev)

tsa.global_broadcaster.setStreamingTiming(interval=0,
                                          duration=0,
                                          delay=0,
                                          delay_offset=0,
                                          filter=dev_list)

tsa.global_broadcaster.setStreamingSlots(slot0='getTaredOrientationAsQuaternion',
                                         slot1='getAllCorrectedComponentSensorData')

tsa.global_broadcaster.startStreaming(filter=dev_list)
tsa.global_broadcaster.startRecordingData(filter=dev_list)

num_devs = len(dev_list)

while not rospy.is_shutdown():
    for i in range(num_devs):
        dev = dev_list[i]
        if len(dev.stream_data) > 0:
            # print len(dev.stream_data)
            # print list(dev.stream_data[0][1])
            # frame = frame_list[i]
            # g.quaternion.w = quat[3]
            batch = dev.stream_data[0][1]
            dv.header.stamp = rospy.get_rostime()
            dv.header.frame_id = frame_list[i]
            dv.quat.header.frame_id = frame_list[i]
            dv.quat.quaternion.x = batch[0]
            dv.quat.quaternion.y = batch[1]
            dv.quat.quaternion.z = batch[2]
            dv.quat.quaternion.w = batch[3]
            dv.gyroX = batch[4]
            dv.gyroY = batch[5]
            dv.gyroZ = batch[6]
            dv.accX = batch[7]
            dv.accY = batch[8]
            dv.accZ = batch[9]
            dv.comX = batch[10]
            dv.comY = batch[11]
            dv.comZ = batch[12]
            publishers_list[i].publish(dv)
            dev.stream_data = []


tsa.global_broadcaster.stopStreaming(filter=dev_list)
tsa.global_broadcaster.stopRecordingData(filter=dev_list)
for d in dongle_list:
    tsa.TSDongle.close(d)
print (publishers)
print (dv_publishers)
print (broadcasters)