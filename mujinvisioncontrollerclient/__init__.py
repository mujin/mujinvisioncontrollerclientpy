# -*- coding: utf-8 -*-
# Copyright (C) 2014-2015 MUJIN Inc.


class VisionControllerClientError(Exception):
    _type = None
    _desc = None

    def __init__(self, errortype, errordesc):
        self._type = errortype
        self._desc = errordesc

    def __unicode__(self):
        return u'%s: %s, %s' % (self.__class__.__name__, self._type, self._desc)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __repr__(self):
        return '<%s(%s, %s)>' % (self.__class__.__name__, self._type, self._desc)

    def __eq__(self, r):
        return self._type == r._type and self._desc == r._desc

    def __ne__(self, r):
        return self._type != r._type or self._desc != r._desc
