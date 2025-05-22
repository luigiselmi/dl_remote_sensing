import numpy as np
import os
import sys
import pathlib
import rasterio
from zipfile import ZipFile
import warnings
warnings.filterwarnings('ignore')

'''
This script implements some functions to create PNG RGB images 
from TIFF images and masks of the BigEarthNet dataset.
'''
## ---------------------------------------------- Start of functions definition -----------------------------------------------
def read_band_name(band_name):
    '''
    Returns the information encoded in the band file name:
    tile, patch, band, and date of acquisition.
    '''
    band = band_name[-7:-4]
    patch = band_name[-13:-8]
    tile = band_name[-25:-14]
    date = band_name[-47:-39]
    return tile, patch, band, date


def create_png_file_name(tile, patch, date):
    return tile + '_' + patch + '_' + date + '.png'

def list_data_files(root_path, start_tile_index, max_num_tiles):
    '''
    This function creates a list of tiles each containing
    lists of patches with three RGB bands each or a mask.
    The 2nd argument is the index of the first tile to be included. 
    The 3rd argument is the number of tiles to be returned. 
    '''
    tiles_list = []
    tiles_paths = [pathlib.Path(x) for x in root_path.iterdir() if x.is_dir()]
    for tile_path in tiles_paths[start_tile_index:max_num_tiles]:
        # print(tile_path.name)
        patches_list = []
        for patches_path in tile_path.iterdir():
            bands_list = []
            for band_path in patches_path.iterdir():
                band_type = band_path.name[-7:]
                if (band_type == 'B02.tif' or band_type == 'B03.tif' or band_type == 'B04.tif' or band_type == 'map.tif'):
                    bands_list.append(band_path)
            patches_list.append(bands_list)
        tiles_list.append(patches_list)
    return tiles_list

def print_raster_list(tiles_list): 
    '''
    Prints the content of the nested folders
    within the list passed as argument.
    tiles[patches[bands[]]]
    '''
    for patches_list in tiles_list:
        for bands_list in patches_list:
            for band in reversed(bands_list):
                print(band.name)
            print('\n')
        print('\n')
        
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

def normalize(data_array):
    '''
    This function transforms the bit depth of the TIFF bands from 16 to 8 (0-255) for the PNG files.
    '''
    return (data_array - np.min(data_array)) * ((255 - 0) / (np.max(data_array) - np.min(data_array))) + 0

def createPNG(source_path_list, target_path):
    '''
    This function creates a multiband PNG file from a list of GeoTIFF files 
    containing one band each. For an RGB file the source list shall contain three bands
    in the RGB order. For Sentinel-2 it is B04, B03, B02. If the target file already exists
    it doesn't create a new one and will return 1, otherwise it will create a new raster
    and will return 0 
    '''
    SUCCESS = 0
    FAILURE = 1
    if (os.path.isfile(target_path)):
        return FAILURE 
        
    band_list = []
    dataset = rasterio.open(source_path_list[0])
    width = dataset.width
    height = dataset.height
    count = len(source_path_list)

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
                print('The PNG file already exists.')
                png_patches.append(png_file_name)
            else:
                png_patches.append(png_file_name)
    return png_patches

def zip_pngs(pngs_list, target_zip_file):
    '''
    This function can be used to compress all the PNG files
    created using the createPNGs function into a zip file
    '''
    with ZipFile(target_zip_file, 'w') as zipObj:
        for png in pngs_list:
            zipObj.write(png)

def unzip_pngs(source_zip_file, target_folder):
    with ZipFile(source_zip_file, 'r') as zipObj:
        zipObj.extractall(path=f'{target_folder}')
## ---------------------------------------------- End of functions definition -----------------------------------------------
