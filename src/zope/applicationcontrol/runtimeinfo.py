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
except ImportError:
    locale = None

import platform

from zope.component import getUtility, ComponentLookupError
from zope.interface import implementer

from zope.applicationcontrol.interfaces import IRuntimeInfo
from zope.applicationcontrol.interfaces import IApplicationControl
from zope.applicationcontrol.interfaces import IZopeVersion

try:
    from zope.app.appsetup import appsetup
except ImportError:
    appsetup = None


@implementer(IRuntimeInfo)
class RuntimeInfo(object):
    """Runtime information."""

    __used_for__ = IApplicationControl

    def __init__(self, context):
        self.context = context

    def getDeveloperMode(self):
        """See zope.app.applicationcontrol.interfaces.IRuntimeInfo"""
        if appsetup is None:
            return 'undefined'

        cc=appsetup.getConfigContext()
        if cc == None:  # make the test run
            return 'undefined'
        if cc.hasFeature('devmode'):
            return 'On'
        return 'Off'

    def getPreferredEncoding(self):
        """See zope.app.applicationcontrol.interfaces.IRuntimeInfo"""
        if locale is not None:
            try:
                return locale.getpreferredencoding()
            except locale.Error:
                pass
        return sys.getdefaultencoding()

    def getFileSystemEncoding(self):
        """See zope.app.applicationcontrol.interfaces.IRuntimeInfo"""
        enc = sys.getfilesystemencoding()
        if enc is None:
            enc = self.getPreferredEncoding()
        return enc

    def getZopeVersion(self):
        """See zope.app.applicationcontrol.interfaces.IRuntimeInfo"""
        try:
            version_utility = getUtility(IZopeVersion)
        except ComponentLookupError:
            return "Unavailable"
        return version_utility.getZopeVersion()
    
    def getPythonVersion(self):
        """See zope.app.applicationcontrol.interfaces.IRuntimeInfo"""
        return unicode(sys.version, self.getPreferredEncoding())

    def getPythonPath(self):
        """See zope.app.applicationcontrol.interfaces.IRuntimeInfo"""
        enc = self.getFileSystemEncoding()
        return tuple([unicode(path, enc) for path in sys.path])

    def getSystemPlatform(self):
        """See zope.app.applicationcontrol.interfaces.IRuntimeInfo"""
        info = []
        enc = self.getPreferredEncoding()
        for item in platform.uname():
            try:
                t = unicode(item, enc)
            except ValueError:
                continue
            info.append(t)
        return u" ".join(info)

    def getCommandLine(self):
        """See zope.app.applicationcontrol.interfaces.IRuntimeInfo"""
        return unicode(" ".join(sys.argv), self.getPreferredEncoding())

    def getProcessId(self):
        """See zope.app.applicationcontrol.interfaces.IRuntimeInfo"""
        return os.getpid()

    def getUptime(self):
        """See zope.app.applicationcontrol.interfaces.IRuntimeInfo"""
        return time.time() - self.context.getStartTime()
