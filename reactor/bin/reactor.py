# -*- coding: utf-8 -*-
"""
See the docs here:
  https://github.com/elo-enterprises/aws-secrets
"""

from __future__ import absolute_import

from reactor import (api, cli, util,)

import click
import functools

LOGGER = util.get_logger(__name__)

@click.command(cls=cli.Group)
def entry(*args, **kargs):
    """
    Tool for accessing secrets
    """
    # this could update global settings here
    # ctx = {}
    # ctx['verbose'] = verbose
    # for key, value in config:
    #     ctx[key] = value
    pass

reactor_init_options = [
    cli.options.host,
    cli.options.port,
]

ApiWrapper = functools.partial(
    cli.ApiWrapper, entry=entry,
    )
# topic =ApiWrapper(
#     fxn=api.list,
#     extra_options=[
#         cli.options.env,
#         cli.args.optional_topic_root,
#     ])

list = ApiWrapper(
    fxn=api.list,
    aliases=['ls','topics'],
    extra_options=reactor_init_options+[
        cli.args.optional_topic_root,
    ])
topic = ApiWrapper(
    fxn=api.topic,
    aliases=['t'],
    extra_options=reactor_init_options+[
        cli.args.required_topic_name,
        click.option('--push', default='', help='push message under topic'),
        click.option('--peek', is_flag=True,  default=False, help='peek on this topic'),
        click.option('--pop', is_flag=True,  default=False, help='pop on this topic'),
        click.option('--add', is_flag=True,  default=False, help='add this topic name'),
        click.option('--create', is_flag=True,  default=False, help='add this topic name'),
        click.option('--keys', is_flag=True,  default=False, help='show keys for this topic'),
        click.option('--list', is_flag=True,  default=False, help='show keys for this topic'),
        click.option('--describe', is_flag=True,  help='show status for this topic'),
        click.option('--stat', is_flag=True, help='show status for this topic'),
        click.option('--wipe', is_flag=True, default=False, help='empty topic and destroy it'),
        click.option('--rm', is_flag=True, default=False, help='empty topic and destroy it'),
        click.option('--clean', is_flag=True, default=False, help='empty topic'),
        click.option('--delete', is_flag=True, default=False, help='empty topic'),
        click.option('--ttl', default='3600', help='set topic ttl (used with --add and --create)'),
    ])

shell = ApiWrapper(
    fxn=api.shell,
    aliases=['sh'],
    extra_options=reactor_init_options+[
        # cli.args.topic_name,
    ])

# stat = ApiWrapper(
#     fxn=api.stat,
#     aliases=['get'],
#     extra_options=[
#         cli.args.optional_topic_root,
#     ])

peek = ApiWrapper(
    fxn=api.peek,
    aliases=['get'],
    extra_options=reactor_init_options+[
        cli.args.required_topic_name,
    ])

pop = ApiWrapper(
    fxn=api.pop,
    # aliases=['pop',],
    extra_options=reactor_init_options+[
        cli.args.required_topic_name,
    ])

get = ApiWrapper(
    fxn=api.get,
    # aliases=['pop',],
    extra_options=reactor_init_options+[
        cli.args.required_topic_name,
    ])

push = ApiWrapper(
    fxn=api.push,
    aliases=['put',],
    extra_options=reactor_init_options+[
        cli.args.required_topic_name,
        cli.args.required_data,
    ])

wipe = ApiWrapper(
    fxn=api.wipe,
    aliases=['clean',],
    extra_options=reactor_init_options + [
    ])

watch = ApiWrapper(
    fxn=api.watch,
    # aliases=['',],
    extra_options=reactor_init_options + [
        cli.args.required_topic_name,
    ])
