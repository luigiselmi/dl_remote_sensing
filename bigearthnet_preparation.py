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

start_tile_index = 0 
end_tile_index = 5

tiles_list = list_image_files(IMAGES_DATA_DIR, start_tile_index, end_tile_index)
num_rgb_bands = print_images_list(tiles_list)

tiles_mask_list = list_mask_files(MASKS_DATA_DIR, start_tile_index, end_tile_index)
num_masks = print_masks_list(tiles_mask_list)

num_tiles = len(tiles_list)

pngs_list = createPNGs(tiles_list)

masks_png_list = createMaskPNGs(tiles_mask_list)

rgb_zip_file = 'data/bigearthnet_pngs.zip'
zip_pngs(pngs_list, rgb_zip_file)

masks_zip_file = 'data/bigearthnet_mask_pngs.zip'
zip_pngs(masks_png_list, masks_zip_file)

#unzip_folder = 'zip/'
#unzip_pngs(target_zip_file, unzip_folder)

print('Number of tiles: {:d}'.format(num_tiles))
print('Number of RGB bands. {:d}'.format(num_rgb_bands))
print('Number of masks. {:d}'.format(num_masks))
print('Number of RGB PNG files: {:d}'.format(len(pngs_list)))
print('Number of mask PNG files: {:d}'.format(len(masks_png_list)))
