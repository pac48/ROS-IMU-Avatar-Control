# ROS IMU Avatar Control


## Prerequisites
---
The package utilizes a ROS package called pocketsphinx, which reqires gstreamer0.10-pocketsphinx installation. 

'''sudo apt-get install gstreamer0.10-pocketsphinx
cd catkin_ws/src
rosdep install --from-paths pocketsphinx
cd ..
sudo apt-get install gstreamer0.10-gconf'''

## Building the Package
---

'''cd catkin_ws/src
git clone https://github.com/pac48/ROS-IMU-Avatar-Control.git
cd ..
catkin_make'''

## Launching the Nodes
---
roslaunch skeleton skeleton.launch
