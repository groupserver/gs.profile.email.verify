# coding=utf-8
from zope.component import createObject
from Products.Five import BrowserView
from Products.CustomUserFolder.interfaces import IGSUserInfo

class VerifyEmailPage(BrowserView):
    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        self.label = u'Verify Email'
        self.userInfo = IGSUserInfo(self.context)
        self.__siteInfo = None
        self.verificationId = request.form.get('verificationId','')
        self.email = 'admin-foo@groupsense.net'
        
    @property
    def siteInfo(self):
        if self.__siteInfo == None:
            self.__siteInfo = createObject('groupserver.SiteInfo', 
                self.context)
        return self.__siteInfo
    
    