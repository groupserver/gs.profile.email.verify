# coding=utf-8
from Products.Five import BrowserView
from queries import VerificationQuery
from emailuser import EmailUser
from emailverifyuser import EmailVerifyUser 

class VerifyEmail(BrowserView):
    def __init__(self, context, request):
        assert context
        assert request
        self.context = context
        self.request = request
        self.query = VerificationQuery(context.zsqlalchemy)
        
    def __call__(self):
        assert self.request
        assert self.context
        assert self.query
        assert hasattr(self.request, 'form'), 'No form in request'
        assert 'verificationId' in self.request.form.keys(), 'No verificationId in form'
        verificationId = self.request.form['verificationId']
        email = self.query.get_email_from_verificationId(verificationId)
        eu = EmailUser(self.context, email)
        evu = EmailVerifyUser(eu.userInfo)
        if evu.verificationId_current(verificationId):
            eu.verify_email(verificationId)
        