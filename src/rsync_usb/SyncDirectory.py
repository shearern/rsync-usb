import os
import re

from ParameterError import ParameterError

from SyncSettings import SyncSettings

from hostname import get_hostname

class SyncDirectory(object):
    '''Wraps interaction with the sync directory

    The sync directory is the directory on the temporary storage medium that
    will be moved between hosts to accomplish the data sync.  This is the USB
    disk location referred to in the name Rsync Over USB.
    '''


    def __init__(self, path):
        '''Init

        @param path: Path to the sync directory
        '''
        self.__path = path
        self.__this_hostname = get_hostname()

        if not os.path.exists(path):
            raise ParameterError("Transfer path does not exist: ", path)
        if not os.path.isdir(path):
            raise ParameterError("Transfer path is not a directory: ", path)


    @property
    def sync_settings_path(self):
        return os.path.join(self.__path, 'sync.settings')


    def read_sync_settings(self):
        settings = SyncSettings()
        if os.path.exists(self.sync_settings_path):
            settings.read(self.sync_settings_path)
        return settings


    def write_sync_settings(self, settings):
        settings.write(self.sync_settings_path)


    def get_target_hash_file_path_for_self(self):
        '''Get path to the file to write target hashes to'''
        return os.path.join(self.__path,
                            'target_hashes.%s.dat' % (self.__this_hostname))


    TARGET_HASH_PATH_PAT = re.compile(r'^target_hashes.(.*).dat$')
    def list_existing_target_hash_files(self):
        '''List the target hash files that exist in the sync directory

        @return generator: (hostname, path)
        '''
        for filename in os.listdir(self.__path):
            m = self.TARGET_HASH_PATH_PAT.match(filename)
            if m:
                yield m.group(1), os.path.join(self.__path, filename)

