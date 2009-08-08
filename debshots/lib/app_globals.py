"""The application's Globals object"""
import threading
import memcache
thread_local = threading.local()

from pylons import config

class Globals(object):
    """Globals acts as a container for objects available throughout the
    life of the application
    """

    @property
    def cache(self):
        try:
            return thread_local.cache
        except AttributeError:
            thread_local.cache = memcache.Client([config['debshots.memcache_server']])
            return thread_local.cache

    def __init__(self):
        """One instance of Globals is created during application
        initialization and is available during requests via the
        'app_globals' variable
        """
        pass

