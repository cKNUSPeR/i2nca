from setuptools import setup, find_packages

setup(
    name='i2nca',
    version='0.3.1',
    packages=find_packages(include=['i2nca', 'i2nca.qctools', 'i2nca.convtools', 'i2nca.workflows', 'i2nca.workflows.cli', 'i2nca.tests']),
    entry_points={
        'console_scripts': [
            'i2nca_version = i2nca.main:get_version',
            'i2nca_agnostic_qc = i2nca.workflows.cli.agnostic_qc_cli:i2nca_angostic_qc',
            'i2nca_calibrant_qc = i2nca.workflows.cli.calibrant_qc_cli:i2nca_calibrant_qc',
            'i2nca_region_qc = i2nca.workflows.cli.region_qc_cli:i2nca_region_qc',
        ]
    },
    install_requires=[
        'numpy<1.25',
        'matplotlib<3.8',
        'm2aia',
        'pyimzml',
    ]    
)

