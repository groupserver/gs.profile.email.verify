# coding=utf-8
from zope.component import createObject, getMultiAdapter
from zope.cachedescriptors.property import Lazy
from gs.profile.notify.sender import MessageSender
UTF8 = 'utf-8'

class Notifier(object):
    textTemplateName = 'verification-mesg.txt'
    htmlTemplateName = 'verification-mesg.html'
    
    def __init__(self, user, request):
        self.context = self.user = user
        self.request = request

    @Lazy
    def textTemplate(self):
        retval = getMultiAdapter((self.context, self.request), 
                    name=self.textTemplateName)
        assert retval
        return retval

    @Lazy
    def htmlTemplate(self):
        retval = getMultiAdapter((self.context, self.request), 
                    name=self.htmlTemplateName)
        assert retval
        return retval
        
    def notify(self, userInfo, emailAddress, verifyLink):
        subject = u'Verify your email address (action required)'.encode(UTF8)
        text = self.textTemplate(userInfo=userInfo, 
                    emailAddress=emailAddress, verifyLink=verifyLink)
        html = self.htmlTemplate(userInfo=userInfo, 
                    emailAddress=emailAddress, verifyLink=verifyLink)
        ms = MessageSender(self.context, userInfo)
        ms.send_message(subject, text, html, toAddresses=[emailAddress])

