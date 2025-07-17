from lib.bigearthnetv2_lib import *
'''
This script can be used to  create new mask PNG files in a target folder 
from source mask PNG files in the source folder to map the Corine2018 color 
codes of the source files to their index in [1, 45]. The script can be 
run using the command line from the root folder of the dl_remote_sensing 
project repository with the command

>python map_corine2018.py source_folder/ target_folder/

Source and target folder paths must end with the forward slash.
'''

SOURCE_DIR = sys.argv[1]
TARGET_DIR = sys.argv[2]

print('Source folder: {}'.format(SOURCE_DIR))
print('Target folder: {}'.format(TARGET_DIR))

nc_masks = mapCorine145_list(SOURCE_DIR, TARGET_DIR)
num_target_masks = len(nc_masks)

print('Printing the unique values of the first 10 new masks:')
for mask in nc_masks[:10]:
    mask_array = get_image_array(mask)
    print(np.unique(mask_array))
    
print('New {:d} mask files created in {}'.format(num_target_masks, TARGET_DIR))

parent_folder = str(pathlib.Path(TARGET_DIR).parent)
zip_file_name = parent_folder + '/' + 'nc_masks.zip'
print('Zip file: {}', zip_file_name)
 
zip_pngs(nc_masks, zip_file_name)