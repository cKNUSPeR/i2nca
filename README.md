# i2nca
 Mass Spectrometry <ins>I</ins>maging <ins>IN</ins>teractive  <ins>C</ins>onversion and Quality <ins>A</ins>ssesment tool bundle

# Installation:
Download the conda recipe provided in the repository and use it to create a new conda env with:
```
conda env create -n env_name -f path\to\file\...\conda_recipe.yml
```

Conda will setup the environment, including the pacakges installable from GitHub.
Activate the enviroment with:

```
conda activate env_name
```

# Updating to Brukertools

Get the additional Bruker Tools by reinstalling i2nca to the conda enviroment:

```
pip uninstall i2nca
```
```
pip install git+https://github.com/cKNUSPeR/i2nca.git@brukertools
```

In order to use the Bruker-specific tools, the TDF-SDK needs to be installed as well (distributed by Bruker).
It is obtainable after registration with Bruker account under this [link](https://www.bruker.com/protected/en/services/software-downloads/mass-spectrometry/raw-data-access-libraries.html)


The timsdata.dll and timsdata.lib files from the SDK need to placed at the directory of the (virtual) Python executable to be addressable.
For conda environments, the Python executable is in the root folder of the env.


