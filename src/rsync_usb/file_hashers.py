'''Functions to calculate hashes from files'''
import hashlib


class RollingHashValue(object):
    def __init__(self):
        self.value = None

        self._a = None
        self._b = None
        self._first = None      # First byte of data hashed
        self._second = None
        self._data_len = None


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
    rtn._data_len = len(data)
    if rtn._data_len == 0:
        raise Exception("Can't hash empty data array")
    rtn._first = data[0]
    if rtn._data_len > 1:
        rtn._second = data[1]

    # Perform first hash
    if prev_hash is None:
        rtn._a = 0
        rtn._b = 0

        for i in range(rtn._data_len):
            rtn._a += ord(data[i])
            rtn._b += (rtn._data_len - i)*ord(data[i])

        rtn.value = (rtn._b << 16) | rtn._a

    # Perform update hash
    else:
        if prev_hash._second is None:
            raise Exception("Previous data didn't have more data to hash...")
        if prev_hash._second != rtn._first:
            msg = "New data doesn't appear to be one byte shifted from prev data"
            raise Exception(msg)

        removed = ord(prev_hash._first)
        new = ord(data[-1])

        if prev_hash._data_len == rtn._data_len:
            rtn._a = prev_hash._a - removed - new
            rtn._b = prev_hash._b - (removed * block_size - rtn._a)
            rtn.value = (rtn._b << 16) | rtn._a
        elif prev_hash._data_len - 1 == rtn._data_len:
            raise NotImplementedError()
            new = None
            rtn._a = prev_hash._a - removed
            rtn._b = prev_hash._b - (removed * block_size - rtn._a)
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
