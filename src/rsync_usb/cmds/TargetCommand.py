
from rsync_usb.hostname import get_hostname
from rsync_usb.ftree import find_files_for_sync
from rsync_usb.trx_files.TargetHashesWriter import TargetHashesWriter
from rsync_usb.file_hashers import get_contig_chunk_hashes

from rsync_usb.trx_files.TargetHashesReader import TargetHashesReader

from CommandBase import CommandBase

class TargetCommand(CommandBase):

    def __init__(self, trx_path=None):
        super(TargetCommand, self).__init__()
        if trx_path is not None:
            self.set_trx_path(trx_path)


    def run(self, target_path):
        # Create file to hold paths and hashes from target sys
        hashes_path = self.sd.get_target_hash_file_path_for_self()
        with open(hashes_path, 'wb') as fh:
            hashes = TargetHashesWriter(fh)
            block_size = self.opt_default_block_size
            hashes.write_header(
                block_size = block_size,
                from_host = get_hostname(),
                strong_hash_type = TargetHashesWriter.MD5_STRONG_HASH,
                weak_hash_ver = 1,
                target_path = target_path)

            # Find files at local path
            if self.opt_verbose:
                print "Scanning %s for files" % (target_path)
                print "Saving chunk hashes to %s" % (hashes_path)
            for file_obj in find_files_for_sync(target_path):
                if self.opt_list_files:
                    print " ", file_obj
                    hashes.write_file_header(file_obj)

                    # Hash chunks
                    if file_obj.is_file:
                        file_hashes = get_contig_chunk_hashes(file_obj.path_on_disk,
                                                              block_size)
                        for weak_hash, strong_hash, chunk_size in file_hashes:
                            hashes.write_chunk_hash(weak_hash, strong_hash, chunk_size)

            hashes.close()


