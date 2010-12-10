# coding=utf-8
import pytz, datetime
import sqlalchemy as sa

class EmailVerifyQuery(object):
    NOT_FOUND  = 0
    CURRENT    = 1
    VERIFY     = 2
    def __init__(self, da):
        self.emailVerifyTable = da.createTable('email_verification')
        
    def get_email_from_verificationId(self, verificationId):
        evt = self.emailVerifyTable
        s = evt.select()
        s.append_whereclause(evt.c.verification_id == verificationId)

        r = s.execute().fetchone()

        retval = (r and r['email']) or ''
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
                retval = self.VERIFY
        else:
            retval = self.NOT_FOUND
        assert retval in (self.NOT_FOUND, self.CURRENT, self.VERIFY)
        return retval

