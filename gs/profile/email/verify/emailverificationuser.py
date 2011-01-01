# coding=utf-8
import time, md5
from zope.component import createObject
from zope.component.factory import Factory
from zope.interface import implements
from Products.XWFCore.XWFUtils import convert_int2b62, get_support_email
from Products.CustomUserFolder.interfaces import IGSUserInfo
from gs.profile.notify.notifyuser import NotifyUser
from verifyemailuser import VerificationIdNotFoundError
from queries import EmailQuery, VerificationQuery
from audit import Auditor, VERIFIED, ADD_VERIFY, CLEAR_VERIFY
from createmessage import create_verification_message
from interfaces import IGSEmailVerificationUser

class EmailVerificationUser(object):
    implements(IGSEmailVerificationUser)
    """ Adapts a userInfo and one of their email addresses  
        to an IGSEmailVerificationUser, which can request 
        verification for, and verify, that email address. 
    """
    def __init__(self, context, userInfo, email):
        self.context = context
        self.userInfo = userInfo
        self.email = email
        
        self.__auditor = self.__siteInfo = None
        self.__verifyQuery = self.__userQuery = None
        
        assert email in userInfo.user.get_emailAddresses(), \
          'Address %s does not belong to %s (%s)' %\
           (email, userInfo.name, userInfo.id)

    @property
    def auditor(self):
        if self.__auditor == None:
            self.__auditor = Auditor(self.context, self.siteInfo)
        return self.__auditor
    
    @property
    def siteInfo(self):
        if self.__siteInfo == None:
            self.__siteInfo = \
              createObject('groupserver.SiteInfo', self.context)
        return self.__siteInfo
        
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

    def send_verification_message(self):
        verificationId = self.create_verification_id()
        self.add_verification_id(verificationId)

        notifyUser = NotifyUser(self.userInfo.user, self.siteInfo)
        fromAddr = get_support_email(self.userInfo.user, self.siteInfo.id)
        msg = create_verification_message(self.userInfo, self.siteInfo,
                self.email, fromAddr, verificationId)
        notifyUser.send_message(msg, self.email, fromAddr)

    def create_verification_id(self):
        # Let us hope that the verification ID *is* unique
        vNum = long(md5.new(time.asctime() + self.email).hexdigest(), 16)
        verificationId = str(convert_int2b62(vNum))
        assert type(verificationId) == str
        return verificationId
    
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

class EmailVerificationUserFromId(object):
    ''' Create an Email Verification User from a Verification ID.
    '''
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
        
        email = queries.get_email_from_verificationId(verificationId)
        assert email in user.get_emailAddresses(), \
          'Address %s does not belong to %s (%s)' %\
          (email, userInfo.name, userInfo.id)

        return EmailVerificationUser(context, userInfo, email)

EmailVerificationUserFromIdFactory = Factory(
        EmailVerificationUserFromId, 
        'Email-Verification User from ID',
        'Create an email-verification user from a verification ID.')

class EmailVerificationUserFromEmail(object):
    ''' Create an Email Verification User from an email address.
    '''
    def __call__(self, context, email):
        aclUsers = context.site_root().acl_users
        user = aclUsers.get_userByEmail(email)
        assert user, 'No user for email address %s' % email
        userInfo = IGSUserInfo(user)
        return EmailVerificationUser(context, userInfo, email)

EmailVerificationUserFromEmailFactory = Factory(
        EmailVerificationUserFromEmail, 
        'Email-Verification User from Email',
        'Create an email-verification user from an email address.')
