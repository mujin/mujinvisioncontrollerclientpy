# -*- coding: utf-8 -*-
# Copyright (C) 2014-2015 MUJIN Inc.
from .version import __version__  # noqa: F401
from .visioncontrollerclienterror import VisionControllerClientError, VisionControllerTimeoutError # noqa: F401


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
