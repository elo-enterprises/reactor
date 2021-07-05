""" reactor.abcs.reactor
"""

from .topic import Topic
from .base import LoggableDatabase

class Reactor(LoggableDatabase):
    """ """

    def sub(self, i):
        """ """
        tmp = self.init_kwargs.copy()
        tmp['db'] = i
        return Topic(*self.init_args, **tmp)

    def create_topic(self, topic_name):
        """ """
        self.logger.debug("Creating topic `{}`".format(topic_name))
        sub = self.sub(self.next_topic_index)
        sub['__name__'] = topic_name
        return sub

    @property
    def next_topic_index(self):
        """ """
        return max(self.topics_by_index.keys(), default=0) + 1

    @property
    def topics_by_name(self):
        """ returns {topic_name: db_index} """
        topics = self.topics_by_index.items()
        topics = [reversed(x) for x in topics]
        topics = dict(topics)
        return topics

    @property
    def topics(self):
        return self.list_topics()

    @property
    def topics_by_index(self):
        """ returns {db_index: topic_name} """
        kspaces = self.info('keyspace').keys()
        kspaces = [int(x.replace('db', '')) for x in kspaces]
        # self.logger.debug("found keyspaces: {}".format(kspaces))
        tmp = []
        for i in kspaces:
            sub = self.sub(i)
            try:
                sub_name = sub['__name__']
            except KeyError:
                msg = "db@{} doesn't have `__name__` key.  is it it managed by reactor?"
                self.logger.warning(msg.format(i))
                continue
            else:
                if sub_name:
                    tmp += [[i, sub_name]]
        tmp = [x for x in tmp if x[1] ]
        tmp = dict(tmp)
        return tmp

    def list_topics(self):
        return list(self.topics_by_name.keys())

    def get_topic(self, topic_name, strict=False):
        """ """
        topics = self.topics_by_name
        if topic_name not in topics:
            if not strict:
                msg = "topic `{}` does not exist in {}, creating it.."
                self.logger.warning(msg.format(topic_name, topics.keys()))
                return self.create_topic(topic_name)
            else:
                raise NoSuchTopic(topic_name)
        return self.sub(topics[topic_name])
