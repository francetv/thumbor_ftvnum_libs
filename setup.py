#!/usr/bin/python
# -*- coding: utf-8 -*-

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license

from distutils.core import setup

setup(
    name = "thumbor_ftvnum_libs",
    version = "0.0.3",
    description = "libs thumbor",
    author = "Bertrand Thill",
    author_email = "bertrand.thill@francetv.fr",
    keywords = ["thumbor", "fallback", "images", "nfs"],
    license = 'MIT',
    url = 'https://github.com/francetv/thumbor_ftvnum_libs',
    packages=[
        'thumbor_ftvnum_libs',
        'thumbor_ftvnum_libs.loaders',
        'thumbor_ftvnum_libs.url_signers',
        'thumbor_ftvnum_libs.metrics',
        'thumbor_ftvnum_libs.storages',
        'thumbor_ftvnum_libs.result_storages'
    ],
    classifiers = ['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Natural Language :: English',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 2.7',
                   'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
                   'Topic :: Multimedia :: Graphics :: Presentation'
    ],
    package_dir = {"thumbor_ftvnum_libs": "thumbor_ftvnum_libs"},
    install_requires=['thumbor>=6.5.0'],
    long_description = """\
This module test support for file.
"""
)