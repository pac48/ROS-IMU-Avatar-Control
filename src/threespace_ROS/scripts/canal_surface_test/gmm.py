#!/usr/env/python
from __future__ import print_function
import platform

print(platform.platform())
import sys

print("Python", sys.version)
import numpy as np;

print("NumPy", np.__version__)
import scipy

print("SciPy", scipy.__version__)
import sklearn

print("Scikit-Learn", sklearn.__version__)

import rospy
import rosbag
import sys
import os
import itertools
import scipy.io as sio
from pomegranate import *
from os import listdir
from dtw import dtw
from sklearn.metrics.pairwise import euclidean_distances
from os.path import isfile, join
from pypr.stattest import *


def align_signal(s_, t, w=5, has_time=True, get_distance=False):
    """
    every column of s or t is a time series
    every row is dimensions of signal at one time point
    w size is symmetric. w=5 means the window has size 11.
    """
    # t = t.transpose(1, 0)
    # s = s.transpose(1, 0)
    if has_time:
        s_ = s_[:, 1:]
        t = t[:, 1:]

    dist_fun = euclidean_distances
    dist_, cost_, acc_, path_ = dtw(s_, t, dist_fun)
    path_ = np.array(path_)

    warped_t = t[path_[1, :], :]
    new_t = np.zeros(s_.shape)

    for i in range(warped_t.shape[0]):
        new_t[path_[0, i], :] = warped_t[i, :]

    if has_time:
        Ts = np.arange(1, s_.shape[0] + 1)
        Ts = Ts.reshape(-1, 1)
        new_t = np.hstack((Ts, new_t))
    if get_distance:
        return new_t, dist_
    return new_t


warnings.simplefilter("ignore", category=RuntimeWarning)
warnings.simplefilter("ignore", category=DeprecationWarning)

exNames = {"circle", "square", "triangle", "complex", "swiperight", "swipeleft", "rotateright", "rotateleft", "scupcw",
           "scupccw"}
idx = 0

LABELS = {}
NAMES = {}
NAMESCAP = {}
exercises_by_type = {}
exercises_extended_by_type = {}
exercises_compressed_by_type = {}
slow_by_type = {}
slow_compressed_to_normal_by_type = {}
slow_compressed_to_fast_by_type = {}
fast_by_type = {}
fast_extended_to_normal_by_type = {}
fast_extended_to_slow_by_type = {}
labels_by_type = {}
lengths_by_type = {}
train_by_type = {}
test_by_type = {}
train_extended_by_type = {}
test_extended_by_type = {}
train_compressed_by_type = {}
test_compressed_by_type = {}

SUBJECTS = ['s1']

for name in exNames:
    LABELS[name] = idx
    NAMES[idx] = name
    exercises_by_type[name] = []
    exercises_extended_by_type[name] = []
    exercises_compressed_by_type[name] = []
    NAMESCAP[name] = name.title()
    train_by_type[name] = []
    slow_by_type[name] = []
    slow_compressed_to_normal_by_type[name] = []
    slow_compressed_to_fast_by_type[name] = []
    fast_by_type[name] = []
    fast_extended_to_normal_by_type[name] = []
    fast_extended_to_slow_by_type[name] = []
    test_by_type[name] = []
    train_extended_by_type[name] = []
    test_extended_by_type[name] = []
    train_compressed_by_type[name] = []
    test_compressed_by_type[name] = []
    labels_by_type[name] = []
    idx += 1
# LOAD FILES
matfiles = [f for f in listdir('matfiles') if (isfile(join('matfiles', f)))]

