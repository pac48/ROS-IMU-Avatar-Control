# ROS IMU Avatar Control

pre req
sudo apt-get install gstreamer0.10-pocketsphinx
rosdep install --from-paths pocketsphinx
sudo apt-get install gstreamer0.10-gconf
catkin_make

roslaunch skeleton skeleton.launch
wEF