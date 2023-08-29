# -*- coding: utf-8 -*-
# Copyright (C) 2014-2015 MUJIN Inc.

import six
import typing # noqa: F401 # used in type check

@six.python_2_unicode_compatible
class VisionClientError(Exception):
    _type = None  # type: six.text_type # In PY2, it is unicode; in PY3, it is str
    _desc = None  # type: six.text_type # In PY2, it is unicode; In PY3, it is str

    def __init__(self, errordesc, errortype='unknownerror'):
        # type: (typing.Union[six.text_type, str], typing.Union[six.text_type, str]) -> None
        if errortype is not None and not isinstance(errortype, six.text_type):
            # Then errortype is str, and we need to decode it back to unicode:
            # noinspection PyUnresolvedReferences
            errortype = errortype.decode('utf-8', 'ignore')
        if errordesc is not None and not isinstance(errordesc, six.text_type):
            # noinspection PyUnresolvedReferences
            errordesc = errordesc.decode('utf-8', 'ignore')

        self._type = errortype
        self._desc = errordesc

    def __str__(self):
        # type: () -> str
        # By doing this we are implicitly not doing any translation
        # To enable translation, need to import mujincommon
        return "%s: %s, %s" % (self.__class__.__name__, self._type, self._desc)

    def __repr__(self):
        # type: () -> str
        return "<%r(%r, %r)>" % (self.__class__.__name__, self._type, self._desc)

    def __hash__(self):
        # type: () -> int
        return hash((self._type, self._desc))

    def __eq__(self, r):
        # type: (VisionClientError) -> bool
        return self._type == r._type and self._desc == r._desc

    def __ne__(self, r):
        # type: (VisionClientError) -> bool
        return self._type != r._type or self._desc != r._desc

class VisionTimeoutError(VisionClientError):
    pass


VisionControllerClientError = VisionClientError
VisionControllerTimeoutError = VisionTimeoutError
