#!/usr/bin/env python
import rospy
import find_dng
import threespace as tsa

# PRINTS CHARGE LEVEL FOR ALL CONNECTED IMUS
rospy.init_node("charge_monitor")
r = rospy.Rate(100)

devlist = find_dng.returnDev("dev")
if len(devlist) == 0:
    rospy.logwarn("No devices found, exiting")
    exit()

while not rospy.is_shutdown():
    for device in devlist:
        id_ = str(device)
        id_ = id_[id_.find('W'):-1]
        rospy.logwarn("Device : %s is at %d", id_, tsa.TSWLSensor.getBatteryPercentRemaining(device))
    rospy.sleep(rospy.Duration(5))
    rospy.logerr("------------------------")

for d in devlist:
    tsa.TSWLSensor.close(d)
