Deep Learning for Remote Sensing
================================
This repository contains Jupyter notebooks about remote sensing, in particular [land use and land cover](https://lpvs.gsfc.nasa.gov/PDF/TerrestrialECV/T09.pdf), and related tasks 
such as change detection ans satellite image time series. The deep learning models are used to address basic computer vision
tasks such as image classification, semantic segmentation, and object detection applied to satellite and aerial imagery. The monitoring of land cover is relevant for land management, agriculture, wildfires, land surface roughness and albedo. Once each pixel of a satellite or aerial image can be mapped to a class from a LULC taxonomy, a set of images can be used to extract statistical information about a region of interest. 

## Satellite and aerial imagery
* [Copernicus Data Space Ecosystem](https://dataspace.copernicus.eu/)
* [Landsat](https://landsat.gsfc.nasa.gov/)
* [Moderate Resolution Imaging Spectroradiometer (MODIS)](https://modis.gsfc.nasa.gov/)
* [OpenAerialMap](https://openaerialmap.org/)
* [Land Information New Zealand](https://data.linz.govt.nz/)


## Training datasets
Several satellite imagery datasets are available that can be used to train a deep learning model for classificattion tasks, at the scene
or pixel levels. A dataset is a set of examples where each example contains a satellite or aerial image patch of one or more bands, a text label of its class within a taxonomy, or a mask, a raster file, where each pixel represents the class of the corresponding pixel in the image.   

### Datasets for pixel classification (semantic segmentation)
| Dataset       | Number of images | Size (pixel)  | Resolution | Format   | Number of categories | Coverage | Model |
| ------------- | -----------------|---------------|------------|----------|----------------------|----------|-------|
| [BigEarthNet](https://bigearth.net/) | 549488 | 120 x 120 | 10 m. | GeoTIFF  | 19 | Europe | ResNet|
| [OpenEarthmap](https://open-earth-map.org/)  | 5000 | 1000 x 1000 | 0.25 - 0.50 m.| GeoTIFF| 8 | Global | U-Net |
| [SeasoNet](https://zenodo.org/records/5850307)| 1759830 | 120 x 120 | 10 m. | GeoTIFF| 44| Germany| DenseNet, DeepLabV3|
| [MultiSenGE](https://multisenge.github.io/)| 8157| 256 x 256| 10 m.| GeoTIFF| 5 |Grand-Est region, France| U-Net|
| [SEN12MS](https://mediatum.ub.tum.de/1474000) |180662 |256 x 256| 10 m. | GeoTIFF| 17| Global |ResNet, DenseNet, FC-DenseNet|
| [Sen-2 LULC](https://data.mendeley.com/datasets/f4ky6ks248/3)| 213761| 64 x 64| 10 m. | PNG | 8 | India| U-Net|
| [Forest Typology](https://github.com/google-deepmind/forest_typology)|200000|128 x 128|10 m.|PNG|8|Global||

* [Dynamic World](https://dynamicworld.app/)
* [BigEarthNet: A Large-Scale Sentinel Benchmark Archive](https://bigearth.net/)
* [SEN12MS: A Curated Dataset of Georeferenced Multi-Spectral Sentinel-1/2 Imagery for Deep Learning and Data Fusion](https://arxiv.org/abs/1906.07789)
* [SeasoNet: A Seasonal Scene Classification, Segmentation and Retrieval Dataset for Satellite Imagery over Germany](https://arxiv.org/abs/2207.09507)
* [Sen-2 LULC: Land use land cover dataset for deep learning approaches](https://www.sciencedirect.com/science/article/pii/S2352340923007953)
* [MultiSenGE: multi-temporal and multi-modal land use land cover mapping](https://multisenge.github.io/)
* [OpenEarthMap](https://open-earth-map.org/)

### Datasets for scene classification
* [UC Merced Land Use Dataset](http://weegee.vision.ucmerced.edu/datasets/landuse.html)
* [EuroSAT](https://github.com/phelber/EuroSAT)

Many more datasets can be found at the [Image Analysis and Data Fusion](https://eod-grss-ieee.com/) and [SpaceNet](https://spacenet.ai/) websites.

### Land cover data
Land cover data annotated by experts can be used as target data to train deep learning models

* [CORINE](https://land.copernicus.eu/en/products/corine-land-cover/clc2018), raster and vector land cover data, 100 m. resolution, Europe
* [ESA World Cover](https://worldcover2021.esa.int/), raster data, 10 m. resolution, global
* [Dynamic World](https://dynamicworld.app/), raster data, 10 m. resolution, global
* [NASA MODIS Land Cover Level 3 Global](https://modis.gsfc.nasa.gov/data/dataprod/mod12.php), raster data, 500 m. resolution, global

## Machine learning models for LULC classification and segmentation
Several deep learning architectures have been used in computer vision for image classification and semantic segmentation tasks that can be used in remote sensing applications.
### Classic machine learning models for pixel level classification
* K-means
* Random Forests
* Boosting
* Conditional Random Fields
### Deep learning models for scene level classification
* Deep Convolutional Neural Networks (DCNN)
* ResNet
* Inception-v3
* DenseNet
### Deep learning models for pixel level classification (segmentation)
* U-Net
* SegNet
* Fully Convolutional Networks (FCN)
* FC-DenseNet
* DeepLab

| Model | Task | Implementation | Number of parameters  | Performance |
| ----- | -----| -------------- | --------------------- |------------ |
| [ResNet](https://arxiv.org/abs/1512.03385) | Image Classification | [Keras](https://keras.io/api/applications/resnet/), PyTorch, Fastai | 10 M. | Accuracy 80%|
| [Inception-v3](https://arxiv.org/abs/1512.00567v3) | Image Classification | [Keras](https://keras.io/api/applications/inceptionv3/), PyTorch, Fastai | 10 M. | Accuracy 85%|
| [DenseNet](https://arxiv.org/abs/1608.06993) | Image Classification | [Keras](https://keras.io/api/applications/densenet/), PyTorch, Fastai | 10 M. | Accuracy 85%|
| [U-Net](https://arxiv.org/abs/1505.04597) | Image Segmentation | [Keras](https://keras.io/examples/vision/oxford_pets_image_segmentation/), PyTorch, Fastai | ? | Accuracy 85%|
| [SegNet](https://arxiv.org/abs/1511.00561) | Image Segmentation | PyTorch, Fastai | ? | Accuracy 85%|
| [FCN](https://arxiv.org/abs/1411.4038) | Image Segmentation | [Keras](https://keras.io/examples/vision/fully_convolutional_network/), PyTorch, Fastai | ? | Accuracy 85%|
| [FC-DenseNet](https://arxiv.org/abs/1611.09326) | Image Segmentation | PyTorch, Fastai | ? | Accuracy 85%|
| [DeepLab](https://arxiv.org/abs/1706.05587) | Image Segmentation | [Keras](https://keras.io/examples/vision/deeplabv3_plus/), PyTorch, Fastai | ? | Accuracy 85%|

## Performance metrics
Several metrics are used to evaluate the performance of a model on a classification or segmentation task
### Classification metrics
* Accuracy (confusion matrix)

### Segmentation metrics
* Mean Intersection over Union (mIoU)
* Boundary F1-measure (BF)

## Notebooks
The notebooks address the basic tasks: classification at the scene and pixel levels.

* [BigEarthNet data preparation](bigearthnetv2_data_preparation.ipynb)
* [PNG files visual check](png_files_visual_check.ipynb)
* [BigEarthNet model](bigearthnet_model.ipynb)

### Scene classification
* [Land Use and Land Cover Classification using a ResNet Deep Learning Architecture](https://github.com/luigiselmi/copernicus/blob/main/deeplearning_land_use_land_cover_classification.ipynb), EuroSAT images classification using Fast.ai
* [EuroSAT images classification](https://github.com/luigiselmi/machine_learning_notes/blob/main/pml3/eurosat_images_classification.ipynb), EuroSAT images classification using PyTorch

### Pixel level classification (semantic segmentation)
* [Rooftop segmentation](https://github.com/luigiselmi/dl_tensorflow/blob/main/epfl_building_footprints.ipynb)
* [Xception based rooftop segmentation model](epfl_building_footprints_xception.ipynb)

## References
* [Campbell - Introduction to Remote Sensing, 5th Edtion](https://www.amazon.com/Introduction-Remote-Sensing-Fifth-Campbell/dp/160918176X/)
* [Lillesand - Remote Sensing and Image Interpretation, 7th Edition](https://www.amazon.com/Remote-Sensing-Interpretation-Thomas-Lillesand/dp/111834328X/)
* [Jensen - Introductory Digital Image Processing - A Remote Sensing Perspective, 4th Edition]()
* [Richards - Remote Sensing Digital Image Analysis, 6th Edition]()
* [Copernicus Land Cover Changes](https://sentivista.copernicus.eu/data/land-cover-changes)
* [Herold et al. - Global Terrestrial Observing System: Land Cover](https://lpvs.gsfc.nasa.gov/PDF/TerrestrialECV/T09.pdf)