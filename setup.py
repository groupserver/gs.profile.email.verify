# -*- coding: utf-8 -*-
############################################################################
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
############################################################################
import codecs
import os
from setuptools import setup, find_packages
from version import get_version

name = 'gs.profile.email.verify'
version = get_version()

with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()
with codecs.open(os.path.join("docs", "HISTORY.rst"),
                 encoding='utf-8') as f:
    long_description += '\n' + f.read()

setup(
    name=name,
    version=version,
    description="Verifying an email address on GroupServer.",
    long_description=long_description,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        "Environment :: Web Environment",
        "Framework :: Zope2",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: Zope Public License',
        "Natural Language :: English",
        "Natural Language :: French",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='profile email address verify verification groupserver',
    author='Alice Murphy',
    author_email='alice@onlinegroups.net',
    maintainer='Michael JasonSmith',
    maintainer_email='mpj17@onlinegroups.net',
    url='https://github.com/groupserver/{0}'.format(name),
    license='ZPL 2.1',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['.'.join(name.split('.')[:i])
                        for i in range(1, len(name.split('.')))],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'pytz',
        'SQLAlchemy',
        'zope.browserpage',  # For the <browser:page /> declaration
        'zope.browserresource',  # For the <browser:resource /> declaration
        'zope.cachedescriptors',
        'zope.component',
        'zope.i18n[compile]',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.pagetemplate',
        'zope.schema',
        'zope.sqlalchemy',
        'zope.tal',
        'zope.tales',
        'AccessControl',
        'Zope2',
        'gs.content.base',
        'gs.content.email.base',
        'gs.content.email.layout',
        'gs.core',
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
