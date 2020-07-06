#! /usr/bin/env python3
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
        __IPYTHON__ :bool = False

    from tqdm import tqdm # throw ImportError

    class TqdmHandler(logging.StreamHandler):
        r"""tqdm logging stream"""

        def __init__(self,
                     *args, **kwargs):
            super().__init__(*args, **kwargs)

        def emit(self, record,
                 *args, **kwargs):
            try:
                msg = self.format(record, *args, **kwargs)
                tqdm.write(msg, file=self.stream)
            except Exception:
                self.handleError(record)

except ImportError:
    default_stream_handler_cls :logging.StreamHandler = logging.StreamHandler
else:
    default_stream_handler_cls :logging.StreamHandler = TqdmHandler


### colored ###


try:
    from termcolor import colored # throw ImportError
except ImportError:
    ATTRIBUTES :'Mapping[str, int]' = dict(zip(
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
    HIGHLIGHTS :'Mapping[str, int]' = dict(zip(
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
    COLORS     :'Mapping[str, int]' = dict(zip(
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

    COLORED :str = '\033[%dm%s'
    RESET   :str = '\033[0m'

    del ATTRIBUTES['']

    import os

    def colored(text:str,
                *args,
                color:'Optional[str]'=None, on_color:'Optional[str]'=None,
                attrs:'Optional[str]'=None)->str:
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

    PERCENT_STYLE_PATTERN :str = r'%\({}\)[\<\>\=\^]?[\+\- ]?\d*\.?\d*\w'

    NAME_COLOR     :str                 = 'white'
    PATH_COLOR     :str                 = 'white'
    TIME_COLOR     :str                 = 'cyan'
    PROCESS_COLOR  :str                 = 'magenta'
    LEVEL_COLOR    :'Mapping[str, str]' = {
            'CRITICAL': 'white',
            'ERROR': 'white',
            'WARNING': 'yellow',
            'INFO' : 'green',
            'DEBUG': 'blue',
            'NOTSET': 'magenta',
            }
    LEVEL_ON_COLOR :'Mapping[str, str]' = {
            'CRITICAL': 'on_red',
            'ERROR': 'on_red',
            }

    BLINK_LEVELS :'Collection[str]' = {'CRITICAL', 'WARNING'}

    import re

    color_level     :bool
    blink_bad_level :bool

    @classmethod
    def colored_fmt(cls, fmt:str, key:str,
                    **kwargs)->str:
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
                 fmt:'Optional[str]'=None, datefmt:'Optional[str]'=None,
                 *args,
                 color:bool=True,
                 color_name:bool=True, color_level:bool=True, color_path:bool=True,
                 color_time:bool=True, color_process:bool=True,
                 bold:bool=True,
                 bold_name:bool=True, bold_level:bool=True, bold_message:bool=True,
                 underline:bool=True,
                 underline_path:bool=True, underline_time:bool=False,
                 blink:bool=True,
                 blink_bad_level:bool=True,
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

        super().__init__(fmt=fmt, datefmt=datefmt, **kwargs)

        # internal API check
        if hasattr(self, '_style'):
            assert hasattr(self._style, '_fmt'), (
                    f'unsupported logging version({logging.__version__})'
                    ) # python3 API: logging 0.5
            assert isinstance(self._style, logging.PercentStyle), (
                    f"only percent style format supported, but got '{type(self._style)}'")
        else:
            assert hasattr(self, '_fmt'), (
                    f'unsupported logging version({logging.__version__})'
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
        msg = super().format(record, *args, **kwargs)
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
        'style': '%',
        }


def basicConfig(
        format:'Optional[str]'=None, datefmt:'Optional[str]'=None, level:'Optional[int]'=None,
        stream:'Optional[io.TextIOBase]'=None, streamLevel:'Optional[int]'=None,
        filename:'Optional[int]'=None, fileLevel:'Optional[int]'=None,
        filemode:str='a', encoding:'Optional[str]'=None,
        backupCount:int=0, maxBytes:int=0, when:str='h',
        **kwargs):
    r"""'logging.basicConfig' override"""

    style = kwargs.get('style')

    if format:
        config['format'] = format
    if datefmt:
        config['datefmt'] = datefmt
    if style:
        config['style'] = style

    if 'handlers' in kwargs:
        return logging.basicConfig(format=format, datefmt=datefmt, level=level, **kwargs)

    has_lock_api = hasattr(logging, '_acquireLock') and hasattr(logging, '_releaseLock')
    has_lock_api and logging._acquireLock()
    try:
        if len(logging.root.handlers) == 0:
            style = config['style']
            if stream or (filename is None):
                handler = default_stream_handler_cls()
                handler.setFormatter((ColoredFormatter if style == '%' else logging.Formatter)(
                        fmt=config['format'], datefmt=config['datefmt'], style=style))
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
                        fmt=config['format'], datefmt=config['datefmt'], style=style))
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
    for idx in tqdm(range(9)):
        logger.critical('critical')
        logger.fatal('fatal')
        logger.error('error')
        logger.warning('warning')
        logger.info('info')
        logger.debug('debug')
