"use strict";
// GroupServer module for checking if email addresses are verified
//
// Copyright © 2011, 2012, 2013, 2014 OnlineGroups.net and Contributors.
// All Rights Reserved.
//
// This software is subject to the provisions of the Zope Public License,
// Version 2.1 (ZPL). http://groupserver.org/downloads/license/
//
// THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
// WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
// WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND
// FITNESS FOR A PARTICULAR PURPOSE.

jQuery.noConflict();

function GSVerifyEmailAddress(email, verificationId, statusId, siteName) {

    // Private variables
    var unverifiedMsg=null,
        verifiedMsg=null, 
        verifyingMsg=null,
        checkingMsg=null,
        statusUpdate=null,
        VERIFY_ADDRESS='verifyemail.ajax',
        CHECK_ADDRESS='checkemailverified.ajax',
        TIMEOUT_DELTA=4000;

    // Private methods
    function init() {
        var e=null;
        e = '<code class="email">' + email + '</code>';
        unverifiedMsg = 'The email address ' + e + ' is ' +
            '<strong>not verified</strong>.';
        verifiedMsg = '<p>The email address ' + e + ' has been ' + 
            '<strong>verified</strong>. You can use this address to send ' + 
            'messages to your groups, receive messages from groups, and '+
            'sign in to ' + siteName + '.</p>'+
            '<p><strong class="label">Important:</strong> You should now ' +
            '<strong>close</strong> this page before returning to ' +
            siteName + '.</p>';
        verifyingMsg = '<strong>Verifying</strong> ' + e + 
            '&#160;<span data-icon="&#xe619;" aria-hidden="true" '+
            'class="loading"> </span>';
        checkingMsg = '<strong>Checking</strong> ' + e + 
            '&#160;<span data-icon="&#xe619;" aria-hidden="true" '+
            'class="loading"> </span>';

        statusUpdate = jQuery(statusId);
        statusUpdate.html(checkingMsg);
    }
    init(); // Note the automatic execution

    function checkServer() {
        var d=null;
        d = {type: "POST",
             url: CHECK_ADDRESS, 
             cache: false,
             data: 'email='+email,
             success: checkReturn
            };
        jQuery.ajax(d);
        jQuery(statusUpdate).html(checkingMsg);
    }

    function checkReturn(data, textStatus) {
        var verified=null;
        verified = data == '1';
        if ( verified ) {
            jQuery(statusUpdate).html(verifiedMsg);
        } else {
            jQuery(statusUpdate).html(verifyingMsg);
            window.setTimeout(verifyAddress, TIMEOUT_DELTA);
        }
    }
    
    function verifyAddress() {
        var d=null;
        d = {
            type: "POST",
            url: VERIFY_ADDRESS, 
            cache: false,
            data: 'verificationId='+verificationId,
            success: checkServer
        };
        jQuery.ajax(d);
    }
    
    function changeCheckingMessage() {
        jQuery(statusUpdate).html(verifyingMsg);              
    }

    // Public methods and properties.
    return {
        start: function () {checkServer();}
    };
} // GSVerifyEmailAddress

jQuery(window).load(function () {
    var script=null, 
        verificationId=null, 
        statusId=null, 
        siteName=null, 
        email=null, 
        checker=null;

    script = jQuery('#gs-profile-email-verify-js');
    email = script.attr('data-email');
    verificationId = script.attr('data-verificationId');
    statusId = script.attr('data-statusId');
    siteName = script.attr('data-siteName');
    checker = GSVerifyEmailAddress(email, verificationId, statusId, siteName);
    checker.start();
});
