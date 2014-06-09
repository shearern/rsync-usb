'''
Created on Jun 6, 2014

@author: nate
'''
import unittest

from rsync_usb.target_chunk_idx.MemoryIndex import MemoryIndex
from fixtures import SampleTargetChunkData
from rsync_usb.file_hashers import calc_chunk_strong_hash, calc_chunk_weak_hash

from rsync_usb.trx_files.TargetHashesReader import TargetHashesChunk


class TargetChunkMemoryIndexTests(unittest.TestCase):


    def setUp(self):
        self.chunks = list()
        self.test_idx = MemoryIndex()
        self.generator = SampleTargetChunkData()
        for data in self.generator.generate_chunks():
            if data.__class__ is TargetHashesChunk:
                self.chunks.append(data)
                self.test_idx.add_chunk(data)



    def testHasChunk(self,):
        self.assertTrue(self.test_idx.has_chunk(self.chunks[3]))


    def testHasWeakHash(self):
        weak, strong = self.generator.file_hashes['test.txt'][0]
        self.assertTrue(self.test_idx.has_weak_hash(weak, 100))
        self.assertFalse(self.test_idx.has_weak_hash(
                calc_chunk_weak_hash('random'), 10))


    def testHasWeakHashWithWrongSize(self):
        weak, strong = self.generator.file_hashes['test.txt'][0]
        self.assertFalse(self.test_idx.has_weak_hash(weak, 99))


    def testHashStrongHash(self):
        weak, strong = self.generator.file_hashes['test.txt'][0]
        self.assertTrue(self.test_idx.has_strong_hash(weak, strong, 100))
        self.assertFalse(self.test_idx.has_strong_hash(
            calc_chunk_weak_hash('random'), calc_chunk_strong_hash('random'),
            100))


    def testFindChunks(self):
        found = list(self.test_idx.find_chunks(
            self.chunks[0].weak_hash,
            self.chunks[0].strong_hash,
            self.chunks[0].chunk_size))

        self.assertEqual(len(found), 1)
        self.assertEqual(found[0], self.chunks[0])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()