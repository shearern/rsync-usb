from abc import ABCMeta, abstractmethod

class TargetChunkIndexBase(object):
    '''Based class for implementations of indexing target chunk hashes

    This is basically an interface specification for different implementations
    of an index of the hashes of chunks of files on the target system.  It is
    expected that large file sets will want to use a different indexing method
    (maybe a sqlite database) than smaller data sets.  This class is used, then,
    to have well defined queires that will be run against the index.

    These indexes will be optimized for finding chunks already on the target
    system that may be utilized to avoid placing the data in the sync plan.
    See the rsync protocol papers.
    '''
    __metaclass__ = ABCMeta

    @abstractmethod
    def add_chunk(self, chunk):
        '''Add a TargetHashesChunk object to the collection'''


    @abstractmethod
    def has_chunk(self, chunk):
        '''Basic test to see if chunk is in the collection'''


    @abstractmethod
    def has_weak_hash(self, hash, chunk_size):
        '''Check to see if there are any chunks with the given weak hash'''


    @abstractmethod
    def has_strong_hash(self, weak_hash, strong_hash, chunk_size):
        '''Check to see if there are any chunks with the given weak hash'''


    @abstractmethod
    def has_inplace_match(self, rel_path, start_pos, weak_hash, strong_hash,
                          chunk_size):
        '''Check to see if the data already in place matches

        This query is to check to see if the data already in place on the
        target system (in the same place, in the same file) is the same as on
        the source system
        '''

    @abstractmethod
    def has_infile_match(self, rel_path, weak_hash, strong_hash, chunk_size):
        '''Check to see if data exists in the same file on the target system 

        Checks to see if data already exists in the target file, but possibly
        in a different location.
        
        @return start_pos: Position (byte number) in file on target.  Else None
        '''


    @abstractmethod
    def find_chunks(self, weak_hash, strong_hash, chunk_size):
        '''List all chunks that match a given signature'''
