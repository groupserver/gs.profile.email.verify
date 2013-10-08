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
from zope.component import createObject
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from gs.errormesg.baseerror import BaseErrorPage


class EmailVerifyError(BaseErrorPage):
    def __init__(self, context, request):
        BaseErrorPage.__init__(self, context, request)
        self.verificationId = request.form.get('verificationId', '')
        self.linkAddress = '%s/r/verify/%s' % \
            (self.siteInfo.url, self.verificationId)


class VerifyIdNotFound(EmailVerifyError):
    fileName = 'browser/templates/verify_id_not_found.pt'
    index = ZopeTwoPageTemplateFile(fileName)

    def __init__(self, context, request):
        EmailVerifyError.__init__(self, context, request)
        m = 'Hi! I tried verifying my email address using the link %s but '\
            'I saw an Email Verification Error page. I tried... but it '\
            'did not help.' % self.linkAddress
        self.message = quote(m)

    def __call__(self, *args, **kw):
        contentType = 'text/html; charset=UTF-8'
        self.request.response.setHeader('Content-Type', contentType)
        # Return 404: Not Found
        self.request.response.setStatus(404)
        return self.index(self, *args, **kw)


class VerifyIdUsed(EmailVerifyError):
    fileName = 'browser/templates/verify_id_used.pt'
    index = ZopeTwoPageTemplateFile(fileName)

    def __init__(self, context, request):
        EmailVerifyError.__init__(self, context, request)
        m = 'Hi! I tried verifying my email address using the link %s but '\
            'I saw an Email Verification Link Used page. I was trying '\
            'to...' % self.linkAddress
        self.__loggedInUser = None
        self.message = quote(m)

    @Lazy
    def loggedInUser(self):
        retval = createObject('groupserver.LoggedInUser', self.context)
        return retval

    def __call__(self, *args, **kw):
        contentType = 'text/html; charset=UTF-8'
        self.request.response.setHeader('Content-Type', contentType)
        # Return 410: Gone
        self.request.response.setStatus(410)
        return self.index(self, *args, **kw)


class VerifyNoId(BaseErrorPage):
    fileName = 'browser/templates/verify_no_id.pt'
    index = ZopeTwoPageTemplateFile(fileName)

    def __init__(self, context, request):
        BaseErrorPage.__init__(self, context, request)
        self.linkAddress = '%s/r/verify/' % self.siteInfo.url
        m = 'Hi! I followed the the link %s but I saw an Email '\
            'Verification Link Error page. I was trying to get to... I found '\
            'the link in...' % self.linkAddress
        self.message = quote(m)

    def __call__(self, *args, **kw):
        contentType = 'text/html; charset=UTF-8'
        self.request.response.setHeader('Content-Type', contentType)
        # Return 400: Bad Request
        self.request.response.setStatus(400)
        return self.index(self, *args, **kw)
