#!/usr/bin/python
'''This script simply propagates the version number into the source files'''
import os
import sys

def abort(msg=None):
    if msg is not None:
        print "ERROR:", msg
    print "ABORTING"
    sys.exit(2)


def replace_version(path, ver_str):
    contents = None
    print "Applying version to", path
    with open(path, 'rb') as fh:
        contents = fh.read()
    contents.replace('DEV_VERSION', ver_str)
    with open(path, 'wb') as fh:
        fh.write(contents)


if __name__ == '__main__':

    # Sanity Checks

    print "This should be run on a tag, not trunk"
    go = raw_input("Proceed? (y/n)")

    if go.lower() != 'y':
        abort()

    if 'setup.py' not in list(os.listdir('.')):
        abort("Don't see setup.py.  Not in project root?")

    # Get Version Number

    version = raw_intput("Version Number to apply:").strip()
    if len(version) == 0:
        abort("No version supplied")

    # Do Replacements

    replace_version('setup.py', version)
    replace_version('ursync.py', version)

    # Finished
    print ""
    print "Finished"
    print "Do you git commit now"
    print "Suggested comment: Apllied version %s to tag" % (version)




