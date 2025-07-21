Processing and storage of the BigEarthNetv2 on Amazon Web Services 
==================================================================
We need to create RGB files in the PNG format using the BigEarthNetv2 patches and mask to train a deep learning model for semantic segmentation tasks. The size of the dataset available for download in a comressed form, tar + zst, is 59 GB for the images and 270 MB for the masks. We use an EC2 instance from AWS () with the following characteristics:

* Type of virtual server: t2.micro, 1 CPU, 1 GB RAM
* Operating system: Ubuntu Server 24.04 LTS
* Volumes (SSD): root 8 GB + 1 vol. 250 GB (tot. 258 GB)

The first volume that comes with the EC2 instance is used for processing the data and can be deleted with the instance. The second volume is used to store the data and can be attached to any (single) instance. Once the EC2 instance is started we can connect to it from a terminal using the ssh protocol and a key pair. We chose to add a volume with 250 GB of space. The added volume /dev/nvme1n1 must be formatted (ext4 file system) and a mount point (a directory, e.g. /data) must be created following the [instructions](https://docs.aws.amazon.com/ebs/latest/userguide/ebs-using-volumes.html) on the AWS website. 

````
$ sudo mount /dev/nvme1n1 /data
````
We can check that the volume is formatted (ext4) and that the mount point is connected with the volume using the command
````
$ sudo lsblk -f
````

Once the volume is available, formatted, and mounted we can download the BigEarthNetv2 dataset (59 GB) in the /data folder
````
$ sudo wget https://zenodo.org/records/10891137/files/BigEarthNet-S2.tar.zst?download=1 -O BigEarthNet-S2.tar.zst
````
and the masks (270 MB)

````
$ sudo wget https://zenodo.org/records/10891137/files/Reference_Maps.tar.zst?download=1 -O Reference_Maps.tar.zst
````
and then extract the image files

````
$ sudo tar xvf BigEarthNet-S2.tar.zst
````

and the masks

````
$ sudo tar xvf Reference_Maps.tar.zst
````

## Installing the required Python packages with Conda
The [Python script](lib/bigearthnetv2_lib.py) for the data preparation steps uses a list of packages that must be installed before using the script. The first step is to install [conda](https://www.anaconda.com/docs/getting-started/anaconda/install#linux-installer). Then we create a new conda environment named _bigearthnet_ with a python interpreter version 3.12.5. We accept the default folder location.  
````
$ (base)conda create -n bigearthnet python=3.12.5
````
Once the new conda environment is created we activate is
````
$ (base)conda activate bigearthnet
````
and we proceed with the installation of the required packages
````
$ (bigearthnet)conda install numpy gdal rasterio tiffile matplotlib scikit-image
````

## Storage of the PNG files in S3
Once the PNG RGB and mask datasets are created they can be stored in the cloud, e.g. in a S3 bucket. A dataset can be uploaded and downloaded from the bucket using the scp protocol or the aws-cli command line APIs

#### AWS-CLI 
send two files to a bucket. From a folder that contains a subdir with the credentials (e.g. .ssh/my_key_pair.pem)

```
$ aws s3 cp bigearthnet_pngs.zip s3://selmilab-bucket
$ aws s3 cp bigearthnet_mask_pngs.zip s3://selmilab-bucket
```

download the files from the same bucket, just reverse the paths

```
$ aws s3 cp s3://selmilab-bucket/bigearthnet_pngs.zip bigearthnet_pngs.zip
$ aws s3 cp s3://selmilab-bucket/bigearthnet_mask_pngs.zip bigearthnet_mask_pngs.zip
```
#### SCP 
download from remote in the current local directory

```
$ scp -i "my_aws_keypair.pem" ubuntu@ec2-15-160-237-53.eu-south-1.compute.amazonaws.com:/home/ubuntu/data/bigearthnet_mask_pngs.zip .  
```

## Sharing an object in a S3 bucket
Objets such as images or zip files by default can only be accessible by the owner using the key pair. An easier way to access an objetc from S3 is by using a presigned url that can last from 1 to 720 minutes or from 1 to 12 hours.
