'''File Tree scanning related functions and classes'''
import os

class DiskObjInfo(object):
    '''Hold inforation to identify an object on the disk'''

    def __init__(self, rel_path, path_on_disk):
        self.__name = os.path.basename(rel_path)
        self.__rel_path = rel_path
        self.__path_on_disk = path_on_disk

    @property
    def name(self):
        '''Name of the disk object without path'''
        return self.__name

    @property
    def rel_path(self):
        '''Path to disk object relative to scan path'''
        return self.__rel_path

    @property
    def path_on_disk(self):
        '''Actual path to disk object'''
        return self.__path_on_disk


    def __eq__(self, obj):
        try:
            return obj.rel_path == self.__rel_path
        except AttributeError:
            return NotImplemented


    def __str__(self):
        return self.__rel_path


class FileInfo(DiskObjInfo):
    '''Hold basic information about a file'''

    def __init__(self, rel_path, path_on_disk=None):
        if rel_path[-1] == '/':
            raise Exception("File path should not end in '/'")
        if path_on_disk is not None:
            if not os.path.isfile(path_on_disk):
                raise Exception("Not a file: " + path_on_disk)
        super(FileInfo, self).__init__(rel_path, path_on_disk)


    @property
    def is_file(self):
        return True
    @property
    def is_dir(self):
        return False
    
    @property
    def fileobj_type(self):
        return 'F'


class DirInfo(DiskObjInfo):
    '''Hold basic information about a directory'''

    def __init__(self, rel_path, path_on_disk=None):
        if rel_path[-1] != '/':
            raise Exception("Dir path should end in '/'")
        if path_on_disk is not None:
            if not os.path.isdir(path_on_disk):
                raise Exception("Not a dir: " + path_on_disk)
        super(DirInfo, self).__init__(rel_path, path_on_disk)


    @property
    def is_file(self):
        return False
    @property
    def is_dir(self):
        return True

    @property
    def fileobj_type(self):
        return 'D'


def find_files_for_sync(root_path):
    '''List all files under a given root path, returning relative paths

    This function will recurse over a directory structure to find all files and
    directories.  It will function similar to os.walk, but is intended
    specifically for finding which files to sync.  It'll therefore be
    influenced by command line options such as include and exclude options.

    Given:
        /home
        /home/nate/
        /home/nate/picture.png
        /home/nate/secret/
        /home/nate/secret/recipe.txt
    And Argument: '/home/nate'
    Will yeild:
        picture.png        - FileInfo()
        secret/            - DirInfo()
        secret/recipe.txt  - FileInfo()

    Relative paths will always use a / path separator for convenience

    @param root_path: Path on disk to search under
    @return: Generator of paths relative to root path
    '''
    # Sanity Check
    # TODO: what if directory disappears during scan?  Handle more cleanly?
    if not os.path.exists(root_path):
        raise Exception("Invalid path: " + root_path)
    if os.path.isfile(root_path):
        yield FileInfo(os.path.basename(root_path), root_path)
        return
    if not os.path.isdir(root_path):
        raise Exception("Not a directory: " + root_path)

    # Yield Files and directories for this directory
    for obj_name, rel_path, disk_path, obj_type in _find_file_paths(root_path):
        if obj_type == 'D':
            yield DirInfo(rel_path, disk_path)
        elif obj_type == 'F':
            yield FileInfo(rel_path, disk_path)


def _find_file_paths(root_path, rel_path=None):
    '''Helper for find_files_for_sync which doesn't worry about DiskObjInfo classes'''

    for obj_name in os.listdir(root_path):
        if obj_name not in ['.', '..']:
            disk_path = os.path.join(root_path, obj_name)

            obj_rel_path = None
            if rel_path is None:
                obj_rel_path = obj_name
            else:
                obj_rel_path = rel_path + '/' + obj_name

            if os.path.isfile(disk_path):
                yield obj_name, obj_rel_path, disk_path, 'F'
            elif os.path.isdir(disk_path):
                yield obj_name,  obj_rel_path + '/', disk_path, 'D'
                for sub_obj in _find_file_paths(disk_path, obj_rel_path):
                    yield sub_obj




