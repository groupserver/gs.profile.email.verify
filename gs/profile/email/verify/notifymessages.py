# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013 OnlineGroups.net and Contributors.
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
from urllib import quote
from zope.cachedescriptors.property import Lazy
from gs.content.email.base import SiteEmail, TextMixin
from gs.profile.base.page import ProfilePage
from Products.GSGroup.interfaces import IGSMailingListInfo
UTF8 = 'utf-8'


class VerifyAddress(SiteEmail, ProfilePage):
    @Lazy
    def email(self):
        l = IGSMailingListInfo(self.groupInfo.groupObj)
        retval = l.get_property('mailto')
        return retval

    def get_support_email(self, verificationLink, emailAddress):
        msg = 'Hi,\n\nI received a message to verify the email address '\
                '<%s>,\nusing the link <%s> and...' %\
          (emailAddress, verificationLink)
        sub = quote('Verify Address')
        retval = 'mailto:%s?Subject=%s&body=%s' % \
            (self.siteInfo.get_support_email(), sub,
             quote(msg.encode(UTF8)))
        return retval


class VerifyAddressText(VerifyAddress, TextMixin):
    def __init__(self, context, request):
        super(VerifyAddressText, self).__init__(context, request)
        filename = 'verify-address-%s.txt' % self.userInfo.name
        self.set_header(filename)
