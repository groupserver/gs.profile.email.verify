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
from zope.interface import Interface
from Products.CustomUserFolder.interfaces import IGSUserInfo


class IGSEmailVerificationUser(Interface):
    ''' Adapts a user to an IGSEmailVerificationUser, which can
        request verification for, and verify, a particular email
        address.
    '''
    def add_verification_id(verificationId):
        ''' Adds the verificationId for the email address to
            the email_verification table, provided the
            verificationId does not already exist in the table.
        '''

    def verify_email(verificationId):
        ''' Verifies the email address in the user_email table,
            and updates all relevant rows in the email_verification
            table (via clear_verification_ids), provided the
            verificationId exists and is current.
        '''

    def clear_verification_ids():
        ''' Updates all rows for the email address in the
            email_verification table to be verified.
        '''


class IGSVerifyEmailUser(IGSUserInfo):
    ''' Adapts a user to be able to verify an email address
        using a particular verificationId, provided that
        that verificationId exists and is current.
    '''
    def verificationId_current(verificationId):
        ''' Returns TRUE if the verificationId exists
            and has not yet been used.
        '''

    def verificationId_exists(verificationId):
        ''' Returns TRUE if the verificationId exists.
        '''
