# Mujin vision controller client for bin picking task
# Copyright (C) 2023 MUJIN Inc
# AUTO GENERATED FILE! DO NOT EDIT!


try:
    import mujincommon.i18n
    ugettext, ungettext = mujincommon.i18n.GetDomain('mujinvisioncontrollerclientpy').GetTranslationFunctions()
except ImportError:
    def ugettext(message):
        return message

    def ungettext(singular, plural, n):
        return singular if n == 1 else plural

_ = ugettext


try:
    import ujson as json  # noqa: F401
except ImportError:
    import json  # noqa: F401

import zmq  # noqa: F401 # TODO: stub zmq
import six

@six.python_2_unicode_compatible
class VisionControllerClientError(Exception):
    _type = None  # type: six.text_type # In PY2, it is unicode; in PY3, it is str
    _desc = None  # type: six.text_type # In PY2, it is unicode; In PY3, it is str

    def __init__(self, errordesc, errortype='unknownerror'):
        # type: (Union[six.text_type, str], Union[six.text_type, str]) -> None
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
        # type: (VisionControllerClientError) -> bool
        return self._type == r._type and self._desc == r._desc

    def __ne__(self, r):
        # type: (VisionControllerClientError) -> bool
        return self._type != r._type or self._desc != r._desc

class VisionControllerTimeoutError(VisionControllerClientError):
    pass

# logging
import logging
log = logging.getLogger(__name__)

