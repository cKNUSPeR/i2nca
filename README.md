# i2nca
 ms <ins>I</ins>maging <ins>IN</ins>teractive quality <ins>C</ins>ontrol and <ins>A</ins>ssesment tool bundle

# Installation:
After downloading the conda recipe and using it to create a new conda env with

conda env create -f path\to\file\conda_recipe.yml

That should do the trick.

Update existing envs with the recipe via

conda env update --name myenv --file path\to\file\conda_recipe.yml --prune


earlier versions used the separated github install:

pip install i2nca@git+https://github.com/cKNUSPeR/i2nca.git

GEt the additional Bruker Tools with the following command:

pip install git+https://github.com/cKNUSPeR/i2nca.git@brukertools

In order to run, they the TDF-SDK (distributed by Bruker).
THe timsdata.dll na dtimsdata.so files need to placed at the directory of the python executable to be addressable.
