#!/usr/env/python
from __future__ import print_function
import platform

print(platform.platform())
import sys

print("Python", sys.version)
import numpy as np

print("NumPy", np.__version__)
import scipy

print("SciPy", scipy.__version__)
import sklearn

print("Scikit-Learn", sklearn.__version__)

import segment
import operator
import scipy.io as sio
import traceback
from pomegranate import *
from os import listdir
from os.path import isfile, join
from pypr.stattest import *
import warnings

np.seterr(divide='ignore', invalid='ignore')

warnings.simplefilter('ignore', np.RankWarning)


def process_angles(array):
    sum_ = 0
    idx_ = 1
    processed = [0]
    while idx_ < len(array):
        if (array[idx] - array[idx - 1]) > 0.5:
            processed.append(1)
        elif (array[idx] - array[idx - 1]) < 0.5:
            processed.append(-1)
        else:
            processed.append(0)
        idx_ += 1
    return processed


def dot(vA, vB):
    return vA[0] * vB[0] + vA[1] * vB[1]


def ang(lineA, lineB):
    # vector form
    vA = [(lineA[0][0] - lineA[1][0]), (lineA[0][1] - lineA[1][1])]
    vB = [(lineB[0][0] - lineB[1][0]), (lineB[0][1] - lineB[1][1])]
    # dot prodcut
    dot_prod = dot(vA, vB)
    magA = dot(vA, vA) * .005
    magB = dot(vB, vB) * .005
    # get cosine value
    cos_ = dot_prod / magA / magB
    angle = math.acos(dot_prod / magB / magA)
    ang_deg = math.degrees(angle) % 360
    if ang_deg - 180 >= 0:
        return 360 - ang_deg
    return ang_deg


def seg(x, y, name_, num):
    xyData = segment.DataContainer(x, y)
    segmenter = segment.TopDown(segment.LinearRegression, num)
    fits = segmenter.segment(xyData)

    fitarr = []
    idx = 0
    for fit_ in fits.fits:
        fitarr.append([fit_.data, len(fit_.data), fit_.coeff[0], fit_.coeff[1], fit_, fits])

    return fitarr


def compare_fits(fit1, fit2):
    d = []
    for i_ in range(min(len(fit1), len(fit2))):
        d.append(compare_individual(fit1, fit2, i_))
    return d


def compare_individual(fit1, fit2, idx_):
    max1 = len(fit1)
    max2 = len(fit2)
    if idx_ > (len(fit1) - 1) or idx_ > (len(fit2) - 1):
        idx_ = min(len(fit1) - 1, len(fit2) - 1)
        pass
    try:
        x1_2 = fit1[idx_][0].x[len(fit1[idx_][0].x) - 1] - fit1[idx_][0].x[0]
        x1_1 = 0
        y1_2 = x1_2 * fit1[idx_][2]
        y1_1 = 0
        dy1 = y1_2 - y1_1
        dx1 = x1_2 - x1_1
        s1 = math.atan2(dy1, dx1)

        x2_2 = fit2[idx_][0].x[len(fit2[idx_][0].x) - 1] - fit2[idx_][0].x[0]
        x2_1 = 0
        y2_2 = x2_2 * fit2[idx_][2]
        y2_1 = 0
        dy2 = y2_2 - y2_1
        dx2 = x2_2 - x2_1
    except:
        ex, val, tb = sys.exc_info()
        traceback.print_exception(ex, val, tb)
        print(idx_)
        print(len(fit1))
        print(len(fit2))
        for i in range(len(fit1)):
            print(fit1[i])
        print(" ############## ")
        for i in range(len(fit2)):
            print(fit2[i])
        exit(-1)

    s2 = math.atan2(dy2, dx2)

    if s2 < 0:
        s2 = math.pi + s2
    if s1 < 0:
        s1 = math.pi + s1

    ret = abs(s1 - s2)
    if ret > math.pi / 2:
        ret = math.pi - ret
    if PRINT and (ret > 2):
        print("****************")
        print(s1)
        print(s2)
        print(ret)
        print("****************")
    return ret


NUM_SEGMENTS = 4
DEC_STEP = 2
POP_NUM = 4
DIF_THRESHOLD = 0.2
PRINT = True
WEIGHTS = True
XYZ_THR = 1.5
ANG_THR = 4.5

