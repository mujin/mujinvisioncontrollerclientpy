# -*- coding: utf-8 -*-
# Copyright (C) 2014-2015 MUJIN Inc.

import six
import unittest
from . import visionclienterror


class TestMethods(unittest.TestCase):
    def test_str(self):
        errorType = "错误类型"
        errorDesc = "错误描述"
        err = visionclienterror.VisionClientError(
            errortype=errorType, errordesc=errorDesc
        )
        if six.PY2:
            self.assertEqual(
                str(err), (u"VisionClientError: %s, %s" % (errorType.decode("utf-8"), errorDesc.decode("utf-8"))).encode("utf-8")
            )
        else:
            self.assertEqual(
                str(err), (u"VisionClientError: %s, %s" % (errorType, errorDesc))
            )

    def test_unicode(self):
        errorType = u"错误类型"
        errorDesc = u"错误描述"
        err = visionclienterror.VisionClientError(
            errortype=errorType, errordesc=errorDesc
        )
        if six.PY2:
            self.assertEqual(
                str(err), (u"VisionClientError: %s, %s" % (errorType, errorDesc)).encode("utf-8")
            )
        else:
            self.assertEqual(
                str(err), (u"VisionClientError: %s, %s" % (errorType, errorDesc))
            )


if __name__ == "__main__":
    unittest.main()
