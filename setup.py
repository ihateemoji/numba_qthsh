import os
import subprocess
import sys
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

if os.name == 'nt':  # Windows
    # Run the Windows-specific build command
    subprocess.check_call(['gcc', '-Wall', 'src/qthsh.c', '-shared', '-fPIC', '-o', 'numba_qthsh/qthsh.dll'])
else:
    # Run the Unix-like build command
    subprocess.check_call(['make'])
super().run()

# Read the contents of README.md
with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    readme = f.read()

# Setup configuration
setup(
    name='numba_qthsh',
    version='0.0.1',
    description='A package that integrates the C implementation of the Tanh-sinh quadrature with Numba',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/ihateemoji/numba_qthsh',
    packages=['numba_qthsh'],
    package_data={'numba_qthsh': ['qthsh.so', 'qthsh.dll']},
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
