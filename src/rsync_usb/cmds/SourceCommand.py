import os
import gflags

from rsync_usb.trx_files.TargetHashesReader import TargetHashesReader

from rsync_usb.trx_files.TargetHashesReader import TargetHashesFileHeader
from rsync_usb.trx_files.TargetHashesReader import TargetHashesFile
from rsync_usb.trx_files.TargetHashesReader import TargetHashesChunk

from rsync_usb.ftree import find_files_for_sync

from rsync_usb.file_hashers import calc_chunk_rolling_weak_hash
from rsync_usb.file_hashers import calc_chunk_strong_hash

from rsync_usb.target_chunk_idx.AdaptiveIndex import AdaptiveIndex

from rsync_usb.trx_files.SyncPlan import CopyFromTargetSystem
from rsync_usb.trx_files.SyncPlan import RawData
from rsync_usb.trx_files.SyncPlan import FileComplete

from rsync_usb.ChunkLocation import ChunkLocation

from CommandBase import CommandBase

class SourceCommand(CommandBase):
    '''Run action on source '''

    def __init__(self, trx_path=None):
        super(CommandBase, self).__init__()

        if trx_path is not None:
            self.set_trx_path(trx_path)

        self.block_size = None


    def run(self, source_path):

        # Read Target Hash File
        target_hashes = AdaptiveIndex()
        target_hostname = None
        for hostname, hashes_path in self.sd.list_existing_target_hash_files():
            if target_hostname is None:
                target_hostname = hostname
                if self.opt_verbose:
                    print "Loading hashes from", target_hostname
                with open(hashes_path, 'rb') as fh:
                    reader = TargetHashesReader(fh)
                    for data in reader:

                        # Load header info
                        if data.__class__ is TargetHashesFileHeader:
                            self.block_size = data.block_size

                        # Load Target Hashes
                        if data.__class__ is TargetHashesChunk:
                            target_hashes.add_chunk(data)
            else:
                raise NotImplemented("Can't handle multiple targets")


        # Scan through files on the source system
        if self.opt_verbose:
            print "Searching for files to sync under", source_path
        for file_obj in find_files_for_sync(source_path):
                if self.opt_list_files:
                    print " ", file_obj



    def create_sync_plan_for_file(self, file_obj, target_hashes):
        '''Create the actions needed to synchronize a single file

        Does not worry about conflict resolution.  Heavily influenced by Eric
        Prutt's version found at
        http://code.activestate.com/recipes/577518-rsync-algorithm/
        '''
        with open(file_obj.path_on_disk, 'rb') as fh:

            # Init window
            window = fh.read(self.block_size)
            weak_hash = calc_chunk_rolling_weak_hash(window, self.block_size)
            pos = ChunkLocation(file_obj.rel_path, 0, len(window))

            # TODO: Check for extra data in target system

            # Loop over all data in the file
            while True: # TODO: Terminate on EOF

                # Fully re-populate window
                if window is None:
                    window = fh.read(self.block_size)
                    weak_hash = calc_chunk_rolling_weak_hash(window, self.block_size)

                # See if data in window already exists on target
                if target_hashes.has_weak_hash(weak_hash.value, len(window)):

                    # Compute strong hash for a more sure match
                    strong_hash = calc_chunk_strong_hash(window)

                    # See if this part of the file is already in sync
                    already_in_sync = target_hashes.has_inplace_match(
                        rel_path = file_obj.rel_path,
                        start_pos = pos.start_pos,
                        weak_hash = weak_hash.value,
                        strong_hash = strong_hash,
                        chunk_size = len(window))
                    if already_in_sync:
                        # Nothing to do to this chunk (and can't conflict)
                        window = None
                        continue

                    # See if data exists in the same file on the target
                    target_pos = target_hashes.has_infile_match(
                        rel_path,
                        weak_hash,
                        strong_hash,
                        chunk_size):

                    # Else, Check to see if data exists anywhere in on the target
                    has_strong_hash = target_hashes.has_strong_hash(
                        weak_hash.value, strong_hash, len(window))
                    if has_strong_hash:

        # TODO: Yield File Complete with Size
