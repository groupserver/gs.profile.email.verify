# coding=utf-8
from zope.component import createObject
from Products.Five import BrowserView
from Products.CustomUserFolder.interfaces import IGSUserInfo
from queries import VerificationQuery

class VerifyEmailPage(BrowserView):
    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        self.label = u'Verify Email'
        self.userInfo = IGSUserInfo(self.context)
        self.verificationId = request.form.get('verificationId','')
        self.__siteInfo = self.__query = self.__email = None

    @property
    def email(self):
        if self.__email == None:
            self.__email = \
              self.query.get_email_from_verificationId(self.verificationId)
        return self.__email
    
    @property
    def query(self):
        if self.__query == None:
            self.__query = \
              VerificationQuery(self.context.zsqlalchemy)
        return self.__query
    
    @property
    def siteInfo(self):
        if self.__siteInfo == None:
            self.__siteInfo = createObject('groupserver.SiteInfo', 
                self.context)
        return self.__siteInfo
    
    