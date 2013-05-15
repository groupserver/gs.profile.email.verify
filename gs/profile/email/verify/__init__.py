# -*- coding: utf-8 -*-
from AccessControl import ModuleSecurityInfo
from AccessControl import allow_class
from gs.profile.email.verify.emailverificationuser import \
    EmailVerificationUserFromUser
allow_class(EmailVerificationUserFromUser)


moduleId = 'gs.profile.email.verify.emailverificationuser'
evu_security = ModuleSecurityInfo(moduleId)
evu_security.declarePublic('EmailVerificationUser')
