from setuptools import setup, find_packages

setup(
    name='i2nca',
    version='0.3.5',
    packages=find_packages(include=['i2nca', 'i2nca.qctools', 'i2nca.convtools', 'i2nca.workflows', 'i2nca.workflows.cli', 'i2nca.tests']),
    entry_points={
        'console_scripts': [
            'i2nca_version = i2nca.main:get_version',
            'i2nca_agnostic_qc = i2nca.workflows.cli.agnostic_qc_cli:i2nca_angostic_qc',
            'i2nca_calibrant_qc = i2nca.workflows.cli.calibrant_qc_cli:i2nca_calibrant_qc',
            'i2nca_region_qc = i2nca.workflows.cli.region_qc_cli:i2nca_region_qc',
            'i2nca_convert_to_cp = i2nca.workflows.cli.pp_2_cp_cli:i2nca_convert_to_cp',
            'i2nca_convert_to_pc = i2nca.workflows.cli.profile_2_centroid_cli:i2nca_convert_to_pc',
            'i2nca_convert_to_cc = i2nca.workflows.cli.pc_2_cc_cli:i2nca_convert_to_cc',
            'i2nca_file_joiner = i2nca.workflows.cli.file_joiner_cli:i2nca_file_joiner',
            'i2nca_file_splitter = i2nca.workflows.cli.file_splitter_cli:i2nca_file_splitter',
        ]
    },
    install_requires=[
        'numpy<1.25',
        'matplotlib<3.8',
        'pandas',
        'scipy',
        'm2aia',
        'pyimzml',
    ]    
)

