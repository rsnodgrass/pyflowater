#!/usr/bin/env python

import os
import sys
import setuptools

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='pyflowater',
      version='0.5.1',
      packages=[ 'pyflowater' ],
      description='Python interface for Flo by Moen API',
#      long_description=long_description,
      url='https://github.com/rsnodgrass/pyflowater',
      author='Ryan Snodgrass',
      author_email='rsnodgrass@gmail.com',
      license='Apache Software License',
      install_requires=[ 'requests>=2.0', 'google-cloud-firestore' ],
      keywords=[ 'flo', 'home automation', 'water monitoring' ], 
      zip_safe=True,
      classifiers=[ "Programming Language :: Python :: 3",
                    "License :: OSI Approved :: Apache Software License",
                    "Operating System :: OS Independent",
      ],
)
