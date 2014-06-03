import cPickle
from datetime import datetime

class TargetHashProtocolError(Exception): pass

class TargetHashesWriter(object):
    '''Store hashes from target system'''

    # Strong Hash Types
    MD5_STRONG_HASH = 'MD5'

    # TYPE KEY
    DATA_TYPE = 'type'

    # HEADER KEYS    (TODO: Shorten)
    HK_FROM_HOST = 'from_host'
    HK_CREATED_AT = 'created_at'
    HK_STRONG_HASH_TYPE = 'strong_hash_type'
    HK_WEAK_HASH_VER = 'weak_hash_ver'
    HK_BLOCK_SIZE = 'block_size'
    HK_TARGET_PATH = 'target_path'

    # FILE HEADER KEYS    (TODO: Shorten)
    FK_PATH = 'path'
    FK_TYPE = 'file_obj_type'

    # FILE CHUNK HASH KEYS    (TODO: Shorten)
    FC_WEAK_HASH = 'weak_hash'
    FC_STRONG_HASH = 'strong_hash'
    FC_CHUNK_SIZE = 'size'              # Not stored if equal to block size

    def __init__(self, path):
        '''Init

        @param path: Path to file to store hash data
        @param mode: Read or Write
        '''
        self.__path = path
        self.__fh = None
        self.__block_size = None

        # Writing Members
        self.__header_written = False
        self.__file_header_written = False


        # Open File
        self.__fh = open(self.__path, 'wb')


    def write_header(self, block_size, from_host, strong_hash_type,
                     weak_hash_ver, target_path):
        '''Record information about this target hash dump'''

        # State Check
        if self.__header_written:
            raise TargetHashProtocolError("Header written twice")

        # Output
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = {
            self.HK_FROM_HOST:          from_host,
            self.HK_CREATED_AT:         ts,
            self.HK_STRONG_HASH_TYPE:   strong_hash_type,
            self.HK_WEAK_HASH_VER:      weak_hash_ver,
            self.HK_BLOCK_SIZE:         block_size,
            self.HK_TARGET_PATH:        target_path,
            }
        cPickle.dump(data, self.__fh, -1)

        # Update State
        self.__block_size = block_size
        self.__header_written = True


    def write_file_header(self, file_obj):
        '''Record a file header.

        All chunks received after this header are assumed to belong to this file
        and to be in order.
        '''
        # State Check
        if not self.__header_written:
            raise TargetHashProtocolError("Must write header first")

        # Output
        data = {
            self.FK_PATH:   file_obj.rel_path,
            self.FK_TYPE:   file_obj.fileobj_type,
            }
        cPickle.dump(data, self.__fh, -1)

        # Update State
        self.__file_header_written = True


    def write_chunk_hash(self, weak_hash, strong_hash, chunk_size):
        '''Save hashes for a chunk to file

        It's assumed that chunk hashes will be provided in order for contiguous
        chunks.
        '''
        # State Check
        if not self.__file_header_written:
            raise TargetHashProtocolError("Must write file header first")

        # Output
        data = {
            self.FC_WEAK_HASH:      weak_hash,
            self.FC_STRONG_HASH:    strong_hash,
            }
        if chunk_size != self.__block_size:
            data[self.FC_CHUNK_SIZE] = chunk_size
        cPickle.dump(data, self.__fh, -1)






