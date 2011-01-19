# coding=utf-8
from zope.contentprovider.interfaces import IContentProvider
from zope.interface import Interface
from zope.schema import Text, TextLine
from gs.profile.email.base.emailaddress import EmailAddress
from Products.CustomUserFolder.interfaces import IGSUserInfo

class IGSEmailVerificationUser(Interface):
    ''' Adapts a user to an IGSEmailVerificationUser, which can
        request verification for, and verify, a particular email 
        address.
    '''
    def add_verification_id(verificationId):
        ''' Adds the verificationId for the email address to 
            the email_verification table, provided the 
            verificationId does not already exist in the table.
        '''
    
    def verify_email(verificationId):
        ''' Verifies the email address in the user_email table,
            and updates all relevant rows in the email_verification
            table (via clear_verification_ids), provided the 
            verificationId exists and is current.
        '''
        
    def clear_verification_ids():
        ''' Updates all rows for the email address in the 
            email_verification table to be verified. 
        '''

class IGSVerifyEmailUser(IGSUserInfo):
    ''' Adapts a user to be able to verify an email address
        using a particular verificationId, provided that 
        that verificationId exists and is current. 
    '''
    def verificationId_current(verificationId):
        ''' Returns TRUE if the verificationId exists
            and has not yet been used. 
        '''
        
    def verificationId_exists(verificationId):
        ''' Returns TRUE if the verificationId exists.
        '''

class IGSVerifyingJavaScriptContentProvider(IContentProvider):
    pageTemplateFileName = Text(title=u"Page Template File Name",
      description=u'The name of the ZPT file that is used to render the '\
        u'javascript.',
      required=False,
      default=u"browser/templates/verify_javascript.pt")
    
    verificationId = TextLine(title=u'Verification ID',
        description=u'The verification identifier',
        required=True)
      
    email = EmailAddress(title=u'Email Address',
        description=u'Your email address.',
        required=True)
    
    siteName = TextLine(title=u'Site Name',
        description=u'The site name',
        required=True)
    