# -*- coding: utf-8 -*-
############################################################################
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
############################################################################
from __future__ import absolute_import
from zope.component import createObject
from Products.Five import BrowserView  # TODO: gs.profile.base.ProfilePage
from .verifyemailuser import VerifyEmailUser


class VerifyEmail(BrowserView):
    def __init__(self, context, request):
        assert context
        assert request
        self.context = context
        self.request = request

    def __call__(self):
        assert self.request
        assert self.context
        if not hasattr(self.request, 'form'):
            raise ValueError('No form in request')
        if 'verificationId' not in self.request.form.keys():
            raise ValueError('No verificationId in form')
        vId = self.request.form['verificationId']
        evu = createObject('groupserver.EmailVerificationUserFromId',
                           self.context, vId)
        veu = VerifyEmailUser(evu.userInfo)
        if veu.verificationId_current(vId):
            evu.verify_email(vId)
