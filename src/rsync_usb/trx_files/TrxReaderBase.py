import os
import zlib
import cPickle

from abc import ABCMeta, abstractmethod
from TrxWriterBase import TrxWriterBase


class TrxFileCorrupt(Exception): pass


def get_req_key(type_desc, data, keyname):
    if not data.has_key(keyname):
        msg = "%s data blocks are required to have a '%s' key"
        raise TrxFileCorrupt(msg % (type_desc, keyname))
    return data[keyname]


def get_opt_key(data, keyname, default=None):
    if data.has_key(keyname):
        return data[keyname]
    return default


class CompressedFileReader(object):
    '''Read a file compressed with zlib'''

    def __init__(self, path):
        self.__path = path
        self.__fh = open(path, 'rb')
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
            if new_data is None:
                eof = True
            else:
                uncompressed += self.__decompress.decompress(new_data)

        # If we read all the data, close the file
        if eof and self.__fh is not None:
            uncompressed += self.__decompress.flush()
            self.__fh.close()
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
            while new_data is not None and "\n" not in data:
                new_data = self.read(4096)
                data += new_data

        # Extract line and place remaining back on buffer
        if len(data) > 0:
            pos = data.find("\n")
            if pos == -1:
                return data
            else:
                self.__decompressed_buffer = data[pos+1:]
                return data[:pos+1]
        else:
            return None



class TrxReaderBase(object):
    '''Base class for reading dicts back from a file created by TrxWriterBase

    See _get_decode_instructions() for processing algorithm.
    '''
    __metaclass__ = ABCMeta

    def __init__(self, path):
        if not os.path.exists(path):
            raise Exception("Trx File Not Found: " + path)
        self.__path = path
        self.__fh = CompressedFileReader(path)
        self.__instruct = self._get_decode_instructions()
        self.__depickler = cPickle.Unpickler(self.__fh)
        self.__depickler.find_global = None # Prevent depickling objects

    AUTO = 'A'
    MANUAL = 'M'

    @abstractmethod
    def _get_decode_instructions(self):
        '''Get rules on how to decode the data blocks

        In general, each block of data from the file is expected to be a dict
        with a special key (TargetHashesWriter.K_TYPE) that designates what
        type of data is stored.  There are two methods for interpretting the
        data dicts that are read:
            MANUAL:    self._intperet_data() is call for each item
            AUTO:      A class is constructed and keys of the dict are mapped
                       class attributes as defined by the map.  Then
                       _process_auto_decoded() is called.


        The format of the expected return structure is a dict:
        {
            data_block_type: {
                'method': 'MANUAL' | 'AUTO',
                'class': DataClass,
                'map': {
                    'DATA_KEY': 'class_attr_name',
                    'DATA_KEY': 'class_attr_name',
                    ...
                    },
                'defaults': {
                    'DATA_KEY': 'default_value',
                    },
            }
        }

        Where:
            data_block_type:    Is the type code passed to
                                TrxWriterBase._write_block
            method:             Is MANUAL or AUTO
            class:              Is the class that will be constructed for each
                                data dict if method is auto.  Contructor must
                                take no arguments
            map:                Is a dict specifying the data dict key ->
                                class attribute name association
            defaults:           Specifies default values for non-required data
                                dict keys.  Data keys with defautls are not
                                required
        '''


    def __iter__(self):
        return self


    def next(self):
        '''Read next data item from file'''

        if self.__fh is None:
            return None

        # Read next data dict from disk
        data = self.__depickler.load()

        # Interpret Type
        type_key = TrxWriterBase.K_TYPE
        if not data.has_key(type_key):
            raise TrxFileCorrupt("Data item missing type key: " + str(data))
        data_type = data[type_key]
        if not self.__instruct.has_key(data_type):
            raise TrxFileCorrupt("Unknown data block type '%s': %s" % (
                data_type, str(data)))

        # Process Data
        if self.__instruct[data_type]['method'] == self.MANUAL:
            return self._intperet_data(data_type, data)
        elif self.__instruct[data_type]['method'] == self.AUTO:
            data = self._auto_interpret_data(data_type, data)
            return self._process_auto_decoded(data_type, data)
        else:
            msg = "Invalid decode method '%s' for data type '%s'"
            raise Exception(msg % (self.__instruct[data_type]['method'],
                                   data_type))


    def _intperet_data(self, data_type, data):
        '''Convert data dict into whatever format is desired'''
        return data


    def _auto_interpret_data(self, data_type, data):
        '''Perform AUTO interpretation of data dict'''

        # Get decoding instructions
        instruct = self.__instruct[data_type]
        if not instruct.has_key('defaults'):
            raise Exception("'defaults' key required in decode instructions")

        # Build object to return
        rtn = instruct['class']()
        for data_key, cls_attr in instruct['map'].items():
            value = None
            if not instruct['defaults'].has_key(data_key):  # Required
                type_desc = '%s Block' % (data_type)
                value = get_req_key(type_desc, data, data_key)
            else:   # Optional
                default = instruct['defaults'][data_key]
                value = get_opt_key(data, data_key, default)
            setattr(rtn, cls_attr, value)

        return rtn


    def _process_auto_decoded(self, data_type, data):
        '''Convert data dict into whatever format is desired'''
        return data


