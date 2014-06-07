
class TargetChunkIndexBase(object):
    '''Based class for implementations of indexing target chunk hashes

    This is basically an interface specification for different implementations
    of an index of the hashes of chunks of files on the target system.  It is
    expected that large file sets will want to use a different indexing method
    (maybe a sqlite database) than smaller data sets.  This class is used, then,
    to have well defined queires that will be run against the index.

    These indexes will be optimized for finding chunks already on the target
    system that may be utilized to avoid placing the data in the sync plan.
    See the rsync protocol papers.
    '''

