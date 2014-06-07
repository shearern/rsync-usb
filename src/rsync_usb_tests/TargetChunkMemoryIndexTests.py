'''
Created on Jun 6, 2014

@author: nate
'''
import unittest

from rsync_usb.target_chunk_idx.MemoryIndex import MemoryIndex
from fixtures import SampleTargetChunkData
from rsync_usb.trx_files.TargetHashesReader import TargetHashesFile

from rsync_usb.trx_files.TargetHashesReader import TargetHashesChunk


class TargetChunkMemoryIndexTests(unittest.TestCase):


    def setUp(self):
        self.test_idx = MemoryIndex()
        for data in SampleTargetChunkData().generate_chunks():
            if data.__class__ is TargetHashesFile:
                self.test_idx.add_file(data)
            elif data.__class__ is TargetHashesChunk:
                self.test_idx.add_chunk(data)



    def testName(self):
        chunks = SampleTargetChunkData().generate_chunks()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()