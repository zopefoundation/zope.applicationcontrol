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
"""Runtime Info Tests
"""
import unittest
import os, sys, time

try:
    import locale
except ImportError:
    locale = None

from zope import component
from zope.interface import implementer
from zope.interface.verify import verifyObject
from zope.applicationcontrol.applicationcontrol import applicationController
from zope.applicationcontrol.interfaces import IRuntimeInfo, IZopeVersion

# seconds, time values may differ in order to be assumed equal
time_tolerance = 2
stupid_version_string = "3085t0klvn93850voids"

PY3 = sys.version_info[0] == 3
if PY3:
    _u = str
else:
    _u = unicode


@implementer(IZopeVersion)
class TestZopeVersion(object):
    """A fallback implementation for the ZopeVersion utility."""

    def getZopeVersion(self):
        return stupid_version_string


class Test(unittest.TestCase):

    def _Test__new(self):
        from zope.applicationcontrol.runtimeinfo import RuntimeInfo
        return RuntimeInfo(applicationController)

    def _getPreferredEncoding(self):
        try:
            result = locale.getpreferredencoding()
        except (locale.Error, AttributeError):
            result = ''
        # Under some systems, getpreferredencoding() can return ''
        # (e.g., Python 2.7/MacOSX/LANG=en_us.UTF-8). This then blows
        # up with 'unknown encoding'
        return result or sys.getdefaultencoding()

    def _getFileSystemEncoding(self):
        enc = sys.getfilesystemencoding()
        if enc is None:
            enc = self._getPreferredEncoding()
        return enc

    def testIRuntimeInfoVerify(self):
        verifyObject(IRuntimeInfo, self._Test__new())

    def test_PreferredEncoding(self):
        runtime_info = self._Test__new()
        enc = self._getPreferredEncoding()
        self.assertEqual(runtime_info.getPreferredEncoding(), enc)

    def test_FileSystemEncoding(self):
        runtime_info = self._Test__new()
        enc = self._getFileSystemEncoding()
        self.assertEqual(runtime_info.getFileSystemEncoding(), enc)

    def test_ZopeVersion(self):
        runtime_info = self._Test__new()

        # we expect that there is no utility
        self.assertEqual(runtime_info.getZopeVersion(), _u("Unavailable"))

        siteManager = component.getSiteManager()
        siteManager.registerUtility(TestZopeVersion(), IZopeVersion)

        self.assertEqual(runtime_info.getZopeVersion(), stupid_version_string)

    def test_PythonVersion(self):
        runtime_info = self._Test__new()
        enc = self._getPreferredEncoding()
        self.assertEqual(
            runtime_info.getPythonVersion(),
            sys.version if PY3 else sys.version.decode(enc))

    def test_SystemPlatform(self):
        runtime_info = self._Test__new()
        self.assertTrue(runtime_info.getSystemPlatform())

    def test_CommandLine(self):
        runtime_info = self._Test__new()
        self.assertEqual(runtime_info.getCommandLine(), " ".join(sys.argv))

    def test_ProcessId(self):
        runtime_info = self._Test__new()
        self.assertEqual(runtime_info.getProcessId(), os.getpid())

    def test_Uptime(self):
        runtime_info = self._Test__new()
        # whats the uptime we expect?

        start_time = applicationController.getStartTime()
        asserted_uptime = time.time() - start_time

        # get the uptime the current implementation calculates
        test_uptime = runtime_info.getUptime()

        self.assertTrue(abs(asserted_uptime - test_uptime) < time_tolerance)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(Test),
        ))

if __name__ == '__main__':
    unittest.main()
