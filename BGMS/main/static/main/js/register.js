$.fn.extend({
    animateCss: function (animationName) {
        var animationEnd = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';
        $(this).addClass('animated ' + animationName).one(animationEnd, function() {
            $(this).removeClass('animated ' + animationName);
        });
    }
});

$.fn.extend({
    animateCssOut: function (animationName) {
        var animationEnd = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';
        $(this).addClass('animated ' + animationName).one(animationEnd, function() {
            $(this).hide();
        });
    }
});

var UserAccount = {

  registerUser: function(formElementSelector, resultElement, buttonId) {
    UserAccount.cleanFormErrorsAndResult(formElementSelector, resultElement);
    $(formElementSelector).unbind('submit').submit(function(event) {
      event.preventDefault();
      if (UserAccount.registerUserFormValidation()) {
        var l = Ladda.create(document.querySelector(buttonId));
        l.start();
        $.post('/register/', $(formElementSelector).serialize())
          .done(function(data) {
            $(resultElement).text(data.data);
            // $('.register-box-body').addClass("animated fadeInUp");
            // $('.register-box-body').animateCssOut("zoomOut");
            $('.register-box-body').hide();
            $(resultElement).show();
          })
          .always(function() {
            l.stop();
          })
          .fail(function(data) {
            $(resultElement).text('');
            $.each(data.responseJSON, function(key, value) {
              $('#error_' + key).text(value);
            });
            console.log(data.responseText)
          });
      }
    });
  },

  cleanFormErrorsAndResult: function(formElementSelector, resultElement) {
    $('.errorlist').text('');
    $(resultElement).text('');
  },

  registerUserFormValidation: function(){
    if($('#id_email').val() === $('#id_email2').val()){
      return true;
    }
    $('#error_email2').text('Please confirm your email address');
    return false;
  },

};
