'''
Created on May 29, 2014

@author: Nathan Shearer
'''
import Eric_Prutt_rsync as rsync
from StringIO import StringIO

target = StringIO('ABCDEFGHIJKLM OPQRSTUVWXYZ') # No N
hashes = rsync.blockchecksums(target, blocksize=10)

source = StringIO('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
delta = rsync.rsyncdelta(source, hashes, blocksize=10)

patched = StringIO()
rsync.patchstream(target, patched, delta)

print source.getvalue()
print patched.getvalue()
