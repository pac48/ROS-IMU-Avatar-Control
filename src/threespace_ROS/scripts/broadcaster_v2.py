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
import threespace_api as tsa
from threespace_api import *
from socket import *
from threespace_ros.msg import dataVec
from gait_hmm_ros.msg import imu_vector

rospy.init_node("broadcasterV2")
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
            dv_pub = rospy.Publisher(frame + suffix, imu_vector, queue_size=100)
            broadcasters[frame] = br
            dv_publishers[frame] = dv_pub
            frame_list.append(frame)
            publishers_list.append(dv_pub)
            tsa.TSWLSensor.setStreamingSlots(device, slot0='getTaredOrientationAsQuaternion',
                                             slot1='getAllCorrectedComponentSensorData')

t = geometry_msgs.msg.TransformStamped()
g = geometry_msgs.msg.QuaternionStamped()
dv = dataVec()
vec = imu_vector()
dev_list = []

for d in dongle_list:
    for dev in d:
        # batch = tsa.TSWLSensor.getStreamingBatch(device)
        if dev is not None:
            tsa.TSWLSensor.setFilterMode(dev, mode=2)
            dev_list.append(dev)
# set streaming timing for the imus
tsa.global_broadcaster.setStreamingTiming(interval=0,
                                          duration=0,
                                          delay=0,
                                          delay_offset=0,
                                          filter=dev_list)
# get the readings as batch
tsa.global_broadcaster.setStreamingSlots(slot0='getTaredOrientationAsQuaternion',
                                         slot1='getAllCorrectedComponentSensorData')
# start streaming and recording
tsa.global_broadcaster.startStreaming(filter=dev_list)
tsa.global_broadcaster.startRecordingData(filter=dev_list)

num_devs = len(dev_list)

while not rospy.is_shutdown():
    for i in range(num_devs):
        dev = dev_list[i]
        vec = []
        if len(dev.stream_data) > 0:
            # print len(dev.stream_data)
            # print list(dev.stream_data[0][1])
            # frame = frame_list[i]
            # g.quaternion.w = quat[3]
            batch = dev.stream_data[0][1]
            vec.header.stamp = rospy.get_rostime()
            vec.header.frame_id = frame_list[i]
            # vec.data.append(frame_list[i])
            # vec.data.append(batch[0])
            # vec.data.append(batch[1])
            # vec.data.append(batch[2])
            # vec.data.append(batch[3])
            # vec.data.append(batch[4])
            # vec.data.append(batch[5])
            # vec.data.append(batch[6])
            # vec.data.append(batch[7])
            # vec.data.append(batch[8])
            # vec.data.append(batch[9])
            # vec.data.append(batch[10])
            # vec.data.append(batch[11])
            # vec.data.append(batch[12])
            vec.data = batch[0:13]
            publishers_list[i].publish(dv)
            dev.stream_data = []

tsa.global_broadcaster.stopStreaming(filter=dev_list)
tsa.global_broadcaster.stopRecordingData(filter=dev_list)
# close all the connected devices
for d in dongle_list:
    tsa.TSDongle.close(d)
print (publishers)
print (dv_publishers)
print (broadcasters)
exit()
