from lib.bigearthnetv2_lib import *

'''
The script can be executed using the command line from the root
folder of the dl_remote_sensing project repository with the command

>python bigearthnet_preparation.py data/BigEarthNet-S2

This script imports some functions from the bigearthnetv2_lib.py python 
script in the lib/ subfolder.
'''

BIGEARTHNETv2_DIR = sys.argv[1]
#BIGEARTHNETv2_DIR = 'data/BigEarthNet-S2'
print('Path to BigEarthNetv2 dataset: {:}'.format(BIGEARTHNETv2_DIR))

IMAGES_DATA_DIR = pathlib.Path(BIGEARTHNETv2_DIR + '/images')
MASKS_DATA_DIR = pathlib.Path(BIGEARTHNETv2_DIR + '/masks')

tiles_list = list_image_files(IMAGES_DATA_DIR, 0, 5)

num_tiles = len(tiles_list)
print('Number of tiles: {:d}'.format(num_tiles))

pngs_list = createPNGs(tiles_list)
print('Number of RGB PNG files: {:d}'.format(len(pngs_list)))

target_zip_file = 'data/bigearthnet_pngs.zip'
zip_pngs(pngs_list, target_zip_file)

#unzip_folder = 'zip/'
#unzip_pngs(target_zip_file, unzip_folder)

tiles_mask_list = list_data_files(MASKS_DATA_DIR, 0, 5)
num_masks = len(tiles_list)
print('Number of masks: {:d}'.format(num_masks))

target_zip_masks = 'data/bigearthnet_pngs.zip'
zip_pngs(pngs_list, target_zip_file)
