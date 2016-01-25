#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict


class Factory(object):
    def __init__(self, base_class, default_name):
        self._D = OrderedDict()
        self._base_class = base_class
        self._default_name = default_name

    def create(self, name=None):
        if name is None:
            name = self._default_name
        try:
            cls = self._D[name]
            return cls
        except KeyError:
            msg = "reader '%s' not in %s" % (name, list(self._D.keys()))
            raise NotImplementedError(msg)

    def register(self, name, cls):
        assert issubclass(cls, self._base_class), \
            "'%s' must be subclass of '%s'" % (cls, self._base_class)
        self._D[name] = cls
