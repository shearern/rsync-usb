from TargetHashesWriter import TargetHashesWriter as THW

from TrxReaderBase import TrxReaderBase


class TargetHashesFileHeader(object):
    '''Hold data from target hashes file header'''
    def __init__(self):
        self.from_host = None
        self.created_at = None
        self.strong_hash_type = None
        self.weak_hash_ver = None
        self.block_size = None
        self.target_path = None

    def __str__(self):
        msg = "Hashes from %s on %s created at %s"
        return msg % (self.target_path, self.from_host, str(self.created_at))


class TargetHashesFile(object):
    '''Hold data about a file on the target system'''
    def __init__(self):
        self.scan_header = None

        self.path = None
        self.fileobj_type = None

        self.file_obj = None


    def __str__(self):
        if self.file_obj is not None:
            return str(self.file_obj)
        return self.path


class TargetHashesChunk(object):
    '''Hold data about a chunk of a file on the target system'''
    def __init__(self):
        self.scan_header = None
        self.file_header = None

        self.weak_hash = None
        self.strong_hash = None
        self.chunk_size = None

        self.start_pos = None
        self.end_pos = None


    def __str__(self):
        if self.file_header is not None:
            msg = self.file_header
        else:
            msg = "chunk"
        return "%s[%s:%s]" % (msg, str(self.start_pos), str(self.end_pos))


class TargetHashesReader(TrxReaderBase):
    '''Read back hashes from target system'''

    def __init__(self, path):
        self.__scan_header = None
        self.__last_file_header = None
        self.__last_file_chunk = None

        super(TargetHashesReader, self).__init__(path)


    def _intperet_data(self, data_type, data):
        '''Convert data dict into whatever format is desired'''
        if data_type == THW.HEADER_TYPE:
            return self._interpret_scan_header_data(data)
        elif data_type == THW.FILE_HEADER_TYPE:
            return self._interpret_file_header_data(data)
        elif data_type == THW.CHUNK_HASH_TYPE:
            return self._interpret_chunk_data(data)

    def _get_decode_instructions(self):
        return {
            THW.HEADER_TYPE: {
                'method':     TrxReaderBase.AUTO,
                'class':      TargetHashesFileHeader,
                'map': {
                    THW.HK_FROM_HOST:           'from_host',
                    THW.HK_CREATED_AT:          'created_at',
                    THW.HK_STRONG_HASH_TYPE:    'strong_hash_type',
                    THW.HK_WEAK_HASH_VER:       'weak_hash_ver',
                    THW.HK_BLOCK_SIZE:          'block_size',
                    THW.HK_TARGET_PATH:         'target_path',
                    },
                'defaults': {
                    },
                },
            THW.FILE_HEADER_TYPE: {
                'method':     TrxReaderBase.AUTO,
                'class':      TargetHashesFile,
                'map': {
                    THW.FK_PATH:                'path',
                    THW.FK_TYPE:                'fileobj_type',
                    },
                'defaults': {
                    },
                },
            THW.CHUNK_HASH_TYPE: {
                'method':     TrxReaderBase.AUTO,
                'class':      TargetHashesChunk,
                'map': {
                    THW.FC_WEAK_HASH:           'weak_hash',
                    THW.FC_STRONG_HASH:         'strong_hash',
                    THW.FC_CHUNK_SIZE:          'chunk_size',
                    },
                'defaults': {
                    THW.FC_CHUNK_SIZE:          None,
                    },
                },
            }


    def _process_auto_decoded(self, data_type, data):
        '''Convert data dict into whatever format is desired'''
        if data_type == THW.HEADER_TYPE:
            self.__scan_header = data
        elif data_type == THW.FILE_HEADER_TYPE:
            data.scan_header = self.__scan_header
            self.__last_file_header = data
            self.__last_file_chunk = None
        elif data_type == THW.CHUNK_HASH_TYPE:
            data.scan_header = self.__scan_header
            data.file_header = self.__last_file_header

            if data.chunk_size is None:
                data.chunk_size = self.__scan_header.block_size

            if self.__last_file_chunk is None:
                data.start_pos = 0
            else:
                data.start_pos = self.__last_file_chunk.end_pos + 1

            data.end_pos = data.start_pos + data.chunk_size - 1

            self.__last_file_chunk = data

        return data