exNames = [
    "swiperight",
    "swipeleft",
    "rotateright",
    "rotateleft",
    "scupcw",
    "scupccw"
]

exWeights = {
    "swiperight": [0.8, 0.2],
    "swipeleft": [0.8, 0.2],
    "rotateright": [0.2, 0.8],
    "rotateleft": [0.2, 0.8],
    "scupcw": [0.6, 0.4],
    "scupccw": [0.6, 0.4],
}

segments = {
    "UPPERXY",
    "UPPERXZ"
    "UPPERYZ"
}

if len(sys.argv) == 2:
    directory = sys.argv[1]
else:
    directory = 'GMM-GMR-v2.0/data/'

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

idx = 0

LABELS = {}
NAMES = {}
NAMESCAP = {}
directrix_upper = {}
directrix_lower = {}
directrix_hand = {}

x_upper = {}
x_upper_rad = {}
y_upper = {}
y_upper_rad = {}
z_upper = {}
z_upper_rad = {}

x_lower = {}
x_lower_rad = {}
y_lower = {}
y_lower_rad = {}
z_lower = {}
z_lower_rad = {}

x_hand = {}
x_hand_rad = {}
y_hand = {}
y_hand_rad = {}
z_hand = {}
z_hand_rad = {}

x_ang_upper = {}
x_ang_upper_rad = {}
y_ang_upper = {}
y_ang_upper_rad = {}
z_ang_upper = {}
z_ang_upper_rad = {}

x_ang_upper_new = {}
y_ang_upper_new = {}
z_ang_upper_new = {}

x_ang_lower = {}
x_ang_lower_rad = {}
y_ang_lower = {}
y_ang_lower_rad = {}
z_ang_lower = {}
z_ang_lower_rad = {}

x_ang_lower_new = {}
y_ang_lower_new = {}
z_ang_lower_new = {}

x_ang_hand = {}
x_ang_hand_rad = {}
y_ang_hand = {}
y_ang_hand_rad = {}
z_ang_hand = {}
z_ang_hand_rad = {}

x_ang_hand_new = {}
y_ang_hand_new = {}
z_ang_hand_new = {}

xyzFFTupper = {}
xyzFFTlower = {}
xyzFFThand = {}

angFFTupper = {}
angFFTlower = {}
angFFThand = {}

fits_ = {}
SUBJECTS = ['s1']

print("Creating empty arrays to store training data")
for name in exNames:
    NAMESCAP[name] = name.title()

    x_upper[name] = []
    y_upper[name] = []
    z_upper[name] = []

    x_ang_upper[name] = []
    y_ang_upper[name] = []
    z_ang_upper[name] = []

    x_ang_upper_new[name] = []
    y_ang_upper_new[name] = []
    z_ang_upper_new[name] = []

    x_lower[name] = []
    y_lower[name] = []
    z_lower[name] = []

    x_ang_lower[name] = []
    y_ang_lower[name] = []
    z_ang_lower[name] = []

    x_ang_lower_new[name] = []
    y_ang_lower_new[name] = []
    z_ang_lower_new[name] = []

    x_hand[name] = []
    y_hand[name] = []
    z_hand[name] = []

    x_ang_hand[name] = []
    y_ang_hand[name] = []
    z_ang_hand[name] = []

    fits_[name] = []

outfiles = [f for f in listdir(directory) if (isfile(join(directory, f)))]

tfiles = [f for f in listdir(directory) if (isfile(join(directory, f))
                                            and ('OutputTest' in f))]

print("Output files")
print(outfiles)
print("Test files")
print(tfiles)

