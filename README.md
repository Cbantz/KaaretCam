# KaaretCam  
# About
This KaaretCam repo is a set of scripts to be used for simplified data processing of KaaretCam data.
# Getting Started
Download or clone the repo to a directory you will work from.

Install [tiff2fits](https://github.com/Cbantz/tiff2fits) from github. (Other dependencies can be installed via pip from pypi.

# Using KaaretCam/process.py

"Data frames" are the frames with events to be counted. Your data frames should be saved in a directory named 'tiff' inside a dedicated data directory. All frames should be named image_[image_number] e.g. /path/to/your/data/tiff/image_0.tiff.

Dark frames should be saved in a directory named 'tiff' inside a dedicated data directory. Dark frames should be named dark_[image_number]. e.g. /path/to/your/darks/dark_0.tiff.

Execute /path/to/your/installation/KaaretCam/process.py using python with the following arguments:

- data_path=/path/to/your/data
- dark_path=/path/to/your/darks
- energy_min=lowest energy (ADU) to include in the processed fits image.
- energy_max=highest energy (ADU) to include in the processed fits image.
- output_path=/path/to/save/your/image/imagename.fits

**Notes:**

- hthr is set to a default value in process.py. This can be changed by editing the variable hthr_value in process.main().
