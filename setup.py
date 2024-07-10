from setuptools import setup, find_packages

setup(
    name='i2nca',
    version='0.2.9',
    packages=find_packages(include=['i2nca', 'i2nca.qctools', 'i2nca.convtools']),
    entry_points={
        'console_scripts': [
            'i2nca_version = i2nca.main:get_version',
        ]
    },
    install_requires=[
        'numpy<1.25',
        'matplotlib<3.8',
        'm2aia',
        'pyimzml',
    ]    
)