print("Loading created model exercises")
for name in exNames:
    nm = NAMESCAP.get(name)
    print("Current exercise: " + nm)
    for of in outfiles:
        if (nm in of) and ('Output' in of) and ('Test' not in of):
            print("Processing " + of)
            if 'Hand' in of:
                data = sio.loadmat(directory + of)
                data = data.get('handset')
                directrix_hand[name] = data[0][1]
                x_hand[name] = data[0][0][:, 0]
                y_hand[name] = data[0][0][:, 1]
                z_hand[name] = data[0][0][:, 2]
                angs = data[0][21]
                x_ang_hand[name] = data[0][21][:, 0]
                y_ang_hand[name] = data[0][21][:, 1]
                z_ang_hand[name] = data[0][21][:, 2]

                x_ang_hand_new[name] = process_angles(data[0][21][:, 0])
                y_ang_hand_new[name] = process_angles(data[0][21][:, 1])
                z_ang_hand_new[name] = process_angles(data[0][21][:, 2])

                x_hand_rad[name] = (abs(x_hand[name] - data[0][8]) + abs(x_hand[name] - data[0][14])) / 2
                y_hand_rad[name] = (abs(y_hand[name] - data[0][10]) + abs(y_hand[name] - data[0][16])) / 2
                z_hand_rad[name] = (abs(z_hand[name] - data[0][12]) + abs(z_hand[name] - data[0][18])) / 2
                x_ang_hand_rad[name] = (abs(x_ang_hand[name] - data[0][22]) + abs(x_ang_hand[name] - data[0][25])) / 2
                y_ang_hand_rad[name] = (abs(y_ang_hand[name] - data[0][23]) + abs(y_ang_hand[name] - data[0][26])) / 2
                z_ang_hand_rad[name] = (abs(z_ang_hand[name] - data[0][24]) + abs(z_ang_hand[name] - data[0][27])) / 2
            elif 'Lower' in of:
                data = sio.loadmat(directory + of)
                data = data.get('lowerset')
                directrix_lower['name'] = data[0][1]
                x_lower[name] = data[0][0][:, 0]
                y_lower[name] = data[0][0][:, 1]
                z_lower[name] = data[0][0][:, 2]

                angs = data[0][21]
                x_ang_lower[name] = data[0][21][:, 0]
                y_ang_lower[name] = data[0][21][:, 1]
                z_ang_lower[name] = data[0][21][:, 2]

                x_ang_lower_new[name] = process_angles(data[0][21][:, 0])
                y_ang_lower_new[name] = process_angles(data[0][21][:, 1])
                z_ang_lower_new[name] = process_angles(data[0][21][:, 2])

                x_lower_rad[name] = (abs(x_lower[name] - data[0][8]) + abs(x_lower[name] - data[0][14])) / 2
                y_lower_rad[name] = (abs(y_lower[name] - data[0][10]) + abs(y_lower[name] - data[0][16])) / 2
                z_lower_rad[name] = (abs(z_lower[name] - data[0][12]) + abs(z_lower[name] - data[0][18])) / 2
                x_ang_lower_rad[name] = (
                                        abs(x_ang_lower[name] - data[0][22]) + abs(x_ang_lower[name] - data[0][25])) / 2
                y_ang_lower_rad[name] = (
                                        abs(y_ang_lower[name] - data[0][23]) + abs(y_ang_lower[name] - data[0][26])) / 2
                z_ang_lower_rad[name] = (
                                        abs(z_ang_lower[name] - data[0][24]) + abs(z_ang_lower[name] - data[0][27])) / 2
            elif 'Upper' in of:
                data = sio.loadmat(directory + of)
                data = data.get('upperset')
                directrix_upper[name] = data[0][1]
                x_upper[name] = data[0][0][:, 0]
                y_upper[name] = data[0][0][:, 1]
                z_upper[name] = data[0][0][:, 2]

                angs = data[0][21]
                x_ang_upper[name] = data[0][21][:, 0]
                y_ang_upper[name] = data[0][21][:, 1]
                z_ang_upper[name] = data[0][21][:, 2]

                x_ang_upper_new[name] = process_angles(data[0][21][:, 0])
                y_ang_upper_new[name] = process_angles(data[0][21][:, 1])
                z_ang_upper_new[name] = process_angles(data[0][21][:, 2])

                x_upper_rad[name] = (abs(x_upper[name] - data[0][8]) + abs(x_upper[name] - data[0][14])) / 2
                y_upper_rad[name] = (abs(y_upper[name] - data[0][10]) + abs(y_upper[name] - data[0][16])) / 2
                z_upper_rad[name] = (abs(z_upper[name] - data[0][12]) + abs(z_upper[name] - data[0][18])) / 2
                x_ang_upper_rad[name] = (
                                        abs(x_ang_upper[name] - data[0][22]) + abs(x_ang_upper[name] - data[0][25])) / 2
                y_ang_upper_rad[name] = (
                                        abs(y_ang_upper[name] - data[0][23]) + abs(y_ang_upper[name] - data[0][26])) / 2
                z_ang_upper_rad[name] = (
                                        abs(z_ang_upper[name] - data[0][24]) + abs(z_ang_upper[name] - data[0][27])) / 2

    print("Splitting the exercise into " + str(NUM_SEGMENTS) + " segments")
    fits_.update({name:
        [
            seg(x_upper.get(name), y_upper.get(name), name + "_XYUpper", NUM_SEGMENTS),
            seg(x_upper.get(name), z_upper.get(name), name + "_XZUpper", NUM_SEGMENTS),
            seg(y_upper.get(name), z_upper.get(name), name + "_YZUpper", NUM_SEGMENTS),
            seg(x_ang_upper.get(name), y_ang_upper.get(name), name + "_XYAngUpper", NUM_SEGMENTS),
            seg(x_ang_upper.get(name), z_ang_upper.get(name), name + "_XZAngUpper", NUM_SEGMENTS),
            seg(y_ang_upper.get(name), z_ang_upper.get(name), name + "_YZAngUpper", NUM_SEGMENTS),
            seg(x_lower.get(name), y_lower.get(name), name + "_XYLower", NUM_SEGMENTS),
            seg(x_lower.get(name), z_lower.get(name), name + "_XZLower", NUM_SEGMENTS),
            seg(y_lower.get(name), z_lower.get(name), name + "_YZLower", NUM_SEGMENTS),
            seg(x_ang_lower.get(name), y_ang_lower.get(name), name + "_XYAngLower", NUM_SEGMENTS),
            seg(x_ang_lower.get(name), z_ang_lower.get(name), name + "_XZAngLower", NUM_SEGMENTS),
            seg(y_ang_lower.get(name), z_ang_lower.get(name), name + "_YZAngLower", NUM_SEGMENTS),
            seg(x_hand.get(name), y_hand.get(name), name + "_XYHand", NUM_SEGMENTS),
            seg(x_hand.get(name), z_hand.get(name), name + "_XZHand", NUM_SEGMENTS),
            seg(y_hand.get(name), z_hand.get(name), name + "_YZHand", NUM_SEGMENTS),
            seg(x_ang_hand.get(name), y_ang_hand.get(name), name + "_XYAngHand", NUM_SEGMENTS),
            seg(x_ang_hand.get(name), z_ang_hand.get(name), name + "_XZAngHand", NUM_SEGMENTS),
            seg(y_ang_hand.get(name), z_ang_hand.get(name), name + "_YZAngHand", NUM_SEGMENTS)
        ]}
    )

