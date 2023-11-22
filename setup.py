from setuptools import setup, find_packages

setup(
    name='i2nca',
    version='0.1.0',
    packages=find_packages(include=['i2nca', 'i2nca.*', 'i2nca.qctools.*']),
    py_modules=['qctools.qctools','qctools.visualization', 'qctools.utils', 'qctools.dependencies'],
    install_requires=[
        'm2aia==0.5.1',
    ]    
)

