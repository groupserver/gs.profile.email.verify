===========================
``gs.profile.email.verify``
===========================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The Verify Email Address page
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2015-03-05
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
`Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.net`_.

..  _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

Introduction
============

In GroupServer email addresses are not *just* added to
profiles. An email address is added in an **unverified**
address. An email is sent to this address to **verify** that it
works. When the member follows the instructions in the email the
email address is **verified**. This product handles this process
[#unverify]_.

Email addresses are not exclusively verified by the `pages`_ in
this product. Other systems (like the *Password Reset* page
[#reset]_) also verify addresses. This product supplies the
`verification-user`_ to support this.

Pages
=====

The *Verify Address* notification (provided by the page
``verification-mesg.html`` in this product) contains a link with
a unique URL. A **redirector** (``/r/verify``, supplied by this
product) checks the ID that is part of the URL.

  * If the ID it exists, and the address is not verified, then
    the user is logged in, and redirected to the *Verify Email*
    page (``verifyemail.html``) under the profile page of the
    user. Then the *Verify Email* page uses AJAX to request
    ``verifyemail.ajax`` to verify the address.

  * If the ID does not exist then a ``404`` **error** is
    returned, but one that is *specific* to email-address
    verification (``email-verify-not-found.html``).
  
  * If an ID has been *used* (the address is already verified)
    then a ``410`` **error** is returned, but one that is
    specific to verification (``email-verify-used.html``).

Verification-User
=================

The *Email Verification User*
(``gs.profile.email.verify.emailverificationuser.EmailVerificationUser``)
is used to actually verify an email address for a user. It is
normally created from a ``context``, a user-info, and an email
address. It can create a verification-ID for an address, or
verify an address.

The confusingly named, but much simpler, *Verify Email User*
(``gs.profile.email.verify.interfaces.IGSVerifyEmailUser``) is
provided factory named ``groupserver.EmailVerificationUser``. It
can tell you if an verification ID exists, and is current. It is
mostly used by the redirector.

Resources
=========

- Code repository:
  https://github.com/groupserver/gs.profile.email.verify
- Questions and comments to
  http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

..  [#unverify] The code for unverifying email addresses
                (i.e. disabling them after bouncing) is
                ``gs.group.member.bounce``
                <https://github.com/groupserver/gs.group.member.bounce>
..  [#reset] The code for resetting a password can be found in
             the ``gs.profile.password`` product
             <https://github.com/groupserver/gs.profile.password>

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
