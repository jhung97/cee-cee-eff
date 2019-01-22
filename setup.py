from setuptools import setup
import sys


setup(
    name='requester',
    packages=['requester'],
    package_dir = {'requester' : './requester'},
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)