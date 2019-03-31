import os
import subprocess

# TODO: where the video is coming from
source_roots = "/Users/suhyunkim/Downloads/action_quality_dataset/figure_skating/videos"

# TODO: where the extracted keyframes should be saved. DON'T FORGET TO END THE NAME WITH
dest_root = '/Users/suhyunkim/Downloads/action_quality_dataset/figure-keyframes'

# TODO: the type of video to be saved
file_type = '.mp4'

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


# list to store the names of the files
mfiles_to_extract = []

# count how many .mp4, .mxf, .MXF are in the source root - don't count duplicates
file_counter = 0
for root, dirs, files in os.walk(source_roots):
    print(f'source_roots: {source_roots}')
    for file in files:
        print(f'file: {file}')

        if file.endswith(file_type) and file not in mfiles_to_extract:
            file_counter += 1
            file_name_w_path = os.path.join(root, file)
            print(file_name_w_path)
            mfiles_to_extract.append(file_name_w_path)

print(f'Total # of files that end with .mp4: {len(mfiles_to_extract)} \n from {mfiles_to_extract}.')

unsuc = []
for i, filename in enumerate(mfiles_to_extract):
    print(f'i: {i}, filename: {filename}')
    dest_dir = filename.replace(source_roots, dest_root)

    # if os.path.exists(dest_dir):
    #     print('path exists - SKIPPING')
    #     continue

    print('extraction about to start in: ')
    print(dest_dir)
    #run_command(f"mkdir -p '{dest_dir}'")
    out = run_command(
        f"ffmpeg -i '{filename}' -r 25 -vsync vfr '{dest_dir}/frame%07d.png'",
        logfile=f"'{dest_dir}/log.txt'"
    )
    if 'failed' in out:
        print(f'Processing {filename} failed.----*******-------')
        unsuc.append(filename)

    print(f'{i+1} out of {len(mfiles_to_extract)} videos processed.')


with open(os.path.join(dest_root, 'unsuc.txt'), 'w') as fout:
    for item in unsuc:
        fout.write(unsuc)
        fout.write('\n')


# ffmpeg -i ICE_SKATING_EUROPEAN_SHORT_MEN_2008_PART_3-cVe-zXZFOww.mp4 -r 25 -vsync vfr /Users/suhyunkim/Downloads/action_quality_dataset/test_skating/frame%07d.png