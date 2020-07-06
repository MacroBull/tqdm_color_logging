#! /usr/bin/env python2
# -*- coding: utf-8 -*-
r"""
Created on Fri Jan  4 14:07:51 2019

@author: Macrobull
"""

from __future__ import absolute_import, division, unicode_literals

import logging


### TqdmHandler ###


try:
    try:
        __IPYTHON__ # throw NameError
    except NameError:
        __IPYTHON__ = False

    from tqdm import tqdm # throw ImportError

    class TqdmHandler(logging.StreamHandler):
        r"""tqdm logging stream"""

        def __init__(self,
                     *args, **kwargs):
            super(TqdmHandler, self).__init__(*args, **kwargs)

        def emit(self, record,
                 *args, **kwargs):
            try:
                msg = self.format(record, *args, **kwargs)
                tqdm.write(msg, file=self.stream)
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                self.handleError(record)

except ImportError:
    default_stream_handler_cls = logging.StreamHandler
else:
    default_stream_handler_cls = TqdmHandler


### colored ###


try:
    from termcolor import colored # throw ImportError
except ImportError:
    ATTRIBUTES = dict(zip(
            (
                'bold',
                'dark',
                '',
                'underline',
                'blink',
                '',
                'reverse',
                'concealed',
            ), range(1, 9)
            ))
    HIGHLIGHTS = dict(zip(
            (
                'on_grey',
                'on_red',
                'on_green',
                'on_yellow',
                'on_blue',
                'on_magenta',
                'on_cyan',
                'on_white',
            ), range(40, 48)
            ))
    COLORS     = dict(zip(
            (
                'grey',
                'red',
                'green',
                'yellow',
                'blue',
                'magenta',
                'cyan',
                'white',
            ), range(30, 38)
            ))

    COLORED = '\033[%dm%s'
    RESET   = '\033[0m'

    del ATTRIBUTES['']

    import os

    def colored(text,
                # *args,
                color=None, on_color=None,
                attrs=None): # ->str:
        r"""colorize text(copied from termcolor)"""

        if not os.getenv('ANSI_COLORS_DISABLED'):
            reset = False
            if color is not None:
                text = COLORED % (COLORS[color], text)
                reset = True

            if on_color is not None:
                text = COLORED % (HIGHLIGHTS[on_color], text)
                reset = True

            if attrs:
                for attr in attrs:
                    text = COLORED % (ATTRIBUTES[attr], text)
                reset = True

            if reset:
                text += RESET
        return text


### ColoredFormatter ###


