Deep Learning for Remote Sensing
================================
This repository contains Jupyter notebooks about remote sensing, in particular land use and land cover and related tasks 
such as change detection ans satellite image time series. The deep learning models are used to address basic computer vision
tasks such as image classification, semantic segmentation, and object detection applied to satellite and aerial imagery.

## Satellite and aerial imagery
* [Copernicus Data Space Ecosystem](https://dataspace.copernicus.eu/)
* [Landsat](https://landsat.gsfc.nasa.gov/)
* [Moderate Resolution Imaging Spectroradiometer (MODIS)](https://modis.gsfc.nasa.gov/)
* [OpenAerialMap](https://openaerialmap.org/)
* [Land Information New Zealand](https://data.linz.govt.nz/)

## Training datasets
Several satellite imagery datasets are available that can be used to train a deep learning model for classificattion tasks, at the scene
or pixel levels. 

### Datasets for pixel classification (semantic segmentation)
* [Dynamic World](https://dynamicworld.app/)
* [BigEarthNet: A Large-Scale Sentinel Benchmark Archive](https://bigearth.net/)
* [SEN12MS: A Curated Dataset of Georeferenced Multi-Spectral Sentinel-1/2 Imagery for Deep Learning and Data Fusion](https://arxiv.org/abs/1906.07789)
* [SeasoNet: A Seasonal Scene Classification, Segmentation and Retrieval Dataset for Satellite Imagery over Germany](https://arxiv.org/abs/2207.09507)
* [Sen-2 LULC: Land use land cover dataset for deep learning approaches](https://www.sciencedirect.com/science/article/pii/S2352340923007953)
* [MultiSenGE: multi-temporal and multi-modal land use land cover mapping](https://multisenge.github.io/)

### datasets for scene classification
* [UC Merced Land Use Dataset](http://weegee.vision.ucmerced.edu/datasets/landuse.html)
* [EuroSAT](https://github.com/phelber/EuroSAT)

Many more datasets can be found at the [Image Analysis and Data Fusion](https://eod-grss-ieee.com/) and [SpaceNet](https://spacenet.ai/) websites.

## Notebooks
The notebooks address the basic tasks: classification at the scene and pixel levels.

### Scene classification
* [Land Use and Land Cover Classification using a ResNet Deep Learning Architecture](https://github.com/luigiselmi/copernicus/blob/main/deeplearning_land_use_land_cover_classification.ipynb), EuroSAT images classification using Fast.ai
* [EuroSAT images classification](https://github.com/luigiselmi/machine_learning_notes/blob/main/pml3/eurosat_images_classification.ipynb), EuroSAT images classification using PyTorch

### Pixel level classification (semantic segmentation)
* [Rooftop segmentation](https://github.com/luigiselmi/dl_tensorflow/blob/main/epfl_building_footprints.ipynb)