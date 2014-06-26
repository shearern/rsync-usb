from rsync_usb.SyncDirectory import SyncDirectory

class CommandBase(object):
    '''Base for defining commands'''

    def __init__(self):
        self.sd = None
        self.opt_verbose = False
        self.opt_list_files = False
        self.opt_default_block_size = 4096


    def set_trx_path(self, trx_path):
        self.sd = SyncDirectory(trx_path)

