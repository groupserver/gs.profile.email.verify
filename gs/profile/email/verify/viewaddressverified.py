# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013, 2014 OnlineGroups.net and Contributors.
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
from urllib import unquote
from zope.component import createObject
from gs.content.base import SitePage


class AddressVerifiedView(SitePage):

    def __call__(self):
        assert self.request
        assert self.context
        assert hasattr(self.request, 'form'), 'No form in request'
        assert 'email' in self.request.form, 'No email in form'

        email = unquote(self.request.form['email'])
        eu = createObject('groupserver.EmailUserFromEmailAddress',
                          self.context, email)
        try:
            verified = eu.is_address_verified(email)
        except AttributeError:
            retval = '-1'
        else:
            retval = '1' if verified else '0'
        return retval
