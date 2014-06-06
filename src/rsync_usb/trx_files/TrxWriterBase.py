import cPickle

from abc import ABCMeta, abstractmethod

from CompressedFileWriter import CompressedFileWriter

class TrxWriterBase(object):
    '''Base class for writing dicts of info to file'''
    __metaclass__ = ABCMeta

    K_TYPE = 'T'

    DT_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, file_handle):
        self.__fh = CompressedFileWriter(file_handle)


    def __del__(self):
        if self.__fh is not None:
            print "ERROR: YOU DID NOT CLOSE a", self.__class__.__name__


    def _write_block(self, block_type, data):
        '''Write a block of data to the file

        @param block_type: Indicator of what this block of data represents
            Used by reader to determine how to process this data later
        @param data: A dictionary of data to write.  Don't include class objects
        '''
        if self.__fh is None:
            raise Exception("File %s is not open")

        if data.has_key(self.K_TYPE):
            raise Exception("Can't use %s as a data key" % (self.K_TYPE))
        data[self.K_TYPE] = block_type

        cPickle.dump(data, self.__fh, -1)


    def close(self):
        if self.__fh is not None:
            self.__fh.close()
            self.__fh = None


    def datetime_to_save(self, dt):
        if dt is None:
            return 'None'
        return dt.strftime(self.DT_FORMAT)
    