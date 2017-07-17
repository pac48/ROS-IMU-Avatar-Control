#!/usr/env/python
from __future__ import print_function
import numpy as np
import rosbag
import sys
import os
import scipy.io as sio
from os import listdir
from os.path import isfile, join

LABELS = {"push_right": 0,
          "push_left": 1,
          "push_straight": 2,
          "pull_right": 3,
          "pull_left": 4,
          "pull_straight": 5,
          "rotate_right": 6,
          "rotate_left": 7,
          "sc_upcw": 8,
          "sc_upccw": 9,
          "sweep_rl": 9,
          "sweep_lr": 9
          }

exercise_name = sys.argv[1]
if len(sys.argv) < 3:
    directory = os.path.dirname(os.path.realpath(__file__))
else:
    directory = sys.argv[2]
if len(sys.argv) > 3:
    subject = sys.argv[3]
else:
    subject = ''
config_files = [f for f in listdir(directory) if
                ((isfile(join(directory, f))) and "_config" in f)]


# FOR EVERY EXERCISE
for cf in config_files:
    with open(directory + cf) as cf_:
        topics = cf_.readline().replace("\n", '').split(' ')
    for i in range(0, len(topics)):
        topics[i] = '/' + topics[i] + '_data_vec'
    print(cf)
    hand = topics[0]
    lower = topics[1]
    upper = topics[2]
    tokens = cf.split('_')
    exercise = tokens[0] + '_' + tokens[1]
    print("Exercise: "+exercise+", topics: "+str(topics))
    exercise_files = [f for f in listdir(directory) if
                      ((isfile(join(directory, f))) and
                       (".bag" in f)and
                       (exercise in f))]
    regular_data_hand = []
    slow_data_hand = []
    stop_data_hand = []
    fast_data_hand = []

    regular_data_upper = []
    slow_data_upper = []
    stop_data_upper = []
    fast_data_upper = []

    regular_data_lower = []
    slow_data_lower = []
    stop_data_lower = []
    fast_data_lower = []

    regular_data_hand_temp = []
    slow_data_hand_temp = []
    stop_data_hand_temp = []
    fast_data_hand_temp = []

    regular_data_upper_temp = []
    slow_data_upper_temp = []
    stop_data_upper_temp = []
    fast_data_upper_temp = []

    regular_data_lower_temp = []
    slow_data_lower_temp = []
    stop_data_lower_temp = []
    fast_data_lower_temp = []

    # FOR EVERY EXERCISE FILE OF THE CURRENT EXERCISE
    for xf in exercise_files:
        bag = rosbag.Bag(directory+xf)
        print(xf)
        # print(directory+xf)
        for topic, msg, t in bag.read_messages(topics=[topics[i] for i in range(0, len(topics))]):
            data = [
                msg.quat.quaternion.x,
                msg.quat.quaternion.y,
                msg.quat.quaternion.z,
                msg.quat.quaternion.w,
                msg.gyroX,
                msg.gyroY,
                msg.gyroZ,
                msg.accX,
                msg.accY,
                msg.accZ,
                # msg.comX,
                # msg.comY,
                # msg.comZ
            ]
            if topic == hand:
                if "_fast_" in xf:
                    fast_data_hand_temp.append(data)
                elif "_slow_" in xf:
                    slow_data_hand_temp.append(data)
                elif "_stop_" in xf:
                    stop_data_hand_temp.append(data)
                else:
                    regular_data_hand_temp.append(data)
            elif topic == lower:
                if "_fast_" in xf:
                    fast_data_lower_temp.append(data)
                elif "_slow_" in xf:
                    slow_data_lower_temp.append(data)
                elif "_stop_" in xf:
                    stop_data_lower_temp.append(data)
                else:
                    regular_data_lower_temp.append(data)
            elif topic == upper:
                if "_fast_" in xf:
                    fast_data_upper_temp.append(data)
                elif "_slow_" in xf:
                    slow_data_upper_temp.append(data)
                elif "_stop_" in xf:
                    stop_data_upper_temp.append(data)
                else:
                    regular_data_upper_temp.append(data)
        bag.close()

        if (len(regular_data_hand_temp)) > 0:
            regular_data_hand_temp = np.array(regular_data_hand_temp)
            regular_data_hand_temp = (regular_data_hand_temp - regular_data_hand_temp.min(
                0)) / regular_data_hand_temp.ptp(0)
        if (len(slow_data_hand_temp)) > 0:
            slow_data_hand_temp = np.array(slow_data_hand_temp)
            slow_data_hand_temp = (slow_data_hand_temp - slow_data_hand_temp.min(0)) / slow_data_hand_temp.ptp(0)
        if (len(fast_data_hand_temp)) > 0:
            fast_data_hand_temp = np.array(fast_data_hand_temp)
            fast_data_hand_temp = (fast_data_hand_temp - fast_data_hand_temp.min(0)) / fast_data_hand_temp.ptp(0)
        if (len(stop_data_hand_temp)) > 0:
            stop_data_hand_temp = np.array(stop_data_hand_temp)
            stop_data_hand_temp = (stop_data_hand_temp - stop_data_hand_temp.min(0)) / stop_data_hand_temp.ptp(0)

        if (len(regular_data_lower_temp)) > 0:
            regular_data_lower_temp = np.array(regular_data_lower_temp)
            regular_data_lower_temp = (regular_data_lower_temp - regular_data_lower_temp.min(
                0)) / regular_data_lower_temp.ptp(0)
        if (len(slow_data_lower_temp)) > 0:
            slow_data_lower_temp = np.array(slow_data_lower_temp)
            slow_data_lower_temp = (slow_data_lower_temp - slow_data_lower_temp.min(0)) / slow_data_lower_temp.ptp(0)
        if (len(fast_data_lower_temp)) > 0:
            fast_data_lower_temp = np.array(fast_data_lower_temp)
            fast_data_lower_temp = (fast_data_lower_temp - fast_data_lower_temp.min(0)) / fast_data_lower_temp.ptp(0)
        if (len(stop_data_lower_temp)) > 0:
            stop_data_lower_temp = np.array(stop_data_lower_temp)
            stop_data_lower_temp = (stop_data_lower_temp - stop_data_lower_temp.min(0)) / stop_data_lower_temp.ptp(0)

        if (len(regular_data_upper_temp)) > 0:
            regular_data_upper_temp = np.array(regular_data_upper_temp)
            regular_data_upper_temp = (regular_data_upper_temp - regular_data_upper_temp.min(
                0)) / regular_data_upper_temp.ptp(0)
        if (len(slow_data_upper_temp)) > 0:
            slow_data_upper_temp = np.array(slow_data_upper_temp)
            slow_data_upper_temp = (slow_data_upper_temp - slow_data_upper_temp.min(0)) / slow_data_upper_temp.ptp(0)
        if (len(fast_data_upper_temp)) > 0:
            fast_data_upper_temp = np.array(fast_data_upper_temp)
            fast_data_upper_temp = (fast_data_upper_temp - fast_data_upper_temp.min(0)) / fast_data_upper_temp.ptp(0)
        if (len(stop_data_upper_temp)) > 0:
            stop_data_upper_temp = np.array(stop_data_upper_temp)
            stop_data_upper_temp = (stop_data_upper_temp - stop_data_upper_temp.min(0)) / stop_data_upper_temp.ptp(0)

        regular_data_hand.append(regular_data_hand_temp) if len(regular_data_hand_temp) != 0 else 1
        slow_data_hand.append(slow_data_hand_temp) if len(slow_data_hand_temp) != 0 else 1
        fast_data_hand.append(fast_data_hand_temp) if len(fast_data_hand_temp) != 0 else 1
        stop_data_hand.append(stop_data_hand_temp) if len(stop_data_hand_temp) != 0 else 1

        regular_data_lower.append(regular_data_lower_temp) if len(regular_data_lower_temp) != 0 else 1
        slow_data_lower.append(slow_data_lower_temp) if len(slow_data_lower_temp) != 0 else 1
        fast_data_lower.append(fast_data_lower_temp) if len(fast_data_lower_temp) != 0 else 1
        stop_data_lower.append(stop_data_lower_temp) if len(stop_data_lower_temp) != 0 else 1

        regular_data_upper.append(regular_data_upper_temp) if len(regular_data_upper_temp) != 0 else 1
        slow_data_upper.append(slow_data_upper_temp) if len(slow_data_upper_temp) != 0 else 1
        fast_data_upper.append(fast_data_upper_temp) if len(fast_data_upper_temp) != 0 else 1
        stop_data_upper.append(stop_data_upper_temp) if len(stop_data_upper_temp) != 0 else 1

        regular_data_hand_temp = []
        slow_data_hand_temp = []
        stop_data_hand_temp = []
        fast_data_hand_temp = []

        regular_data_upper_temp = []
        slow_data_upper_temp = []
        stop_data_upper_temp = []
        fast_data_upper_temp = []

        regular_data_lower_temp = []
        slow_data_lower_temp = []
        stop_data_lower_temp = []
        fast_data_lower_temp = []

    output_file = ('/home/lydakis-local/PycharmProjects/InvarianceStudy/matfiles/'+exercise+'_'+subject+'.mat')
    print(output_file)
    sio.savemat(output_file, mdict={'regular_data_hand': regular_data_hand,
                                    'slow_data_hand': slow_data_hand,
                                    'fast_data_hand': fast_data_hand,
                                    'stop_data_hand': stop_data_hand,
                                    'regular_data_upper': regular_data_upper,
                                    'slow_data_upper': slow_data_upper,
                                    'fast_data_upper': fast_data_upper,
                                    'stop_data_upper': stop_data_upper,
                                    'regular_data_lower': regular_data_lower,
                                    'slow_data_lower': slow_data_lower,
                                    'fast_data_lower': fast_data_lower,
                                    'stop_data_lower': stop_data_lower,
                                    'label': LABELS[exercise]
                                    })
