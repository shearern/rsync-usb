from setuptools import setup, find_packages
import sys, os

version = 'DEV_VERSION'

setup(name='python-rsync-usb',
    version=version,
    description="An implementation of the Rsync protocol that can be used with offline storage when two hosts are not connected by a network.",
    long_description="""\
    This package provides an implementation of the rsync protocol that can be used on offline media.  The rsync protocol is designed to work in only three phases:""",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: System",
        "Topic :: Utilities",
        ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='rsync',
    author='Nathan Shearer',
    author_email='shearern@gmail.com',
    url='https://github.com/shearern/rsync-usb',
    license='GPL',

    scripts=['src/ursync.py',
             'src/debug_ursync_target_hashes.py',
             ],
    package_dir= {'': 'src'},
    packages=['rsync_usb', 'rsync_usb.ui', 'rsync_usb.trx_files'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'python-gflags',
    ],
    requires=[
        'sqlite3'
    ],
#    entry_points="""
#    # -*- Entry points: -*-
#    """,
    )