class ColoredFormatter(logging.Formatter):
    r"""ColoredFormatter"""

    PERCENT_STYLE_PATTERN = r'%\({}\)[\<\>\=\^]?[\+\- ]?\d*\.?\d*\w'

    NAME_COLOR     = 'white'
    PATH_COLOR     = 'white'
    TIME_COLOR     = 'cyan'
    PROCESS_COLOR  = 'magenta'
    LEVEL_COLOR    = {
            'CRITICAL': 'white',
            'ERROR': 'white',
            'WARNING': 'yellow',
            'INFO' : 'green',
            'DEBUG': 'blue',
            'NOTSET': 'magenta',
            }
    LEVEL_ON_COLOR = {
            'CRITICAL': 'on_red',
            'ERROR': 'on_red',
            }

    BLINK_LEVELS = {'CRITICAL', 'WARNING'}

    import re

    @classmethod
    def colored_fmt(cls, fmt, key,
                    **kwargs): # ->str:
        r"""format with color"""

        res = []
        pos = 0
        for match in cls.re.finditer(cls.PERCENT_STYLE_PATTERN.format(key), fmt):
            res.append(fmt[pos:match.start()])
            res.append(colored(match.group(), **kwargs))
            pos = match.end()
        res.append(fmt[pos:])
        return ''.join(res)

    def __init__(self,
                 fmt=None, datefmt=None,
                 # *args,
                 color=True,
                 color_name=True, color_level=True, color_path=True,
                 color_time=True, color_process=True,
                 bold=True,
                 bold_name=True, bold_level=True, bold_message=True,
                 underline=True,
                 underline_path=True, underline_time=False,
                 blink=True,
                 blink_bad_level=True,
                 **kwargs):

        if fmt is not None:
            # name
            color_, on_color, attrs = None, None, set()
            if color and color_name:
                color_ = self.NAME_COLOR
            if bold and bold_name:
                attrs.add('bold')
            fmt = self.colored_fmt(fmt, 'name', color=color_, on_color=on_color, attrs=attrs)

            # levelno

            # levelname
            color_, on_color, attrs = None, None, set()
            if bold and bold_level:
                attrs.add('bold')
            fmt = self.colored_fmt(
                    fmt, 'levelname', color=color_, on_color=on_color, attrs=attrs)

            # pathname
            color_, on_color, attrs = None, None, set()
            if color and color_path:
                color_ = self.PATH_COLOR
            if underline and underline_path:
                attrs.add('underline')
            fmt = self.colored_fmt(
                    fmt, 'pathname', color=color_, on_color=on_color, attrs=attrs)

            # filename
            color_, on_color, attrs = None, None, set()
            if color and color_path:
                color_ = self.PATH_COLOR
            if underline and underline_path:
                attrs.add('underline')
            fmt = self.colored_fmt(
                    fmt, 'filename', color=color_, on_color=on_color, attrs=attrs)

            # module

            # lineno
            color_, on_color, attrs = None, None, set()
            if color and color_path:
                color_ = self.PATH_COLOR
            if underline and underline_path:
                attrs.add('underline')
            fmt = self.colored_fmt(fmt, 'lineno', color=color_, on_color=on_color, attrs=attrs)

            # funcName
            color_, on_color, attrs = None, None, set()
            if color and color_name:
                color_ = self.NAME_COLOR
            if bold and bold_name:
                attrs.add('bold')
            fmt = self.colored_fmt(
                    fmt, 'funcName', color=color_, on_color=on_color, attrs=attrs)

            # created
            color_, on_color, attrs = None, None, set()
            if color and color_time:
                color_ = self.TIME_COLOR
            if underline and underline_time:
                attrs.add('underline')
            fmt = self.colored_fmt(fmt, 'created', color=color_, on_color=on_color, attrs=attrs)

            # asctime
            color_, on_color, attrs = None, None, set()
            if color and color_time:
                color_ = self.TIME_COLOR
            if underline and underline_time:
                attrs.add('underline')
            fmt = self.colored_fmt(fmt, 'asctime', color=color_, on_color=on_color, attrs=attrs)

            # msecs
            color_, on_color, attrs = None, None, set()
            if color and color_time:
                color_ = self.TIME_COLOR
            if underline and underline_time:
                attrs.add('underline')
            fmt = self.colored_fmt(fmt, 'msecs', color=color_, on_color=on_color, attrs=attrs)

            # relativeCreated
            color_, on_color, attrs = None, None, set()
            if color and color_time:
                color_ = self.TIME_COLOR
            if underline and underline_time:
                attrs.add('underline')
            fmt = self.colored_fmt(
                    fmt, 'relativeCreated', color=color_, on_color=on_color, attrs=attrs)

            # thread

            # threadName

            # process
            color_, on_color, attrs = None, None, set()
            if color and color_process:
                color_ = self.PROCESS_COLOR
            fmt = self.colored_fmt(fmt, 'process', color=color_, on_color=on_color, attrs=attrs)

            # message
            color_, on_color, attrs = None, None, set()
            if bold and bold_message:
                attrs.add('bold')
            fmt = self.colored_fmt(fmt, 'message', color=color_, on_color=on_color, attrs=attrs)

        super(ColoredFormatter, self).__init__(fmt=fmt, datefmt=datefmt, **kwargs)

        # internal API check
        if hasattr(self, '_style'):
            assert hasattr(self._style, '_fmt'), (
                    'unsupported logging version(%s)' % (logging.__version__, )
                    ) # python3 API: logging 0.5
        else:
            assert hasattr(self, '_fmt'), (
                    'unsupported logging version(%s)' % (logging.__version__, )
                    ) # python2 API: logging 0.5

        self.color_level = color and color_level
        self.blink_bad_level = blink and blink_bad_level

    def format(self, record,
               *args, **kwargs):
        fmt = orig_fmt = self._fmt

        # levelname
        color, on_color, attrs = None, None, set()
        levelname = record.levelname
        if self.color_level:
            color = self.LEVEL_COLOR.get(levelname, color)
            on_color = self.LEVEL_ON_COLOR.get(levelname, on_color)
        if self.blink_bad_level:
            if levelname in self.BLINK_LEVELS:
                attrs.add('blink')
        fmt = self.colored_fmt(fmt, 'levelname', color=color, on_color=on_color, attrs=attrs)

        # apply format
        if hasattr(self, '_style'):
            self._style._fmt = fmt # python3 API: logging 0.5
        else:
            self._fmt = fmt # python2 API: logging 0.5
        msg = super(ColoredFormatter, self).format(record, *args, **kwargs)
        if hasattr(self, '_style'):
            self._style._fmt = orig_fmt # python3 API: logging 0.5
        else:
            self._fmt = orig_fmt # python2 API: logging 0.5

        return msg


