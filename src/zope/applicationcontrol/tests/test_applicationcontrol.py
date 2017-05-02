##############################################################################
#
# Copyright (c) 2001, 2002 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
##############################################################################
"""Application Control Tests
"""
import unittest
from zope.interface.verify import verifyObject

import time
from zope.applicationcontrol.applicationcontrol import ApplicationControl
from zope.applicationcontrol.interfaces import IApplicationControl

# seconds, time values may differ in order to be assumed equal
time_tolerance = 2

class Test(unittest.TestCase):

    def _Test__new(self):
        return ApplicationControl()

    def test_IVerify(self):
        verifyObject(IApplicationControl, self._Test__new())

    def test_startTime(self):
        assert_time = time.time()
        test_time = self._Test__new().getStartTime()
        self.assertAlmostEqual(assert_time, test_time, delta=time_tolerance)


def test_suite():
    return unittest.TestSuite((
        unittest.defaultTestLoader.loadTestsFromName(__name__),
    ))

if __name__ == '__main__':
    unittest.main()
