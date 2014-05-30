#!/bin/bash

function abort {
	if [ -n "$1" ]; then
		echo "ERROR: $1"
	fi
	echo "ABORTING"
	exit 2
}

if [ $USER != 'root' ]; then
	abort "Run as root"
fi

if ! python setup.py bdist_egg; then
	abort "Failed to build .egg"
fi

if [ -d "/usr/local/lib/python2.7/dist-packages/python_rsync_usb-DEV_VERSIONdev-py2.7.egg" ]; then
	if ! easy_install -m python_rsync_usb; then
		abort "Failed to call easy_install -m"
	fi

	if ! rm -rf /usr/local/lib/python2.7/dist-packages/python_rsync_usb-DEV_VERSIONdev-py2.7.egg; then
		abort "Failed to remove egg directory"
	fi

	if ! rm /usr/local/bin/ursync.py; then
		abort "Failed to remove ursync.py script"
	fi
else
	echo "Not already installed?"
fi

if ! easy_install dist/python_rsync_usb-DEV_VERSIONdev-py2.7.egg; then
	echo "Failed to install new .egg"
fi
