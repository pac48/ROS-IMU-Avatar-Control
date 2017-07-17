#!/usr/env/python
from __future__ import print_function
import platform
import copy

print(platform.platform())
import sys

print("Python", sys.version)
import numpy as np;

print("NumPy", np.__version__)
import scipy

print("SciPy", scipy.__version__)
import sklearn

print("Scikit-Learn", sklearn.__version__)

import scipy.io as sio
import segment
from pomegranate import *
from os import listdir
from os.path import isfile, join
from pypr.stattest import *
import warnings

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
    # get angle in radians and then convert to degrees
    angle = math.acos(dot_prod / magB / magA)
    ang_deg = math.degrees(angle) % 360
    if ang_deg - 180 >= 0:
        return 360 - ang_deg
    return ang_deg


def seg(x, y, name_, num):
    xyData = segment.DataContainer(x, y)
    # Create a segmenter instance which fill fit 2 straight lines
    segmenter = segment.TopDown(segment.LinearRegression, num)
    # segmenter = segment.BottomUp(segment.LinearRegression, num)
    # segmenter = segment.TopDown(segment.LineThroughEndPoints, num)
    # do the fitting
    fits = segmenter.segment(xyData)

    fitarr = []
    idx = 0
    for fit_ in fits.fits:
        # print(fit)
        # print(fit.data)
        # print(fit.coeff[0])
        # print(fit.coeff[1])
        # print((fit.data.y[len(fit.data.y) - 1] - fit.data.y[0]) / (fit.data.x[len(fit.data.x) - 1] - fit.data.x[0]))
        fitarr.append([fit_.data, len(fit_.data), fit_.coeff[0], fit_.coeff[1], fit_, fits])
    # print(fits)
    # fits.plot()
    # segment.plt.show()
    # exit()
    # segment.plt.savefig(name_ + "_segments")
    # segment.plt.close()
    return fitarr


def compare_fits(fit1, fit2):
    d = []
    for i_ in range(min(len(fit1), len(fit2))):
        d.append(compare_individual(fit1, fit2, i_))
    return d


def compare_individual(fit1, fit2, idx_):
    # try:
    #     dy1 = fit1[idx_][0].y[len(fit1[idx_][0].y) - 1] * fit1[idx_][2] - fit1[idx_][0].y[0] * fit1[idx_][2]
    #     dx1 = fit1[idx_][0].x[len(fit1[idx_][0].x) - 1] - fit1[idx_][0].x[0]
    # except:
    #     print(idx_)
    #     print(len(fit1[0]))
    #     print(len(fit2[0]))
    #     print(fit1[0])
    #     print(" ############## ")
    #     print(fit2[0])
    #
    if (idx_ >= len(fit1)) or (idx_ >= len(fit2)):
        idx_ = min(len(fit1) - 1, len(fit2) - 1)
    # print("------------")
    # print(idx_)
    # print(len(fit1))
    # print(len(fit2[idx_]))
    # p = fit1[idx_][0].x[len(fit1[idx_][0].x) - 1]
    # pp = fit1[idx_][0].x[0]
    # print("------------")
    x1_2 = fit1[idx_][0].x[len(fit1[idx_][0].x) - 1] - fit1[idx_][0].x[0]
    x1_1 = 0
    y1_2 = x1_2 * fit1[idx_][2]
    y1_1 = 0
    dy1 = y1_2 - y1_1
    dx1 = x1_2 - x1_1
    s1 = math.atan2(dy1, dx1)

    # dy2 = fit2[idx_][0].y[len(fit2[idx_][0].y) - 1] * fit2[idx_][2] - fit2[idx_][0].y[0] * fit2[idx_][2]
    # dx2 = fit2[idx_][0].x[len(fit2[idx_][0].x) - 1] - fit2[idx_][0].x[0]
    x2_2 = fit2[idx_][0].x[max(len(fit2[idx_][0].x) - 1, 0)] - fit2[idx_][0].x[0]
    x2_1 = 0
    y2_2 = x2_2 * fit2[idx_][2]
    y2_1 = 0
    dy2 = y2_2 - y2_1
    dx2 = x2_2 - x2_1

    s2 = math.atan2(dy2, dx2)
    # ret = abs(s1) - abs(s2)

    if s2 < 0:
        s2 = math.pi + s2
    if s1 < 0:
        s1 = math.pi + s1
    # print(s1 - s2)
    # print(s2 - s1)
    # anga = [[x1_1, y1_1], [x1_2, y1_2]]
    # angb = [[x2_1, y2_1], [x2_2, y2_2]]
    # ret_a = math.atan2(x2_2, y2_2)
    # ret_b = math.atan2(x1_2, y1_2)
    # ret = ang([[x1_1, y1_1], [x1_2, y1_2]], [[x2_1, y2_1], [x2_2, y2_2]])
    # print(math.atan2(dy2, dx2))
    # print(math.atan2(dx2, dy2))

    # cosang = np.dot(anga, angb)
    # sinang = la.norm(np.cross(anga, angb))

    ret = abs(s1 - s2)
    if ret > math.pi / 2:
        ret = math.pi - ret
    # ret = abs(min(s1 - s2, s2 - s1))
    if PRINT and (ret > 2):
        # return s1 - s2
        # print(fit1)
        # print("****************")
        # print(fit2)
        print("****************")
        # fit1[idx_][5].plot()
        # fit2[idx_][5].plot()
        # print(fit1[idx_])
        print(s1)
        print(s2)
        print(ret)
        # print(fit1[idx_][2])
        # print(fit2[idx_][2])
        print("****************")
    # segment.plt.show()
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

