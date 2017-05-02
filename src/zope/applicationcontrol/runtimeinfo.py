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

import sys
import os
import time

try:
    import locale
except ImportError: # pragma: no cover
    locale = None

import platform

from zope.component import getUtility, ComponentLookupError, adapter
from zope.interface import implementer

from zope.applicationcontrol.interfaces import IRuntimeInfo
from zope.applicationcontrol.interfaces import IApplicationControl
from zope.applicationcontrol.interfaces import IZopeVersion

try:
    from zope.app.appsetup import appsetup
except ImportError:
    appsetup = None

try:
    text_type = unicode
except NameError:
    text_type = str


@implementer(IRuntimeInfo)
@adapter(IApplicationControl)
class RuntimeInfo(object):
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
        except (locale.Error, AttributeError): # pragma: no cover
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
        return sys.version if isinstance(sys.version, text_type) else sys.version.decode(
            self.getPreferredEncoding())

    def getPythonPath(self):
        """See zope.app.applicationcontrol.interfaces.IRuntimeInfo"""
        enc = self.getFileSystemEncoding()
        return tuple([path if isinstance(path, text_type) else path.decode(enc)
                      for path in sys.path])

    def getSystemPlatform(self):
        """See zope.app.applicationcontrol.interfaces.IRuntimeInfo"""
        info = []
        enc = self.getPreferredEncoding()
        for item in platform.uname():
            try:
                t = item if isinstance(item, text_type) else item.decode(enc)
            except UnicodeError:
                continue
            info.append(t)
        return u' '.join(info)

    def getCommandLine(self):
        """See zope.app.applicationcontrol.interfaces.IRuntimeInfo"""
        cmd = " ".join(sys.argv)
        return cmd if isinstance(cmd, text_type) else cmd.decode(self.getPreferredEncoding())

    def getProcessId(self):
        """See zope.app.applicationcontrol.interfaces.IRuntimeInfo"""
        return os.getpid()

    def getUptime(self):
        """See zope.app.applicationcontrol.interfaces.IRuntimeInfo"""
        return time.time() - self.context.getStartTime()
