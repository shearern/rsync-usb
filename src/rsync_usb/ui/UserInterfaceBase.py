from abc import ABCMeta, abstractmethod

class UserInterfaseBase(object):
    '''Collection of methods for interacting with user'''
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def inform_version(self):
        '''Prompt to display program version at beginning of execution'''


    @abstractmethod
    def abort(self, error_msg):
        '''Warn the user right before aborting execution'''


    @abstractmethod
    def inform(self, msg):
        '''Display a single message to the user (will interrupt progress?)'''


    @abstractmethod
    def usage_error(self, error_msg):
        '''Inform the user when the program was started with invalid arguments'''


