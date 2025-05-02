import os
import sys
import pathlib

'''
This script implements some functions to copy a subset of TIFF 
images and masks from the BigEarthNet folder to another folder.
The script can be executed using the command line from the root
folder of the dl_remote_sensing project repository with the command

>python move_files.py ../data/BigEarthNet-S2/images/S2A_MSIL2A_20170613T101031_N9999_R022_T33UUP

'''
path = pathlib.Path(sys.argv[1])

for file in os.listdir(path):
    print(file)

num_files = len(os.listdir(path))
print('Number of files in {0:s}: {1:d}'.format(str(path), num_files))