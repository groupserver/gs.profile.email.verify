# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
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
import os
from setuptools import setup, find_packages
from version import get_version

version = get_version()

setup(name='gs.profile.email.verify',
    version=version,
    description="Verifying an email address on GroupServer.",
    long_description=open("README.txt").read() + "\n" +
                      open(os.path.join("docs", "HISTORY.txt")).read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        "Environment :: Web Environment",
        "Framework :: Zope2",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: Zope Public License',
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux"
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
      ],
    keywords='profile email address verify verification groupserver',
    author='Alice Murphy',
    author_email='alice@onlinegroups.net',
    url='http://groupserver.org/',
    license='ZPL 2.1',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['gs', 'gs.profile', 'gs.profile.email'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'pytz',
        'sqlalchemy',
        'zope.browserpage',  # For the <browser:page /> declaration
        'zope.cachedescriptors',
        'zope.component',
        'zope.interface',
        'zope.pagetemplate',
        'zope.browserresource',  # For the <browser:resource /> declaration
        'zope.schema',
        'zope.sqlalchemy',
        'AccessControl',
        'Zope2',
        'gs.content.base',
        'gs.content.email.base',
        'gs.content.email.layout',
        'gs.database',
        'gs.errormesg',
        'gs.profile.base',
        'gs.profile.email.base',
        'gs.profile.notify',
        'Products.CustomUserFolder',
        'Products.GSAuditTrail',
        'Products.GSGroup',
        'Products.GSRedirect',
        'Products.XWFCore',
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,)
