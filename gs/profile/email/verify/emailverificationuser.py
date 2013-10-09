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
import time
import md5
from zope.cachedescriptors.property import Lazy
from zope.component import createObject, adapts
from zope.component.factory import Factory
from zope.interface import implements, Interface
from zope.schema.interfaces import IASCIILine
from gs.profile.email.base.emailuser import EmailUser
from gs.profile.notify.notifyuser import NotifyUser as CoreNotifyUser
from Products.XWFCore.XWFUtils import convert_int2b62, get_support_email
from Products.CustomUserFolder.interfaces import IGSUserInfo
from .audit import Auditor, VERIFIED, ADD_VERIFY, CLEAR_VERIFY
from .createmessage import create_verification_message
from .interfaces import IGSEmailVerificationUser
from .notify import Notifier
from .queries import EmailQuery, VerificationQuery
from .verifyemailuser import VerificationIdNotFoundError


class EmailVerificationUser(object):
    implements(IGSEmailVerificationUser)
    adapts(Interface, IGSUserInfo, IASCIILine)
    """ Adapts a userInfo and one of their email addresses
        to an IGSEmailVerificationUser, which can request
        verification for, and verify, that email address.
    """
    def __init__(self, context, userInfo, email):
        self.context = context
        self.userInfo = userInfo
        self.email = email

        assert email in self.emailUser.get_addresses(), \
          'Address %s does not belong to %s (%s)' %\
           (email, userInfo.name, userInfo.id)

    @Lazy
    def emailUser(self):
        retval = EmailUser(self.context, self.userInfo)
        return retval

    @Lazy
    def auditor(self):
        retval = Auditor(self.context, self.siteInfo)
        return retval

    @Lazy
    def siteInfo(self):
        retval = createObject('groupserver.SiteInfo', self.context)
        return retval

    @Lazy
    def verifyQuery(self):
        retval = VerificationQuery()
        return retval

    @Lazy
    def userQuery(self):
        retval = EmailQuery(self.email)
        return retval

    def send_verification_message(self):
        # TODO: Depricate
        verificationId = self.create_verification_id()
        self.add_verification_id(verificationId)

        notifyUser = CoreNotifyUser(self.userInfo.user, self.siteInfo)
        fromAddr = get_support_email(self.userInfo.user, self.siteInfo.id)
        msg = create_verification_message(self.userInfo, self.siteInfo,
                self.email, fromAddr, verificationId)
        notifyUser.send_message(msg, self.email, fromAddr)

    def send_verification(self, request):
        verificationId = self.create_verification_id()
        self.add_verification_id(verificationId)
        notifier = Notifier(self.context, request)
        link = '%s/r/verify/%s' % (self.siteInfo.url, verificationId)
        notifier.notify(self.userInfo, self.email, link)

    def create_verification_id(self):
        # Let us hope that the verification ID *is* unique
        vNum = long(md5.new(time.asctime() + self.email).hexdigest(), 16)
        verificationId = str(convert_int2b62(vNum))
        assert type(verificationId) == str
        return verificationId

    def add_verification_id(self, verificationId):
        assert verificationId, 'No verificationId'
        idStatus = self.verifyQuery.verificationId_status(verificationId)
        assert idStatus == self.verifyQuery.NOT_FOUND, \
          'Email Verification ID %s exists' % verificationId
        self.userQuery.set_verification_id(verificationId)
        self.auditor.info(ADD_VERIFY, self.userInfo, self.email)

    def verify_email(self, verificationId):
        if not verificationId:
            raise ValueError('No verification ID')
        idStatus = self.verifyQuery.verificationId_status(verificationId)
        # FIXME: Raise actual errors
        assert idStatus != self.verifyQuery.NOT_FOUND, \
          'Verification ID %s not found' % verificationId
        assert idStatus != self.verifyQuery.VERIFIED, \
          'Verification ID %s already used' % verificationId
        assert idStatus == self.verifyQuery.CURRENT, \
          'Status of email verification ID %s is not ' \
          'one of CURRENT, VERIFIED or NOT_FOUND.' % verificationId

        self.userQuery.verify_address(verificationId)
        self.possibly_set_delivery()
        self.auditor.info(VERIFIED, self.userInfo, self.email,
                          verificationId)
        self.clear_verification_ids()

    def possibly_set_delivery(self):
        if len(self.emailUser.get_delivery_addresses()) == 0:
            self.emailUser.set_delivery(self.email)
        m = 'No delivery addresses after setting <{0}> for delivery'
        assert len(self.emailUser.get_delivery_addresses()) != 0, \
            m.format(self.email)

    def clear_verification_ids(self):
        self.userQuery.clear_verification_ids()
        self.auditor.info(CLEAR_VERIFY, self.userInfo, self.email)


class EmailVerificationUserFromId(object):
    ''' Create an Email Verification User from a Verification ID.
    '''
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
        emailUser = EmailUser(context, userInfo)

        email = queries.get_email_from_verificationId(verificationId)
        assert email in emailUser.get_addresses(), \
          'Address %s does not belong to %s (%s)' %\
          (email, userInfo.name, userInfo.id)

        return EmailVerificationUser(context, userInfo, email)

EmailVerificationUserFromIdFactory = Factory(
        EmailVerificationUserFromId,
        'Email-Verification User from ID',
        'Create an email-verification user from a verification ID.')


class EmailVerificationUserFromEmail(object):
    ''' Create an Email Verification User from an email address.
    '''
    def __call__(self, context, email):
        aclUsers = context.site_root().acl_users
        user = aclUsers.get_userByEmail(email)
        assert user, 'No user for email address %s' % email
        userInfo = IGSUserInfo(user)
        return EmailVerificationUser(context, userInfo, email)

EmailVerificationUserFromEmailFactory = Factory(
        EmailVerificationUserFromEmail,
        'Email-Verification User from Email',
        'Create an email-verification user from an email address.')


class EmailVerificationUserFromUser(EmailVerificationUser):
    implements(IGSEmailVerificationUser)

    def __init__(self, context, user, email):
        userInfo = IGSUserInfo(user)
        EmailVerificationUser.__init__(self, context, userInfo, email)
