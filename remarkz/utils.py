# -*- coding:utf-8 -*-

import time

from functools import wraps

def split_tags(func):
    @wraps(func)
    def wrapper(self, tags=''):
        if tags:
            return func(self, *set((tag.lower().strip() for tag
                                    in tags.split('/') if tag)))
        else:
            return func(self)
    return wrapper

def uni(st):
    return st.decode('utf-8')

def format_output(pair):
    (item, tmpstmp) = pair
    item = uni(item)
    dttm = time.strftime("%Y-%m-%d %H:%M", time.gmtime(tmpstmp))
    return (item, dttm)
