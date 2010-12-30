# coding=utf-8
from zope.component import createObject
from zope.interface import implements
from Products.CustomUserFolder.interfaces import IGSUserInfo
from queries import EmailQuery, VerificationQuery
from audit import Auditor, VERIFIED, ADD_VERIFY, CLEAR_VERIFY
from interfaces import IGSEmailUser

class EmailUser(object):
    implements(IGSEmailUser)
    """ Adapts an email address to an IGSEmailUser, which can
        request verification for, and verify, email addresses. 
    """
    def __init__(self, context, email):
        self.context = context
        self.email = email
        self.__userInfo = self.__auditor = None
        self.__verifyQuery = self.__userQuery = None
        assert self.userInfo.user, 'No user for email address %s' % email
        
    def __nonzero__(self):
        return bool(self.userInfo.user)
    
    @property
    def userInfo(self):
        if self.__userInfo == None:
            aclUsers = self.context.site_root().acl_users
            user = aclUsers.get_userByEmail(self.email)
            self.__userInfo = IGSUserInfo(user)
        return self.__userInfo
    
    @property
    def auditor(self):
        if self.__auditor == None:
            si = createObject('groupserver.SiteInfo', self.context)
            self.__auditor = Auditor(self.context, si)
        return self.__auditor
        
    @property
    def verifyQuery(self):
        if self.__verifyQuery == None:
            da = self.context.zsqlalchemy
            self.__verifyQuery = VerificationQuery(da)
        return self.__verifyQuery
    
    @property
    def userQuery(self):
        if self.__userQuery == None:
            da = self.context.zsqlalchemy
            self.__userQuery = EmailQuery(da, self.email)
        return self.__userQuery

    def add_verification_id(self, verificationId):
        assert verificationId, 'No verificationId'
        idStatus = self.verifyQuery.verificationId_status(verificationId)
        assert idStatus == self.verifyQuery.NOT_FOUND, \
          'Email Verification ID %s exists' % verificationId
        self.userQuery.set_verification_id(verificationId)
        self.auditor.info(ADD_VERIFY, self.userInfo, self.email)
        
    def verify_email(self, verificationId):
        assert verificationId, 'No verification ID'
        idStatus = self.verifyQuery.verificationId_status(verificationId)
        assert idStatus != self.verifyQuery.NOT_FOUND, \
          'Verification ID %s not found' % verificationId
        assert idStatus != self.verifyQuery.VERIFIED, \
          'Verification ID %s already used' % verificationId
        assert idStatus == self.verifyQuery.CURRENT, \
          'Status of email verification ID %s is not ' \
          'one of CURRENT, VERIFIED or NOT_FOUND.' % verificationId

        self.userQuery.verify_address(verificationId)
        self.auditor.info(VERIFIED, self.userInfo, self.email)
        self.clear_verification_ids()
    
    def clear_verification_ids(self):
        self.userQuery.clear_verification_ids()
        self.auditor.info(CLEAR_VERIFY, self.userInfo, self.email)
