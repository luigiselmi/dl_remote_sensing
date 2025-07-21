Experiments
===========
In order to achive a good result with the segmentaion model we use different subsets of the BirErathNetv2 datasets. We may also apply two transformations to the pixel values of the masks. Originally the masks pixel values are taken from the 3rd level of the Corine2018 Land Cover classes. These are integer values between 111 and 523 that represnt a total of 44 classes. From the statistics we can see that the images are not distributed uniformely among these classes. The 1st transformation change the pixel values to their index value, i.e. in the interval [1, 44]. These transformation allows us to use only 1 byte instead of two to store a pixel value. The problem of the non uniform distribution of the images in the 44 classes still remain and might have an impact on the performance of the training. The second transfromation is from the original Corine2018 level 3 to level 1 for which only 5 classes are defined. We add one more class for the pixel that are not classified and have the non-standard value of 999 in the original BigEarthNet masks.

## BigEarthNetv2 dataset
The images and masks are divided in 115 tiles each of which may have a different number of patches. The total number of patches is 549489. Thisnumber was calculated using the
bash command
````
$ find . -maxdepth 2 -type d | wc -l
````
from the dataset root folder.
## Workflow 
The worflow to prepare the data for the model training is

1. The BigEarthNet patches, bands B2, B3 and B4 in GeoTIFF format are transformed in PNG files each containing the three RGB bands 
2. The corresponding GeoTIFF masks are also transformed into PNG files
3. The Corine2018 level 3 pixel values of the masks are further mapped to [1, 45], same level but different numbering, or to level 1 (only 6 classes from 1 to 6)  

All the subsets and the transformed masks are stored in S3 buckets as zip files. The dataset have the naming convention

* Subset PNG images: bigearthnet_exp<number>_img.zip
* Subset PNG masks: bigearthnet_exp<number>_mask.zip
* Subset PNG masks Corine level 3 [1, 45]: bigearthnet_exp<number>_mask_l3.zip
* Subset PNG masks Corine level 1 [1, 6]: bigearthnet_exp<number>_mask_l1.zip

We may use the level 1 or level 3 classes for the pixel value of the masks. We have developed two script to perform such transformations. In the last case we always map the original values to the corresponding index value from 1 to 45, where 45 is used for 999.

## Subsets and model hyperparameters
We use different subsets of the BigEarthNet dataset to test the model performance using different hyperparameters such as learning rate,  batch size and number of epochs. The validation accuracy is the best among all the epochs. the subset is split in 70% training, 20% validation, 10% test. 

| Experiment  | Subset Size | Corine2018 Level | Learning rate | Batch size   | Epochs | Validation Accuracy |
| ----------- | ------------|------------------|---------------|--------------|--------|---------------------|
| 1 | 75465 | L1 | 10^-4 | 32 | 50 | 0.7437 |
| 2 | 115672 | L1 | 10^-4 | 32 | 50 |       |


