#!/usr/bin/env python
from os import path
from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="golden_hour",
    version="1.3.2",
    description="Record a sunset timelapse and post it to Bluesky with a weather report",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ddrieck/golden-hour",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "golden-hour=golden_hour.main:main",        ]
    },
    install_requires=[
        "astral==2.2",
        "pytz==2023.3",
        "PyYAML==6.0.2",
        "schema==0.7.5",
        "requests==2.31.0",
        "atproto==0.0.61" 
    ],
    include_package_data=True,
)
