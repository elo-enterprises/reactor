""" reactor.abcs.base
"""
from walrus import Database

from .loggable import Loggable

class NoSuchTopic(ValueError):
    pass

class LoggableDatabase(Database, Loggable):
    """ """
    def __init__(self, *args, **kwargs):
        """ """
        self.init_args = args
        self.init_kwargs = kwargs
        Database.__init__(self, *args, **kwargs)
        Loggable.__init__(self)

    def keys(self):
        """ """
        tmp = [ k.decode('utf8') for k in Database.keys(self) ]
        return [k for k in tmp if not k.startswith('__')]

    def __getitem__(self, name):
        return Database.__getitem__(self, name).decode('utf8')

    def __str__(self):
        """ """
        return "{}[{}]".format(
            self.__class__.__name__,
            getattr(self,'name',''))
    __repr__=__str__
