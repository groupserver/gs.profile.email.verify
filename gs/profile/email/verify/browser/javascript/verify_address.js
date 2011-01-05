// GroupServer module for checking if email addresses are verified
jQuery.noConflict();
GSVerifyEmailAddress = function () {

    // Private variables
    var email = null;
    var verificationId = null;
    var statusUpdate = null;
    var siteName = null;
    var unverifiedMsg = null;
    var verifiedMsg = null; 
    var verifyingMsg = null;
    var checkingMsg = null;
    
    var VERIFY_ADDRESS = 'verifyemail.ajax';
    var CHECK_ADDRESS = 'checkemailverified.ajax';
    var TIMEOUT_DELTA = 2000;
    // Private methods

    // Public methods and properties. The "checkServer" and "checkReturn"
    // methods have to be public, due to oddities with "setTimeout".
    return {
        init: function (e, v, s, n) {
            /* Add the address-checking code to the correct widgets
            
            ARGUMENTS
              e:  String containing the email address
              v:  String containing the verification id
              s:  String containing the selector for the status-update
                  container.
              n:  String containing the site name
            */
            email = e;
            verificationId = v;
            statusUpdate = s;
            siteName = n;
            unverifiedMsg = 'The email address <code class="email">' + e + 
              '</code> is <strong>not verified</strong>.';
            verifiedMsg = 'The email address <code class="email">' + e + 
              '</code> has been <strong>verified</strong>. You can ' + 
              'use this address to send messages to your groups, ' +
              'receive messages from groups, and log in to ' + n + '.';
            verifyingMsg = '<strong>Verifying</strong> ' + 
              '<code class="email">' + e + '</code>' + 
              '&#160;<img src="/++resource++anim/wait.gif"/>';
            checkingMsg = '<strong>Checking</strong> ' + 
              '<code class="email">' + e + '</code>' + 
              '&#160;<img src="/++resource++anim/wait.gif"/>';
            jQuery(statusUpdate).html(checkingMsg);
            setTimeout("GSVerifyEmailAddress.checkServer()", TIMEOUT_DELTA);
        },
        checkServer: function () {
            jQuery.ajax({
              type: "POST",
              url: CHECK_ADDRESS, 
              cache: false,
              data: 'email='+email,
              success: GSVerifyEmailAddress.checkReturn});
            jQuery(statusUpdate).html(checkingMsg);
        },
        checkReturn: function (data, textStatus) {
            var verified = data == '1';
            if (verified) {
                jQuery(statusUpdate).html(verifiedMsg);
            } else {
                jQuery(statusUpdate).html(verifyingMsg);
                setTimeout("GSVerifyEmailAddress.verifyAddress()",
                  TIMEOUT_DELTA);
            }
        },
        verifyAddress: function () {
            jQuery.ajax({
              type: "POST",
              url: VERIFY_ADDRESS, 
              cache: false,
              data: 'verificationId='+verificationId,
              success: GSVerifyEmailAddress.checkServer});
        },
        changeCheckingMessage: function() {
            jQuery(statusUpdate).html(verifyingMsg);              
        }
    };
}(); // GSVerifyEmailAddress

