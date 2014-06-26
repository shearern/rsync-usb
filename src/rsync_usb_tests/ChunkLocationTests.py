import unittest


from rsync_usb.ChunkLocation import ChunkLocation


class ChunkLocationTests(unittest.TestCase):
    '''Test TargetHashesWriter and TargetHashesReader'''


    def testProperties(self):
        pos = ChunkLocation('dummy', 100, 10)
        self.assertEqual(pos.path, 'dummy')
        self.assertEqual(pos.start_pos, 100)
        self.assertEqual(pos.data_len, 10)


    def testEndPos(self):
        pos = ChunkLocation('dummy', 100, 10)
        self.assertEqual(pos.start_pos + pos.data_len - 1, pos.end_pos)
        self.assertEqual(pos.end_pos, 109)


    def testEqual(self):
        pos_a = ChunkLocation('dummy', 100, 10)
        pos_b = ChunkLocation('dummy', 100, 10)
        self.assertEqual(pos_a, pos_b)


    # -- Overlaping chunk tests -----------------------------------------------


    def assertOverlaping(self, pos_a, pos_b):
        msg = "%s should overlap %s but did not"
        self.assertTrue(pos_a.overlaps(pos_b), msg % (str(pos_a), str(pos_b)))
        self.assertTrue(pos_b.overlaps(pos_a), msg % (str(pos_b), str(pos_a)))


    def assertNotOverlaping(self, pos_a, pos_b):
        msg = "%s should not overlap %s but does"
        self.assertFalse(pos_a.overlaps(pos_b), msg % (str(pos_a), str(pos_b)))
        self.assertFalse(pos_b.overlaps(pos_a), msg % (str(pos_b), str(pos_a)))


    def testNoOverlapBefore(self):
        pos_a = ChunkLocation('dummy', 10, 10)
        pos_b = ChunkLocation('dummy', 100, 10)
        self.assertNotOverlaping(pos_a, pos_b)

    def testNoOverlapAfter(self):
        pos_a = ChunkLocation('dummy', 1000, 10)
        pos_b = ChunkLocation('dummy', 100, 10)
        self.assertNotOverlaping(pos_a, pos_b)

    def testNoOverlapDifferentPaths(self):
        pos_a = ChunkLocation('dummy_a', 100, 10)
        pos_b = ChunkLocation('dummy_b', 100, 10)
        self.assertNotOverlaping(pos_a, pos_b)

    def testOverlapEqual(self):
        #     0000000000111111111112
        #     0123456789001234567890
        #  A: ------|=======|-------
        #  B: ------|=======|-------
        pos_a = ChunkLocation('dummy', 6, 9)
        pos_b = ChunkLocation('dummy', 6, 9)
        self.assertOverlaping(pos_a, pos_b)

    def testOverlapStartsBefore(self):
        #     0000000000111111111112
        #     0123456789001234567890
        #  A: ----|=======|---------
        #  B: ------|=======|-------
        pos_a = ChunkLocation('dummy', 4, 9)
        pos_b = ChunkLocation('dummy', 6, 9)
        self.assertOverlaping(pos_a, pos_b)


    def testOverlapStartsBeforeAndEqual(self):
        #     0000000000111111111112
        #     0123456789001234567890
        #  A: ----|=========|-------
        #  B: ------|=======|-------
        pos_a = ChunkLocation('dummy', 4, 11)
        pos_b = ChunkLocation('dummy', 6, 9)
        self.assertOverlaping(pos_a, pos_b)

    def testOverlapInside(self):
        #     0000000000111111111112
        #     0123456789001234567890
        #  A: ------|=======|-------
        #  B: -----|=========|------
        pos_a = ChunkLocation('dummy', 6, 9)
        pos_b = ChunkLocation('dummy', 5, 11)
        self.assertOverlaping(pos_a, pos_b)

    def testOverlapInsideSameStart(self):
        #     0000000000111111111112
        #     0123456789001234567890
        #  A: ------|=======|-------
        #  B: ------|========|------
        pos_a = ChunkLocation('dummy', 6, 9)
        pos_b = ChunkLocation('dummy', 6, 10)
        self.assertOverlaping(pos_a, pos_b)

    def testOverlapInsideSameEnd(self):
        #     0000000000111111111112
        #     0123456789001234567890
        #  A: ------|=======|-------
        #  B: -----|========|-------
        pos_a = ChunkLocation('dummy', 6, 9)
        pos_b = ChunkLocation('dummy', 5, 10)
        self.assertOverlaping(pos_a, pos_b)

    def testOverlapEndsAfter(self):
        #     0000000000111111111112
        #     0123456789001234567890
        #  A: -------|=======|------
        #  B: ------|=======|-------
        pos_a = ChunkLocation('dummy', 7, 9)
        pos_b = ChunkLocation('dummy', 6, 9)
        self.assertOverlaping(pos_a, pos_b)

    def testOverlapEndsAfterAndEqual(self):
        #     0000000000111111111112
        #     0123456789001234567890
        #  A: ------|=========|-----
        #  B: ------|=======|-------
        pos_a = ChunkLocation('dummy', 6, 11)
        pos_b = ChunkLocation('dummy', 6, 9)
        self.assertOverlaping(pos_a, pos_b)

