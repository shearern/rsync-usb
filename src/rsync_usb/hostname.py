import socket

def get_hostname():
    '''Get a hostname to use for this host'''
    try:
        return socket.gethostname()
    except:
        return "UNKNOWN"