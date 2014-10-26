# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import sys

import dosca

from .remarkz import Remarkz

__all__ = ('Remarkz', 'run_app')

def run_app():
    if len(sys.argv) > 1:
        config = dosca.parse_file(sys.argv[1])
        app = Remarkz(config=config)
        app.run()
    else:
        print 'Usage: {0} config_file'.format(sys.argv[0])
