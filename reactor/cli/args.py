# -*- coding: utf-8 -*-
""" reactor.cli.args (boilerplate for click)

    Common CLI arguments for reuse
"""
from __future__ import absolute_import
import os
import click
from functools import partial

optional_topic_name = click.argument(
    'topic_name', nargs=1,
    default=os.environ.get('R_TOPIC', ''))
required_topic_name = click.argument(
    'topic_name', nargs=1, required=True)
required_data = click.argument(
    'data', nargs=1, required=True)
optional_topic_root = click.argument(
    'topic_root', nargs=1,
    default=os.environ.get('R_TOPIC_ROOT', ''))
# namespace = click.argument('namespace', nargs=1)
