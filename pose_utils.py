import subprocess
import numpy as np
import os.path
import pickle
import scipy.io as sio

# TODO:
#ANNOTATION_FILE = '/home/suhyunkim011/Pasion/Diving.txt'
ANNOTATION_FILE = 'Diving.txt'

#MAT_FILE = '/home/suhyunkim011/Pasion/diving.mat'
MAT_FILE = 'diving.mat'

def get_pose_labels2():
    # move the pictures to a certain directory and create labels
    contents = sio.loadmat(MAT_FILE)
    # print(len(contents))
    tracked = contents['boxes_tracked_wholevideo']
    # print(tracked)
    # print(len(tracked))
    # (298387, 107)
    # print(tracked.shape)

    # print(tracked[0].shape)

    # batchsize = 298387; timesteps = 202; shape = 104;
    arr_frame = []
    arr_score = np.array([])
    arr_score_flat = []
    arr_difficulty = np.array([])
    arr_difficulty_flat = []

    with open(ANNOTATION_FILE) as filename:
        max_counter = 202
        group_counter = 0
        one_group_counter = 202
        supposed_to_be_counter = 0
        for line in filename:
            print(line)
            if '#' in line:
                continue

            if 'A' in line:

                group_counter += 1
                line_arr = line.split()
                # print(line_arr[0])
                # print(line_arr[1])
                start = -1
                end = -1

                for i in range(0, 2):
                    if i == 0:
                        start = line_arr[0]
                        start = int(start)

                    elif i == 1:
                        end = line_arr[1]
                        end = int(end)

                start = start - 1

                pose_group = np.zeros([202, 104])

                for i in range(start, end + 1):
                    supposed_to_be_counter += 1
                    converted = tracked[i][:104]
                    pose_group[one_group_counter, :] = converted
                    one_group_counter += 1

                if one_group_counter > max_counter:
                    max_counter = one_group_counter
                    print("-------------*********-----------------WARNING: Max counter changed: %d-------------*********", max_counter)
                # len(pose_group): 169; one_group_counter: 169; max_one_group_counter: 202

                # print(pose_group)
                arr_frame.append(pose_group)  # figure out why it worked when I put it above the if one_group_counter > max_one_group_counter:
                one_group_counter = 0

            if 'Score' in line:
                line_arr = line.split()
                arr_sub_total_score = np.empty(max_counter)
                arr_sub_total_score.fill(line_arr[2])

                arr_sub_difficulty_score = np.empty(max_counter)
                arr_sub_difficulty_score.fill(line_arr[3])

                arr_score = np.append(arr_score, arr_sub_total_score)
                arr_difficulty = np.append(arr_difficulty, arr_sub_difficulty_score)
                # print(arr_sub_total_score)

                arr_score_flat.append(line_arr[2])
                arr_difficulty_flat.append(line_arr[3])

        # print(f'arr_frame: {len(arr_frame)}, arr_score_flat: {len(arr_score_flat)}, arr_difficulty_concat: {len(arr_difficulty_flat)}')
        # print(f'arr_frame: {len(arr_frame)}')
        # print(arr_frame[71])
        print(np.array(arr_frame).shape)
    return np.array(arr_frame), arr_score_flat, arr_difficulty_flat

get_pose_labels2()