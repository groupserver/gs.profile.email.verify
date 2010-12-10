# coding=utf-8
from zope.interface import Interface
from zope.schema import ASCIILine

class IGSEmailVerifyUser(Interface):
    '''A user who can verify email addresses'''
    pass
