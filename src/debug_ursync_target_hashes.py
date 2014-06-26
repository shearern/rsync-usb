'''Dump the contents of the target hash file to be examined'''


import sys
import gflags

from rsync_usb.ui.ConsoleUI import ConsoleUI

from rsync_usb.ParameterError import ParameterError
from rsync_usb.trx_files.TargetHashesReader import TargetHashesReader

from rsync_usb.trx_files.TargetHashesReader import TargetHashesFileHeader
from rsync_usb.trx_files.TargetHashesReader import TargetHashesFile
from rsync_usb.trx_files.TargetHashesReader import TargetHashesChunk


def make_header(num, title):
    header = '-- Record %03i - %s ' % (num, title.upper())
    header += '-' * (header_len-len(header))
    return header


def print_attrib(name, value):
    if value is None:
        value = '[None]'
    value = str(value)
    if len(value) > 50:
        value = value[:47] + '...'
    print "    %-25s %s" % (name+':', value)


if __name__ == '__main__':

    ui = ConsoleUI()

    # Parse arguments
    try:
        argv = gflags.FLAGS(sys.argv)

        # Arguments
        if len(argv) != 2:
            raise gflags.FlagsError("Must specify path to target hash file")
        hashes_path = argv[1]

    except gflags.FlagsError, e:
        print "Usage Error: " + str(e)
        print ""
        print 'Usage: %s [options] hashes_path' % (sys.argv[0])
        print "Where:"
        print "   options      are defined below"
        print "   hashes_path  is path to the target_hashes.dat"
        sys.exit(1)

    # Debug File
    with open(hashes_path, 'rb') as fh:
        hashes = TargetHashesReader(fh)
        header_len = 80
        for i, data in enumerate(hashes):

            # -- HEADER -------------------------------------------------------
            if data.__class__ is TargetHashesFileHeader:
                print make_header(i, 'HEADER')

                print_attrib('from_host', data.from_host)
                print_attrib('created_at', data.created_at)
                print_attrib('strong_hash_type', data.strong_hash_type)
                print_attrib('weak_hash_ver', data.weak_hash_ver)
                print_attrib('block_size', data.block_size)
                print_attrib('target_path', data.target_path)

            # -- FILE_HEADER --------------------------------------------------
            elif data.__class__ is TargetHashesFile:
                print make_header(i, 'FILE HEADER')

                if data.scan_header is not None:
                    print_attrib('scan_header.from_host',
                                 data.scan_header.from_host)
                else:
                    print_attrib('scan_header.from_host',
                                 "scan_header is None")

                print_attrib('path', data.path)
                print_attrib('file_obj', data.file_obj)


            # -- FILE_CHUNK ---------------------------------------------------
            elif data.__class__ is TargetHashesChunk:
                print make_header(i, 'FILE CHUNK HASHES')

                if data.scan_header is not None:
                    print_attrib('scan_header.from_host',
                                 data.scan_header.from_host)
                else:
                    print_attrib('scan_header.from_host',
                                 "scan_header is None")

                if data.file_header is not None:
                    print_attrib('file_header.file_obj',
                                 data.file_header.file_obj)
                else:
                    print_attrib('file_header.file_obj',
                                 "file_header is None")


                print_attrib('weak_hash', data.weak_hash)
                print_attrib('strong_hash', str([ord(c) for c in data.strong_hash]))
                print_attrib('chunk_size', data.chunk_size)
                print_attrib('pos', data.pos)


            # -- UNKNOWN RECORD -----------------------------------------------
            elif data.__class__ is TargetHashesFileHeader:
                header = '-- Record %i -- %s ' % (i, "UNKNWON")
                header += '-' * (header_len-len(header))
                print header
                print str(data)
