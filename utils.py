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
ANNOTATION_FILE = '/Users/suhyunkim/Downloads/action_quality_dataset/diving/annotations/Diving.txt'

# TODO: it's the dir where all the pictures will be moved to. END IT WITH THE SLASH
KEYFRAME_DIR = '/Users/suhyunkim/Downloads/action_quality_dataset/keyframes_diving/val/'

# TODO: it's the dir where all the pictures will be moved to. END IT WITH THE SLASH
TEST_DIR = '/home/ek2993/michael/'

# TODO: it's the dir where all the pictures will be moved to. END IT WITH THE SLASH
TRAIN_DIR = '/home/ek2993/train/'

is_diving = True


def run_command(command, logfile=None, print_output=True, return_output=True):
    # if logfile != None:
    #     command += ' |& tee ' + logfile
    output = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        executable='/bin/bash'
    ).stdout.read()
    if print_output:
        print(output)
    if return_output:
        return str(output)


# move the pictures to a certain directory and create labels
arr_picture = np.array([])
arr_total_score = np.array([])
arr_difficulty_score = np.array([])


def get_x_and_y():
    with open(ANNOTATION_FILE) as filename:
        counter = 0
        supposed_to_be_counter = 0
        for line in filename:
            print(line)
            if '#' in line:
                continue
            if 'A' in line:
                print(line)
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

                for i in range(start, end + 1):
                    str_num = "{:0>7d}".format(i)
                    pic_name = "frame" + str_num + ".png"
                    supposed_to_be_counter += 1
                    if os.path.exists(f"{KEYFRAME_DIR}{pic_name}"):
                        counter += 1
                        arr_picture = np.append(arr_picture, f"{KEYFRAME_DIR}{pic_name}")

                    # print(pic_name)

                    # choose the right pictures
                    # run_command(f"mv {PICTURE_SOURCE_DIR}{pic_name} {KEYFRAME_DIR}")

            if 'Score' in line and is_diving:
                line_arr = line.split()
                arr_sub_total_score = np.empty(counter)
                arr_sub_total_score.fill(line_arr[2])

                arr_sub_difficulty_score = np.empty(counter)
                arr_sub_difficulty_score.fill(line_arr[3])

                arr_total_score = np.append(arr_total_score, arr_sub_total_score)
                arr_difficulty_score = np.append(arr_difficulty_score, arr_sub_difficulty_score)

                # print(arr_sub_total_score)
    return arr_picture, arr_total_score


# print(arr_total_score)
# print(arr_difficulty_score)


def get_total_score_labels():
    return arr_total_score


def get_difficulty_score_labels():
    return arr_difficulty_score


