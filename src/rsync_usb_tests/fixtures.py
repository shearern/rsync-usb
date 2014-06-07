from StringIO import StringIO

from rsync_usb.trx_files.TargetHashesWriter import TargetHashesWriter
from rsync_usb.trx_files.TargetHashesReader import TargetHashesReader
from rsync_usb.ftree import FileInfo, DirInfo
from rsync_usb.file_hashers import calc_chunk_strong_hash, calc_chunk_weak_hash

class SampleTargetChunkData(object):
    '''Sample chunk hash data as if generated from a Target system'''

    def __init__(self):
        self.__writer = None
        self.files = list()
        self.file_hashes = dict()
        self.block_size = 4096


    def generate_chunks(self):
        fh = StringIO()
        self.__writer = TargetHashesWriter(fh)

        self.__writer.write_header(block_size=self.block_size,
            from_host = 'test',
            strong_hash_type = TargetHashesWriter.MD5_STRONG_HASH,
            weak_hash_ver = 1,
            target_path = '/')

        self.gen_file('test.txt', size=100)
        self.gen_file('data.dat', size=1024*1024)
        self.gen_dir('home')
        self.gen_dir('home/nate')
        self.gen_dir('home/nate/.ssh')
        self.gen_file('home/nate/contacts', size=1024)
        self.gen_dir('home/nate/pictures')
        for i in range(100):
            self.gen_file('home/nate/pictures/IMG_%03d.jpg' % (i), size=1024*1024)
        self.gen_file('home/nate/.ssh/authorized_keys', size=10)
        self.gen_file('home/nate/empty', size=0)

        self.__writer.close()

        fh.seek(0)
        reader = TargetHashesReader(fh)
        rtn = list(reader.all())

        return rtn


    def gen_file(self, name, size):
        self.__writer.write_file_header(FileInfo(name))

        self.files.append(name)
        self.file_hashes[name] = list()

        start = 0
        stop = min(0 + self.block_size - 1, size-1)
        while start < size:

            weak_hash = calc_chunk_weak_hash(name)
            strong_hash = calc_chunk_strong_hash(name)
            self.__writer.write_chunk_hash(weak_hash, strong_hash,
                                           stop - start + 1)

            self.file_hashes[name].append( (weak_hash, strong_hash) )

            start = stop + 1
            stop = min(start + self.block_size - 1, size-1)


    def gen_dir(self, name):
        self.__writer.write_file_header(DirInfo(name + '/'))

