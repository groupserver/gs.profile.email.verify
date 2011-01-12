# coding=utf-8
from pytz import UTC
from datetime import datetime
from zope.component import createObject
from zope.component.interfaces import IFactory
from zope.interface import implements, implementedBy
from Products.GSAuditTrail import IAuditEvent, BasicAuditEvent, \
  AuditQuery, event_id_from_data
from Products.XWFCore.XWFUtils import munge_date
from Products.CustomUserFolder.userinfo import userInfo_to_anchor

SUBSYSTEM = 'gs.profile.email.verify'
import logging
log = logging.getLogger(SUBSYSTEM) #@UndefinedVariable

UNKNOWN      = '0'
# verification user
VERIFIED     = '1'
ADD_VERIFY   = '2'
CLEAR_VERIFY = '3'
# Not implemented: currently handled by 
#  Products.XWFMailingListManager.bounceaudit
UNVERIFIED   = '4'
# redirect
VERIFY_LOGIN  = '7'
VERIFY_ID_400 = '8'
VERIFY_ID_404 = '9'
VERIFY_ID_410 = '10'


class AuditEventFactory(object):
    implements(IFactory)

    title=u'Email Verification Audit-Event Factory'
    description=u'Creates a GroupServer audit event for email address verification'

    def __call__(self, context, event_id, code, date,
        userInfo, instanceUserInfo, siteInfo, groupInfo=None,
        instanceDatum='', supplementaryDatum='', subsystem=''):
        if code == VERIFIED:
            event = VerifiedEvent(context, event_id, date, 
                        instanceUserInfo, siteInfo, instanceDatum,
                        supplementaryDatum)
        elif code == ADD_VERIFY:
            event = AddVerifyEvent(context, event_id, date, userInfo,
                        instanceUserInfo, siteInfo, instanceDatum)
        elif code == CLEAR_VERIFY:
            event = ClearVerifyEvent(context, event_id, date, 
                        instanceUserInfo, siteInfo, instanceDatum)
        elif code == VERIFY_LOGIN:
            event = VerifyLoginEvent(context, event_id, date, 
                        instanceUserInfo, siteInfo)
        elif code == VERIFY_ID_400:
            event = VerifyLoginNoIdEvent(context, event_id, date,
                        siteInfo)
        elif code == VERIFY_ID_404:
            event = VerifyLoginIdNotFoundEvent(context, event_id, date,
                        siteInfo, instanceDatum)
        elif code == VERIFY_ID_410:
            event = VerifyLoginIdUsedEvent(context, event_id, date,
                        instanceUserInfo, siteInfo, instanceDatum)
        else:
            event = BasicAuditEvent(context, event_id, UNKNOWN, date, 
              userInfo, instanceUserInfo, siteInfo, groupInfo, 
              instanceDatum, supplementaryDatum, SUBSYSTEM)
        assert event
        return event
    
    def getInterfaces(self):
        return implementedBy(BasicAuditEvent)
        
class VerifiedEvent(BasicAuditEvent):
    ''' An audit-trail event representing a person verifying an email address.'''
    implements(IAuditEvent)

    def __init__(self, context, id, d, userInfo, siteInfo, instanceDatum, supplementaryDatum):
        BasicAuditEvent.__init__(self, context, id,  VERIFIED, d, 
            userInfo, userInfo, siteInfo, None, instanceDatum, 
            supplementaryDatum, SUBSYSTEM)
    
    def __unicode__(self):
        retval = u'%s (%s) verified the email address <%s> on %s (%s) '\
          u'using the verification code %s.' %\
           (self.userInfo.name, self.userInfo.id,
            self.instanceDatum,
            self.siteInfo.name, self.siteInfo.id,
            self.supplementaryDatum)
        return retval
        
    def __str__(self):
        retval = unicode(self).encode('ascii', 'ignore')
        return retval
    
    @property
    def xhtml(self):
        cssClass = u'audit-event gs-profile-email-verify-%s' %\
          self.code
        retval = u'<span class="%s">Verified the address '\
          u'<code class="email">%s</code>.</span>' % \
          (cssClass, self.instanceDatum)
        retval = u'%s (%s)' % \
          (retval, munge_date(self.context, self.date))
        return retval