joints = {"upper", "lower", "hand"}

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
y_upper = {}
z_upper = {}
x_lower = {}
y_lower = {}
z_lower = {}
x_hand = {}
y_hand = {}
z_hand = {}

x_ang_upper = {}
y_ang_upper = {}
z_ang_upper = {}

x_ang_upper_new = {}
y_ang_upper_new = {}
z_ang_upper_new = {}

x_ang_lower = {}
y_ang_lower = {}
z_ang_lower = {}

x_ang_lower_new = {}
y_ang_lower_new = {}
z_ang_lower_new = {}

x_ang_hand = {}
y_ang_hand = {}
z_ang_hand = {}

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
# print(outfiles)
# print(tfiles)

fastFiles = [f for f in listdir(directory) if (isfile(join(directory, f))
                                               and ('OutputFastTest' in f)
                                               and ('Extended' not in f)
                                               and ('Square' not in f)
                                               and ('Triangle' not in f)
                                               and ('Circle' not in f)
                                               and ('Complex' not in f)
                                               and ('Compressed' not in f))]

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

print(fastFiles)
print(slowFiles)

for name in exNames:
    nm = NAMESCAP.get(name)
    for of in outfiles:
        if (nm in of) and ('Output' in of) and ('Test' not in of):
            print(of)
            if 'Hand' in of:
                data = sio.loadmat(directory + of)
                data = data.get('handset')
                directrix_hand[name] = data[0][1]
                # print(directrix_hand['name'].shape)

                # x_hand[name] = data[0][1][:, 0]
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
    # fits_.get(name).append(seg(x_upper.get(name), y_upper.get(name), name + "_XYUpper", NUM_SEGMENTS))
    # fits_.get(name).append(seg(x_upper.get(name), z_upper.get(name), name + "_XZUpper", NUM_SEGMENTS))
    # fits_.get(name).append(seg(y_upper.get(name), z_upper.get(name), name + "_YZUpper", NUM_SEGMENTS))
    #
    # fits_.get(name).append(seg(x_ang_upper.get(name), y_ang_upper.get(name), name + "_XYAngUpper", NUM_SEGMENTS))
    # fits_.get(name).append(seg(x_ang_upper.get(name), z_ang_upper.get(name), name + "_XZAngUpper", NUM_SEGMENTS))
    # fits_.get(name).append(seg(y_ang_upper.get(name), z_ang_upper.get(name), name + "_YZAngUpper", NUM_SEGMENTS))

    # fits_.get(name).append(seg(x_ang_upper_new.get(name), y_ang_upper_new.get(name)))
    # fits_.get(name).append(seg(x_ang_upper_new.get(name), z_ang_upper_new.get(name)))
    # fits_.get(name).append(seg(y_ang_upper_new.get(name), z_ang_upper_new.get(name)))
    # fits_.get(name).append(seg(x_ang_upper.get(name), range(len(x_ang_upper.get(name)))))
    # fits_.get(name).append(seg(y_ang_upper.get(name), range(len(x_ang_upper.get(name)))))
    # fits_.get(name).append(seg(z_ang_upper.get(name), range(len(x_ang_upper.get(name)))))

    # fits_.get(name).append(seg(x_lower.get(name), y_lower.get(name), name + "_XYLower", NUM_SEGMENTS))
    # fits_.get(name).append(seg(x_lower.get(name), z_lower.get(name), name + "_XZLower", NUM_SEGMENTS))
    # fits_.get(name).append(seg(y_lower.get(name), z_lower.get(name), name + "_YZLower", NUM_SEGMENTS))
    #
    # fits_.get(name).append(seg(x_ang_lower.get(name), y_ang_lower.get(name), name + "_XYAngLower", NUM_SEGMENTS))
    # fits_.get(name).append(seg(x_ang_lower.get(name), z_ang_lower.get(name), name + "_XZAngLower", NUM_SEGMENTS))
    # fits_.get(name).append(seg(y_ang_lower.get(name), z_ang_lower.get(name), name + "_YZAngLower", NUM_SEGMENTS))

    # fits_.get(name).append(seg(x_ang_lower_new.get(name), y_ang_lower_new.get(name)))
    # fits_.get(name).append(seg(x_ang_lower_new.get(name), z_ang_lower_new.get(name)))
    # fits_.get(name).append(seg(y_ang_lower_new.get(name), z_ang_lower_new.get(name)))
    # fits_.get(name).append(seg(x_ang_lower.get(name), range(len(x_ang_upper.get(name)))))
    # fits_.get(name).append(seg(y_ang_lower.get(name), range(len(x_ang_upper.get(name)))))
    # fits_.get(name).append(seg(z_ang_lower.get(name), range(len(x_ang_upper.get(name)))))

    # fits_.get(name).append(seg(x_hand.get(name), y_hand.get(name), name + "_XYHand", NUM_SEGMENTS))
    # fits_.get(name).append(seg(x_hand.get(name), z_hand.get(name), name + "_XZHand", NUM_SEGMENTS))
    # fits_.get(name).append(seg(y_hand.get(name), z_hand.get(name), name + "_YZHand", NUM_SEGMENTS))
    #
    # fits_.get(name).append(seg(x_ang_hand.get(name), y_ang_hand.get(name), name + "_XYAngHand", NUM_SEGMENTS))
    # fits_.get(name).append(seg(x_ang_hand.get(name), z_ang_hand.get(name), name + "_XZAngHand", NUM_SEGMENTS))
    # fits_.get(name).append(seg(y_ang_hand.get(name), z_ang_hand.get(name), name + "_YZAngHand", NUM_SEGMENTS))

    # fits_.get(name).append(seg(x_ang_hand_new.get(name), y_ang_hand_new.get(name)))
    # fits_.get(name).append(seg(x_ang_hand_new.get(name), z_ang_hand_new.get(name)))
    # fits_.get(name).append(seg(y_ang_hand_new.get(name), z_ang_hand_new.get(name)))
    # fits_.get(name).append(seg(x_ang_hand.get(name), range(len(x_ang_upper.get(name)))))
    # fits_.get(name).append(seg(x_ang_hand.get(name), range(len(x_ang_upper.get(name)))))
    # fits_.get(name).append(seg(y_ang_hand.get(name), range(len(x_ang_upper.get(name)))))

