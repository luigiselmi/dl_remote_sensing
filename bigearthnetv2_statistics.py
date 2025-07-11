from lib.bigearthnetv2_lib import *

'''
The script can be executed using the command line from the root
folder of the dl_remote_sensing project repository with the command

>python bigearthnetv2_statistics.py data/BigEarthNet-S2

This script imports some functions from the bigearthnetv2_lib.py python 
script in the lib/ subfolder.

The purpose of this script is to calculate the number of images in the BigEarthNetv2
dataset for each of the Corine2018 Land Cover class. The task is accomplished by collecting
the unique values in the mask file that is linked to an image.
'''

BIGEARTHNETv2_DIR = sys.argv[1]
#BIGEARTHNETv2_DIR = 'data/BigEarthNet-S2'
print('Path to BigEarthNetv2 dataset: {:}'.format(BIGEARTHNETv2_DIR))

MASKS_DATA_DIR = pathlib.Path(BIGEARTHNETv2_DIR + '/Reference_Maps')

start_tile_index = 0 
end_tile_index = 5

start = time.time()
corine2018_buckets = collect_statistics(MASKS_DATA_DIR, start_tile_index, end_tile_index, print_msg=True)
end = time.time()
elapsed_time = end - start
print('Elapsed time (seconds): {:.2f}'.format(elapsed_time))

save_statistics(corine2018_buckets, 'data/statistics.txt')

print('Done !')