class AddVerifyEvent(BasicAuditEvent):
    ''' An audit-trail event representing a person adding a
        verification request for an email address.'''
    implements(IAuditEvent)

    def __init__(self, context, id, d, userInfo, instanceUserInfo, 
                 siteInfo, instanceDatum):
        BasicAuditEvent.__init__(self, context, id,  ADD_VERIFY, d, 
            userInfo, instanceUserInfo, siteInfo, None, instanceDatum, 
            None, SUBSYSTEM)

    @property
    def adminAdded(self):
        retval = False
        if self.userInfo.id and self.userInfo.id!= self.instanceUserInfo.id:
            retval = True
        return retval
    
    def __unicode__(self):
        if self.adminAdded:
            retval = u'%s (%s) added a verification request for '\
              '<%s> for %s (%s) on %s (%s).' %\
               (self.userInfo.name, self.userInfo.id,
                self.instanceDatum,
                self.instanceUserInfo.name, self.instanceUserInfo.id,
                self.siteInfo.name, self.siteInfo.id)
        else:
            retval = u'%s (%s) added a verification request for '\
              '<%s> on %s (%s).' %\
               (self.instanceUserInfo.name, self.instanceUserInfo.id,
                self.instanceDatum,
                self.siteInfo.name, self.siteInfo.id)
        return retval
        
    def __str__(self):
        retval = unicode(self).encode('ascii', 'ignore')
        return retval
    
    @property
    def xhtml(self):
        cssClass = u'audit-event gs-profile-email-verify-%s' %\
          self.code
        if self.adminAdded:
            retval = u'<span class="%s">%s added a verification request '\
              u'for <code class="email">%s</code>.</span>' % \
              (cssClass, userInfo_to_anchor(self.userInfo), 
               self.instanceDatum)
        else:
            retval = u'<span class="%s">Added a verification request '\
              u'for <code class="email">%s</code>.</span>' % \
              (cssClass, self.instanceDatum)
        retval = u'%s (%s)' % \
          (retval, munge_date(self.context, self.date))
        return retval

class ClearVerifyEvent(BasicAuditEvent):
    ''' An audit-trail event representing a person clearing all verification
        IDs for an email address.'''
    implements(IAuditEvent)

    def __init__(self, context, id, d, userInfo, siteInfo, instanceDatum):
        BasicAuditEvent.__init__(self, context, id,  CLEAR_VERIFY, d, 
            userInfo, userInfo, siteInfo, None, instanceDatum, None,
            SUBSYSTEM)
    
    def __unicode__(self):
        retval = u'%s (%s) cleared all email verification IDs '\
          'for <%s> on %s (%s).' %\
           (self.userInfo.name, self.userInfo.id,
            self.instanceDatum,
            self.siteInfo.name, self.siteInfo.id)
        return retval
        
    def __str__(self):
        retval = unicode(self).encode('ascii', 'ignore')
        return retval
    
    @property
    def xhtml(self):
        cssClass = u'audit-event gs-profile-email-verify-%s' %\
          self.code
        retval = u'<span class="%s">Cleared email verification '\
          u'IDs for <code class="email">%s</code>.</span>' % \
          (cssClass, self.instanceDatum)
        retval = u'%s (%s)' % \
          (retval, munge_date(self.context, self.date))
        return retval

class VerifyLoginEvent(BasicAuditEvent):
    ''' An audit-trail event representing a person logging in upon
        verifying his or her email address.'''
    implements(IAuditEvent)

    def __init__(self, context, id, d, userInfo, siteInfo):
        BasicAuditEvent.__init__(self, context, id, VERIFY_LOGIN, d, 
            userInfo, userInfo, siteInfo, None, None, None, SUBSYSTEM)
    
    def __unicode__(self):
        retval = u'Logging in %s (%s) and sending the user to the '\
            u'email verified page on %s (%s). ' %\
            (self.userInfo.name,  self.userInfo.id,
             self.siteInfo.name,  self.siteInfo.id)
        return retval
        
    def __str__(self):
        retval = unicode(self).encode('ascii', 'ignore')
        return retval
    
    @property
    def xhtml(self):
        cssClass = u'audit-event gs-profile-email-verify-%s' %\
          self.code
        retval = u'<span class="%s">Logging in for email '\
            u'verification.</span>' % cssClass
        retval = u'%s (%s)' % \
          (retval, munge_date(self.context, self.date))
        return retval

