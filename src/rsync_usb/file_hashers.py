'''Functions to calculate hashes from files'''
import hashlib


class RollingHashValue(object):

    HALF_SIZE = pow(2, 16)

    def __init__(self):
        self.__a = None
        self.__b = None

        self.data_len = None
        self.first_data = None      # First byte of data hashed
        self.second_data = None


    def get_a(self):
        return self.__a
    def set_a(self, v):
        v = v % self.HALF_SIZE
        self.__a = v
    a = property(get_a, set_a)


    def get_b(self):
        return self.__b
    def set_b(self, v):
        v = v % self.HALF_SIZE
        self.__b = v
    b = property(get_b, set_b)


    @property
    def value(self):
        return (self.__b << 16) | self.__a



def calc_chunk_rolling_weak_hash(data, block_size, prev_hash=None):
    '''Given a chunk of data, calculate the weak hash in a rolling fassion

    This method assumes that either prev_hash is None, or the data is the same
    data provided on the previous execution minus the first character and with
    one or zero more characters added to the end.

    Source copied from https://docs.python.org/2/library/hashlib.html#module-hashlib
    and modified.

    @param data: Data to be hashed
    @param prev_hash: Hash created from previous run
    @param block_size: Block size being used
    @return RollingHashValue
    '''
    # Init return data
    rtn = RollingHashValue()
    rtn.data_len = len(data)
    if rtn.data_len == 0:
        raise Exception("Can't hash empty data array")
    rtn.first_data = data[0]
    if rtn.data_len > 1:
        rtn.second_data = data[1]

    # Perform first hash
    if prev_hash is None:
        a = 0
        b = 0

        for i in range(rtn.data_len):
            a += ord(data[i])
            b += (rtn.data_len - i)*ord(data[i])

        rtn.a = a
        rtn.b = b

    # Perform update hash
    else:
        if prev_hash.second_data is None:
            raise Exception("Previous data didn't have more data to hash...")
        if prev_hash.second_data != rtn.first_data:
            msg = "New data doesn't appear to be one byte shifted from prev data"
            raise Exception(msg)

        removed = ord(prev_hash.first_data)
        new = ord(data[-1])

        # s(k+1, m+1)
        if prev_hash.data_len == rtn.data_len:
            rtn.a = prev_hash.a - removed + new
            rtn.b = prev_hash.b - (prev_hash.data_len*removed) + rtn.a

        # s(k+1, m)
        elif prev_hash.data_len - 1 == rtn.data_len:
            new = None
            rtn.a = prev_hash.a - removed
            rtn.b = prev_hash.b - (prev_hash.data_len*removed)

        else:
            msg = "Previous block %d bytes, this block %d bytes"
            raise Exception(msg % (prev_hash._data_len, rtn._data_len))


    return rtn


def calc_chunk_weak_hash(data):
    '''Given a chunk of data, calculate the weak hash

    TODO: Allow specification of weak hash version?
    Source copied from http://code.activestate.com/recipes/577518-rsync-algorithm/
    '''
#    a = b = 0
#    l = len(data)
#    for i in range(l):
#        a += ord(data[i])
#        b += (l - i)*ord(data[i])
#
#    return (b << 16) | a
    return calc_chunk_rolling_weak_hash(data, len(data)).value


def calc_chunk_strong_hash(data):
    '''Given a chunk of data, calculate the strong hash

    TODO: Allow specification of strong hash type?
    Source copied from https://docs.python.org/2/library/hashlib.html#module-hashlib
    '''
    m = hashlib.md5()
    m.update(data)
    return m.digest()


def get_contig_chunk_hashes(path, block_size):
    '''Get the hashes for contiguous blocks in a file

    This function is used to calculate the weak and strong hash for every
    contiguous chunk of data in the file with size block_size (the last chunk
    may be smaller).  This method is derived from Eric Prutt's example code,
    (Source copied from http://code.activestate.com/recipes/577518-rsync-algorithm/)
    but modified to yield hashes iterativly.

    bs = 10 will return 3 hash pairs for a 15 byte file
    ----------|----------|-----

    TODO: Not Python 3 compatible?  bytes

    @param path: Path to file on disk to hash
    @param block_size: Will hash chunks of this size out of the file
    @return: generator of (weak_hash, strong_hash, chunk_size)
    '''
    with open(path, 'rb') as fh:
        data = fh.read(block_size)
        while data:
            weak_hash = calc_chunk_weak_hash(data)
            strong_hash = calc_chunk_strong_hash(data)
            yield weak_hash, strong_hash, len(data)

            data = fh.read(block_size)
