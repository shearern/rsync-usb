import os
import unittest

from rsync_usb import ftree

class FtreeTests(unittest.TestCase):

    def setUp(self):
        # Run a test scan of the source dir
        path = os.path.join(os.path.dirname(__file__), '..')
        path = os.path.abspath(path)
        self.test_scan = list(ftree.find_files_for_sync(path))

    def testFileObjectsEqual(self):
        file_a = ftree.FileInfo('path/to/file')
        file_b = ftree.FileInfo('path/to/file')
        self.assertEqual(file_a, file_b)


    def testFileObjectsNotEqual(self):
        file_a = ftree.FileInfo('path/to/file')
        file_b = ftree.FileInfo('path/to/file_b')
        self.assertNotEqual(file_a, file_b)


    def testScanFiles(self):
        self.assertIn(ftree.FileInfo('ursync.py'),
                      self.test_scan)

    def testScanDeepFile(self):
        self.assertIn(ftree.FileInfo('rsync_usb/ftree.py'), self.test_scan)

    def testScanForDirs(self):
        self.assertIn(ftree.DirInfo('rsync_usb/'), self.test_scan)

    def testScanDeepDir(self):
        self.assertIn(ftree.DirInfo('rsync_usb/ui/'), self.test_scan)


    def testIsFile(self):
        self.assertTrue(ftree.FileInfo('file').is_file)
        self.assertFalse(ftree.DirInfo('dir/').is_file)

    def testIsDir(self):
        self.assertTrue(ftree.DirInfo('dir/').is_dir)
        self.assertFalse(ftree.FileInfo('file').is_dir)


    def testToString(self):
        file_a = ftree.FileInfo('path/to/file')
        self.assertEqual(str(file_a), 'path/to/file')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()