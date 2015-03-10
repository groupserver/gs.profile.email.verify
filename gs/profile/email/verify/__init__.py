# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from zope.i18nmessageid import MessageFactory
GSMessageFactory = MessageFactory('gs.profile.email.verify')

from AccessControl import ModuleSecurityInfo
from AccessControl import allow_class
#lint:disable
from .emailverificationuser import EmailVerificationUser, \
    EmailVerificationUserFromUser, VerificationIdExists, \
    VerificationIdNotFound, VerificationIdUsed, NoUserForVerificationId
#lint:enable

allow_class(EmailVerificationUserFromUser)
moduleId = 'gs.profile.email.verify.emailverificationuser'
evu_security = ModuleSecurityInfo(moduleId)
evu_security.declarePublic('EmailVerificationUser')
