from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='python-rsync-usb',
      version=version,
      description="An implementation of the Rsync protocol that can be used with offline storage when two hosts are not connected by a network.",
      long_description="""\
This package provides an implementation of the rsync protocol that can be used on offline media.  The rsync protocol is designed to work in only three phases:""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='rsync',
      author='Nathan Shearer',
      author_email='shearern@gmail.com',
      url='https://github.com/shearern/rsync-usb',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
