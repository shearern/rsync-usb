from rsync_usb.target_chunk_idx.MemoryIndex import MemoryIndex

class TargetChunkCollection(object):
    '''Collection of chunks from existing files on the target system'''

    def __init__(self):
        self.idx = TargetChunkCollection()

