'''Functions to calculate hashes from files'''
from Eric_Prutt_rsync import bytes
import hashlib

def calc_chunk_weak_hash(data):
    '''Given a chunk of data, calculate the weak hash

    TODO: Allow specification of weak hash version?
    Source copied from http://code.activestate.com/recipes/577518-rsync-algorithm/
    '''
    a = b = 0
    l = len(data)
    for i in range(l):
        a += ord(data[i])
        b += (l - i)*ord(data[i])

    return (b << 16) | a


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