### ColoredLogger ###


# detail time: (%(asctime)s.%(msecs)03d)
config = {
        'format': '[%(levelname)8s](%(asctime)8s)<%(process)5d> '
            '%(name)s::%(funcName)s @ %(filename)s:%(lineno)d: %(message)s',
        'datefmt': '%H:%M:%S',
        }


def basicConfig(
        format=None, datefmt=None, level=None,
        stream=None, streamLevel=None, filename=None, fileLevel=None,
        filemode='a', encoding=None, backupCount=0, maxBytes=0, when='h',
        **kwargs):
    r"""'logging.basicConfig' override"""

    if format:
        config['format'] = format
    if datefmt:
        config['datefmt'] = datefmt

    if 'handlers' in kwargs:
        return logging.basicConfig(format=format, datefmt=datefmt, level=level, **kwargs)

    has_lock_api = hasattr(logging, '_acquireLock') and hasattr(logging, '_releaseLock')
    has_lock_api and logging._acquireLock()
    try:
        if len(logging.root.handlers) == 0:
            if stream or (filename is None):
                handler = default_stream_handler_cls()
                handler.setFormatter(ColoredFormatter(
                        fmt=config['format'], datefmt=config['datefmt']))
                if streamLevel is not None:
                    level = min(level or streamLevel, streamLevel)
                    handler.setLevel(streamLevel)
                logging.root.addHandler(handler)
            if filename:
                if backupCount > 0:
                    if maxBytes > 0:
                        handler = logging.handlers.RotatingFileHandler(
                            filename,
                            mode=filemode, maxBytes=maxBytes, backupCount=backupCount,
                            encoding=encoding)
                    else:
                        handler = logging.handlers.TimedRotatingFileHandler(
                            filename,
                            when=when, backupCount=backupCount, encoding=encoding)
                else:
                    handler = logging.FileHandler(filename, mode=filemode, encoding=encoding)
                handler.setFormatter(logging.Formatter(
                        fmt=config['format'], datefmt=config['datefmt']))
                if fileLevel is not None:
                    level = min(level or fileLevel, fileLevel)
                    handler.setLevel(fileLevel)
                logging.root.addHandler(handler)
            if level is not None:
                logging.root.setLevel(level)
    finally:
        has_lock_api and logging._releaseLock()


if __name__ == '__main__':
    logger = logging.getLogger('sample1')
    logger.setLevel(logging.DEBUG)
    logger.critical('critical')
    logger.fatal('fatal')
    logger.error('error')
    logger.warning('warning')
    logger.info('info')
    logger.debug('debug')

    import sys

    FORMAT = '[%(levelname)8s]%(name)s: %(message)s'
    basicConfig(format=FORMAT, level=logging.DEBUG, stream=sys.stderr, filename='/tmp/test.log')

    from tqdm import tqdm

    logger = logging.getLogger('sample2')
    for idx in tqdm(range(9), write_bytes=False):
        logger.critical('critical')
        logger.fatal('fatal')
        logger.error('error')
        logger.warning('warning')
        logger.info('info')
        logger.debug('debug')
