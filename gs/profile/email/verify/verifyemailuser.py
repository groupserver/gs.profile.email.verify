# coding=utf-8
from zope.component import createObject
from zope.component.factory import Factory
from queries import VerificationQuery
from Products.CustomUserFolder.userinfo import GSUserInfo
from Products.CustomUserFolder.interfaces import IGSUserInfo

class VerifyEmailUser(GSUserInfo):
    def __init__(self, userInfo):
        GSUserInfo.__init__(self, userInfo.user)
        self.__emailVerifyUrl = self.__query = None
    
    @property
    def emailVerifyUrl(self):
        if self.__emailVerifyUrl == None:
            self.__emailVerifyUrl = '%s/verifyemail.html' % self.url
        return self.__emailVerifyUrl
    
    @property
    def query(self):
        if self.__query == None:
            da = self.user.zsqlalchemy
            self.__query = VerificationQuery(da)
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

class VerifyEmailUserFromId(object):
    ''' Create a Verify Email User from a Verification ID
    
        We do not always have an IGSUserInfo to hand when we want a 
        verify-email user. Sometimes we do have a verification ID.'''
    def __call__(self, context, verificationId):
    
        da = context.zsqlalchemy
        queries = VerificationQuery(da)
        
        s = queries.verificationId_status(verificationId)
        if s == queries.NOT_FOUND:
            raise VerificationIdNotFoundError(verificationId)

        userId = queries.get_userId_from_verificationId(verificationId)
        aclUsers = context.site_root().acl_users
        user = aclUsers.getUser(userId)
        assert user, 'No user for userId %s' % userId
        
        userInfo = IGSUserInfo(user)
        return VerifyEmailUser(userInfo)

VerifyEmailUserFactory = Factory(
                        VerifyEmailUserFromId, 
                        'Verify-Email User from ID',
                        'Create a verify-email user from a verification ID.')

