import subprocess
import numpy as np
import os.path

# TODO: end it with the slash
PICTURE_SOURCE_DIR = '/Users/suhyunkim/Downloads/action_quality_dataset/keyframes/'

# TODO:
#ANNOTATION_FILE = '/Users/suhyunkim/Downloads/action_quality_dataset/diving/annotations/Diving_-_Men_10_Prel._-_London_2012_Olympic_Game__eEKo5bGe5bU.txt'
ANNOTATION_FILE = '/Users/suhyunkim/Downloads/action_quality_dataset/diving/annotations/Diving_-_Men_10_Prel._-_London_2012_Olympic_Game__eEKo5bGe5bU.txt'

# TODO: it's the dir where all the pictures will be moved to. END IT WITH THE SLASH
KEYFRAME_DIR = '/Users/suhyunkim/Downloads/action_quality_dataset/keykey/'

# TODO: it's the dir where all the pictures will be moved to. END IT WITH THE SLASH
VAL_DIR = '/Users/suhyunkim/Downloads/action_quality_dataset/val/'

# TODO: it's the dir where all the pictures will be moved to. END IT WITH THE SLASH
TEST_DIR = '/Users/suhyunkim/Downloads/action_quality_dataset/test/'

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
                    if os.path.exists(f"{KEYFRAME_DIR}/{pic_name}"):
                        counter += 1
                        arr_picture = np.append(arr_picture, f"{KEYFRAME_DIR}/{pic_name}")

                    # print(pic_name)

                    # choose the right pictures
                    #run_command(f"mv {PICTURE_SOURCE_DIR}{pic_name} {KEYFRAME_DIR}")

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
                        print(f'$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ WARNING {pic_name} DOES NOT EXIST $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

                # print(arr_sub_total_score)