# FIND ALL THE TEST FILES
testfiles = []
for tf_ in tfiles:
    for nm in exNames:
        if (NAMESCAP.get(nm) in tf_) and ('Compressed' not in tf_) and ('Extended' not in tf_):
            testfiles.append(tf_)

print(testfiles)

correct = 0
wrong = 0
total = 0
fileidx = 0

correct = 0
wrong = 0
almost_correct = 0

# LOAD A TEST FILE
correct_answers = {1: 0, 2: 0, 3: 0, 4: 0}
wrong_answers = {1: 0, 2: 0, 3: 0, 4: 0}

for exercise in exNames:
    array_idx = 0
    test_idx = 0
    upperfile = directory + NAMESCAP.get(exercise) + 'UpperOutputTest.mat'
    lowerfile = directory + NAMESCAP.get(exercise) + 'LowerOutputTest.mat'
    handfile = directory + NAMESCAP.get(exercise) + 'HandOutputTest.mat'

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
    print(exercise_size)
    print(file_size)
    while array_idx < file_size:
        xyzData = []

        xyzUpper = []
        xUpper = []
        yUpper = []
        zUpper = []
        xyzLower = []
        xLower = []
        yLower = []
        zLower = []
        xyzHand = []
        xHand = []
        yHand = []
        zHand = []

        angUpper = []
        xAngUpper = []
        yAngUpper = []
        zAngUpper = []
        angLower = []
        xAngLower = []
        yAngLower = []
        zAngLower = []
        angHand = []
        xAngHand = []
        yAngHand = []
        zAngHand = []

        split = exercise_size / NUM_SEGMENTS
        lastPoint = 1

        while test_idx < exercise_size:
            xUpper.append(xUpperTest[array_idx])
            yUpper.append(yUpperTest[array_idx])
            zUpper.append(zUpperTest[array_idx])

            xLower.append(xLowerTest[array_idx])
            yLower.append(yLowerTest[array_idx])
            zLower.append(zLowerTest[array_idx])

            xHand.append(xHandTest[array_idx])
            yHand.append(yHandTest[array_idx])
            zHand.append(zHandTest[array_idx])

            xAngUpper.append(xAngUpperTest[array_idx])
            yAngUpper.append(yAngUpperTest[array_idx])
            zAngUpper.append(zAngUpperTest[array_idx])

            xAngLower.append(xAngLowerTest[array_idx])
            yAngLower.append(yAngLowerTest[array_idx])
            zAngLower.append(zAngLowerTest[array_idx])

            xAngHand.append(xAngHandTest[array_idx])
            yAngHand.append(yAngHandTest[array_idx])
            zAngHand.append(zAngHandTest[array_idx])

            point = test_idx / split

            test_idx += 1
            array_idx += 1

            for cnt in range(1, NUM_SEGMENTS + 1):
                if point == cnt:
                    if lastPoint < point:
                        lastPoint = point
                        testFits = [
                            seg(xUpper, yUpper, str(fileidx) + "_test_" + exercise + "_XYUpper", point),  # 0
                            seg(xUpper, zUpper, str(fileidx) + "_test_" + exercise + "_XZUpper", point),  # 1
                            seg(yUpper, zUpper, str(fileidx) + "_test_" + exercise + "_YZUpper", point),  # 2

                            seg(xAngUpper, yAngUpper, str(fileidx) + "_test_" + exercise + "_XYAngUpper", point),
                            # 3
                            seg(xAngUpper, zAngUpper, str(fileidx) + "_test_" + exercise + "_XZAngUpper", point),
                            # 4
                            seg(yAngUpper, zAngUpper, str(fileidx) + "_test_" + exercise + "_YZAngUpper", point),
                            # 5
                            seg(xLower, yLower, str(fileidx) + "_test_" + exercise + "_XYLower", point),  # 6
                            seg(xLower, zLower, str(fileidx) + "_test_" + exercise + "_XZLower", point),  # 7
                            seg(yLower, zLower, str(fileidx) + "_test_" + exercise + "_YZLower", point),  # 8
                            seg(xAngLower, yAngLower, str(fileidx) + "_test_" + exercise + "_XYAngLower", point),
                            # 9
                            seg(xAngLower, zAngLower, str(fileidx) + "_test_" + exercise + "_XZAngLower", point),
                            # 10
                            seg(yAngLower, zAngLower, str(fileidx) + "_test_" + exercise + "_YZAngLower", point),
                            # 11
                            seg(xHand, yHand, str(fileidx) + "_test_" + exercise + "_XYHand", point),  # 12
                            seg(xHand, zHand, str(fileidx) + "_test_" + exercise + "_XZHand", point),  # 13
                            seg(yHand, zHand, str(fileidx) + "_test_" + exercise + "_YZHand", point),  # 14

                            seg(xAngHand, yAngHand, str(fileidx) + "_test_" + exercise + "_XYAngHand", point),
                            # 15
                            seg(xAngHand, zAngHand, str(fileidx) + "_test_" + exercise + "_XZAngHand", point),
                            # 16
                            seg(yAngHand, zAngHand, str(fileidx) + "_test_" + exercise + "_YZAngHand", point)
                            # 17
                        ]

                        candidates = {}
                        for name in exNames:
                            candidates[name] = 0

                        lastDec = 1
                        for sg in range(lastPoint):
                            for c in exNames:
                                if c not in candidates.keys():
                                    continue
                                print("---------------" + str(len(candidates)) + "--------------------")
                                candidate_exercise = c
                                print("Segment #" + str(sg + 1))
                                print("Actual exercise :" + exercise)
                                print("Comparing with :" + c)
                                # print(0)
                                d0 = compare_individual(testFits[0], fits_.get(c)[0], sg)
                                # print(d0)

                                # print(1)
                                d1 = compare_individual(testFits[1], fits_.get(c)[1], sg)
                                # print(d1)

                                # print(2)
                                d2 = compare_individual(testFits[2], fits_.get(c)[2], sg)
                                # print(d2)

                                # print(6)
                                d6 = compare_individual(testFits[6], fits_.get(c)[6], sg)
                                # print(d6)

                                # print(7)
                                d7 = compare_individual(testFits[7], fits_.get(c)[7], sg)
                                # print(d7)

                                # print(8)
                                d8 = compare_individual(testFits[8], fits_.get(c)[8], sg)
                                # print(d8)

                                # print(12)
                                d12 = compare_individual(testFits[12], fits_.get(c)[12], sg)
                                # print(d12)

                                # print(13)
                                d13 = compare_individual(testFits[13], fits_.get(c)[13], sg)
                                # print(d13)

                                # print(14)
                                d14 = compare_individual(testFits[14], fits_.get(c)[14], sg)
                                # print(d14)
                                # print(d0 + d1 + d2 + d6 + d7 + d8 + d12 + d13 + d14)
                                if WEIGHTS:
                                    total_distance_xy = ((d0 + d1 + d2 + d6 + d7 + d8 + d12 + d13 + d14) / 9) * \
                                                        exWeights.get(exercise)[0]
                                else:
                                    total_distance_xy = ((d0 + d1 + d2 + d6 + d7 + d8 + d12 + d13 + d14) / 9)
                                print(total_distance_xy)
                                # if ((d0 + d1 + d2 + d6 + d7 + d8 + d12 + d13 + d14) / 9) < XYZ_THR:
                                #     print(candidates)
                                #     print(candidate_exercise)
                                #     candidates.remove(candidate_exercise)
                                #     continue
                                # print("===============================")
                                # angle differences
                                # print(3)
                                d3 = compare_individual(testFits[3], fits_.get(c)[3], sg)
                                # print(d3)
                                #
                                # print(4)
                                d4 = compare_individual(testFits[4], fits_.get(c)[4], sg)
                                # print(d4)
                                #
                                # print(5)
                                d5 = compare_individual(testFits[5], fits_.get(c)[5], sg)
                                # print(d5)
                                #
                                # print(9)
                                d9 = compare_individual(testFits[9], fits_.get(c)[9], sg)
                                # print(d9)
                                #
                                # print(10)
                                d10 = compare_individual(testFits[10], fits_.get(c)[10], sg)
                                # print(d10)
                                #
                                # print(11)
                                d11 = compare_individual(testFits[11], fits_.get(c)[11], sg)
                                # print(d11)
                                #
                                # print(15)
                                d15 = compare_individual(testFits[15], fits_.get(c)[15], sg)
                                # print(d15)
                                #
                                # print(16)
                                d16 = compare_individual(testFits[16], fits_.get(c)[16], sg)
                                # print(d16)
                                #
                                # print(17)
                                d17 = compare_individual(testFits[17], fits_.get(c)[17], sg)
                                # print(d17)
                                # print(d3 + d4 + d5 + d9 + d10 + d11 + d15 + d16 + d17)
                                if WEIGHTS:
                                    total_distance_ang = ((d3 + d4 + d5 + d9 + d10 + d11 + d15 + d16 + d17) / 9) * \
                                                         exWeights.get(exercise)[1]
                                else:
                                    total_distance_ang = ((d3 + d4 + d5 + d9 + d10 + d11 + d15 + d16 + d17) / 9)
                                print(total_distance_ang)
                                # if ((d3 + d4 + d5 + d9 + d10 + d11 + d15 + d16 + d17) / 9) < ANG_THR:
                                #     print(candidates)
                                #     print(candidate_exercise)
                                #     candidates.remove(candidate_exercise)
                                #     continue
                                combined_distance = (total_distance_xy + total_distance_ang) / 2
                                # candidates.get(c).append(combined_distance)
                                candidates[c] = candidates.get(c) + combined_distance
                                print("Combined distance = " + str(combined_distance))
                                # print("---------------- &&&&&&&&&&&&&&&& -----------------")
                            # if (sg + 1) % NUM_SEGMENTS == DEC_STEP:
                            if lastDec == DEC_STEP:
                                lastDec = 0
                                # print("Popping")
                                for pop in range(POP_NUM):
                                    max_val = candidates.get(max(candidates, key=lambda i: candidates[i]))
                                    # itemSet = copy.copy(candidates.iteritems())
                                    for k in candidates.keys():
                                        if (candidates.get(k) == max_val) and (len(candidates) > 1):
                                            del candidates[k]
                            print(candidates)
                            lastDec += 1
                        min_value = candidates.get(min(candidates, key=lambda i: candidates[i]))
                        if exercise in candidates.keys():
                            almost_correct += 1
                            for k in candidates.keys():
                                if candidates.get(k) == min_value:
                                    if k == exercise:
                                        correct_answers[lastPoint] += 1
                                    else:
                                        wrong_answers[lastPoint] += 1
                        else:
                            wrong_answers[lastPoint] += 1
                        total += 1
        test_idx = 0

        # CALCULATE THE SEGMENTS FOR THE EXERCISE WE WANT TO PREDICT
        # print("Segmenting")
# print(str(correct) + "/" + str(total))
print(correct_answers)
print(wrong_answers)
print(almost_correct)
exit()
