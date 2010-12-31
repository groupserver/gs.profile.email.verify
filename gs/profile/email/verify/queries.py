# coding=utf-8
import pytz, datetime
import sqlalchemy as sa

class EmailQuery(object):
    def __init__(self, da, email):
        assert da, 'No da'
        assert email, 'No email'
        self.email = email
        self.userEmailTable = da.createTable('user_email')
        self.emailVerifyTable = da.createTable('email_verification')
        # One day we will have constraints
        aclUsers = da.site_root().acl_users
        user = aclUsers.get_userByEmail(email)
        assert user, 'No user for email address %s' % email
        
    def set_verification_id(self, verificationId):
        assert verificationId, 'No verificationId'
        evt = self.emailVerifyTable
        i = evt.insert()
        i.execute(verification_id = verificationId, 
                  email = self.email)

    def verify_address(self, verificationId):
        assert verificationId, 'No verificationId'
        uet = self.userEmailTable
        d = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        s = uet.update(sa.func.lower(uet.c.email) == self.email.lower())
        s.execute(verified_date = d)

    def clear_verification_ids(self):
        evt = self.emailVerifyTable
        u = evt.update(sa.and_(evt.c.email == self.email,
                               evt.c.verified == None))
        d = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        u.execute(verified = d)

    def unverify_address(self):
        uet = self.userEmailTable
        s = uet.update(sa.func.lower(uet.c.email) == self.email.lower())
        s.execute(verified_date = None)

class VerificationQuery(object):
    NOT_FOUND  = 0
    CURRENT    = 1
    VERIFIED   = 2
    
    def __init__(self, da):
        self.userEmailTable = da.createTable('user_email')
        self.emailVerifyTable = da.createTable('email_verification')
        
    def get_email_from_verificationId(self, verificationId):
        evt = self.emailVerifyTable
        s = evt.select()
        s.append_whereclause(evt.c.verification_id == verificationId)
        r = s.execute().fetchone()
        retval = r and r['email'] or ''
        assert type(retval) == str
        return retval
    
    def get_userId_from_verificationId(self, verificationId):
        retval = ''
        email = self.get_email_from_verificationId(verificationId)
        if email:
            uet = self.userEmailTable
            s = uet.select()
            s.append_whereclause(sa.func.lower(uet.c.email) == email)
            r = s.execute().fetchone()
            retval = r and r['user_id'] or ''
            assert retval, 'No userId in user_email table for '\
              'address %s in email_verification table' % email
        assert type(retval) == str
        return retval

    def verificationId_status(self, verificationId):
        evt = self.emailVerifyTable
        s = evt.select()
        s.append_whereclause(evt.c.verification_id == verificationId)
        
        r  = s.execute().fetchone()
        if r:
            if r['verified'] == None:
                retval = self.CURRENT
            else:
                retval = self.VERIFIED
        else:
            retval = self.NOT_FOUND
        assert retval in (self.NOT_FOUND, self.CURRENT, self.VERIFIED)
        return retval

