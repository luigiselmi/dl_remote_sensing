import numpy as np
import os
import sys
from osgeo import gdal, osr, ogr
import pathlib
import rasterio
from rasterio.plot import show_hist
from rasterio.plot import show
import PIL
from PIL import Image, ImageDraw
from skimage import io
from skimage import exposure
from skimage.io import imread
import tifffile as tiff
import matplotlib
import matplotlib.pyplot as plt
import zipfile
from zipfile import ZipFile
import warnings
warnings.filterwarnings('ignore')

'''
This script implements some functions to create PNG RGB images 
from TIFF images and masks of the BigEarthNet dataset.
'''
## ---------------------------------------------- Start of functions definition -----------------------------------------------
# The script is divided into four sections: 
# 1. Data collection
# 2. TIFF to PNG transformation
# 3. Compression
# 4. Normalization
# 5. Visualization
#------------------------- 1) Data collection --------------------------------------------------
def read_band_name(band_name):
    '''
    Returns the information encoded in a TIFF image band file name:
    tile, patch, band, and date of acquisition.
    '''
    band = band_name[-7:-4]
    patch = band_name[-13:-8]
    tile = band_name[-25:-14]
    date = band_name[-47:-39]
    return tile, patch, band, date

def read_mask_name(mask_name):
    '''
    Returns the information encoded in a TIFF mask file name:
    tile, patch, band, and date of acquisition.
    '''
    patch = mask_name[-23:-18]
    tile = mask_name[-35:-24]
    date = mask_name[-57:-49]
    return tile, patch, date

def create_png_file_name(tile, patch, date):
    return tile + '_' + patch + '_' + date + '.png'

def create_mask_png_file_name(tile, patch, date):
    return tile + '_' + patch + '_' + date + '_mask.png'

def list_image_files(root_path, start_tile_index, end_tile_index):
    '''
    This function creates a list of tiles each containing
    lists of patches with three RGB bands each or a mask.
    The 2nd argument is the index of the first tile to be included. 
    The 3rd argument is the number of tiles to be returned. 
    '''
    tiles_list = []
    tiles_paths = [pathlib.Path(x) for x in root_path.iterdir() if x.is_dir()]
    for tile_path in tiles_paths[start_tile_index:end_tile_index]:
        # print(tile_path.name)
        patches_list = []
        for patches_path in tile_path.iterdir():
            bands_list = []
            for band_path in patches_path.iterdir():
                band_type = band_path.name[-7:]
                if (band_type == 'B02.tif' or band_type == 'B03.tif' or band_type == 'B04.tif'):
                    bands_list.append(band_path)
            patches_list.append(bands_list)
        tiles_list.append(patches_list)
    return tiles_list

def list_mask_files(root_path, start_tile_index, end_tile_index):
    '''
    This function, like the one for bands, creates a list of tiles 
    each containing lists of patches with a mask.
    The 2nd argument is the index of the first tile to be included. 
    The 3rd argument is the number of tiles to be returned. 
    '''
    tiles_list = []
    tiles_paths = [pathlib.Path(x) for x in root_path.iterdir() if x.is_dir()]
    #print('Number of tiles: ', len(tiles_paths))
    for tile_path in tiles_paths[start_tile_index:end_tile_index]:
        #print('Tile:', tile_path.name)
        patches_list = []
        for patch_path in tile_path.iterdir():
            mask_list = []
            for mask_path in patch_path.iterdir():
                file_type = mask_path.name[-7:]
                #print('File type: {}'.format(file_type))
                if (file_type == 'map.tif'):
                    mask_list.append(mask_path)
            patches_list.append(mask_list)
        tiles_list.append(patches_list)
    return tiles_list

def print_images_list(tiles_list): 
    '''
    Prints the content of the nested folders
    within the list passed as argument.
    tiles[patches[bands[]]]
    '''
    count = 0
    for patches_list in tiles_list:
        for bands_list in patches_list:
            for band in reversed(bands_list):
                print(band.name)
                count += 1
            print('\n')
        print('\n')
    return count
        
def print_masks_list(tiles_list): 
    '''
    Prints the content of the nested folders
    within the list passed as argument.
    tiles[patches[mask]]
    '''
    count = 0
    for patches_list in tiles_list:
        for mask_list in patches_list:
            for mask in mask_list:
                print(mask.name)
                count += 1
            print('\n')
        print('\n')
    return count

def get_raster_attributes(img_path):
    width = 0.0
    height = 0.0
    d_type = None
    crs = None
    transform = None
    with rasterio.open(img_path) as dataset:
        d_types = dataset.dtypes[0]
        print('dtypes: {}'.format(d_types))
        print('Number of bands: {:d}'.format(dataset.count))
        width = dataset.width
        height = dataset.height
        print('Band width: {:d}, band height: {:d}'.format(width, height))
        transform = dataset.transform
        print('Dataset affine transform:\n {}'.format(transform))
        crs = dataset.crs
        print('EPSG Coordinates Reference System: {}'.format(crs))
        bb_left = dataset.bounds.left
        bb_bottom = dataset.bounds.bottom
        bb_right = dataset.bounds.right
        bb_top = dataset.bounds.top
        print('Bounding box \n left: {:.2f}, \n bottom: {:.2f}, \n right: {:.2f}, \n top: {:.2f}'.format(bb_left, bb_bottom, bb_right, bb_top))                                                   
    return width, height, d_type, transform

#----------------------------2) TIFF to PNG transformation ----------------------------------

def normalize(data_array):
    '''
    This function transforms the bit depth of the TIFF bands from 16 to 8 (0-255) for the PNG files.
    '''
    return (data_array - np.min(data_array)) * ((255 - 0) / (np.max(data_array) - np.min(data_array))) + 0

