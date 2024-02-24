# i2nca
 Mass Spectrometry <ins>I</ins>maging <ins>IN</ins>teractive  <ins>C</ins>onversion and Quality <ins>A</ins>ssesment tool bundle

# Installation:
Download the conda recipe provided in the repository and use it to create a new conda env with:

"""
conda env create -n env_name -f path\to\file\...\conda_recipe.yml
"""
Conda will setup the environment, including the pacakges installable from GitHub.
Activate the enviroment with:

"""
conda activate env_name
"""

# Updating 

Update the full  conda env with the  conda recipe via:
"""
conda env update --name env_name --file path\to\file\...\conda_recipe.yml --prune
"""

To only update the i2nca package, use:
"""
pip uninstall i2nca
pip install i2nca@git+https://github.com/cKNUSPeR/i2nca.git
"""

