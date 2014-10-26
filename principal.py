# -*- coding:utf-8 -*-

# principal algorhytm of work

from collections import defaultdict
from itertools import chain

STORAGE = defaultdict(set)

def lazyset(it):
    guard = set()
    for item in it:
        if item not in guard:
            guard.add(item)
            yield item


def add(item, *tags):
    for tag in tags:
        STORAGE[tag].add(item)

def get(*tags):
    if tags:
        return lazyset(chain(*(cont for (tag, cont) in
                           STORAGE.iteritems() if tag in tags)))
    else:
        return lazyset(chain(*STORAGE.values()))

def clean():
    global STORAGE
    STORAGE = defaultdict(set)

def test():
    add('x', '42')
    add('y', '42', '23')
    add('z', '23')
    assert 'x' in get('42')
    assert 'x' in get('42')
    assert 'z' not in get('42')
    assert 'z' in get('23')
    assert 'y' in get('42', '23')
