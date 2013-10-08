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
from zope.component import createObject
from Products.Five import BrowserView
from Products.CustomUserFolder.interfaces import IGSUserInfo
from queries import VerificationQuery


class VerifyEmailPage(BrowserView):
    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        self.label = u'Verify Email'
        self.userInfo = IGSUserInfo(self.context)
        self.verificationId = request.form.get('verificationId', '')
        self.__email = self.__quotedEmail = None
        self.__siteInfo = self.__query = None

    @property
    def email(self):
        if self.__email == None:
            self.__email = \
              self.query.get_email_from_verificationId(self.verificationId)
        return self.__email

    @property
    def quotedEmail(self):
        if self.__quotedEmail == None:
            self.__quotedEmail = \
              self.__quotedEmail = quote(self.email)
        return self.__quotedEmail

    @property
    def query(self):
        if self.__query == None:
            self.__query = \
              VerificationQuery()
        return self.__query

    @property
    def siteInfo(self):
        if self.__siteInfo == None:
            self.__siteInfo = createObject('groupserver.SiteInfo',
                self.context)
        return self.__siteInfo
