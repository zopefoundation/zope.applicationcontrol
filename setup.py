##############################################################################
#
# Copyright (c) 2006-2007 Zope Corporation and Contributors.
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
"""Setup for zope.annotation package

$Id$
"""

import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name='zope.annotation',
    version='3.5.0',
    url='http://pypi.python.org/pypi/zope.annotation',
    license='ZPL 2.1',
    description='Object annotation mechanism',
    author='Zope Corporation and Contributors',
    author_email='zope-dev@zope.org',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development',
        ],
    long_description= \
        read('src', 'zope', 'annotation', 'README.txt') 
        + '\n\n' +
        read('CHANGES.txt'),
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['zope',],
    install_requires=['setuptools',
                      'zope.interface',
                      'zope.component',
                      'zope.location',
                      'zope.proxy',
                      'ZODB3',
                      ],
    extras_require=dict(
        test=['zope.testing'],
        ),
    include_package_data=True,
    zip_safe=False,
    )
