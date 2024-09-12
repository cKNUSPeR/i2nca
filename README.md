# i2nca

i2nca is a Mass Spectrometry <ins>I</ins>maging <ins>IN</ins>teractive  <ins>C</ins>onversion and Quality <ins>A</ins>ssesment tool bundle. It is desinged to utilize the powerful file reading capabilities of [m2aia](https://m2aia.de/) and provide a workflow package. The current workflows allow for MSI data preprocessing in the .imzml data format. 

# Installation:
i2nca is distributed through a number of channels. The builds of i2nca are plattform-independent and testes on Linux and Windows.

### Install for Python envs

Install i2nca with pip from the Pypi repository via:
```
pip install i2nca
```


### Install within a container
To get a docker container with i2nca installed, use the biocontainer. Pull this docker with
```
docker pull biocontainers/i2nca
```


### Install from github
For development use, install i2nca from github using the provided conda recipe (and use the pip+github install)
```
conda env create -n env_name -f path\to\file\...\conda_recipe.yml
conda activate env_name
pip install i2nca@git+https://github.com/cKNUSPeR/i2nca.git
```
Update from github via:
```
pip uninstall i2nca
pip install i2nca@git+https://github.com/cKNUSPeR/i2nca.git
```


# Brukertools 

i2nca features tools that access the Bruker propietary formats for MSI data (.tsf and .tdf). These need the additional TDF-SKD distributed by Bruker.
To install these tools, follow these steps:
1) Get the TDF-SKD from Bruker (distributed for free at [Bruker](https://www.bruker.com/en/services/software-downloads.html))
2) Install i2nca into a virtual env (like a conda env)
3) Copy the files timsdata.dll and timsdata.lib from the TDF-SDK and place them at the level of the python executable of the env.
4) Reinstall i2nca into the env with the following command
```
pip uninstall i2nca
pip install i2nca@git+https://github.com/cKNUSPeR/i2nca.git@brukertools
```



