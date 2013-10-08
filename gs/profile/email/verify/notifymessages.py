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
from urllib import quote
from zope.cachedescriptors.property import Lazy
from gs.profile.base.page import ProfilePage
from Products.GSGroup.interfaces import IGSMailingListInfo
UTF8 = 'utf-8'


class VerifyAddress(ProfilePage):
    @Lazy
    def email(self):
        l = IGSMailingListInfo(self.groupInfo.groupObj)
        retval = l.get_property('mailto')
        return retval

    def get_support_email(self, verificationLink, emailAddress):
        msg = u'Hi,\n\nI received a message to verify the email '\
          u'address <%s>,\nusing the link <%s> and...' %\
          (emailAddress, verificationLink)
        sub = quote('Verify Address')
        retval = 'mailto:%s?Subject=%s&body=%s' % \
            (self.siteInfo.get_support_email(), sub, quote(msg.encode(UTF8)))
        return retval


class VerifyAddressText(VerifyAddress):
    def __init__(self, context, request):
        VerifyAddress.__init__(self, context, request)
        response = request.response
        response.setHeader("Content-Type", 'text/plain; charset=UTF-8')
        filename = 'verify-address-%s.txt' % self.userInfo.name
        response.setHeader('Content-Disposition',
                            'inline; filename="%s"' % filename)