fastFiles = [f for f in listdir(directory) if (isfile(join(directory, f))
                                               and ('OutputFastTest' in f)
                                               and ('Extended' not in f)
                                               and ('Square' not in f)
                                               and ('Triangle' not in f)
                                               and ('Circle' not in f)
                                               and ('Complex' not in f)
                                               and ('Compressed' not in f))]

print("Fast files")
print(fastFiles)
slowFiles = [
    f for f in listdir(directory) if (isfile(join(directory, f))
                                      and ('OutputSlowTest' in f)
                                      and ('Extended' not in f)
                                      and ('Square' not in f)
                                      and ('Triangle' not in f)
                                      and ('Circle' not in f)
                                      and ('Complex' not in f)
                                      and ('Compressed' not in f))
]
print("Slow files")
print(slowFiles)

# FIND ALL THE TEST FILES
testfiles = []
for tf_ in tfiles:
    for nm in exNames:
        if (NAMESCAP.get(nm) in tf_) and ('Compressed' not in tf_) and ('Extended' not in tf_):
            testfiles.append(tf_)

print("Testifles")
print(testfiles)


def load_random_test_from_exercise(exercise_name):
    upperfile = directory + NAMESCAP.get(exercise_name) + 'UpperOutputTest.mat'
    lowerfile = directory + NAMESCAP.get(exercise_name) + 'LowerOutputTest.mat'
    handfile = directory + NAMESCAP.get(exercise_name) + 'HandOutputTest.mat'

    upper_data_test = sio.loadmat(upperfile)
    upper_data_test = upper_data_test.get('upperset')
    xUpperTest = upper_data_test[0][0][:, 0]
    yUpperTest = upper_data_test[0][0][:, 1]
    zUpperTest = upper_data_test[0][0][:, 2]
    xAngUpperTest = upper_data_test[0][20][:, 0]
    yAngUpperTest = upper_data_test[0][20][:, 1]
    zAngUpperTest = upper_data_test[0][20][:, 2]

    lower_data_test = sio.loadmat(lowerfile)
    lower_data_test = lower_data_test.get('lowerset')
    xLowerTest = lower_data_test[0][0][:, 0]
    yLowerTest = lower_data_test[0][0][:, 1]
    zLowerTest = lower_data_test[0][0][:, 2]
    xAngLowerTest = lower_data_test[0][20][:, 0]
    yAngLowerTest = lower_data_test[0][20][:, 1]
    zAngLowerTest = lower_data_test[0][20][:, 2]

    hand_data_test = sio.loadmat(handfile)
    hand_data_test = hand_data_test.get('handset')
    xHandTest = hand_data_test[0][0][:, 0]
    yHandTest = hand_data_test[0][0][:, 1]
    zHandTest = hand_data_test[0][0][:, 2]
    xAngHandTest = hand_data_test[0][20][:, 0]
    yAngHandTest = hand_data_test[0][20][:, 1]
    zAngHandTest = hand_data_test[0][20][:, 2]

    exercise_size = len(hand_data_test[0][19][0])
    file_size = len(hand_data_test[0][0])

    index = random.randrange(file_size / exercise_size)

    upper_x = xUpperTest[index * exercise_size:index * exercise_size + exercise_size]
    upper_y = yUpperTest[index * exercise_size:index * exercise_size + exercise_size]
    upper_z = zUpperTest[index * exercise_size:index * exercise_size + exercise_size]
    upper_x_ang = xAngUpperTest[index * exercise_size:index * exercise_size + exercise_size]
    upper_y_ang = yAngUpperTest[index * exercise_size:index * exercise_size + exercise_size]
    upper_z_ang = zAngUpperTest[index * exercise_size:index * exercise_size + exercise_size]

    lower_x = xLowerTest[index * exercise_size:index * exercise_size + exercise_size]
    lower_y = yLowerTest[index * exercise_size:index * exercise_size + exercise_size]
    lower_z = zLowerTest[index * exercise_size:index * exercise_size + exercise_size]
    lower_x_ang = xAngLowerTest[index * exercise_size:index * exercise_size + exercise_size]
    lower_y_ang = yAngLowerTest[index * exercise_size:index * exercise_size + exercise_size]
    lower_z_ang = zAngLowerTest[index * exercise_size:index * exercise_size + exercise_size]

    hand_x = xHandTest[index * exercise_size:index * exercise_size + exercise_size]
    hand_y = yHandTest[index * exercise_size:index * exercise_size + exercise_size]
    hand_z = zHandTest[index * exercise_size:index * exercise_size + exercise_size]
    hand_x_ang = xAngHandTest[index * exercise_size:index * exercise_size + exercise_size]
    hand_y_ang = yAngHandTest[index * exercise_size:index * exercise_size + exercise_size]
    hand_z_ang = zAngHandTest[index * exercise_size:index * exercise_size + exercise_size]

    upper = [upper_x, upper_y, upper_z, upper_x_ang, upper_y_ang, upper_z_ang]
    lower = [lower_x, lower_y, lower_z, lower_x_ang, lower_y_ang, lower_z_ang]
    hand = [hand_x, hand_y, hand_z, hand_x_ang, hand_y_ang, hand_z_ang]

    return [upper, lower, hand]


