# -*- coding: utf-8 -*-
""" reactor.api

See the docs here:
  https://github.com/elo-enterprises/reactor
"""
from __future__ import absolute_import

import os
import io
import sys
import json
import yaml
import functools

from walrus import Database

from reactor import (abcs, util, )

LOGGER = util.get_logger(__name__)

def returns_json(fxn):
    """ """
    def wrapper(*args, **kargs):
        result = fxn(*args, **kargs)
        return json.loads(json.dumps(result))
    wrapper.__name__=fxn.__name__
    wrapper.__doc__ = fxn.__doc__
    return wrapper

def get_reactor(**kwargs):
    """ """
    LOGGER.debug("{}".format(kwargs))
    return abcs.Reactor(
        host=kwargs['host'],
        port=kwargs['port'],
        db=0)

def shell(topic_name='/', **kwargs):
    """drops to interactive shell for debugging """
    reactor = get_reactor(**kwargs)
    import IPython; IPython.embed()
    return {}

# @returns_json
def push(topic_name='', data=None, expire=None, **kwargs):
    """ pushes data to given topic """
    assert topic_name and data
    reactor = get_reactor(**kwargs)
    topic = reactor.get_topic(topic_name)
    result = topic.push(data)
    return result

# @returns_json
def pop(topic_name='', **kwargs):
    """ pops data off of the given topic """
    assert topic_name
    reactor = get_reactor(**kwargs)
    topic = reactor.get_topic(topic_name)
    choice = sorted(topic.keys())[0]
    result = topic.get(choice)
    topic.delete(choice)
    return result.decode('utf8')

def topic(topic_name, **kwargs):
    """ actions on a topic """
    reactor = get_reactor(**kwargs)
    reactor.logger.debug('api.topic: {}'.format(kwargs))
    # NB: lots of action aliases here but these actions might diverge later
    add = kwargs.pop('add')
    clean = kwargs.pop('clean') or kwargs.pop('wipe') or kwargs.pop('rm') or kwargs.pop('delete')
    stat = kwargs.pop('list') or kwargs.pop('stat') or kwargs.pop('describe')
    _push = kwargs.pop('push')
    _peek = kwargs.pop('peek')
    _pop = kwargs.pop('pop')
    # set a default action
    # if not any([add, stat, clean, _push]): stat = True
    if add:
        reactor.logger.debug("adding requested topic `{}`".format(topic_name))
        if add in reactor.topics_by_name:
            msg='topic `{}` already exists at index {}'
            reactor.logger.debug(msg.format(add, reactor.topics_by_name[topic_name]))
            return None
        reactor.create_topic(topic_name)
        return True
    else:
        topic = reactor.get_topic(topic_name)
        if _push: return push(topic_name, data=_push)
        elif _peek: return peek(topic_name)
        if _pop: return pop(topic_name)
        elif stat: return topic.stat()
        elif clean:
            return topic.clean()
        else:
            raise ValueError('undefined behaviour')


def peek(topic_name='', **kwargs):
    """ runs peek instruction for given topic """
    assert topic_name
    reactor = get_reactor(**kwargs)
    topic = reactor.get_topic(topic_name, strict=True)
    return topic.list_messages()
get = peek
read = peek

def list(topic_root='', **kwargs):
    """ list topics below the given path """
    reactor = get_reactor(**kwargs)
    return [x for x in reactor.topics if x.startswith(topic_root)]

def tree(topic_root, **kwargs):
    """ """
    return list

def wipe(**kwargs):
    """ wipes out the entire reactor (careful!) """
    reactor = get_reactor(**kwargs)
    return reactor.flushall()

import time
def watch(topic_name, **kwargs):
    """ watch the given topic for all changes (uses `peek`, not `pop`) """
    reactor = get_reactor(**kwargs)
    topic = reactor.get_topic(topic_name, strict=True)
    topic.logger.debug("watching topic: {}".format(topic_name))
    while True:
        msg_ids = topic.list_messages()
        for mid in msg_ids:
            msg = topic[mid]
            reactor.logger.debug("{}: {}".format(mid, msg))
        time.sleep(1)

def subscribe(**kwargs):
    """ NIY """
    reactor = get_reactor(**kwargs)
    return None
