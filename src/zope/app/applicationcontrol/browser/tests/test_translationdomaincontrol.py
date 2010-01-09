##############################################################################
#
# Copyright (c) 2008 Zope Corporation and Contributors.
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
"""Translation Domain Control View Tests

$Id$
"""
import unittest

import zope.component

from zope.interface import implements
from zope.app.applicationcontrol.browser.translationdomaincontrol import (
    TranslationDomainControlView)
from zope.app.component.testing import PlacefulSetup
from zope.i18n.interfaces import ITranslationDomain

class TranslationDomainStub(object):
    implements(ITranslationDomain)

    def __init__(self, domain, languages):
        self.domain = domain
        self.languages = languages
        self.reloadDone = False

    def translate(self, msgid, mapping=None, context=None,
                  target_language=None, default=None):
        return msgid

    def getCatalogsInfo(self):
        template = 'locales/%s/LC_MESSAGES/%s.mo'
        return dict([(lang, template % (lang, self.domain))
                     for lang in self.languages])

    def reloadCatalogs(self, fileNames):
        self.reloadDone = True


class Test(PlacefulSetup, unittest.TestCase):

    def _TestView__newView(self, request):
        view = TranslationDomainControlView()
        view.context = object() # the context does not matter in this view
        view.request = request
        return view

    def test_TranslationDomainControlView(self):
        languages = ['de', 'en', 'es'] # these are sorted, see below
        domains = ['zope', 'plone']
        translationDomains = []
        globalSiteManager = zope.component.getGlobalSiteManager()
        for domain in domains:
            translationDomain = TranslationDomainStub(domain, languages)
            globalSiteManager.registerUtility(translationDomain,
                                              ITranslationDomain,
                                              domain)
            translationDomains.append(translationDomain)

        test_translationDomainView = self._TestView__newView({})
        catalogs = test_translationDomainView.getCatalogsInfo()

        self.assertEqual(len(catalogs), 2)
        for i, domain in enumerate(domains):
            catalog = catalogs[i]
            self.assertEqual(domain, catalog['domain'])
            langs = [li['language'] for li in catalog['languagesInfo']]
            self.assertEqual(sorted(langs), languages)
            files = [li['fileNames'] for li in catalog['languagesInfo']]
            self.assertEqual(sorted(files), [
                    'locales/de/LC_MESSAGES/%s.mo' % domain,
                    'locales/en/LC_MESSAGES/%s.mo' % domain,
                    'locales/es/LC_MESSAGES/%s.mo' % domain,
                    ])


        # test catalog reloading
        translationDomain = translationDomains[0]
        test_translationDomainView = self._TestView__newView({
                'RELOAD': 1,
                'domain': 'zope',
                'language': 'fr' # fr is not in languages list
                })

        test_translationDomainView.reloadCatalogs()
        self.assertEqual(translationDomain.reloadDone, False)

        test_translationDomainView = self._TestView__newView({
                'RELOAD': 1,
                'domain': 'zope',
                'language': 'en' # en is in languages list
                })

        test_translationDomainView.reloadCatalogs()
        self.assertEqual(translationDomain.reloadDone, True)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(Test),
        ))

if __name__ == '__main__':
    unittest.main()
