import os
import gflags

from SyncDirectory import SyncDirectory
from hostname import get_hostname
from ftree import find_files_for_sync
from rsync_usb.trx_files.TargetHashesWriter import TargetHashesWriter
from file_hashers import get_contig_chunk_hashes

from rsync_usb.trx_files.TargetHashesReader import TargetHashesReader

def do_target_cmd(local_path, trx_path):
    # Init transfer path
    sd = SyncDirectory(trx_path)

    # Update transfer settings
    hostname = get_hostname()
    sd.target_host = hostname

    # Create file to hold paths and hashes from target sys
    hashes_path = os.path.join(trx_path, 'target_hashes.dat')
    hashes = TargetHashesWriter(hashes_path)
    block_size = gflags.FLAGS.block_size
    hashes.write_header(
        block_size = block_size,
        from_host = hostname,
        strong_hash_type = TargetHashesWriter.MD5_STRONG_HASH,
        weak_hash_ver = 1,
        target_path = local_path)

    # Find files at local path
    if gflags.FLAGS.verbose:
        print "Scanning %s for files" % (local_path)
        print "Saving chunk hashes to %s" % (hashes_path)
    for file_obj in find_files_for_sync(local_path):
        if gflags.FLAGS.list_files:
            print " ", file_obj
            hashes.write_file_header(file_obj)

            # Hash chunks
            if file_obj.is_file:
                file_hashes = get_contig_chunk_hashes(file_obj.path_on_disk,
                                                      block_size)
                for weak_hash, strong_hash, chunk_size in file_hashes:
                    hashes.write_chunk_hash(weak_hash, strong_hash, chunk_size)

    hashes.close()


    # Debug
    hashes = TargetHashesReader(hashes_path)
    for data in hashes:
        print str(data)
