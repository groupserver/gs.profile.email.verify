# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013, 2015 OnlineGroups.net and Contributors.
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
from __future__ import unicode_literals
from zope.cachedescriptors.property import Lazy
from gs.content.email.base import SiteEmail, TextMixin
from gs.profile.base.page import ProfilePage
from Products.GSGroup.interfaces import IGSMailingListInfo
UTF8 = 'utf-8'


class VerifyAddress(ProfilePage, SiteEmail):
    @Lazy
    def email(self):
        l = IGSMailingListInfo(self.groupInfo.groupObj)
        retval = l.get_property('mailto')
        return retval

    def get_support_email(self, verificationLink, emailAddress, userInfo):
        b = '''Hello,

I received a message to verify the email address <{email}>,
using the link <{link}>
and...

--
Me: {userInfo.name}
    <{siteInfo.url}{userInfo.url}>
'''
        body = b.format(email=emailAddress, link=verificationLink,
                        siteInfo=self.siteInfo, userInfo=userInfo)
        retval = self.mailto(self.siteInfo.get_support_email(),
                             'Verify address', body)
        return retval


class VerifyAddressText(VerifyAddress, TextMixin):
    def __init__(self, context, request):
        super(VerifyAddressText, self).__init__(context, request)
        filename = 'verify-address-%s.txt' % self.userInfo.name
        self.set_header(filename)
