import os
import subprocess
from setuptools import setup

# Read the contents of README.md
with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    readme = f.read()

# Run the make command to compile the shared library
subprocess.run(['make'], check=True)

# Setup configuration
setup(
    name='numba_qthsh',
    version='0.0.1',
    description='A package that integrates the C implementation of the Tanh-sinh quadrature with Numba',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/ihateemoji/numba_qthsh',
    packages=['numba_qthsh'],
    package_data={'numba_qthsh': ['qthsh.so']},
    include_package_data=True,
    install_requires=[
        'numba',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: C',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
