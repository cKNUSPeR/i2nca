# i2nca

i2nca is a Mass Spectrometry <ins>I</ins>maging <ins>IN</ins>teractive  <ins>C</ins>onversion and Quality <ins>A</ins>ssesment tool bundle. It is desinged to utilize the powerful file reading capabilities of [m2aia](https://m2aia.de/) and provide a workflow package. The current workflows allow for MSI data preprocessing in the .imzml data format. 

# Installation:
i2nca is available for a number of different applications.
Choose among the following installation depending on what solution suits best.
The builds of i2nca are plattform-independent and testes on Linux and Windows. 

### Installation into conda env (recommended)

To use i2nca from a Python enviroment, it is recommended to set up a virtual enviroment (like conda or venv).

To do this, first create a conda enviroment (You can get conda for example from the Anaconda distribution).
Create a conda env with the name `i2nca_env` with the following command. To smoothen out the process, we'll directly install Python 3.10 into that env aswell, so that pip is also directly accessible.

```
conda create --name i2nca_env python=3.10
```
And activate the enviroment afterwards with:
```
conda activate i2nca_env 
```

Into this enviroment, we can now install i2nca. Do this via pip with the following command:

```
pip install i2nca
```


### Jupyter Notebooks
If you want to use the jupyter notebooks included in this repo, you need an additional jupyter kernel to run the notebooks.
To keep the installations lightweight, jupyter is not included directly in the dependencies of i2nca.
For this, install ´jupyter´ into your virtual env via: 
```
pip install jupyter
```


### Simple Installation with pip

I2nca is pip-installable with:
```
pip install i2nca
```
However, installation into a virtual env is recommended.


### Installation with docker
Biocontainers offers a docker container for i2nca. Pull this docker with
```
docker pull biocontainers/i2nca
```


## Install from github
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
4) Install git into the env
5) Uninstall i2nca
6) Reinstall into the env

```
conda install git
pip uninstall i2nca
pip install git+https://github.com/cKNUSPeR/i2nca.git@brukertools
```



