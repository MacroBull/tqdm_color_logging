#! /usr/bin/env python2
# -*- coding: utf-8 -*-
r"""
Created on Fri Jan  4 14:07:51 2019

@author: Macrobull
"""

from __future__ import absolute_import, division, unicode_literals

import logging, re


try:
   try:
       __IPYTHON__
   except NameError:
       __IPYTHON__ = False

   class TqdmHandler(logging.StreamHandler):
       r"""tqdm logging stream"""

       from sys import stderr

       from tqdm import tqdm

       def __init__(self,
                    *args, **kwargs):
           super(TqdmHandler, self).__init__(*args, **kwargs)

       def emit(self, record,
                *args, **kwargs):
           msg = self.format(record, *args, **kwargs)
           self.tqdm.write(msg, file=self.stderr) # output to stderr

   default_handler_cls = TqdmHandler
except ImportError:
   default_handler_cls = logging.StreamHandler


try:
   from termcolor import colored
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
   COLORS = dict(zip(
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
   RESET = '\033[0m'

   del ATTRIBUTES['']

   import os

   def colored(text,
               # *args, # py3
               color=None, on_color=None,
               attrs=None): # ->str:
       r"""colorize text(copied from termcolor)"""

       if not os.getenv('ANSI_COLORS_DISABLED'):
           fmt_str = '\033[%dm%s'
           reset = False
           if color is not None:
               text = fmt_str % (COLORS[color], text)
               reset = True

           if on_color is not None:
               text = fmt_str % (HIGHLIGHTS[on_color], text)
               reset = True

           if attrs is not None:
               for attr in attrs:
                   text = fmt_str % (ATTRIBUTES[attr], text)
                   reset = True

           if reset:
               text += RESET
       return text


class ColoredFormatter(logging.Formatter):
   r"""ColoredFormatter"""

   PERCENT_STYLE_PATTERN = r'%\({}\)[\<\>\=\^]?[\+\- ]?\d*\.?\d*\w'
   TIME_COLOR = 'cyan'
   LEVEL_COLOR = {
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
   BLINK_LEVELS = ['CRITICAL', 'WARNING']

   @classmethod
   def colored_fmt(
           cls, fmt, key,
           **kwargs): # ->str:
       r"""format with color"""

       ret = ''
       pos = 0
       for match in re.finditer(cls.PERCENT_STYLE_PATTERN.format(key), fmt):
           ret += fmt[pos:match.start()]
           ret += colored(match.group(), **kwargs)
           pos = match.end()
       ret += fmt[pos:]
       return ret

   def __init__(self,
                fmt=None, datefmt=None,
                # *args, # py3
                color=True, color_level=True, color_time=True,
                bold=True, bold_name=True,
                bold_level=True, bold_message=True,
                underline=True, underline_time=False, underline_path=True,
                blink=True, blink_bad_level=True,
                **kwargs):

       if isinstance(fmt, basestring):
           # name
           color_, on_color, attrs = None, None, set()
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
           if underline and underline_path:
               attrs.add('underline')
           fmt = self.colored_fmt(
                   fmt, 'pathname', color=color_, on_color=on_color, attrs=attrs)

           # filename
           color_, on_color, attrs = None, None, set()
           if underline and underline_path:
               attrs.add('underline')
           fmt = self.colored_fmt(
                   fmt, 'filename', color=color_, on_color=on_color, attrs=attrs)

           # module

           #
           color_, on_color, attrs = None, None, set()
           if underline and underline_path:
               attrs.add('underline')
           fmt = self.colored_fmt(fmt, 'lineno', color=color_, on_color=on_color, attrs=attrs)

           # funcName

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

           # message
           color_, on_color, attrs = None, None, set()
           if bold and bold_message:
               attrs.add('bold')
           fmt = self.colored_fmt(fmt, 'message', color=color_, on_color=on_color, attrs=attrs)

       super(ColoredFormatter, self).__init__(fmt=fmt, datefmt=datefmt, **kwargs)

       # internal API check
       if hasattr(self, '_style'):
           assert kwargs.get('style', '%') == '%' and hasattr(self._style, '_fmt'), (
                   'unsupported logging version: %s' % (logging.__version__, )
                   ) # python3 API: logging 0.5
       else:
           assert hasattr(self, '_fmt'), (
                   'unsupported logging version: %s' % (logging.__version__, )
                   ) # python2 API: logging 0.5

       self.color_level = color and color_level
       self.blink_bad_level = blink and blink_bad_level

   def format(self, record,
              *args, **kwargs):
       fmt = orig_fmt = self._fmt

       # levelname
       color = None
       on_color = None
       attrs = set()
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


# (%(asctime)s.%(msecs)03d)
config = {
        'format': '[%(levelname)8s](%(asctime)8s)'
            '%(name)s::%(funcName)s:%(lineno)4d: %(message)s',
        'datefmt': '%H:%M:%S',
}


def basicConfig(*args, **kwargs):
   r"""'logging.basicConfig' override"""

   config['format'] = kwargs.get('format', config['format'])
   config['datefmt'] = kwargs.get('datefmt', config['datefmt'])
   logging.basicConfig(*args, **kwargs)


class ColoredLogger(logging.Logger):
   r"""custom 'logger' class with multiple destinations and tqdm + colored support"""

   _global_handler_infos = [] # shared instances

   @classmethod
   def add_global_handler(
           cls, handler,
           share_formatter=False):
       cls._global_handler_infos.append((handler, share_formatter))

   def __init__(self,
                *args, **kwargs):
       super(ColoredLogger, self).__init__(*args, **kwargs)
       self.propagate = False
       formatter = ColoredFormatter(fmt=config['format'], datefmt=config['datefmt'])

       for handler, share_formatter in self._global_handler_infos:
           if share_formatter:
               handler.setFormatter(formatter) # shared formatter
           self.addHandler(handler)

       handler = default_handler_cls()
       handler.setFormatter(formatter)
       self.addHandler(handler)


# override default loggig logger class
logging.setLoggerClass(ColoredLogger)


if __name__ == '__main__':
   logger = logging.getLogger("sample1")
   logger.setLevel(logging.DEBUG)
   logger.critical('critical')
   logger.fatal('fatal')
   logger.error('error')
   logger.warning('warning')
   logger.info('info')
   logger.debug('debug')

   FORMAT = '[%(levelname)8s]%(name)s: %(message)s'
   basicConfig(format=FORMAT, level=logging.DEBUG)

   ColoredLogger.add_global_handler(logging.FileHandler('/tmp/test.log'), share_formatter=True)

   logger = logging.getLogger('sample2')
   logger.critical('critical')
   logger.fatal('fatal')
   logger.error('error')
   logger.warning('warning')
   logger.info('info')
   logger.debug('debug')
