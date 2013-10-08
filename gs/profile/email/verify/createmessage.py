# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from textwrap import TextWrapper
from email.Header import Header
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
utf8 = 'utf-8'


def create_verification_message(userInfo, siteInfo, toAddr, fromAddr,
                                verificationId):
    container = MIMEMultipart('alternative')
    subject = u'Verify Address on %s' % siteInfo.name
    container['Subject'] = str(Header(subject.encode(utf8), utf8))
    container['From'] = str(fromAddr)
    container['To'] = str(toAddr)

    wrapper = TextWrapper(width=72)
    b = 'We received a request to add the email address <%s> '\
        'to your profile on %s. To verify that you control this '\
        'email address, please click the following link.' % \
         (toAddr, siteInfo.name)
    body = '\n'.join(wrapper.wrap(b))

    u = '%s/r/verify/%s' % (siteInfo.url, verificationId)
    d = {
        'siteName': siteInfo.name,
        'siteUrl': siteInfo.url,
        'body': body,
        'verificationUrl': u
    }

    t = u'''Hi there!

%(body)s
  %(verificationUrl)s

--
%(siteName)s
  %(siteUrl)s
''' % d
    text = MIMEText(t.strip().encode(utf8), 'plain', utf8)
    container.attach(text)

    hb = 'We received a request to add the email address '\
        '<a href="mailto:%s">%s</a> '\
        'to your profile on %s. To verify that you control this '\
        'email address, please click the following link.' % \
         (toAddr, toAddr, siteInfo.name)
    hbody = '\n'.join(wrapper.wrap(hb))
    d['hbody'] = hbody

    h = u'''<p><strong>Hi there!</strong></p>

<p>%(hbody)s</p>
<pre>
  <a href="%(verificationUrl)s">%(verificationUrl)s</a>
</pre>
<hr/>
<p><a href="%(siteUrl)s">%(siteName)s</a></p>
''' % d
    html = MIMEText(h.encode(utf8), 'html', utf8)
    container.attach(html)

    retval = container.as_string()
    assert retval
    assert type(retval) == str
    return retval
