""" reactor.abcs.topic
"""

from .base import LoggableDatabase

class Topic(LoggableDatabase):
    """ """

    def push(self, data):
        """
            if expire:
                db.expire(topic_name)
        """
        id = str(datetime.now().timestamp())
        self[id] = data
        return dict(id=id, data=data)

    @property
    def name(self):
        """ """
        tmp = getattr(self, '_topic_name', None)
        if tmp is None:
            tmp = self._topic_name = self['__name__']
            Loggable.__init__(self, name=tmp)
        return tmp

    @property
    def messages(self):
        return self.list_messages()

    def list_messages(self):
        """ """
        return [x for x in self.keys() if not x.startswith('__')]


    def clean(self):
        """ """
        raise RuntimeError('niy')

    def stat(self):
        """ """
        keys = self.keys()
        return dict(
            _metadata=dict(
                name=self.name,
                length=len(keys),
            data=keys))
