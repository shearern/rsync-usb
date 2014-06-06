import os
import unittest
import random
import string
from tempfile import TemporaryFile
from StringIO import StringIO
from textwrap import dedent

from rsync_usb.trx_files.CompressedFileWriter import CompressedFileWriter
from rsync_usb.trx_files.CompressedFileReader import CompressedFileReader

class CompressedFileWriterTests(unittest.TestCase):

    def testSimpleCompression(self):

        source = "ABCDEFG"
        compressed_file = StringIO()

        cfw = CompressedFileWriter(compressed_file)
        cfw.write(source)
        cfw.close()

        compressed_file.seek(0)
        cfr = CompressedFileReader(compressed_file)
        decompressed = cfr.read()

        self.assertEqual(len(source), len(decompressed))
        self.assertEqual(source, decompressed)
        self.assertTrue(cfr.eof)


    def testLongSimpleCompression(self):

        source = "ABCDEFG" * 3000
        compressed_file = StringIO()

        cfw = CompressedFileWriter(compressed_file)
        cfw.write(source)
        cfw.close()

        compressed_file.seek(0)
        cfr = CompressedFileReader(compressed_file)
        decompressed = cfr.read()

        self.assertEqual(len(source), len(decompressed))
        self.assertEqual(source, decompressed)
        self.assertTrue(cfr.eof)


    def testReadline(self):
        source = ''
        for i in range(3000):
            source += "ABCDEFGHIJKLMNOPQRSTUVWXYZ\n"
        compressed_file = StringIO()

        cfw = CompressedFileWriter(compressed_file)
        cfw.write(source)
        cfw.close()

        compressed_file.seek(0)
        cfr = CompressedFileReader(compressed_file)
        decompressed = "".join(list(cfr.readlines()))

        for i in range(min(len(source), len(decompressed))):
            msg = "Source byte Byte %d not equal (source: %s, decomp: %s)"
            self.assertEqual(ord(source[i]), ord(decompressed[i]),
                msg % (i, source[i], decompressed[i]))
        self.assertEqual(len(source), len(decompressed),
                "Source length: %d, Decompressed: %d" % (len(source),
                                                         len(decompressed)))
        self.assertTrue(cfr.eof)


    def testCompressLargeBinaryData(self):
        source = ''
        for i in range(10):
            source += "\n"
            source += ''.join(chr(random.randrange(0, 255)) for _ in range(4096))

        compressed_file = StringIO()

        cfw = CompressedFileWriter(compressed_file)
        cfw.write(source)
        cfw.close()

        compressed_file.seek(0)
        cfr = CompressedFileReader(compressed_file)
        decompressed = cfr.read()

        self.assertEqual(len(source), len(decompressed))
        self.assertEqual(source, decompressed)
        self.assertTrue(cfr.eof)


    def testMixedReadAndReadlineAscii(self):
        source = ''
        for i in range(5):
            source += "\n"
            source += ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4096))

        compressed_file = StringIO()

        cfw = CompressedFileWriter(compressed_file)
        cfw.write(source)
        cfw.close()

        compressed_file.seek(0)
        cfr = CompressedFileReader(compressed_file)
        decompressed = ""
        while not cfr.eof:
            if random.choice(['read', 'readline']) == 'read()':
                decompressed += cfr.read(4096)
            else:
                decompressed += cfr.readline()

        for i in range(min(len(source), len(decompressed))):
            msg = "Source byte Byte %d not equal (source: %s, decomp: %s)"
            self.assertEqual(ord(source[i]), ord(decompressed[i]),
                msg % (i, source[i], decompressed[i]))
        self.assertEqual(len(source), len(decompressed))
        self.assertTrue(cfr.eof)


    def testMixedReadAndReadlineBinary(self):
        source = ''
        for i in range(5):
            source += "\n"
            source += ''.join(chr(random.randrange(0, 255)) for _ in range(4096))

        compressed_file = StringIO()

        cfw = CompressedFileWriter(compressed_file)
        cfw.write(source)
        cfw.close()

        compressed_file.seek(0)
        cfr = CompressedFileReader(compressed_file)
        decompressed = ''
        while not cfr.eof:
            if random.choice(['read', 'readline']) == 'read()':
                decompressed += cfr.read(4096)
            else:
                decompressed += cfr.readline()

        for i in range(min(len(source), len(decompressed))):
            msg = "Source byte Byte %d not equal (source: %d, decomp: %d)"
            self.assertEqual(ord(source[i]), ord(decompressed[i]),
                msg % (i, ord(source[i]), ord(decompressed[i])))
        self.assertEqual(len(source), len(decompressed))
        self.assertTrue(cfr.eof)