exercise_data = []
labels = []
addAccels = True
# DTW REGULAR DEMONSTRATIONS
addAccels = True
print('Aligning regular demonstrations')
for l in LABELS:
    print(l)
    tf_data = []
    for f in matfiles:
        if ('slow' not in f) and ('full' not in f) and ('fast' not in f) and (l in f):
            print(f)
            data = sio.loadmat('matfiles/' + f)
            data = data.get('data')
            for i in range(len(data)):
                exercise_data.append(data[i][:-1])
                labels.append(data[i][-1])
                tf_data.append(data[i][0:22])
            labels_by_type.get(l).append(data[:][:-1])
            if addAccels:
                t = data[:, 0:22]
                t = np.hstack((t, data[:, 26:29]))
                t = np.hstack((t, data[:, 33:36]))
                t = np.hstack((t, data[:, 40:43]))
                exercises_by_type.get(l).append(t)
            else:
                exercises_by_type.get(l).append(data[:, 0:22])
        else:
            continue

    maxlen = -1
    index = 0
    x = exercises_by_type.get(l)
    for ex in range(0, len(x)):
        if len(x[ex]) > maxlen:
            maxlen = len(x[ex])
            index = ex
    lengths_by_type[l] = maxlen
    for ex in range(0, len(x)):
        # print('----------')
        # print(x[ex].shape)
        x[ex], dis = align_signal(x[index],
                                  x[ex],
                                  has_time=True,
                                  get_distance=True)
        print(x[ex].shape)

    print("Adding slow and fast demonstrations")
    # for l in LABELS:
    tf_data = []
    for f in matfiles:
        if (('slow' in f) or ('fast' in f)) and ('full' not in f) and (l in f):
            print(f)
            data = sio.loadmat('matfiles/' + f)
            data = data.get('data')
            for i in range(len(data)):
                tf_data.append(data[i][0:22])
            if addAccels:
                t = data[:, 0:22]
                t = np.hstack((t, data[:, 26:29]))
                t = np.hstack((t, data[:, 33:36]))
                t = np.hstack((t, data[:, 40:43]))
                if 'slow' in f:
                    slow_by_type.get(l).append(t)
                else:
                    fast_by_type.get(l).append(t)
            else:
                if 'slow' in f:
                    slow_by_type.get(l).append(data[:, 0:22])
                else:
                    fast_by_type.get(l).append(data[:, 0:22])
        else:
            continue

        # COMPRESS SLOW DEMONSTRATIONS
        #     print('Compressing slow and normal demonstrations')
        # for l in LABELS:
        #     print(NAMES.get(LABELS.get(l)))
        #     print('-----compress slow to normal-------')
        #     print(slow_by_type.get(l)[0].shape)
    slow_compressed_to_normal_by_type.get(l).append(align_signal(exercises_by_type.get(l)[0],
                                                                 slow_by_type.get(l)[0],
                                                                 has_time=True,
                                                                 get_distance=False)
                                                    )
    print(slow_compressed_to_normal_by_type.get(l)[0].shape)
    # print('-----compress slow to fast-------')
    # print(slow_by_type.get(l)[0].shape)
    slow_compressed_to_fast_by_type.get(l).append(align_signal(fast_by_type.get(l)[0],
                                                               slow_by_type.get(l)[0],
                                                               has_time=True,
                                                               get_distance=False)
                                                  )
    print(slow_compressed_to_fast_by_type.get(l)[0].shape)
    # print('----- compress normal to fast ----')
    x = exercises_by_type.get(l)
    # print(x[0].shape)
    for ex in range(len(x)):
        exercises_compressed_by_type.get(l).append(align_signal(fast_by_type.get(l)[0],
                                                                exercises_by_type.get(l)[ex],
                                                                has_time=True,
                                                                get_distance=False)
                                                   )
        # print('--------------------------')
        # print(exercises_compressed_by_type.get(l)[ex].shape)

    # EXTEND NORMAL DEMONSTRATIONS
    #     print("Extending normal and fast demonstration")
    # for l in LABELS:
    #     print(str(len(exercises_by_type.get(l)))+' ***********')
    x = exercises_by_type.get(l)
    # print('--------- extend normal to slow ---------')
    for ex in range(len(x)):
        exercises_extended_by_type.get(l).append(align_signal(slow_by_type.get(l)[0],
                                                              exercises_by_type.get(l)[ex],
                                                              has_time=True,
                                                              get_distance=False))
        print(exercises_extended_by_type.get(l)[ex].shape)
        # print('--------------------')
    # print('--------- extend fast to normal ---------')
    fast_extended_to_normal_by_type.get(l).append(align_signal(exercises_by_type.get(l)[0],
                                                               fast_by_type.get(l)[0],
                                                               has_time=True,
                                                               get_distance=False)
                                                  )
    # print(fast_extended_to_normal_by_type.get(l)[0].shape)
    # print('--------- extend fast to slow ---------')
    fast_extended_to_slow_by_type.get(l).append(align_signal(slow_by_type.get(l)[0],
                                                             fast_by_type.get(l)[0],
                                                             has_time=True,
                                                             get_distance=False)
                                                )
    print(fast_extended_to_slow_by_type.get(l)[0].shape)

    # print("Adding stamps")
    # ADD SEQUENCE NUMBERS
    #     for l in LABELS:
    x = exercises_by_type.get(l)
    maxlen = len(x[0])
    stamps = [[i] for i in range(maxlen)]
    for ex in range(0, len(x)):
        x[ex] = np.hstack((stamps, x[ex]))
    lengths_by_type[l] = maxlen

    x = slow_compressed_to_normal_by_type.get(l)
    for ex in range(0, len(x)):
        x[ex] = np.hstack((stamps, x[ex]))

    x = fast_extended_to_normal_by_type.get(l)
    for ex in range(0, len(x)):
        x[ex] = np.hstack((stamps, x[ex]))

    x = slow_by_type.get(l)
    maxlen = len(x[0])
    stamps = [[i] for i in range(maxlen)]
    for ex in range(len(x)):
        x[ex] = np.hstack((stamps, x[ex]))

    x = exercises_extended_by_type.get(l)
    for ex in range(len(x)):
        x[ex] = np.hstack((stamps, x[ex]))

    x = fast_extended_to_slow_by_type.get(l)
    for ex in range(len(x)):
        x[ex] = np.hstack((stamps, x[ex]))

    x = fast_by_type.get(l)
    maxlen = len(x[0])
    stamps = [[i] for i in range(maxlen)]
    for ex in range(len(x)):
        x[ex] = np.hstack((stamps, x[ex]))

    x = slow_compressed_to_fast_by_type.get(l)
    for ex in range(len(x)):
        x[ex] = np.hstack((stamps, x[ex]))

    x = exercises_compressed_by_type.get(l)
    for ex in range(len(x)):
        x[ex] = np.hstack((stamps, x[ex]))
    print("--------------------------------------")

