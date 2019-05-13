#-----------------------------------------------------------------------------
#  Copyright (C) 2019 Alberto Sottile
#
#  Distributed under the terms of the 3-clause BSD License.
#-----------------------------------------------------------------------------

import setuptools
from darkdetect import __version__ as ddVersion

def read(fname):
    with open(fname, 'r') as f:
        return f.read()

setup_args = dict(
    name = "darkdetect",
    version = ddVersion,
    author = "Alberto Sottile",
    author_email = "asottile@gmail.com",
    url = 'http://github.com/albertosottile/darkdetect',
    download_url = 'http://github.com/albertosottile/darkdetect/releases',
    description = "Detect macOS Mojave Dark Mode from Python",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    license = "BSD",
    include_package_data=True,
    packages=setuptools.find_packages(),
    classifiers = [
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',                
    ],
)

setuptools.setup(**setup_args)