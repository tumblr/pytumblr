#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import io
import sys
from shutil import rmtree
from setuptools import setup, Command

readme_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           'README.rst')
with io.open(readme_file, encoding='utf-8') as f:
    long_description = '\n' + f.read()


class TestUploadCommand(Command):
    """Allow testing setup.py upload to testpypi."""

    description = 'Build and publish the package to the test pypi server.'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            import twine
        except ImportError:
            print('Twine is required for testing uploads')
            sys.exit()

        assert twine

        try:
            print('Removing previous builds…')
            rmtree(os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                'dist'))
        except OSError:
            pass

        print('Building Source and Wheel (universal) distribution…')
        os.system('{} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        print('Uploading the package to PyPi via Twine…')
        os.system('twine upload --repository-url https://test.pypi.org/legacy/ dist/*')

        sys.exit()


class UploadCommand(Command):
    """Allow uploading to pypi with setup.py"""

    description = 'Build and publish the package to pypi.'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            import twine
        except ImportError:
            print('Twine is required for testing uploads')
            sys.exit()

        assert twine

        try:
            print('Removing previous builds…')
            rmtree(os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                'dist'))
        except OSError:
            pass

        print('Building Source and Wheel (universal) distribution…')
        os.system('{} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        print('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        sys.exit()


setup(
    name="PyTumblr",
    version="0.1.0",
    description="A Python API v2 wrapper for Tumblr",
    long_description=long_description,
    author="Tumblr",
    author_email="accounts@tumblr.com",
    url="https://github.com/tumblr/pytumblr",
    download_url="https://github.com/tumblr/pytumblr/archive/0.1.0.tar.gz",
    packages=['pytumblr'],
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='pytumblr',
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    test_suite='nose.collector',

    install_requires=[
        'future',
        'requests-oauthlib',
    ],

    tests_require=[
        'nose',
        'nose-cov',
        'mock'
    ],

    cmdclass={
        'testupload': TestUploadCommand,
        'upload': UploadCommand,
    },
)
