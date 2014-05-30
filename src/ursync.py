#!/usr/bin/python
'''Script to perform rsync using offline storage'''

URSYNC_VERSION = 'DEV_VERSION'

import sys
import gflags

from rsync_usb import Eric_Prutt_rsync as rsync
from StringIO import StringIO

if __name__ == '__main__':

    # Parse arguments
    try:
        argv = gflags.FLAGS(sys.argv)
    except gflags.FlagsError, e:
        print '%s\nUsage: %s ARGS\n%s' % (e, sys.argv[0], gflags.FLAGS)
        sys.exit(1)

    # Dummy
    target = StringIO('ABCDEFGHIJKLM OPQRSTUVWXYZ') # No N
    hashes = rsync.blockchecksums(target, blocksize=10)

    source = StringIO('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    delta = rsync.rsyncdelta(source, hashes, blocksize=10)

    patched = StringIO()
    rsync.patchstream(target, patched, delta)

    print source.getvalue()
    print patched.getvalue()
