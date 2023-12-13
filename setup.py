from setuptools import setup, find_packages

setup(
    name='i2nca',
    version='0.2.0',
    packages=find_packages(include=['i2nca','i2nca.qctools']),
    install_requires=[
        'm2aia==0.5.1',
    ]    
)

