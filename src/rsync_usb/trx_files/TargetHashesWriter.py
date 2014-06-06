from datetime import datetime
from TrxWriterBase import TrxWriterBase

class TargetHashProtocolError(Exception): pass

class TargetHashesWriter(TrxWriterBase):
    '''Store hashes from target system

    This file is used to store file hashes calculated from the target system
    (where files are being copied to) to be read by the source system (where
    files are being read from) in order to enable ursync determine what data
    already exists on the target system and doesn't need to be transfered.
    '''

    # Strong Hash Types
    MD5_STRONG_HASH = 'MD5'

    # Block Types
    HEADER_TYPE = 'H'
    FILE_HEADER_TYPE = 'F'
    CHUNK_HASH_TYPE = 'C'

    # HEADER KEYS
    HK_FROM_HOST = 'H'
    HK_CREATED_AT = 'C'
    HK_STRONG_HASH_TYPE = 'S'
    HK_WEAK_HASH_VER = 'W'
    HK_BLOCK_SIZE = 'B'
    HK_TARGET_PATH = 'P'

    # FILE HEADER KEYS
    FK_PATH = 'P'
    FK_TYPE = 'O'

    # FILE CHUNK HASH KEYS
    FC_WEAK_HASH = 'w'
    FC_STRONG_HASH = 's'
    FC_CHUNK_SIZE = 'z'              # Not stored if equal to block size

    def __init__(self, file_handle):
        '''Init

        @param file_handle: File to write data to
        '''
        super(TargetHashesWriter, self).__init__(file_handle)
        self.__block_size = None

        # State
        self.__header_written = False
        self.__file_header_written = False


    def write_header(self, block_size, from_host, strong_hash_type,
                     weak_hash_ver, target_path):
        '''Record information about this target hash dump'''

        # State Check
        if self.__header_written:
            raise TargetHashProtocolError("Header written twice")

        # Output
        ts = self.datetime_to_save(datetime.now())
        data = {
            self.HK_FROM_HOST:          from_host,
            self.HK_CREATED_AT:         ts,
            self.HK_STRONG_HASH_TYPE:   strong_hash_type,
            self.HK_WEAK_HASH_VER:      weak_hash_ver,
            self.HK_BLOCK_SIZE:         block_size,
            self.HK_TARGET_PATH:        target_path,
            }
        self._write_block(self.HEADER_TYPE, data)

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
        self._write_block(self.FILE_HEADER_TYPE, data)

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
        self._write_block(self.CHUNK_HASH_TYPE, data)






