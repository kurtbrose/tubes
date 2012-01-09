'''
A microframework designed to allow for building up of event handlers out of
generic components.

Just exploring the problem space to see if anything interesting pops up.

Here is an unexciting example:

>>> import tubes
>>> tubes.sub('keydown',
              tubes.link(lambda x: x=='a',
                         tubes.stop_unless,
                         tubes.pub('a_pressed')))
>>> import sys
>>> tubes.sub('a_pressed', lambda x: sys.stdout.write('a pressed\n'))
>>> tubes.pub('keydown')('a')
a pressed
'''
import collections

class AbortTube(Exception): pass

def link(*funcs):
    'chain functions of a single parameter together'
    def linked(p):
        try:
            for f in funcs:
                p = f(p)
        except AbortTube as e:
            pass
        return sofar
    return linked

_subs = collections.defaultdict(list)

def sub(event, func):
    'subscribe to be notified whenever an event happens'
    _subs[event].append(func)

def pub(event):
    'publish that an event just happened'
    def _pub(*a, **kw):
        for f in _subs[event]:
            f(*a, **kw)
    return _pub

def stop_unless(v):
    if not v:
        raise AbortTube

def stop_if(v):
    if v:
        raise AbortTube