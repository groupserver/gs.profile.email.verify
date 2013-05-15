# -*- coding: utf-8 -*-
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
        verified = eu.is_address_verified(email)
        retval = '1' if verified else '0'
        return retval
