# coding=utf-8
from zope.component import createObject
from zope.component.factory import Factory
from queries import EmailVerifyQuery
from Products.CustomUserFolder.userinfo import GSUserInfo
from Products.CustomUserFolder.interfaces import IGSUserInfo

class EmailVerifyUser(GSUserInfo):
    def __init__(self, userInfo):
        GSUserInfo.__init__(self, userInfo.user)
        self.__query = None
    
    @property
    def query(self):
        if self.__query == None:
            da = self.user.zsqlalchemy
            self.__query = EmailVerifyQuery(da)
        return self.__query
        
    def verificationId_current(self, verificationId):
        return self.query.verificationId_status(verificationId) == self.query.CURRENT
    
    def verificationId_exists(self, verificationId):
        return self.query.verificationId_status(verificationId) != self.query.NOT_FOUND

class VerificationIdNotFoundError(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return 'Could not find verification ID (%s)' % self.value

class EmailVerifyUserFromId(object):
    '''Create an Email Verify User from a Verification ID
    
    We do not always have a IGSUserInfo to hand when we want an 
    email-verify user. Sometimes we have a verification ID.'''
    def __call__(self, context, verificationId):
    
        da = context.zsqlalchemy
        queries = EmailVerifyQuery(da)
        
        s = queries.verificationId_status(verificationId)
        if s == queries.NOT_FOUND:
            raise VerificationIdNotFoundError(verificationId)

        email = queries.get_email_from_verificationId(verificationId)
        aclUsers = context.site_root().acl_users
        user = aclUsers.get_userByEmail(email)
        if not user:
            raise VerificationIdNotFoundError(verificationId) # TODO
        
        userInfo = IGSUserInfo(user)
        return EmailVerifyUser(userInfo)

EmailVerifyUserFactory = Factory(
                        EmailVerifyUserFromId, 
                        'Email-Verify User from ID',
                        'Create an email-verify user from a verification ID.')

