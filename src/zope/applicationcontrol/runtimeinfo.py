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
#
##############################################################################
""" Runtime Information
"""
__docformat__ = 'restructuredtext'

import os
import sys
import time


try:
    import locale
except ModuleNotFoundError:  # pragma: no cover
    locale = None

import platform

from zope.component import ComponentLookupError
from zope.component import adapter
from zope.component import getUtility
from zope.interface import implementer

from zope.applicationcontrol.interfaces import IApplicationControl
from zope.applicationcontrol.interfaces import IRuntimeInfo
from zope.applicationcontrol.interfaces import IZopeVersion


try:
    from zope.app.appsetup import appsetup
except ModuleNotFoundError:
    appsetup = None


@implementer(IRuntimeInfo)
@adapter(IApplicationControl)
class RuntimeInfo:
    """Runtime information."""

    def __init__(self, context):
        self.context = context

    def getDeveloperMode(self):
        """See zope.app.applicationcontrol.interfaces.IRuntimeInfo"""
        if appsetup is None:
            return 'undefined'

        cc = appsetup.getConfigContext()
        if cc is None:  # make the test run
            return 'undefined'
        if cc.hasFeature('devmode'):
            return 'On'
        return 'Off'

    def getPreferredEncoding(self):
        """See zope.app.applicationcontrol.interfaces.IRuntimeInfo"""
        try:
            result = locale.getpreferredencoding()
        except (locale.Error, AttributeError):  # pragma: no cover
            result = ''
        # Under some systems, getpreferredencoding() can return ''
        # (e.g., Python 2.7/MacOSX/LANG=en_us.UTF-8). This then blows
        # up with 'unknown encoding'
        return result or sys.getdefaultencoding()

    def getFileSystemEncoding(self):
        """See zope.app.applicationcontrol.interfaces.IRuntimeInfo"""
        enc = sys.getfilesystemencoding()
        return enc if enc is not None else self.getPreferredEncoding()

    def getZopeVersion(self):
        """See zope.app.applicationcontrol.interfaces.IRuntimeInfo"""
        try:
            version_utility = getUtility(IZopeVersion)
        except ComponentLookupError:
            return "Unavailable"
        return version_utility.getZopeVersion()

    def getPythonVersion(self):
        """See zope.app.applicationcontrol.interfaces.IRuntimeInfo"""
        return sys.version

    def getPythonPath(self):
        """See zope.app.applicationcontrol.interfaces.IRuntimeInfo"""
        return tuple(path for path in sys.path)

    def getSystemPlatform(self):
        """See zope.app.applicationcontrol.interfaces.IRuntimeInfo"""
        info = []
        enc = self.getPreferredEncoding()
        for item in platform.uname():
            try:
                t = item if isinstance(item, str) else item.decode(enc)
            except UnicodeError:
                continue
            info.append(t)
        return ' '.join(info)

    def getCommandLine(self):
        """See zope.app.applicationcontrol.interfaces.IRuntimeInfo"""
        return " ".join(sys.argv)

    def getProcessId(self):
        """See zope.app.applicationcontrol.interfaces.IRuntimeInfo"""
        return os.getpid()

    def getUptime(self):
        """See zope.app.applicationcontrol.interfaces.IRuntimeInfo"""
        return time.time() - self.context.getStartTime()
