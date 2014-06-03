import os

from ParameterError import ParameterError

from SyncSettings import SyncSettings

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