def createPNG(source_path_list, target_path):
    '''
    This function creates a multiband PNG file from a list of GeoTIFF files 
    containing one band each. For an RGB file the source list shall contain three bands
    in the RGB order. For Sentinel-2 it is B04, B03, B02. The bin depth of each band is
    reduced from 16 bits to 8 bits. If the target file already exists
    it doesn't create a new one and will return 1, otherwise it will create a new raster
    and will return 0 
    '''
    SUCCESS = 0
    FAILURE = 1
    if (os.path.isfile(target_path)):
        return FAILURE 
        
    band_list = []
    with rasterio.open(source_path_list[0]) as source_dataset:
        width = source_dataset.width
        height = source_dataset.height
        count = len(source_path_list)

    #print('createPNG source_path_list', source_path_list)
    for raster_path in source_path_list:
        dataset = rasterio.open(raster_path)
        band = normalize(dataset.read(1))
        band_list.append(band)
        
        
    with rasterio.open(target_path,
                    mode='w',
                    driver='PNG',
                    height=height,
                    width=width,
                    count=count,
                    dtype='uint8') as target_dataset:
        band_index = 1
        for band in band_list:
            target_dataset.write(band, band_index)
            band_index += 1
    
    return SUCCESS

def createMaskPNG(source_path, target_path):
    '''
    This function creates a one band PNG file from a GeoTIFF mask file. 
    If the target file already exists it doesn't create a new one and 
    will return 1, otherwise it will create a new raster and will return 0. 
    '''
    #print('createMaskPNG source_path=', source_path[0])
    SUCCESS = 0
    FAILURE = 1
    if (os.path.isfile(target_path)):
        return FAILURE 
        
    with rasterio.open(source_path[0]) as source_dataset:
        width = source_dataset.width
        height = source_dataset.height
        band = source_dataset.read(1)
        
    with rasterio.open(target_path,
                    mode='w',
                    driver='PNG',
                    height=height,
                    width=width,
                    count=1,
                    dtype='uint16') as target_dataset:
        band_index = 1
        target_dataset.write(band, band_index)

    return SUCCESS

def createPNGs(tiles_list):
    '''
    This function creates a PNG for each patch of the tiles
    in the list. The path of the PNG files is added to a list 
    that will be returned. In case a PNG file already exist it 
    only adds its path to the list.
    '''
    png_patches = []
    for patches_list in tiles_list:
        for bands_list in patches_list: 
            band_name = bands_list[0].name
            #print('Band name: {}'.format(band_name))
            tile, patch, band, date = read_band_name(band_name)
            patch_dir = bands_list[0].parent
            png_file_name = str(patch_dir) +  '/' + create_png_file_name(tile, patch, date)
            if (createPNG(bands_list, png_file_name) == 1):
                print('The image PNG file already exists.')
                png_patches.append(png_file_name)
            else:
                png_patches.append(png_file_name)
    return png_patches

def createMaskPNGs(tiles_list):
    '''
    This function creates a PNG mask for each patch of the tiles
    in the list. The path of the PNG files is added to a list 
    that will be returned. In case a PNG file already exist it 
    only adds its path to the list.
    '''
    png_patches = []
    for patches_list in tiles_list:
        for patch_path in patches_list: 
            #print('Patch path: {}'.format(patch_path))
            patch_dir = patch_path[0].parent
            patch_name = patch_path[0].name
            #print('Patch name: {}'.format(patch_name))
            tile, patch, date = read_mask_name(patch_name)
            #print('Tile: {}, Patch: {}, Date: {}'.format(tile, patch, date))
            png_file_name = str(patch_dir) +  '/' + create_mask_png_file_name(tile, patch, date)
            #print('Mask file name: {}'.format(png_file_name))
            if (createMaskPNG(patch_path, png_file_name) == 1):
                print('The mask PNG file already exists.')
                png_patches.append(png_file_name)
            else:
                png_patches.append(png_file_name)
    return png_patches
    
#----------4) Compression ----------------------------------------------------

def zip_pngs(pngs_list, target_zip_file):
    '''
    This function can be used to compress all the PNG files
    created using the createPNGs function into a zip file
    '''
    with ZipFile(target_zip_file, 'w', zipfile.ZIP_DEFLATED) as zipObj:
        for png in pngs_list:
            png_path = pathlib.Path(png)
            zipObj.write(png, arcname=png_path.name)

def unzip_pngs(source_zip_file, target_folder):
    with ZipFile(source_zip_file, 'r') as zipObj:
        zipObj.extractall(path=f'{target_folder}')

## ---------------------- 5) Normalization ------------------------------------
def norm_image(image_array):
    '''
    This function takes a NumPy array as input, computes min and max
    and returns a normalized array with values in [0, 1]
    '''
    max_image = image_array.max()
    min_image = image_array.min()
    image_array_norm = (image_array - min_image) / (max_image - min_image + 1)
    return image_array_norm
## ---------------------- Visualization ---------------------------------------

def plot_examples(images_list, masks_list):
    fig_rows = len(masks_list)
    fig, axs = plt.subplots(nrows=fig_rows, ncols=2, figsize=(5, 3), layout='constrained')
    for row in range(0, fig_rows):
        img = norm_image(np.array(Image.open(images_list[row])))
        msk = norm_image(np.array(Image.open(masks_list[row])))
        axs[row, 0].set_axis_off()
        axs[row, 1].set_axis_off()
        axs[row, 0].imshow(img)
        axs[row, 1].imshow(msk)
        
## ---------------------------------------------- End of functions definition -----------------------------------------------
