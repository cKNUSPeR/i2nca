from setuptools import setup, find_packages

setup(
    name='i2nca',
    version='0.2.0',
    packages=find_packages(include=['i2nca', 'i2nca.qctools', 'i2nca.convtools']),
    install_requires=[
        'numpy>1.25',
        'matplotlib>3.8',
        'm2aia',
        'pyimzml',
    ]    
)