def move_train_files_to_test():
    # counter: 159, test: 31
    counter_action_set = 0
    # count how many files are in ls -1 | wc -l

    with open(ANNOTATION_FILE) as filename:
        counter = 0
        supposed_to_be_counter = 0
        for line in filename:
            if counter_action_set == 30:
                break
            print(line)
            if '#' in line:
                continue
            if 'A' in line:
                counter_action_set += 1
                print(line)
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

                for i in range(start, end + 1):
                    str_num = "{:0>7d}".format(i)
                    pic_name = "frame" + str_num + ".png"
                    supposed_to_be_counter += 1
                    if os.path.exists(f"{KEYFRAME_DIR}/{pic_name}"):
                        counter += 1
                        run_command(f"mv {KEYFRAME_DIR}{pic_name} {VAL_DIR}")
                        # print(pic_name)

                    else:
                        print(
                            f'$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ WARNING {pic_name} DOES NOT EXIST $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

                # print(arr_sub_total_score)


def train_labels():
    # move the pictures to a certain directory and create labels
    arr_frame = np.array([])
    arr_score = np.array([])
    arr_difficulty = np.array([])

    with open(ANNOTATION_FILE) as filename:
        counter = 0
        supposed_to_be_counter = 0
        for line in filename:
            print(line)
            if '#' in line:
                continue
            if 'A' in line:
                print(line)
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

                for i in range(start, end + 1):
                    str_num = "{:0>7d}".format(i)
                    pic_name = "frame" + str_num + ".png"
                    supposed_to_be_counter += 1
                    if os.path.exists(f"{TRAIN_DIR}{pic_name}"):
                        counter += 1
                        arr_frame = np.append(arr_frame, f"{pic_name}")

                    # print(pic_name)

                    # choose the right pictures
                    # run_command(f"mv {PICTURE_SOURCE_DIR}{pic_name} {KEYFRAME_DIR}")

            if 'Score' in line and is_diving:
                line_arr = line.split()
                arr_sub_total_score = np.empty(counter)
                arr_sub_total_score.fill(line_arr[2])

                arr_sub_difficulty_score = np.empty(counter)
                arr_sub_difficulty_score.fill(line_arr[3])

                arr_score = np.append(arr_score, arr_sub_total_score)
                arr_difficulty = np.append(arr_difficulty, arr_sub_difficulty_score)
                counter = 0
                # print(arr_sub_total_score)

    stacked_array = np.stack((arr_frame, arr_score, arr_difficulty), axis=-1)
    dataset_write = pd.DataFrame(
        {'0': stacked_array[:, 0], '1': stacked_array[:, 1], '2': stacked_array[:, 2]})

    print('data_write')
    print(dataset_write)
    data_in_csv = dataset_write.to_csv(index=False)

    with open('train.csv', 'wb') as f:
        pickle.dump(data_in_csv, f)

    data_read = pd.read_csv('train.csv', encoding="ISO-8859-1")

    print('data_read')
    print(data_read)
    return dataset_write.equals(data_read)


def test_labels():
    # move the pictures to a certain directory and create labels
    arr_frame = np.array([])
    arr_score = np.array([])
    arr_difficulty = np.array([])

    with open(ANNOTATION_FILE) as filename:
        counter = 0
        supposed_to_be_counter = 0
        for line in filename:
            print(line)
            if '#' in line:
                continue
            if 'A' in line:
                print(line)
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

                for i in range(start, end + 1):
                    str_num = "{:0>7d}".format(i)
                    pic_name = "frame" + str_num + ".png"
                    supposed_to_be_counter += 1
                    if os.path.exists(f"{TEST_DIR}{pic_name}"):
                        counter += 1
                        arr_frame = np.append(arr_frame, f"{pic_name}")

                    # print(pic_name)

                    # choose the right pictures
                    # run_command(f"mv {PICTURE_SOURCE_DIR}{pic_name} {KEYFRAME_DIR}")

            if 'Score' in line and is_diving:
                line_arr = line.split()
                arr_sub_total_score = np.empty(counter)
                arr_sub_total_score.fill(line_arr[2])

                arr_sub_difficulty_score = np.empty(counter)
                arr_sub_difficulty_score.fill(line_arr[3])

                arr_score = np.append(arr_score, arr_sub_total_score)
                arr_difficulty = np.append(arr_difficulty, arr_sub_difficulty_score)
                counter = 0
                # print(arr_sub_total_score)

    stacked_array = np.stack((arr_frame, arr_score, arr_difficulty), axis=-1)
    dataset_write = pd.DataFrame(
        {'0': stacked_array[:, 0], '1': stacked_array[:, 1], '2': stacked_array[:, 2]})

    print('data_write')
    print(dataset_write)
    data_in_csv = dataset_write.to_csv(index=False)

    with open('test.csv', 'wb') as f:
        pickle.dump(data_in_csv, f)

    data_read = pd.read_csv('test.csv', encoding="ISO-8859-1")

    print('data_read')
    print(data_read)
    return dataset_write.equals(data_read)


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

    return arr_frame_flat, arr_score, arr_difficulty

    # print(f'final: {len(arr_frame)}; group counter: {group_counter}; one_group_counter: {one_group_counter}')
    #stacked_array = np.stack((arr_frame, arr_score, arr_difficulty), axis=-1)

get_pose_labels()
# test_labels()
