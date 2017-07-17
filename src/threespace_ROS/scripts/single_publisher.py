#!/usr/bin/env python
import rospy
import tf2_ros
import geometry_msgs.msg
import sensor_table
import find_dng
import threespace_api as tsa
from threespace.msg import dataVec


class SinglePublisher:
    def __init__(self):
        rospy.init_node("publisher")
        r = rospy.Rate(100)
        suffix = "_data_vec"
        dongle_list = find_dng.returnDev("dng")
        publishers = {}
        dv_publishers = {}
        broadcasters = {}
        if len(dongle_list) == 0:
            rospy.logerr("No dongles found, exiting")
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
                    rospy.logwarn("Adding publisher for %s : %s", id_, frame)
                    rospy.logwarn("Battery at %s Percent ", tsa.TSWLSensor.getBatteryPercentRemaining(device))
                    br = tf2_ros.TransformBroadcaster()
                    dv_pub = rospy.Publisher(frame + suffix, dataVec, queue_size=100)
                    broadcasters[frame] = br
                    dv_publishers[frame] = dv_pub
                    tsa.TSWLSensor.setStreamingSlots(device, slot0='getTaredOrientationAsQuaternion',
                                                     slot1='getAllCorrectedComponentSensorData')

        t = geometry_msgs.msg.TransformStamped()
        dv = dataVec()
        dev_list = []
        for d in dongle_list:
            for dev in d:
                if dev is not None:
                    dev_list.append(dev)

        while not rospy.is_shutdown():
            for device in dev_list:
                if device is not None:
                    batch = tsa.TSWLSensor.getStreamingBatch(device)
                    if batch is not None:
                        quat = batch[0:4]
                        full = batch[4:]
                        id_ = str(device)
                        id_ = id_[id_.find('W'):-1]
                        frame = sensor_table.sensor_table.get(id_)
                        dp = dv_publishers.get(frame)
                        b = broadcasters.get(frame)
                        t.header.stamp = rospy.Time.now()
                        t.header.frame_id = "world"
                        t.child_frame_id = frame
                        t.transform.translation.x = 0.0
                        t.transform.translation.y = 0.0
                        t.transform.translation.z = 0.0
                        dv.header.stamp = rospy.get_rostime()
                        dv.quat.quaternion.x = -quat[2]
                        dv.quat.quaternion.y = quat[0]
                        dv.quat.quaternion.z = -quat[1]
                        dv.quat.quaternion.w = quat[3]
                        dv.gyroX = full[0]
                        dv.gyroY = full[1]
                        dv.gyroZ = full[2]
                        dv.accX = full[3]
                        dv.accY = full[4]
                        dv.accZ = full[5]
                        dv.comX = full[6]
                        dv.comY = full[7]
                        dv.comZ = full[8]
                        t.transform.rotation = dv.quat.quaternion
                        b.sendTransform(t)
                        dp.publish(dv)
                    else:
                        # rospy.logerr("None")
                        pass
            r.sleep()
        for d in dongle_list:
            tsa.TSDongle.close(d)
        print (publishers)
        print (dv_publishers)
        print (broadcasters)

if __name__ == "__main__":
    SinglePublisher()
