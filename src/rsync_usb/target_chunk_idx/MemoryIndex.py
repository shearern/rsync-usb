from TargetChunkIndexBase import TargetChunkIndexBase

class MemoryIndex(TargetChunkIndexBase):
    '''An in-memory indexing of target file chunks'''

    def __init__(self):
        self.__chunks = set()
        self.__files = dict()   # Indexed by relpath
        self.__chunks_by_hash = dict()# [(weak, size)][(strong)] = list()


    def add_chunk(self, chunk):
        '''Add a TargetHashesChunk object to the collection'''

        assert(chunk.chunk_size != 0)

        self.__chunks.add(chunk)

        # File
        if chunk.file_header is not None:
            if not self.__files.has_key(chunk.file_header):
                self.__files[chunk.file_header] = list()
            self.__files[chunk.file_header].append(chunk)

        # By hashes
        weak_key = (chunk.weak_hash, chunk.chunk_size)
        if not self.__chunks_by_hash.has_key(weak_key):
            self.__chunks_by_hash[weak_key] = dict()
        if not self.__chunks_by_hash[weak_key].has_key(chunk.strong_hash):
            self.__chunks_by_hash[weak_key][chunk.strong_hash] = list()
        self.__chunks_by_hash[weak_key][chunk.strong_hash].append(chunk)


    def has_chunk(self, chunk):
        '''Basic test to see if chunk is in the collection'''
        return chunk in self.__chunks


    def has_weak_hash(self, hash, chunk_size):
        '''Check to see if there are any chunks with the given weak hash'''
        weak_key = (hash, chunk_size)
        return self.__chunks_by_hash.has_key(weak_key)


    def has_strong_hash(self, weak_hash, strong_hash, chunk_size):
        '''Check to see if there are any chunks with the given weak hash'''
        weak_key = (weak_hash, chunk_size)
        if not self.__chunks_by_hash.has_key(weak_key):
            return False
        return self.__chunks_by_hash[weak_key].has_key(strong_hash)


    def find_chunks(self, weak_hash, strong_hash, chunk_size):
        '''List all chunks that match a given signature'''
        weak_key = (weak_hash, chunk_size)
        if not self.__chunks_by_hash.has_key(weak_key):
            return
        if not self.__chunks_by_hash[weak_key].has_key(strong_hash):
            return
        for chunk in self.__chunks_by_hash[weak_key][strong_hash]:
            yield chunk

