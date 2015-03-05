"use strict";
// GroupServer module for checking if email addresses are verified
//
// Copyright © 2011, 2012, 2013, 2014, 2015 OnlineGroups.net and 
// Contributors.
//
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

function GSVerifyEmailAddress(email, verificationId, msgCheckingId,
                              msgVerifyingId, msgVerifiedId, msgProblemId) {

    // Private variables
    var checkingMsg=null, 
        verifyingMsg=null,
        verifiedMsg=null,
        problemMsg=null,
        VERIFY_ADDRESS='verifyemail.ajax',
        CHECK_ADDRESS='checkemailverified.ajax',
        TIMEOUT_DELTA=4000;

    // Private methods
    function init() {
        checkingMsg = jQuery(msgCheckingId);
        verifyingMsg = jQuery(msgVerifyingId);
        verifiedMsg = jQuery(msgVerifiedId);
        problemMsg = jQuery(msgProblemId);

    }
    init(); // Note the automatic execution

    function checkServer() {
        var d=null;
        d = {type: "POST",
             url: CHECK_ADDRESS, 
             cache: false,
             data: {'email': email},
             success: checkReturn
            };
        jQuery.ajax(d);
        //
    }

    function checkReturn(data, textStatus) {
        jQuery('.status').removeClass('status-current');
        if ( data == '1' ) {
            verifiedMsg.addClass('status-current');
        } else if (data == '0') {
            verifyingMsg.addClass('status-current');
            window.setTimeout(verifyAddress, TIMEOUT_DELTA);
        } else {
            problemMsg.addClass('status-current');
        }
    }
    
    function verifyAddress() {
        var d=null;
        d = {
            type: "POST",
            url: VERIFY_ADDRESS, 
            cache: false,
            data: {'verificationId': verificationId},
            success: checkServer
        };
        jQuery.ajax(d);
    }
    
    function changeCheckingMessage() {
        jQuery('.status').removeClass('status-current');
        checkingMsg.addClass('status-current');
    }

    // Public methods and properties.
    return {
        start: function () {changeCheckingMessage(); checkServer();}
    };
} // GSVerifyEmailAddress

jQuery(window).load(function () {
    var script=null, 
        verificationId=null, 
        email=null,
        msgChecking=null,
        msgVerifying=null,
        msgVerified=null,
        msgProblem=null,
        checker=null;

    script = jQuery('#gs-profile-email-verify-js');
    verificationId = script.data('verification-id');
    email = script.data('email');
    msgChecking = script.data('msg-checking');
    msgVerifying = script.data('msg-verifying');
    msgVerified = script.data('msg-verified');
    msgProblem = script.data('msg-verified');
    
    checker = GSVerifyEmailAddress(email, verificationId, msgChecking,
                                   msgVerifying, msgVerified, msgProblem);
    checker.start();
});
