#!/usr/bin/env python

import sys
# for support to Python 3
__py3__ = sys.version_info >= (3, 0)

from setuptools import setup

if __py3__:
    oauth = 'oauth2.3'
else:
    oauth = 'oauth2'


setup(
    name="PyTumblr",
    version="0.0.6",
    description="A Python API v2 wrapper for Tumblr",
    author="John Bunting",
    author_email="johnb@tumblr.com",
    url="https://github.com/tumblr/pytumblr",
    packages = ['pytumblr'],
    license = "LICENSE",

    test_suite='nose.collector',

    install_requires = [
        oauth,
        'httpretty'
        ],

    tests_require=[
        'nose',
        'nose-cov',
        'mock'
        ]
)