# coding=utf-8
from zope.component import createObject
from Products.GSRedirect.view import GSRedirectBase
from Products.GSProfile.utils import login
from emailverifyuser import VerificationIdNotFoundError
from audit import Auditor, VERIFY_LOGIN, VERIFY_ID_400, VERIFY_ID_404,\
    VERIFY_ID_410

class RedirectEmailVerification(GSRedirectBase):
    def __call__(self):
        siteInfo = createObject('groupserver.SiteInfo', self.context)
        auditor = Auditor(self.context, siteInfo)

        if len(self.traverse_subpath) == 1:
            # A verification ID is present
            verificationId = self.traverse_subpath[0]
            try:
                emailVerificationUser = \
                    createObject('groupserver.EmailVerificationUser', 
                                    self.context, verificationId)
            except VerificationIdNotFoundError, e:
                auditor.info(VERIFY_ID_404, instanceDatum=verificationId)
                uri = '/email-verify-not-found.html?verificationId=%s' % \
                    verificationId
            else:
                if emailVerificationUser.verificationId_current(verificationId):
                    auditor.info(VERIFY_LOGIN, emailVerificationUser)
                    # Only log in when able to verify the email address
                    login(self.context, emailVerificationUser.user)
                    uri = emailVerificationUser.emailVerifyUrl
                else:
                    auditor.info(VERIFY_ID_410, emailVerificationUser, 
                        verificationId)
                    uri = '/email-verify-used.html?verificationId=%s' %\
                        verificationId
        else:
            auditor.info(VERIFY_ID_400)
            # No verification ID is present
            uri = '/email-verify-no-id.html'
        assert uri, 'URI not set'
        return self.request.RESPONSE.redirect(uri)
