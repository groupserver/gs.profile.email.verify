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
from __future__ import absolute_import
from urllib import quote
from zope.cachedescriptors.property import Lazy
from gs.profile.base import ProfilePage
from .queries import VerificationQuery


class VerifyEmailPage(ProfilePage):
    def __init__(self, context, request):
        super(VerifyEmailPage, self).__init__(context, request)
        self.label = u'Verify Email'

        self.__email = self.__quotedEmail = None
        self.__siteInfo = self.__query = None

    @Lazy
    def verificationId(self):
        retval = self.request.form.get('verificationId', '')
        return retval

    @Lazy
    def email(self):
        retval = self.query.get_email_from_verificationId(self.verificationId)
        return retval

    @Lazy
    def quotedEmail(self):
        retval = quote(self.email)
        return retval

    @Lazy
    def query(self):
        retval = VerificationQuery()
        return retval
