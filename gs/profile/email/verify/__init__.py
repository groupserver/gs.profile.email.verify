# coding=utf-8
from AccessControl import ModuleSecurityInfo
from AccessControl import allow_class

evu_security = ModuleSecurityInfo('gs.profile.email.verify.emailverificationuser')
evu_security.declarePublic('EmailVerificationUser')

from gs.profile.email.verify.emailverificationuser import EmailVerificationUserFromUser
allow_class(EmailVerificationUserFromUser)

import verifyingcontentprovider
