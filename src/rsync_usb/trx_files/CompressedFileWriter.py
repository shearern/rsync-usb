import zlib


class CompressedFileWriter(object):
    '''(somewhat) File like object that compresses data as it is written'''

    def __init__(self, file_handle):
        self.__fh = file_handle
        self.__compress = zlib.compressobj()


    def write(self, data):
        compressed = self.__compress.compress(data)
        self.__fh.write(compressed)


    def close(self):
        compressed = self.__compress.flush()
        self.__fh.write(compressed)
        self.__fh = None
        self.__compress = None