def extend_from_ending_point(array1, array2):
    ending_point = array1[-1]
    array2 = [x - array2[0] for x in array2]
    array2 = [x + ending_point for x in array2]
    return np.concatenate([array1, array2])


def reset_signal(trial):
    # print(trial['upper_x'])
    for joint in trial.keys():
        trial[joint] = [x - trial[joint][0] for x in trial[joint]]
    # print(trial['upper_x'])
    # exit()
    return trial


def classify(trial, exer="", num_segs=NUM_SEGMENTS, pop_num=POP_NUM, weights=WEIGHTS, exercise_string=""):
    print("Classifying incoming signal of " + exer)

    trial_segments = [seg(trial['upper_x'], trial['upper_y'], "", num_segs),
                      seg(trial['upper_x'], trial['upper_z'], "", num_segs),
                      seg(trial['upper_y'], trial['upper_z'], "", num_segs),
                      seg(trial['upper_x_ang'], trial['upper_y_ang'], "", num_segs),
                      seg(trial['upper_x_ang'], trial['upper_z_ang'], "", num_segs),
                      seg(trial['upper_y_ang'], trial['upper_z_ang'], "", num_segs),
                      seg(trial['lower_x'], trial['lower_y'], "", num_segs),
                      seg(trial['lower_x'], trial['lower_z'], "", num_segs),
                      seg(trial['lower_y'], trial['lower_z'], "", num_segs),
                      seg(trial['lower_x_ang'], trial['lower_y_ang'], "", num_segs),
                      seg(trial['lower_x_ang'], trial['lower_z_ang'], "", num_segs),
                      seg(trial['lower_y_ang'], trial['lower_z_ang'], "", num_segs),
                      seg(trial['hand_x'], trial['hand_y'], "", num_segs),
                      seg(trial['hand_x'], trial['hand_z'], "", num_segs),
                      seg(trial['hand_y'], trial['hand_z'], "", num_segs),
                      seg(trial['hand_x_ang'], trial['hand_y_ang'], "", num_segs),
                      seg(trial['hand_x_ang'], trial['hand_z_ang'], "", num_segs),
                      seg(trial['hand_y_ang'], trial['hand_z_ang'], "", num_segs)
                      ]
    candidates = {}
    for en in exNames:
        candidates[en] = 0

    # compare with primitive segments
    for i in range(num_segs):
        for ex in exNames:
            d0 = compare_individual(trial_segments[0], fits_.get(ex)[0], i)
            d1 = compare_individual(trial_segments[1], fits_.get(ex)[1], i)
            d2 = compare_individual(trial_segments[2], fits_.get(ex)[2], i)
            d6 = compare_individual(trial_segments[6], fits_.get(ex)[6], i)
            d7 = compare_individual(trial_segments[7], fits_.get(ex)[7], i)
            d8 = compare_individual(trial_segments[8], fits_.get(ex)[8], i)
            d12 = compare_individual(trial_segments[12], fits_.get(ex)[12], i)
            d13 = compare_individual(trial_segments[13], fits_.get(ex)[13], i)
            d14 = compare_individual(trial_segments[14], fits_.get(ex)[14], i)
            if weights:
                total_distance_xy = ((d0 + d1 + d2 + d6 + d7 + d8 + d12 + d13 + d14) / 9) * exWeights.get(ex)[0]
            else:
                total_distance_xy = ((d0 + d1 + d2 + d6 + d7 + d8 + d12 + d13 + d14) / 9)
            # print(total_distance_xy)
            d3 = compare_individual(trial_segments[3], fits_.get(ex)[3], i)
            d4 = compare_individual(trial_segments[4], fits_.get(ex)[4], i)
            d5 = compare_individual(trial_segments[5], fits_.get(ex)[5], i)
            d9 = compare_individual(trial_segments[9], fits_.get(ex)[9], i)
            d10 = compare_individual(trial_segments[10], fits_.get(ex)[10], i)
            d11 = compare_individual(trial_segments[11], fits_.get(ex)[11], i)
            d15 = compare_individual(trial_segments[15], fits_.get(ex)[15], i)
            d16 = compare_individual(trial_segments[16], fits_.get(ex)[16], i)
            d17 = compare_individual(trial_segments[17], fits_.get(ex)[17], i)
            if weights:
                total_distance_ang = ((d3 + d4 + d5 + d9 + d10 + d11 + d15 + d16 + d17) / 9) * exWeights.get(ex)[1]
            else:
                total_distance_ang = ((d3 + d4 + d5 + d9 + d10 + d11 + d15 + d16 + d17) / 9)
            # print(total_distance_ang)
            combined_distance = (total_distance_xy + total_distance_ang) / 2
            candidates[ex] = candidates.get(ex) + combined_distance
        print("*********************************")
        for cdt in candidates.keys():
            print(cdt + " " + str(candidates[cdt]))
        mindif = min(candidates.iteritems(), key=operator.itemgetter(1))[0]
        print(mindif)
        return mindif
