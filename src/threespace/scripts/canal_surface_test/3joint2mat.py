#!/usr/env/python
from __future__ import print_function
import rosbag
import sys
import scipy.io as sio
from os import listdir
from os.path import isfile, join

LABELS = {"circle": 0,
          "square": 1,
          "triangle": 2,
          "complex": 3,
          "swiperight": 4,
          "swipeleft": 5,
          "rotateright": 6,
          "rotateleft": 7,
          "scupcw": 8,
          "scupccw": 9
          }

SUBJECTS = ['s1']

if len(sys.argv) == 2:
    directory = sys.argv[1]
else:
    directory = 'exercises/'

data = []
config_files = [f for f in listdir(directory) if (isfile(join(directory, f))) and 'config' in f]
print(config_files)
for cf in config_files:
    tokens = cf.strip('\n').split('_')
    print(tokens)
    subject = tokens[1]
    exercise = tokens[0]
    print(subject)
    exercise_files = [f for f in listdir(directory) if (isfile(join(directory, f)))
                      and ('_' + subject + '.' in f) and ('.bag' in f) and (exercise in f)]
    print(exercise_files)
    # read topics from config file
    with open(directory + cf) as cf_:
        topics = cf_.readline().replace("\n", '').split(' ')
    for i in range(0, len(topics)):
        topics[i] = '/' + topics[i] + '_data_vec'
    topics.append('/tf')
    full_data = []
    data_compressed = []
    for xf in exercise_files:
        print(xf)
        tk = xf.strip('.bag').split('_')
        ex = tk[0]
        rep = tk[1]
        topics_counter = [0 for i in range(len(topics))]
        bag = rosbag.Bag(directory + xf)
        hand_imu = []
        lower_imu = []
        upper_imu = []
        tf_upper = []
        tf_lower = []
        tf_hand = []
        start = -1
        # get tf from bag and add the readings to the appropriate list
        for topic, msg, t in bag.read_messages(topics=[topics[i] for i in range(0, len(topics))]):
            if start == -1:
                start = t.to_nsec() / 1000000.0
            time = t.to_nsec() / 1000000.0 - start
            # print('%f' % time)
            if topic == '/tf':
                transforms = msg.transforms
                for tr in transforms:
                    if tr.child_frame_id == 'upper':
                        tf_upper.append([
                            time,
                            tr.transform.translation.x,
                            tr.transform.translation.y,
                            tr.transform.translation.z,
                            tr.transform.rotation.x,
                            tr.transform.rotation.y,
                            tr.transform.rotation.z,
                            tr.transform.rotation.w
                        ])
                    if tr.child_frame_id == 'lower':
                        tf_lower.append([
                            tr.transform.translation.x,
                            tr.transform.translation.y,
                            tr.transform.translation.z,
                            tr.transform.rotation.x,
                            tr.transform.rotation.y,
                            tr.transform.rotation.z,
                            tr.transform.rotation.w
                        ])
                    if tr.child_frame_id == 'hand':
                        tf_hand.append([
                            tr.transform.translation.x,
                            tr.transform.translation.y,
                            tr.transform.translation.z,
                            tr.transform.rotation.x,
                            tr.transform.rotation.y,
                            tr.transform.rotation.z,
                            tr.transform.rotation.w,
                        ])
            elif topic == topics[0]:
                upper_imu.append([msg.quat.quaternion.x,
                                  msg.quat.quaternion.y,
                                  msg.quat.quaternion.z,
                                  msg.quat.quaternion.w,
                                  msg.accX,
                                  msg.accY,
                                  msg.accZ,
                                  msg.gyroX,
                                  msg.gyroY,
                                  msg.gyroZ,
                                  msg.comX,
                                  msg.comY,
                                  msg.comZ
                                  ])
            elif topic == topics[1]:
                lower_imu.append([msg.quat.quaternion.x,
                                  msg.quat.quaternion.y,
                                  msg.quat.quaternion.z,
                                  msg.quat.quaternion.w,
                                  msg.accX,
                                  msg.accY,
                                  msg.accZ,
                                  msg.gyroX,
                                  msg.gyroY,
                                  msg.gyroZ,
                                  msg.comX,
                                  msg.comY,
                                  msg.comZ
                                  ])
            elif topic == topics[2]:
                hand_imu.append([msg.quat.quaternion.x,
                                 msg.quat.quaternion.y,
                                 msg.quat.quaternion.z,
                                 msg.quat.quaternion.w,
                                 msg.accX,
                                 msg.accY,
                                 msg.accZ,
                                 msg.gyroX,
                                 msg.gyroY,
                                 msg.gyroZ,
                                 msg.comX,
                                 msg.comY,
                                 msg.comZ
                                 ])
        minlen = min(len(hand_imu), len(lower_imu))
        minlen = min(len(upper_imu), minlen)
        minlen = min(len(tf_hand), minlen)
        minlen = min(len(tf_lower), minlen)
        minlen = min(len(tf_upper), minlen)
        data_compressed_ex = []
        j = 0
        for i in range(minlen):
            temp = []
            for j in tf_upper[i]:
                temp.append(j)
            for j in tf_lower[i]:
                temp.append(j)
            for j in tf_hand[i]:
                temp.append(j)
            for j in upper_imu[i]:
                temp.append(j)
            for j in lower_imu[i]:
                temp.append(j)
            for j in hand_imu[i]:
                temp.append(j)
            temp.append(LABELS.get(ex))

            data_compressed_ex.append(temp)
            if 'slow' not in xf:
                data_compressed.append(temp)
        print(len(data_compressed))
        print(len(data_compressed_ex))
        sio.savemat('matfiles/' + ex + '_' + rep + '_' + subject + '_data.mat',
                    mdict={'data': data_compressed_ex})
        print('******************')
    sio.savemat('matfiles/' + exercise + '_full_data.mat', mdict={'data': data_compressed})
