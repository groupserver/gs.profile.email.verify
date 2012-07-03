# coding=utf-8
import pytz, datetime
import sqlalchemy as sa
from gs.database import getTable, getSession
from zope.sqlalchemy import mark_changed

class EmailQuery(object):
    def __init__(self, email):
        self.email = email
        self.userEmailTable = getTable('user_email')
        self.emailVerifyTable = getTable('email_verification')
        
    def set_verification_id(self, verificationId):
        assert verificationId, 'No verificationId'
        evt = self.emailVerifyTable
        i = evt.insert()
        d = {'verification_id': verificationId, 
             'email': self.email}

        session = getSession()
        session.execute(i, params=d)
        mark_changed(session)

    def verify_address(self, verificationId):
        assert verificationId, 'No verificationId'
        uet = self.userEmailTable
        u = uet.update(sa.func.lower(uet.c.email) == self.email.lower())
        d = {'verified_date': 
             datetime.datetime.utcnow().replace(tzinfo=pytz.utc)}

        session = getSession()
        session.execute(u, params=d)
        mark_changed(session)

    def clear_verification_ids(self):
        evt = self.emailVerifyTable
        u = evt.update(sa.and_(evt.c.email == self.email,
                               evt.c.verified == None))
        now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        d = {'verified': now}

        session = getSession()
        session.execute(u, params=d)
        mark_changed(session)

    def unverify_address(self):
        uet = self.userEmailTable
        u = uet.update(sa.func.lower(uet.c.email) == self.email.lower())
        d = {'verified_date': None}

        session = getSession()
        session.execute(u, params=d)
        mark_changed(session)

class VerificationQuery(object):
    NOT_FOUND  = 0
    CURRENT    = 1
    VERIFIED   = 2
    
    def __init__(self):
        self.userEmailTable = getTable('user_email')
        self.emailVerifyTable = getTable('email_verification')
        
    def get_email_from_verificationId(self, verificationId):
        evt = self.emailVerifyTable
        s = sa.select([evt.c.email], limit=1)
        s.append_whereclause(evt.c.verification_id == verificationId)

        session = getSession()
        r = session.execute(s).fetchone()
        retval = r and r['email'] or ''
        assert type(retval) in (str, unicode), 'Wrong return type "%s"' % \
            type(retval)
        return retval
    
    def get_userId_from_verificationId(self, verificationId):
        retval = ''
        email = self.get_email_from_verificationId(verificationId)
        if email:
            uet = self.userEmailTable
            s = sa.select([uet.c.user_id], limit=1)
            s.append_whereclause(sa.func.lower(uet.c.email) == email.lower())

            session = getSession()
            r = session.execute(s).fetchone()
            retval = r and r['user_id'] or ''
            assert retval, 'No userId in user_email table for '\
              'address %s in email_verification table' % email
        assert type(retval) in (str, unicode), 'Wrong return type "%s"' % \
            type(retval)
        return retval

    def verificationId_status(self, verificationId):
        evt = self.emailVerifyTable
        s = sa.select([evt.c.verified], limit=1)
        s.append_whereclause(evt.c.verification_id == verificationId)
        
        session = getSession()
        r  = session.execute(s).fetchone()
        if r:
            if r['verified'] == None:
                retval = self.CURRENT
            else:
                retval = self.VERIFIED
        else:
            retval = self.NOT_FOUND
        assert retval in (self.NOT_FOUND, self.CURRENT, self.VERIFIED)
        return retval

