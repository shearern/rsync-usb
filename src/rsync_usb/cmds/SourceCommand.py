import os
import gflags

from SyncDirectory import SyncDirectory

class SourceCommand(object):
    '''Run action on source '''

    def __init__(self, trx_path=None):
        self.sd = None

        if trx_path is not None:
            self.set_trx_path(trx_path)


    def set_trx_path(self, trx_path):
        self.sd = SyncDirectory(trx_path)


    def run(self, target_path):