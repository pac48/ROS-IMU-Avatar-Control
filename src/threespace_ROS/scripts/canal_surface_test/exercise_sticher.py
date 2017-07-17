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

from pomegranate import *
import intialize_exercises as iex

print("Available test files")
print(iex.tfiles)
NUM_TESTS = 1
STITCH_LEN = 5
NUM_EXERCISES = len(iex.directrix_hand)
print(str(NUM_EXERCISES) + " available exercises")
for i in range(NUM_TESTS):
    current_exercise_primitive_index = []
    current_exercise_primitive = []
    current_exercise_primitive_upper = []
    current_exercise_primitive_lower = []
    current_exercise_primitive_hand = []
    exercise_string = ""

    # CREATE THE EXERCISE STICHED FROM THE PRIMITIVES
    print("Creating motion from primitives")
    for j in range(STITCH_LEN):
        new_ind = 0
        while True:
            new_ind = random.randrange(NUM_EXERCISES)
            if new_ind not in current_exercise_primitive_index:
                current_exercise_primitive_index.append(new_ind)
                exercise_string += (iex.exNames[new_ind] + " ")
                break
        if len(current_exercise_primitive_index) == 1:
            # This is the first primitive so just put the coordinates in the array
            current_exercise_primitive_upper_x = iex.x_upper[iex.exNames[new_ind]]
            current_exercise_primitive_upper_y = iex.y_upper[iex.exNames[new_ind]]
            current_exercise_primitive_upper_z = iex.z_upper[iex.exNames[new_ind]]
            current_exercise_primitive_upper_x_ang = iex.x_ang_upper[iex.exNames[new_ind]]
            current_exercise_primitive_upper_y_ang = iex.y_ang_upper[iex.exNames[new_ind]]
            current_exercise_primitive_upper_z_ang = iex.z_ang_upper[iex.exNames[new_ind]]
            ########################################
            current_exercise_primitive_lower_x = iex.x_upper[iex.exNames[new_ind]]
            current_exercise_primitive_lower_y = iex.y_lower[iex.exNames[new_ind]]
            current_exercise_primitive_lower_z = iex.z_lower[iex.exNames[new_ind]]
            current_exercise_primitive_lower_x_ang = iex.x_ang_lower[iex.exNames[new_ind]]
            current_exercise_primitive_lower_y_ang = iex.y_ang_lower[iex.exNames[new_ind]]
            current_exercise_primitive_lower_z_ang = iex.z_ang_lower[iex.exNames[new_ind]]
            ########################################
            current_exercise_primitive_hand_x = iex.x_upper[iex.exNames[new_ind]]
            current_exercise_primitive_hand_y = iex.y_hand[iex.exNames[new_ind]]
            current_exercise_primitive_hand_z = iex.z_hand[iex.exNames[new_ind]]
            current_exercise_primitive_hand_x_ang = iex.x_ang_hand[iex.exNames[new_ind]]
            current_exercise_primitive_hand_y_ang = iex.y_ang_hand[iex.exNames[new_ind]]
            current_exercise_primitive_hand_z_ang = iex.z_ang_hand[iex.exNames[new_ind]]
            continue
        else:
            # For the next add the end coordinates of the last
            primitive_array = iex.x_upper[iex.exNames[new_ind]]
            current_exercise_primitive_upper_x = iex.extend_from_ending_point(current_exercise_primitive_upper_x,
                                                                              primitive_array)

            primitive_array = iex.y_upper[iex.exNames[new_ind]]
            current_exercise_primitive_upper_y = iex.extend_from_ending_point(current_exercise_primitive_upper_y,
                                                                              primitive_array)

            primitive_array = iex.z_upper[iex.exNames[new_ind]]
            current_exercise_primitive_upper_z = iex.extend_from_ending_point(current_exercise_primitive_upper_z,
                                                                              primitive_array)

            primitive_array = iex.x_ang_upper[iex.exNames[new_ind]]
            current_exercise_primitive_upper_x_ang = iex.extend_from_ending_point(current_exercise_primitive_upper_x,
                                                                                  primitive_array)

            primitive_array = iex.y_ang_upper[iex.exNames[new_ind]]
            current_exercise_primitive_upper_y_ang = iex.extend_from_ending_point(
                current_exercise_primitive_upper_y_ang, primitive_array)

            primitive_array = iex.z_ang_upper[iex.exNames[new_ind]]
            current_exercise_primitive_upper_z_ang = iex.extend_from_ending_point(
                current_exercise_primitive_upper_z_ang, primitive_array)
            ########################################
            primitive_array = iex.x_lower[iex.exNames[new_ind]]
            current_exercise_primitive_lower_x = iex.extend_from_ending_point(current_exercise_primitive_lower_x,
                                                                              primitive_array)

            primitive_array = iex.y_lower[iex.exNames[new_ind]]
            current_exercise_primitive_lower_y = iex.extend_from_ending_point(current_exercise_primitive_lower_y,
                                                                              primitive_array)

            primitive_array = iex.z_lower[iex.exNames[new_ind]]
            current_exercise_primitive_lower_z = iex.extend_from_ending_point(current_exercise_primitive_lower_z,
                                                                              primitive_array)

            primitive_array = iex.x_ang_lower[iex.exNames[new_ind]]
            current_exercise_primitive_lower_x_ang = iex.extend_from_ending_point(current_exercise_primitive_lower_x,
                                                                                  primitive_array)

            primitive_array = iex.y_ang_lower[iex.exNames[new_ind]]
            current_exercise_primitive_lower_y_ang = iex.extend_from_ending_point(
                current_exercise_primitive_lower_y_ang, primitive_array)

            primitive_array = iex.z_ang_lower[iex.exNames[new_ind]]
            current_exercise_primitive_lower_z_ang = iex.extend_from_ending_point(
                current_exercise_primitive_lower_z_ang, primitive_array)
            ########################################
            primitive_array = iex.x_hand[iex.exNames[new_ind]]
            current_exercise_primitive_hand_x = iex.extend_from_ending_point(current_exercise_primitive_hand_x,
                                                                             primitive_array)

            primitive_array = iex.y_hand[iex.exNames[new_ind]]
            current_exercise_primitive_hand_y = iex.extend_from_ending_point(current_exercise_primitive_hand_y,
                                                                             primitive_array)

            primitive_array = iex.z_hand[iex.exNames[new_ind]]
            current_exercise_primitive_hand_z = iex.extend_from_ending_point(current_exercise_primitive_hand_z,
                                                                             primitive_array)

            primitive_array = iex.x_ang_hand[iex.exNames[new_ind]]
            current_exercise_primitive_hand_x_ang = iex.extend_from_ending_point(current_exercise_primitive_hand_x,
                                                                                 primitive_array)

            primitive_array = iex.y_ang_hand[iex.exNames[new_ind]]
            current_exercise_primitive_hand_y_ang = iex.extend_from_ending_point(
                current_exercise_primitive_hand_y_ang, primitive_array)

            primitive_array = iex.z_ang_hand[iex.exNames[new_ind]]
            current_exercise_primitive_hand_z_ang = iex.extend_from_ending_point(
                current_exercise_primitive_hand_z_ang, primitive_array)

    # CREATE THE STITCHED TEST EXERCISE
    print("Creating Stitched Exercise")
    test_exercise_upper_x = []
    test_exercise_upper_y = []
    test_exercise_upper_z = []
    test_exercise_upper_x_ang = []
    test_exercise_upper_y_ang = []
    test_exercise_upper_z_ang = []
    ##########################
    test_exercise_lower_x = []
    test_exercise_lower_y = []
    test_exercise_lower_z = []
    test_exercise_lower_x_ang = []
    test_exercise_lower_y_ang = []
    test_exercise_lower_z_ang = []
    ##########################
    test_exercise_hand_x = []
    test_exercise_hand_y = []
    test_exercise_hand_z = []
    test_exercise_hand_x_ang = []
    test_exercise_hand_y_ang = []
    test_exercise_hand_z_ang = []
    #########################
    for j in current_exercise_primitive_index:
        test_exercise = iex.exNames[j]
        random_ex = iex.load_random_test_from_exercise(test_exercise)
        if len(test_exercise_hand_x) == 0:
            test_exercise_upper_x = random_ex[0][0]
            test_exercise_upper_y = random_ex[0][1]
            test_exercise_upper_z = random_ex[0][2]
            test_exercise_upper_x_ang = random_ex[0][3]
            test_exercise_upper_y_ang = random_ex[0][4]
            test_exercise_upper_z_ang = random_ex[0][5]
            ##########################
            test_exercise_lower_x = random_ex[1][0]
            test_exercise_lower_y = random_ex[1][1]
            test_exercise_lower_z = random_ex[1][2]
            test_exercise_lower_x_ang = random_ex[1][3]
            test_exercise_lower_y_ang = random_ex[1][4]
            test_exercise_lower_z_ang = random_ex[1][5]
            ##########################
            test_exercise_hand_x = random_ex[2][0]
            test_exercise_hand_y = random_ex[2][1]
            test_exercise_hand_z = random_ex[2][2]
            test_exercise_hand_x_ang = random_ex[2][3]
            test_exercise_hand_y_ang = random_ex[2][4]
            test_exercise_hand_z_ang = random_ex[2][5]
            #########################
        else:
            test_exercise_upper_x = iex.extend_from_ending_point(test_exercise_upper_x, random_ex[0][0])
            test_exercise_upper_y = iex.extend_from_ending_point(test_exercise_upper_y, random_ex[0][1])
            test_exercise_upper_z = iex.extend_from_ending_point(test_exercise_upper_z, random_ex[0][2])
            test_exercise_upper_x_ang = iex.extend_from_ending_point(test_exercise_upper_x_ang, random_ex[0][3])
            test_exercise_upper_y_ang = iex.extend_from_ending_point(test_exercise_upper_y_ang, random_ex[0][4])
            test_exercise_upper_z_ang = iex.extend_from_ending_point(test_exercise_upper_z_ang, random_ex[0][5])
            ##########################
            test_exercise_lower_x = iex.extend_from_ending_point(test_exercise_lower_x, random_ex[1][0])
            test_exercise_lower_y = iex.extend_from_ending_point(test_exercise_lower_y, random_ex[1][1])
            test_exercise_lower_z = iex.extend_from_ending_point(test_exercise_lower_z, random_ex[1][2])
            test_exercise_lower_x_ang = iex.extend_from_ending_point(test_exercise_lower_x_ang, random_ex[1][3])
            test_exercise_lower_y_ang = iex.extend_from_ending_point(test_exercise_lower_y_ang, random_ex[1][4])
            test_exercise_lower_z_ang = iex.extend_from_ending_point(test_exercise_lower_z_ang, random_ex[1][5])
            ##########################
            test_exercise_hand_x = iex.extend_from_ending_point(test_exercise_hand_x, random_ex[2][0])
            test_exercise_hand_y = iex.extend_from_ending_point(test_exercise_hand_y, random_ex[2][1])
            test_exercise_hand_z = iex.extend_from_ending_point(test_exercise_hand_z, random_ex[2][2])
            test_exercise_hand_x_ang = iex.extend_from_ending_point(test_exercise_hand_x_ang, random_ex[2][3])
            test_exercise_hand_y_ang = iex.extend_from_ending_point(test_exercise_hand_y_ang, random_ex[2][4])
            test_exercise_hand_z_ang = iex.extend_from_ending_point(test_exercise_hand_z_ang, random_ex[2][5])
            #########################

    print("Stiched exercise: " + exercise_string)
    exercise_parts = exercise_string.split(" ")
    print(exercise_parts)
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # plt.title(exercise_string)
    # plt.plot(current_exercise_primitive_hand_x, current_exercise_primitive_hand_y, current_exercise_primitive_hand_z)
    # ax.set_xlabel('X axis')
    # ax.set_ylabel('Y axis')
    # ax.set_zlabel('Z axis')
    # plt.show()
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # plt.title(exercise_string)
    # plt.plot(test_exercise_hand_x, test_exercise_hand_y, test_exercise_hand_z)
    # ax.set_xlabel('X axis')
    # ax.set_ylabel('Y axis')
    # ax.set_zlabel('Z axis')
    # plt.show()
    print("Exercise :" + exercise_string)
    print(current_exercise_primitive_index)
    print("Exercise Length: " + str(len(test_exercise_hand_x)))

    idx = 0
    window = 0
    predicted_string = ""
    current_segment = {'upper_x': [], 'upper_y': [], 'upper_z': [], 'upper_x_ang': [], 'upper_y_ang': [],
                       'upper_z_ang': [], 'lower_x': [], 'lower_y': [], 'lower_z': [], 'lower_x_ang': [],
                       'lower_y_ang': [], 'lower_z_ang': [], 'hand_x': [], 'hand_y': [], 'hand_z': [], 'hand_x_ang': [],
                       'hand_y_ang': [], 'hand_z_ang': []}
    ################################
    while idx < len(test_exercise_hand_x):
        current_segment['upper_x'].append(test_exercise_upper_x[idx])
        current_segment['upper_y'].append(test_exercise_upper_y[idx])
        current_segment['upper_z'].append(test_exercise_upper_z[idx])
        current_segment['upper_x_ang'].append(test_exercise_upper_x_ang[idx])
        current_segment['upper_y_ang'].append(test_exercise_upper_y_ang[idx])
        current_segment['upper_z_ang'].append(test_exercise_upper_z_ang[idx])
        ################################
        current_segment['lower_x'].append(test_exercise_lower_x[idx])
        current_segment['lower_y'].append(test_exercise_lower_y[idx])
        current_segment['lower_z'].append(test_exercise_lower_z[idx])
        current_segment['lower_x_ang'].append(test_exercise_lower_x_ang[idx])
        current_segment['lower_y_ang'].append(test_exercise_lower_y_ang[idx])
        current_segment['lower_z_ang'].append(test_exercise_lower_z_ang[idx])
        ################################
        current_segment['hand_x'].append(test_exercise_hand_x[idx])
        current_segment['hand_y'].append(test_exercise_hand_y[idx])
        current_segment['hand_z'].append(test_exercise_hand_z[idx])
        current_segment['hand_x_ang'].append(test_exercise_hand_x_ang[idx])
        current_segment['hand_y_ang'].append(test_exercise_hand_y_ang[idx])
        current_segment['hand_z_ang'].append(test_exercise_hand_z_ang[idx])
        window += 1
        if window == (len(test_exercise_hand_x) / STITCH_LEN):
            predicted_string += iex.classify(current_segment) + " "
            window = 0
            current_segment = {'upper_x': [], 'upper_y': [], 'upper_z': [], 'upper_x_ang': [], 'upper_y_ang': [],
                               'upper_z_ang': [], 'lower_x': [], 'lower_y': [], 'lower_z': [], 'lower_x_ang': [],
                               'lower_y_ang': [], 'lower_z_ang': [], 'hand_x': [], 'hand_y': [], 'hand_z': [],
                               'hand_x_ang': [],
                               'hand_y_ang': [], 'hand_z_ang': []}
        idx += 1
    print("------------------------")
    print("Actual: " + exercise_string)
    print("Predicted: " + predicted_string)
    print("------------------------")
