import zlib

class CompressedFileReader(object):
    '''(somewhat) File like object to read files from CompressedFileWriter'''

    def __init__(self, file_handle):
        self.__fh = file_handle
        self.__decompress = zlib.decompressobj()
        self.__decompressed_buffer = ''


    def read(self, size=None):
        '''Read uncompressed data from file'''
        uncompressed = self.__decompressed_buffer

        # State check
        eof = False
        if self.__fh is None:
            eof = True

        # Feed data into decompresser until we get enough uncompressed data
        while not eof and (size is None or len(uncompressed) < size):

            # Get more data for decompressor
            new_data = self.__fh.read(4096)
            if not new_data:
                eof = True
            else:
                uncompressed += self.__decompress.decompress(new_data)

        # If we read all the data, close the file
        if eof and self.__fh is not None:
            uncompressed += self.__decompress.flush()
            self.__fh = None
            self.__decompress = None


        # Take requested uncompressed data
        if size is None:
            self.__decompressed_buffer = ''
            return uncompressed
        else:
            self.__decompressed_buffer = uncompressed[size:]
            return uncompressed[:size]


    def readline(self):

        # Read data until we reach a newline (\n) or end of file
        data = self.__decompressed_buffer
        self.__decompressed_buffer = ''

        if "\n" not in data:
            new_data = self.read(4096)
            data += new_data
            while new_data and "\n" not in data:
                new_data = self.read(4096)
                data += new_data

        # Extract line and place remaining back on buffer
        pos = data.find("\n")
        if pos == -1:
            return data
        else:
            self.__decompressed_buffer = data[pos+1:] + self.__decompressed_buffer
            return data[:pos+1]


    def readlines(self):
        while True:
            line = self.readline()
            yield line

            if not line:
                return


    @property
    def eof(self):
        return self.__fh is None and len(self.__decompressed_buffer) == 0



