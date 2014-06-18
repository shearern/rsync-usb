import unittest
from StringIO import StringIO
from random import randint

from rsync_usb.file_hashers import calc_chunk_rolling_weak_hash
from rsync_usb.file_hashers import calc_chunk_weak_hash

from rsync_usb import Eric_Prutt_rsync as rsync

class TestRollingHash(unittest.TestCase):
    '''Test the rolling weak hash'''


    # Test Parameters
    TEST_FILE_SIZE = 26
    WINDOW_SIZE = 10


    def _test_windows(self, rand=False):

        # Generate test data to hash
        data = ''
        for i in range(self.TEST_FILE_SIZE):
            if rand:
                data += chr(randint(33, 125))
            else:
                data += chr(ord('a') + i)

        # Return "rolling" windows of data
        for start in range(self.TEST_FILE_SIZE):
            yield data[start:start+self.WINDOW_SIZE]


    def testEricPruttHashImnplementation(self):

        target = StringIO('ABCDEFGHIJKLM OPQRSTUVWXYZ') # No N
        hashes = rsync.blockchecksums(target, blocksize=10)

        source = StringIO('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        delta = rsync.rsyncdelta(source, hashes, blocksize=10)

        patched = StringIO()
        rsync.patchstream(target, patched, delta)

        self.assertEqual(patched.getvalue(), source.getvalue())


    def testEricPruttRollingHash(self):

        # Create test file/data
        a = 0
        b = 0
        rolling_hash = None
        prev_data = None
        for data in self._test_windows(rand=False):
            data = rsync.bytes(data)

            # Update weak hash
            if rolling_hash is None:
                rolling_hash, a, b = rsync.weakchecksum(data)
            else:
                # New byte is 0 if no new bytes added
                new = data[-1]
                if len(data) < self.WINDOW_SIZE:
                    new = 0
                # Perform rolling math
                rolling_hash, a, b = rsync.rollingchecksum(
                    removed = prev_data[0],
                    new = new,
                    a = a,
                    b = b,
                    blocksize = self.WINDOW_SIZE)

            # Compute straight hash
            straight_hash = rsync.weakchecksum(data)[0]

            # Compare
            if prev_data is None:
                prev_data = list()
            msg = "%s != %s (prev_data: %s, this data: %s)"
            msg = msg % (str(rolling_hash), str(straight_hash),
                         "".join([chr(c) for c in prev_data]),
                         "".join([chr(c) for c in data]))
            self.assertEqual(rolling_hash, straight_hash, msg)

            prev_data = data


    def testMyWeakHashSameAsErics(self):
        for data in self._test_windows(rand=True):
            self.assertEqual(calc_chunk_weak_hash(data),
                             rsync.weakchecksum(rsync.bytes(data))[0])


    def testRollingHashWithoutTail(self):

        # Create test file/data
        rolling_hash = None
        prev_data = None
        for data in self._test_windows(rand=False):
            if len(data) == self.WINDOW_SIZE:
                rolling_hash = calc_chunk_rolling_weak_hash(
                    data = data,
                    block_size = self.WINDOW_SIZE,
                    prev_hash = rolling_hash)
                straight_hash = calc_chunk_weak_hash(data)

                msg = "%s != %s (prev_data: %s, this data: %s)"
                msg = msg % (str(rolling_hash.value), str(straight_hash),
                             str(prev_data), str(data))
                self.assertEqual(rolling_hash.value, straight_hash, msg)

                prev_data = data


    def testRollingHash(self):

        # Create test file/data
        rolling_hash = None
        prev_data = None
        for data in self._test_windows(rand=False):
            rolling_hash = calc_chunk_rolling_weak_hash(
                data = data,
                block_size = self.WINDOW_SIZE,
                prev_hash = rolling_hash)
            straight_hash = calc_chunk_weak_hash(data)

            msg = "%s != %s (prev_data: %s, this data: %s)"
            msg = msg % (str(rolling_hash.value), str(straight_hash),
                         str(prev_data), str(data))
            self.assertEqual(rolling_hash.value, straight_hash)

            prev_data = data


    def testRollingHashRandomWindow(self):

        # Create test file/data
        rolling_hash = None
        for data in self._test_windows(rand=True):
            rolling_hash = calc_chunk_rolling_weak_hash(
                data = data,
                block_size = self.WINDOW_SIZE,
                prev_hash = rolling_hash)
            straight_hash = calc_chunk_weak_hash(data)
            self.assertEqual(rolling_hash.value, straight_hash)