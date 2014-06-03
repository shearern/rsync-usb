from cPickle import Unpickler

class SaferUnpickler(Unpickler):
    def __init__(self):
        self.find_global = None