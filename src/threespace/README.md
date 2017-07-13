# Ros node for the YostLabs 3Space IMUs.

## General Use Nodes
* **find_ports.py**: gets all available serial ports
* **find_dng.py**: gets all connected bluetooth dongles and IMUs
* **pair.py**: pairs connected IMUs with a single conencted dongle
* **chargemonitor.py**: periodically prints the charge level of connected IMUs
* **single_publisher.py**: Finds Connected IMUs and starts publishing
 batches of data in the topics defined in sensor_table.py

## Gait Detection Related Nodes & Scripts
* **arduino_listener.py**: Listens for readings from an XBee and converts
them to ROS messages.
* **live_broadcaster.py**: starts a mock live classification session for the gait 
detection system. Waits for a certain amount of readings to create basic user
 mins and maxs and then starts classifying batches of incoming messages
 
## Canal Surface Related Nodes & Scripts (/scripts/canal_surface_test)
* **Segmentation**: segmentation library
* **three_joint_publisher.py**: takes three imu topics and publishes transformations between them, assuming the first 
    is located on the upper arm, the second on the forearm and the third on the hand. When the program is started, it 
    assumes that the hand is stretched forward to create the inital transformations.
* **3joint2mat.py**: reads a config file for an exercise and converts rosbags to .mat files
    the config file is named [exercise_name]_[subject_id]_config, and is formatted as:
    [upper_arm_topic] [lower_arm_topic] [hand_topic]
    The output mat files are formatted as:
    [timestamp][upper transform readings][lower transform readings][hand transform readings]
    [upper imu readings][lower imu readings][hand imu readings][label]
    output files are saved as: 'matfiles/' + exercise + '_full_data.mat'
* **gmm.py**: create the test and training data for each exercise (60-40 split). It creates a number of files for each
    exercise including the original demonstrations, and aligned demonstrations for the different speeds (normal, slow, fast)
    in different combinations (normal stretched to slow, fast stretched to slow, normal compressed to fast, normal compressed to slow etc.)
* **canalSurfaceSlow/Fast/Test.m**: creates the canal surface data for a given exercise.
    The script extends the number of joints to six, extending them to include the actual joints, in addition to the middle
     of the limbs. The newly created joints are suffixed with '2'. The output file includes the average readings 
     (translation and orientation) for each dimension of the joint, the radius of the canal surface, and the min and max
     values for each aligned frame.
* **initialize_exercises.py**: different utilities, including segmenting functions, comparing functions, loading testfiles etc.
* **exercise_sticher.py**: creates random exercises comprised of a number basic primitives. 
* **classify_window**: classifies incoming signals based on a set of parameters including window length, drop out number,
    weight inclusion, see report for more details.
    
