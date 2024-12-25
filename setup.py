import os.path
import subprocess

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    readme = f.read()

subprocess.call(['make'])

setup(name='numba_qthsh',
  version='0.0.1',
  long_description=readme,
  url='https://github.com/ihateemoji/numba_qthsh',
  packages=['numba_qthsh'],
  package_data={'numba_qthsh': ['qthsh.so']},
  include_package_data=True,
  classifiers=[
      'Programming Language :: Python',
      'Programming Language :: C',
      ],
 )

