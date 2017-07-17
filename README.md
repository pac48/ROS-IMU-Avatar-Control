# ROS IMU Avatar Control


## Prerequisites

The package utilizes a ROS package called pocketsphinx, which reqires gstreamer0.10-pocketsphinx installation. 

```
sudo apt-get install gstreamer0.10-pocketsphinx
cd catkin_ws/src
rosdep install --from-paths pocketsphinx
cd ..
sudo apt-get install gstreamer0.10-gconf
```

## Building the Package

```
cd catkin_ws/src
svn checkout https://github.com/pac48/ROS-IMU-Avatar-Control/trunk/src
cd ..
catkin_make
```

## Launching the Nodes

The package can be run with the following command:

```
roslaunch skeleton skeleton.launch
```

If the package fails to launch correctly and a due to the error "No dongles found, exiting", then there is a problem accessing the dongles in the serial port. 
Make sure you wait at lleast 30 seconds after you plug in the dongle before trying to run the launch command, or you will most likely get this error. If the error persist you
may have to change the permissions for your serial port. For example:

```
sudo chmod 666 ttyACM0
sudo chmod 666 ttyACM1
```

You can also add you account to a group with access to the serial port. 

```
sudo adduser pac48 dialout
```
Finally, if the application crashes due to and you recieve this error:

VMware: vmw_ioctl_command error Invalid argument

Then you can run the following command to permanently fix it. In my case this problem occured because I was running Ubuntu in VMware.

```
echo "export SVGA_VGPU10=0" >> ~/.bashrc
```

The launch file will create four node:

* `/Skeleton_node`
* `/recognizer` 
* `/single_publisher` 
* `/Blender`   

In addition to four nodes, the following parameters will be initiated.

### PARAMETERS

 * /Skeleton_node/chest_IMU: 0
 * /Skeleton_node/l_foot: 0
 * /Skeleton_node/l_hand_IMU: 
 * /Skeleton_node/l_lower_leg_IMU: 
 * /Skeleton_node/l_shoulder_IMU: 
 * /Skeleton_node/l_upper_arm_IMU: 
 * /Skeleton_node/l_upper_leg_IMU: 
 * /Skeleton_node/r_foot_IMU: 
 * /Skeleton_node/r_hand_IMU: 
 * /Skeleton_node/r_lower_arm_IMU: 
 * /Skeleton_node/r_lower_leg_IMU: 
 * /Skeleton_node/r_shoulder_IMU: 
 * /Skeleton_node/r_upper_arm_IMU: 
 * /Skeleton_node/temp_1_IMU: 
 * /Skeleton_node/temp_2_IMU: 
 * /Skeleton_node/temp_3_IMU: 
 * /Skeleton_node/temp_4_IMU: 
 * /Skeleton_node/temp_5_IMU: 
 * /Skeleton_node/temp_6_IMU: 

For details on the how to use the package, please see the [Wiki page](https://github.com/pac48/ROS-IMU-Avatar-Control/wiki)