
from TargetChunkIndexBase import TargetChunkIndexBase
from MemoryIndex import MemoryIndex

class AdaptiveIndex(TargetChunkIndexBase):
    '''Index of hashes from the target system.

    This index uses a memory index until a certain threshold and then switches
    over to a disk-based index
    '''

    MEMORY_CHUNK_LIMIT = 1000000

    def __init__(self):
        self.__is_in_memory = True
        self.__idx = MemoryIndex()
        self.__cnt = 0


    def add_chunk(self, chunk):
        '''Add a TargetHashesChunk object to the collection'''
        self.__cnt += 1
        if self.__is_in_memory and self.__cnt > self.MEMORY_CHUNK_LIMIT:
            self.switch_to_disk_index()

        return self.__idx.add_chunk(chunk)


    def switch_to_disk_index(self):
        # TODO: Implement Disk Index
        self.__is_in_memory = False


    def has_chunk(self, chunk):
        '''Basic test to see if chunk is in the collection'''
        return self.__idx.has_chunk(chunk)


    def has_weak_hash(self, hash, chunk_size):
        '''Check to see if there are any chunks with the given weak hash'''
        return self.__idx.has_weak_hash(hash, chunk_size)


    def has_strong_hash(self, weak_hash, strong_hash, chunk_size):
        '''Check to see if there are any chunks with the given weak hash'''
        return self.__idx.has_strong_hash(weak_hash, strong_hash, chunk_size)


    def find_chunks(self, weak_hash, strong_hash, chunk_size):
        '''List all chunks that match a given signature'''
        return self.__idx.find_chunks(weak_hash, strong_hash, chunk_size)