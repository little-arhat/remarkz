#!/usr/local/bin/python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import time
from itertools import ifilter, imap

import eventlet
import eventlet.wsgi
from flask import Flask, request, render_template, url_for, redirect
import redis

from .utils import split_tags, format_output



class Remarkz(object):
    def __new__(cls, *args, **kwargs):
        obj = super(type(cls), cls).__new__(cls, *args, **kwargs)
        obj.app = Flask(__name__)
        obj.app.route('/', methods=['GET'])(obj.main)
        obj.app.route('/<path:tags>', methods=['GET'])(obj.main)
        obj.app.route('/', methods=['GET'])(obj.get)
        obj.app.route('/<path:tags>', methods=['GET'])(obj.get)
        obj.app.route('/add/', methods=['POST'])(obj.add)
        obj.app.route('/add/<path:tags>', methods=['POST'])(obj.add)
        obj.app.route('/bookmarklet/<path:tags>', methods=['POST'])(obj.bookmarklet)
        obj.app.route('/about', methods=['GET'])(obj.about)
        obj.app.route('/about/', methods=['GET', 'POST'])(obj.about)
        obj.app.route('/about/<path:tags>', methods=['GET', 'POST'])(obj.about)
        return obj

    def __init__(self, config):
        self.config = config
        self.storage = redis.Redis(**config['redis'])
        self.app.static_url_path = config['http']['static_path']
        self.app.debug = config['http']['debug']
        self.app.context_processor(lambda: dict(char_limit=config['char_limit']))

    def run(self):
        eventlet.wsgi.server(eventlet.listen((self.config['http']['host'],
                                              self.config['http']['port'])),
                             self.app)

    @split_tags
    def main(self, *tags):
        if tags:
            page = int(request.args.get('page', 1))
            count = self.config['items_count']
            tempkey = str(time.time())
            self.storage.zinterstore(tempkey, tags, 'MAX')
            start = (page - 1) * count
            result = self.storage.zrevrange(tempkey, start,
                                            (page * count) - 1,
                                            True)
            self.storage.delete(tempkey)
            items = imap(format_output, result)
            last_page = True if len(result) < count else False
            return render_template('list.html', tags=tags, page=page,
                                   start=start, last_page=last_page,
                                   items=items)
        else:
            return render_template('main.html')

    def get(self, tags):
        redirect(url_for('main'), tags)

    @split_tags
    def add(self, *tags):
        if tags:
            try:
                self._add(tags)
                return redirect(url_for('get', tags='/'.join(tags)))
            except ValueError as e:
                return render_template('main.html', error=unicode(e))
        else:
            return render_template('main.html',
                                   error='Provide at least one tag!')

    @split_tags
    def bookmarklet(self, *tags):
        try:
            _add(tags)
            msg = '''Remark was succesfully added with tags:{tags}.
            <a href="{url}">Show</a>
            '''.format(tags=' '.join(tags),
                       url=url_for('get', tags='/'.join(tags)))
        except ValueError as e:
            msg = unicode(e)
            return msg

    @split_tags
    def about(self, *tags):
        if request.method == 'GET':
            return render_template('about.html')
        else:
            return render_template('about.html', tags=tags)

    def _add(self, tags):
        item = request.form['item'].strip()
        if len(item) > self.config['char_limit']:
            raise ValueError('Error! Remark can contain at most {} characters.'.format(
                self.config['char_limit']))
        for tag in tags:
            self.storage.zadd(tag, item, int(time.time()))
