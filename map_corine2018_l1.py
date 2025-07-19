from lib.bigearthnetv2_lib import *
'''
This script can be used to  create new mask PNG files in a target folder 
from source mask PNG files in the source folder to map the Corine2018 
level 3 color codes of the source files to level 1 (6 color codes). The 
script can be run using the command line from the root folder of the 
dl_remote_sensing project repository with the command

>python map_corine2018_l1.py source_folder/ target_folder/ zip_folder/

Source and target folder paths must end with the forward slash.
'''
SOURCE_DIR = sys.argv[1]
TARGET_DIR = sys.argv[2]
ZIP_DIR = sys.argv[3]

print('Source folder: ', SOURCE_DIR)
print('Target folder: ', TARGET_DIR)

l1_masks = mapCorineL1_list(SOURCE_DIR, TARGET_DIR)
num_target_masks = len(l1_masks)

print('Printing the unique values of the first 10 new masks:')
for mask in l1_masks[:10]:
    mask_array = get_image_array(mask)
    print(np.unique(mask_array))
    
print('New {:d} mask files created in {}'.format(num_target_masks, TARGET_DIR))

zip_file_name = ZIP_DIR + 'l1_masks.zip'
print('Zip file: ', zip_file_name)
 
zip_pngs(l1_masks, zip_file_name)