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
from zope.component.factory import Factory
from queries import VerificationQuery
from Products.CustomUserFolder.userinfo import GSUserInfo
from Products.CustomUserFolder.interfaces import IGSUserInfo


class VerifyEmailUser(GSUserInfo):
    def __init__(self, userInfo):
        GSUserInfo.__init__(self, userInfo.user)
        self.__emailVerifyUrl = self.__query = None

    @property
    def emailVerifyUrl(self):
        if self.__emailVerifyUrl == None:
            self.__emailVerifyUrl = '%s/verifyemail.html' % self.url
        return self.__emailVerifyUrl

    @property
    def query(self):
        if self.__query == None:
            self.__query = VerificationQuery()
        return self.__query

    def verificationId_current(self, verificationId):
        retval = self.query.verificationId_status(verificationId) == \
            self.query.CURRENT
        return retval

    def verificationId_exists(self, verificationId):
        retval = self.query.verificationId_status(verificationId) != \
            self.query.NOT_FOUND
        return retval


class VerificationIdNotFoundError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'Could not find verification ID (%s)' % self.value


class VerifyEmailUserFromId(object):
    ''' Create a Verify Email User from a Verification ID

        We do not always have an IGSUserInfo to hand when we want a
        verify-email user. Sometimes we do have a verification ID.'''
    def __call__(self, context, verificationId):
        queries = VerificationQuery()

        s = queries.verificationId_status(verificationId)
        if s == queries.NOT_FOUND:
            raise VerificationIdNotFoundError(verificationId)

        userId = queries.get_userId_from_verificationId(verificationId)
        aclUsers = context.site_root().acl_users
        user = aclUsers.getUser(userId)
        assert user, 'No user for userId %s' % userId

        userInfo = IGSUserInfo(user)
        return VerifyEmailUser(userInfo)

VerifyEmailUserFactory = Factory(
                        VerifyEmailUserFromId,
                        'Verify-Email User from ID',
                        'Create a verify-email user from a verification ID.')
