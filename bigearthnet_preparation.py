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

images_list = list_data_files(IMAGES_DATA_DIR, max_images=1)

print_raster_list(images_list)
    
print('Number of TIFF images: {:d}'.format(len(images_list)))

pngs_list = createPNGs(images_list, print_png=True)
print('Number of RGB PNG files: {:d}'.format(len(pngs_list)))
