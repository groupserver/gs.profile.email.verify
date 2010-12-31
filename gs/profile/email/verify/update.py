# coding=utf-8
from zope.component import createObject
from Products.Five import BrowserView
from verifyemailuser import VerifyEmailUser 

class VerifyEmail(BrowserView):
    def __init__(self, context, request):
        assert context
        assert request
        self.context = context
        self.request = request
        
    def __call__(self):
        assert self.request
        assert self.context
        assert hasattr(self.request, 'form'), 'No form in request'
        assert 'verificationId' in self.request.form.keys(), 'No verificationId in form'
        vId = self.request.form['verificationId']
        evu = createObject('groupserver.EmailVerificationUserFromId', 
                            self.context, vId)
        veu = VerifyEmailUser(evu.userInfo)
        if veu.verificationId_current(vId):
            evu.verify_email(vId)
        