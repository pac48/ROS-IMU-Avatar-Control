#!/bin/bash
# waits 5 seconds and starts the recording of whatever joint data is being published for
# arg1 = bag naem
# arg2 = recording duration in minutes
sleep 5
roslaunch gait_hmm_ros record.launch prefix:=$1 dur:=$2
rosbag info ~/.ros/$1.bag
rosnode kill /usb_cam
