import os
import unittest
import random
import string
import datetime
from tempfile import TemporaryFile
from StringIO import StringIO
from textwrap import dedent
import hashlib

from rsync_usb.file_hashers import calc_chunk_strong_hash, calc_chunk_weak_hash
from rsync_usb.trx_files.TargetHashesWriter import TargetHashesWriter
from rsync_usb.trx_files.TargetHashesReader import TargetHashesReader

from rsync_usb.trx_files.TargetHashesReader import TargetHashesFileHeader
from rsync_usb.trx_files.TargetHashesReader import TargetHashesFile
from rsync_usb.trx_files.TargetHashesReader import TargetHashesChunk

from rsync_usb.ftree import FileInfo, DirInfo

class TargetHashTrxTests(unittest.TestCase):
    '''Test TargetHashesWriter and TargetHashesReader'''

    STRONG_HASH_A = calc_chunk_strong_hash('A')
    STRONG_HASH_B = calc_chunk_strong_hash('B')
    STRONG_HASH_C = calc_chunk_strong_hash('C')
    STRONG_HASH_D = calc_chunk_strong_hash('D')
    STRONG_HASH_E = calc_chunk_strong_hash('E')

    WEAK_HASH_A = calc_chunk_weak_hash('A')
    WEAK_HASH_B = calc_chunk_weak_hash('B')
    WEAK_HASH_C = calc_chunk_weak_hash('C')
    WEAK_HASH_D = calc_chunk_weak_hash('D')
    WEAK_HASH_E = calc_chunk_weak_hash('E')

    def _test_write(self):
        trx_file = StringIO()
        writer = TargetHashesWriter(trx_file)

        writer.write_header(block_size=10,
                            from_host='hostname',
                            strong_hash_type=TargetHashesWriter.MD5_STRONG_HASH,
                            weak_hash_ver=1,
                            target_path='/fake/path') #0

        writer.write_file_header(FileInfo('names.dat', '/fake/path/names.dat')) #1
        writer.write_chunk_hash(self.WEAK_HASH_A, self.STRONG_HASH_A, 10) #2
        writer.write_chunk_hash(self.WEAK_HASH_B, self.STRONG_HASH_B, 10) #3
        writer.write_chunk_hash(self.WEAK_HASH_C, self.STRONG_HASH_C, 5) #4

        writer.write_file_header(DirInfo('home/', '/fake/path/home')) #5

        writer.write_file_header(FileInfo('home/secrets', '/fake/path/home/secrets')) #6
        writer.write_chunk_hash(self.WEAK_HASH_D, self.STRONG_HASH_A, 10) #7
        writer.write_chunk_hash(self.WEAK_HASH_E, self.STRONG_HASH_B, 7) #8

        writer.close()
        trx_file.seek(0)
        return trx_file


    def _test_read(self, trx_file):
        reader = TargetHashesReader(trx_file)
        return list(reader.all())


    def testWrite(self):
        trx_file = self._test_write()
        self.assertGreater(len(trx_file.read()), 0)


    def testRead(self):
        trx_file = self._test_write()
        read_data = self._test_read(trx_file)
        self.assertEqual(len(read_data), 9)


    def testReadHeader(self):
        trx_file = self._test_write()
        read_data = self._test_read(trx_file)

        header =  read_data[0]

        self.assertIsInstance(header, TargetHashesFileHeader)
        self.assertEqual(header.from_host, 'hostname')
        self.assertIsInstance(header.created_at, datetime.datetime)
        self.assertEqual(header.strong_hash_type, TargetHashesWriter.MD5_STRONG_HASH)
        self.assertEqual(header.weak_hash_ver, 1)
        self.assertEqual(header.block_size, 10)
        self.assertEqual(header.target_path, '/fake/path')


    def testReadFileHeader(self):
        trx_file = self._test_write()
        read_data = self._test_read(trx_file)

        header =  read_data[0]
        names_file = read_data[1]

        self.assertIsInstance(names_file, TargetHashesFile)
        self.assertTrue(names_file.scan_header is header)
        self.assertEqual(names_file.path, 'names.dat')
        self.assertEqual(names_file.file_obj, FileInfo('names.dat'))

        secret_file = read_data[6]
        self.assertTrue(secret_file.scan_header is header)
        self.assertEqual(secret_file.path, 'home/secrets')
        self.assertEqual(secret_file.file_obj, FileInfo('home/secrets'))


    def testReadFileHeaderForDir(self):
        trx_file = self._test_write()
        read_data = self._test_read(trx_file)

        header =  read_data[0]
        home =  read_data[5]

        self.assertIsInstance(home, TargetHashesFile)
        self.assertTrue(home.scan_header is header)
        self.assertEqual(home.path, 'home/')
        self.assertEqual(home.file_obj, DirInfo('home/'))


    def testReadFileChunk(self):
        trx_file = self._test_write()
        read_data = self._test_read(trx_file)

        header =  read_data[0]
        names_file =  read_data[1]
        chunk = read_data[3]

        self.assertIsInstance(chunk, TargetHashesChunk)
        self.assertTrue(chunk.scan_header is header)
        self.assertTrue(chunk.file_header is names_file)
        self.assertEqual(chunk.weak_hash, self.WEAK_HASH_B)
        self.assertEqual(chunk.strong_hash, self.STRONG_HASH_B)
        self.assertEqual(chunk.chunk_size, 10)
        self.assertEqual(chunk.start_pos, 10)
        self.assertEqual(chunk.end_pos, 19)

        # A chunk smaller than block size:
        self.assertEqual(read_data[8].chunk_size, 7)
        self.assertEqual(read_data[8].start_pos, 10)
        self.assertEqual(read_data[8].end_pos, 16)