labels = np.asarray(labels, dtype=np.int32)
exercise_data = np.asarray(exercise_data, dtype=np.float64)
tf_upper_data = exercise_data[:, 0:9]
tf_lower_data = exercise_data[:, 9:16]
tf_hand_data = exercise_data[:, 16:23]
imu_upper_data = exercise_data[:, 23:36]
imu_upper_data = imu_upper_data[:, 4:-3]
imu_lower_data = exercise_data[:, 36:49]
imu_lower_data = imu_lower_data[:, 4:-3]
imu_hand_data = exercise_data[:, 49:62]
imu_hand_data = imu_hand_data[:, 4:-3]
# print(exercise_data.shape)
# print('-------------')
# print('tf upper: {0}'.format(tf_upper_data.shape))
# print('tf lower: {0}'.format(tf_lower_data.shape))
# print('tf hand: {0}'.format(tf_hand_data.shape))
# print('-------------')
# print('imu upper: {0}'.format(imu_upper_data.shape))
# print('imu lower: {0}'.format(imu_lower_data.shape))
# print('imu hand: {0}'.format(imu_hand_data.shape))
# print('-------------')
full_data_tf = np.hstack((tf_upper_data, tf_lower_data))
full_data_tf = np.hstack((full_data_tf, tf_hand_data))
# print('tf full: {0}'.format(full_data_tf.shape))
# print('-------------')
full_data_imu = np.hstack((imu_upper_data, imu_lower_data))
full_data_imu = np.hstack((full_data_imu, imu_hand_data))
# print('imu full: {0}'.format(full_data_imu.shape))
# print('-------------')
full_data = np.hstack((full_data_imu, full_data_tf))
# print('full data: {0}'.format(full_data.shape))
# print('-------------')

training_data = []
training_labels = []
testing_data = []
testing_labels = []

