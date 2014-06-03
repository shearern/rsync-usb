import sys, os
import gflags

from UserInterfaceBase import UserInterfaseBase
from rsync_usb.version import URSYNC_VERSION

class ConsoleUI(UserInterfaseBase):
    '''Interacting with the user on the console'''


    def __init__(self):
        super(ConsoleUI, self).__init__()


    def inform_version(self):
        '''Prompt to display program version at beginning of execution'''
        print "%s - v%s" % (os.path.basename(sys.argv[0]), URSYNC_VERSION)


    def abort(self, error_msg):
        '''Warn the user right before aborting execution'''
        print "ERROR: " + error_msg
        print "ABORTING"


    def inform(self, msg):
        '''Display a single message to the user (will interrupt progress?)'''
        print msg


    def usage_error(self, error_msg):
        '''Inform the user when the program was started with invalid arguments'''
        print "Usage Error: " + str(error_msg)
        print ""
        print 'Usage: %s [options] local_path trx_path' % (sys.argv[0])
        print "Where:"
        print "   options     are defined below"
        print "   local path  is the path on the local host to sync"
        print "   trx_path    is the path to the transferring storage medium"
        print gflags.FLAGS