class VerifyLoginNoIdEvent(BasicAuditEvent):
    ''' An audit-trail event representing a email-verify with no ID.'''
    implements(IAuditEvent)

    def __init__(self, context, id, d, siteInfo):
        BasicAuditEvent.__init__(self, context, id, VERIFY_ID_400, d, 
            None, None, siteInfo, None, None, None, SUBSYSTEM)
    
    def __unicode__(self):
        retval = u'Email verification on %s (%s) with no ID.' %\
            (self.siteInfo.name,  self.siteInfo.id)
        return retval
        
    def __str__(self):
        retval = unicode(self).encode('ascii', 'ignore')
        return retval
    
    @property
    def xhtml(self):
        cssClass = u'audit-event gs-profile-email-verify-%s' %\
          self.code
        retval = u'<span class="%s">No ID with email '\
            u'verification.</span>' % cssClass
        retval = u'%s (%s)' % \
          (retval, munge_date(self.context, self.date))
        return retval

# VERIFY_ID_404
class VerifyLoginIdNotFoundEvent(BasicAuditEvent):
    ''' An audit-trail event representing an email-verify with an unknown ID.'''
    implements(IAuditEvent)

    def __init__(self, context, id, d, siteInfo, instanceDatum):
        BasicAuditEvent.__init__(self, context, id, VERIFY_ID_404, d, 
            None, None, siteInfo, None, instanceDatum, None, SUBSYSTEM)
    
    def __unicode__(self):
        retval = u'Email-verify on %s (%s) but the ID was not '\
            u'found (%s).' % \
            (self.siteInfo.name,  self.siteInfo.id,
            self.instanceDatum)
        return retval
        
    def __str__(self):
        retval = unicode(self).encode('ascii', 'ignore')
        return retval
    
    @property
    def xhtml(self):
        cssClass = u'audit-event gs-profile-email-verify-%s' %\
          self.code
        retval = u'<span class="%s">Email verification ID %s not '\
            u'found.</span>' % (cssClass, self.instanceDatum)
        retval = u'%s (%s)' % \
          (retval, munge_date(self.context, self.date))
        return retval

# VERIFY_ID_410
class VerifyLoginIdUsedEvent(BasicAuditEvent):
    ''' An audit-trail event representing someone following a used
        email-verify link.'''
    implements(IAuditEvent)

    def __init__(self, context, id, d, userInfo, siteInfo,
                instanceDatum):
        BasicAuditEvent.__init__(self, context, id, VERIFY_ID_410, d, 
            userInfo, userInfo, siteInfo, None, instanceDatum, None,
            SUBSYSTEM)
    
    def __unicode__(self):
        retval = u'The user %s (%s) followed a used email-verify '\
            u'link (%s) on %s (%s).' % \
            (self.userInfo.name, self.userInfo.id,
            self.instanceDatum,
            self.siteInfo.name,  self.siteInfo.id)
        return retval
        
    def __str__(self):
        retval = unicode(self).encode('ascii', 'ignore')
        return retval
    
    @property
    def xhtml(self):
        cssClass = u'audit-event gs-profile-email-verify-%s' %\
          self.code
        retval = u'<span class="%s">Followed a used email-verify '\
            u'link.</span>' % cssClass
        retval = u'%s (%s)' % \
          (retval, munge_date(self.context, self.date))
        return retval

class Auditor(object):
    def __init__(self, context, siteInfo):
        self.siteInfo = siteInfo
        self.context = context
        da = context.zsqlalchemy
        self.queries = AuditQuery(da)
        self.factory = AuditEventFactory()
        
    def info(self, code, instanceUserInfo='', instanceDatum = '', 
                supplementaryDatum = ''):
        d = datetime.now(UTC)
        userInfo = createObject('groupserver.LoggedInUser', self.context)
        instanceUserInfo = instanceUserInfo and instanceUserInfo or userInfo 
        eventId = event_id_from_data(userInfo, instanceUserInfo, 
                    self.siteInfo, code,
                    instanceDatum, supplementaryDatum)
          
        e = self.factory(self.context, eventId,  code, d, 
                userInfo, instanceUserInfo, self.siteInfo, None,
                instanceDatum, supplementaryDatum, SUBSYSTEM)
          
        self.queries.store(e)
        log.info(e)

