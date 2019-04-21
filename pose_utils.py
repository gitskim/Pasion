import subprocess
import numpy as np
import os.path
import pandas as pd
import pickle
import scipy.io as sio

# TODO: end it with the slash
PICTURE_SOURCE_DIR = '/Users/suhyunkim/Downloads/action_quality_dataset/keyframes/'

# TODO:
# ANNOTATION_FILE = '/Users/suhyunkim/Downloads/action_quality_dataset/diving/annotations/Diving_-_Men_10_Prel._-_London_2012_Olympic_Game__eEKo5bGe5bU.txt'
ANNOTATION_FILE = '/home/suhyunkim011/Pasion/Diving.txt'

# TODO: it's the dir where all the pictures will be moved to. END IT WITH THE SLASH
KEYFRAME_DIR = '/Users/suhyunkim/Downloads/action_quality_dataset/keyframes_diving/val/'

# TODO: it's the dir where all the pictures will be moved to. END IT WITH THE SLASH
TEST_DIR = '/home/ek2993/michael/'

# TODO: it's the dir where all the pictures will be moved to. END IT WITH THE SLASH
TRAIN_DIR = '/home/ek2993/train/'

MAT_FILE = '/home/suhyunkim011/Pasion/diving.mat'
is_diving = True

def get_pose_labels():
    # move the pictures to a certain directory and create labels
    contents = sio.loadmat("/Users/suhyunkim/git/Pasion/diving.mat")
    print(len(contents))
    tracked = contents['boxes_tracked_wholevideo']
    print(tracked)
    print(len(tracked))
    # (298387, 107)
    print(tracked.shape)

    print(tracked[0].shape)

    arr_frame = []
    arr_frame_flat = []
    arr_score = np.array([])
    arr_difficulty = np.array([])

    with open(ANNOTATION_FILE) as filename:
        max_counter = 202
        group_counter = 0
        one_group_counter = 0
        max_one_group_counter = 0
        supposed_to_be_counter = 0
        for line in filename:
            print(line)
            if '#' in line:
                continue

            if 'A' in line:
                # print(line)
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

                pose_group = []
                for i in range(start, end + 1):
                    one_group_counter += 1
                    supposed_to_be_counter += 1

                    pose_group.append(tracked[i])
                    arr_frame_flat.append(tracked[i])
                    # print(len(arr_frame))

                    # print(pic_name)

                    # choose the right pictures
                    # run_command(f"mv {PICTURE_SOURCE_DIR}{pic_name} {KEYFRAME_DIR}")


                if one_group_counter > max_one_group_counter:
                    max_one_group_counter = one_group_counter

                # len(pose_group): 169; one_group_counter: 169; max_one_group_counter: 202
                print(f'len(pose_group): {len(pose_group)};  one_group_counter * 202 = {one_group_counter * 202}; one_group_counter: {one_group_counter}; max_one_group_counter: {max_one_group_counter};'
                      f'group_counter: {group_counter}')

                if one_group_counter < 202:
                    rem_count = 202 - one_group_counter
                    for i in range(one_group_counter, 202):
                        pose_group.append(np.zeros(107))
                        arr_frame_flat.append(tracked[i])


                arr_frame.append(pose_group) #figure out why it worked when I put it above the if one_group_counter > max_one_group_counter:
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

        print(f'arr_frame_flat: {len(arr_frame_flat)}, arr_frame: {len(arr_frame)}, arr_frame[1]: {len(arr_frame[1])}, arr_score: {len(arr_score)}, arr_difficulty: {len(arr_difficulty)}')
        print(f'arr_frame_flat: {len(arr_frame_flat)}, arr_score: {len(arr_score)}, arr_difficulty: {len(arr_difficulty)}')
    return arr_frame_flat, arr_score, arr_difficulty

get_pose_labels()
