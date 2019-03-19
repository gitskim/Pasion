import subprocess

# TODO: end it with the slash
PICTURE_SOURCE_DIR = '/Users/suhyunkim/Downloads/action_quality_dataset/keyframes/'

# TODO:
ANNOTATION_FILE = '/Users/suhyunkim/Downloads/action_quality_dataset/diving/annotations/Diving_-_Men_10_Prel._-_London_2012_Olympic_Game__eEKo5bGe5bU.txt'

# TODO: it's the dir where all the pictures will be moved to. END IT WITH THE SLASH
KEYFRAME_DIR = '/Users/suhyunkim/Downloads/action_quality_dataset/keykey/'


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


with open(ANNOTATION_FILE) as filename:
    for line in filename:
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
                print(pic_name)
                run_command(f"mv {PICTURE_SOURCE_DIR}{pic_name} {KEYFRAME_DIR}")
