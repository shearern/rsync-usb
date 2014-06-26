
class ChunkLocation(object):
    '''Location for a piece of data on the source or target system'''

    def __init__(self, path, start_pos, data_len):
        self.__path = path
        self.__start = start_pos
        self.__len = data_len


    @property
    def path(self):
        return self.__path

    @property
    def start_pos(self):
        return self.__start

    @property
    def data_len(self):
        return self.__len

    @property
    def end_pos(self):
        return self.__start + self.__len - 1


    def __eq__(self, other):
        try:
            if self.__path == other.path:
                if self.__start == other.start_pos:
                    if self.__len == other.data_len:
                        return True
        except AttributeError:
            raise NotImplemented()


    def __str__(self):
        return "%s[%d:%d]" % (self.__path, self.__start, self.end_pos + 1)

    def __repr__(self):
        return "ChunkLocation('%s', %d, %d" % (self.__path,
                                               self.__start, self.__len)


    def overlaps(self, pos):
        '''Checks to see if two chunk locations overlap at all'''
        if self.path != pos.path:
            return False
        if self.start_pos < pos.end_pos:
            if self.end_pos > pos.start_pos:
                return True
        return False

