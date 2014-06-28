'''Actions that can be used to change files on target to match source'''
from abc import ABCMeta, abstractmethod

class SyncAction(object):
    '''An action to be taken on the target system

    Each action is to make the target files more like those on the target
    system.
    '''
    __metaclass__= ABCMeta

    def __init__(self):
        # Conflicting actions record when performing this action prevents
        # the successful completion of these actions
        self.conflicts_with = set()

        # Effectively the reverse of the conflicts_with set.  The referenced
        # actions must be completed before completing this action
        self.perform_before = set()

        # Flag for marking "visited" actions when resolving dependency graphs
        # in order to prevent circular reference loops
        self.queued_in_plan = False

    @property
    def action_code(self):
        return self._get_action_code()

    @abstractmethod
    def _get_action_code(self):
        '''Code to uniquely identify this action type'''


class CopyFromTargetSystem(SyncAction):
    '''Copy data already on the target system'''

    def __get_action_code(self):
        return 'C'


class PreserveTargetData(SyncAction):
    '''Copy data already on the target system to a temporary location

    This action must be referenced by a future WritePreservedTargetData to
    actually place the data in the desired location.  These actions are used
    to work around dependency cycles.
    '''

    def __get_action_code(self):
        return 'P'


class WritePreservedTargetData(SyncAction):
    '''Write data previously preserved by a PreserveTargetData'''

    def __get_action_code(self):
        return 'W'


class RawData(SyncAction):
    '''Includes data to write in sync plan'''

    def __get_action_code(self):
        return 'D'


class FileComplete(SyncAction):
    '''Indicate that a file has been synchronized'''

    def __get_action_code(self):
        return 'Z'