print("Saving Test and training data")
for name in exNames:
    tfExercise = exercises_by_type.get(name)
    print(tfExercise[0].shape)
    tfExerciseExtended = exercises_extended_by_type.get(name)
    tfExerciseCompressed = exercises_compressed_by_type.get(name)
    fastExtendedToNormalExercise = fast_extended_to_normal_by_type.get(name)
    fastExtendedToSlowExercise = fast_extended_to_slow_by_type.get(name)
    slowCompressedtoFastExercise = slow_compressed_to_normal_by_type.get(name)
    slowCompressedtoNormalExercise = slow_compressed_to_fast_by_type.get(name)
    slowTfExercise = slow_by_type.get(name)[0]
    fastTfExercise = fast_by_type.get(name)[0]
    sio.savemat('matfiles/FastExtendedToNormal' + NAMESCAP.get(name) + 'Data.mat',
                mdict={'data': fastExtendedToNormalExercise})
    sio.savemat('matfiles/FastExtendedToSlow' + NAMESCAP.get(name) + 'Data.mat',
                mdict={'data': fastExtendedToSlowExercise})
    sio.savemat('matfiles/SlowCompressedToNormal' + NAMESCAP.get(name) + 'Data.mat',
                mdict={'data': slowCompressedtoNormalExercise})
    sio.savemat('matfiles/SlowCompressedToFast' + NAMESCAP.get(name) + 'Data.mat',
                mdict={'data': slowCompressedtoFastExercise})
    sio.savemat('matfiles/Slow' + NAMESCAP.get(name) + 'Data.mat', mdict={'data': slowTfExercise})
    sio.savemat('matfiles/Fast' + NAMESCAP.get(name) + 'Data.mat', mdict={'data': fastTfExercise})

    tfExerciseTrain = tfExercise[0:int((len(tfExercise)) * 0.6)]
    tfExerciseTest = tfExercise[int((len(tfExercise)) * 0.6):len(tfExercise)]
    tfExExtendedTrain = tfExerciseExtended[0:(len(tfExerciseExtended)) / 10 * 6]
    tfExExtendedTest = tfExerciseExtended[(len(tfExerciseExtended)) / 10 * 6 + 1:len(tfExerciseExtended)]
    tfExCompressedTrain = tfExerciseCompressed[0:(len(tfExerciseCompressed)) / 10 * 6]
    tfExCompressedTest = tfExerciseCompressed[(len(tfExerciseCompressed)) / 10 * 6 + 1:len(tfExerciseCompressed)]

    print("Training data size: " + str(len(tfExerciseTrain)))
    print("Tesing data size: " + str(len(tfExerciseTest)))
    for i in tfExerciseTrain:
        for x in i:
            training_data.append(x)
            train_by_type.get(name).append(x)
            training_labels.append(LABELS.get(name))
    sio.savemat('matfiles/' + NAMESCAP.get(name) + 'Data.mat', mdict={'data': train_by_type.get(name)})

    for i in tfExExtendedTrain:
        for x in i:
            train_extended_by_type.get(name).append(x)
    sio.savemat('matfiles/' + NAMESCAP.get(name) + 'ExtendedData.mat', mdict={'data': train_extended_by_type.get(name)})

    for i in tfExCompressedTrain:
        for x in i:
            train_compressed_by_type.get(name).append(x)
    sio.savemat('matfiles/' + NAMESCAP.get(name) + 'CompressedData.mat',
                mdict={'data': train_compressed_by_type.get(name)})

    for i in tfExerciseTest:
        for x in i:
            testing_data.append(x)
            test_by_type.get(name).append(x)
            testing_labels.append(LABELS.get(name))
            # print(l + ' ' + str(LABELS.get(name)))
    sio.savemat('matfiles/' + NAMESCAP.get(name) + 'DataTest.mat', mdict={'data': test_by_type.get(name)})

    for i in tfExExtendedTest:
        for x in i:
            # print(x)
            test_extended_by_type.get(name).append(x)
    sio.savemat('matfiles/' + NAMESCAP.get(name) + 'ExtendedDataTest.mat',
                mdict={'data': test_extended_by_type.get(name)})

    for i in tfExCompressedTest:
        for x in i:
            test_compressed_by_type.get(name).append(x)
    sio.savemat('matfiles/' + NAMESCAP.get(name) + 'CompressedDataTest.mat',
                mdict={'data': test_compressed_by_type.get(name)})
