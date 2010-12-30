# coding=utf-8
from zope.contentprovider.interfaces import IContentProvider
from zope.interface import Interface
from zope.schema import ASCIILine, Text, TextLine
from Products.GSProfile.emailaddress import EmailAddress
from Products.CustomUserFolder.interfaces import IGSUserInfo

class IGSEmailUser(Interface):
    ''' Adapts an email address to an IGSEmailUser, which can
        request verification for, and verify, email addresses.
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

class IGSEmailVerifyUser(IGSUserInfo):
    ''' Adapts a user to be able to log them in and redirect them
        appropriately, provided the verificationId they authenticate 
        with exists and is current. 
    '''
    def verificationId_current(verificationId):
        ''' Returns TRUE if the verificationId exists
            and has not yet been used. 
        '''
        
    def verificationId_exists(verificationId):
        ''' Returns TRUE if the verificationId exists.
        '''

class IVerifyEmail(Interface):
    """Schema for verifying the email address."""
      
    verificationId = ASCIILine(title=u'Verification ID',
        description=u'The verification ID',
        required=False)

class IRequestVerification(Interface):
    email = EmailAddress(title=u'Email Address',
        description=u'Your email address.',
        required=True)

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
    