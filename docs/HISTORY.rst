Changelog
=========

3.4.0 (2015-07-17)
------------------

* Updating the ``mailto:`` addresses so they include a link to
  the profile page of the person
* Adding a ``preheader`` to the HTML notification
* ``s/Dear/Hello/g``

3.3.0 (2015-03-12)
------------------

* Handling email addresses with ``+`` characters in them, partly
  closing `Bug 4036`_
* Adding internationalisation_
* [FR] Adding a French translation, thanks to  `Razique Mahroua`_
* Naming the reStructuredText files as such
* Pointing at GitHub_ as the primary repository

.. _Bug 4036: https://redmine.iopen.net/issues/4036
.. _internationalisation:
   https://www.transifex.com/projects/p/gs-profile-email-verify/
.. _Razique Mahroua:
   https://www.transifex.com/accounts/profile/Razique/
.. _GitHub:
   https://github.com/groupserver/gs.profile.email.verify/


3.2.1 (2014-10-07)
------------------

* Metadata cleanup.

3.2.0 (2014-06-15)
------------------

* Moving the SQL files relating to verification here

3.1.3 (2014-04-08)
------------------

Switching to ``strict`` mode in the JavaScript

3.1.3 (2014-02-28)
------------------

* Ensuring the old content-type is set
* Switching to Unicode literals

3.1.2 (2014-01-27)
------------------

* Adding ``EmailVerificationUser`` to the general API
* Turning assert-statements into ``raise``.

3.1.1 (2013-11-15)
------------------

* Changing the link to the *Email settings* page

3.1.0 (2013-10-08)
------------------

* Switching to ``gs.content.email.layout`` for the email-message layout

3.0.0 (2013-05-15)
------------------

* Update to the new UI
* Making the JavaScript work with a *deferred* jQuery
* Code cleanup, thanks to Ninja-IDE

2.2.2 (2012-08-02)
------------------

* ``lock`` not supported by ``infrae.wsgi``

2.2.1 (2012-07-03)
------------------

* Fixing the return-type checks

2.2.0 (2012-06-22)
-----------------

* Following the changes to ``gs.database``

2.1.2 (2012-04-20)
------------------

* Escaping the site-name so it works in JavaScript

2.1.1 (2012-02-09)
------------------

* Fixing a URL
* Fixing the old ``send_verification_message`` method

2.1.0 (2012-01-12)
------------------

* Using page-templates for the email-verification message
* Adding HTML as well as plain-text versions of the message

2.0.0 (2011-06-16)
------------------

* Making the verification process less confusing
* Updating the JavaScript

1.1.0 (2011-05-25)
------------------

* Setting the verified email address to delivery if the member
  has no delivery addresses


1.0.2 (2011-03-23)
------------------

* Updating the URL for the JavaScript

1.0.1 (2011-02-23)
------------------

* Fix to handle special characters

1.0.0 (2011-02-07)
------------------

* Initial version

..  LocalWords:  Changelog reStructuredText GitHub
