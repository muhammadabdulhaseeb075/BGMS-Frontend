
/** @module
 *  Admin site portal module
 */

var adminSite = {
  
  
  /**
   * Submit form to add site user
   * @param  {[String]} form                 form element to sent
   * @param  {[String]} buttonId            button in which ladda will be activated
   */
  addSiteUser: function(form, button) {
    if (adminSite.FormValidation()) {
        var l = Ladda.create(document.querySelector(button));
        l.start();
        $.post($(form).attr('action'), $(form).serialize())
            .done(function(data) {
                if(data.url !== ''){
                    notificationService.successSticky('Username exists!');
                    window.location.href = data.url;
                }else{
                    notificationService.errorSticky('Username does not exist');
                }
            })
            .always(function() {
                l.stop();
            })
            .fail(function(data) {
                notificationService.errorSticky();
                console.log(data);
            });
    }
  },

  /**
   * Send email invitation to register in site
   * @param  {[String]} form                 form element to sent
   * @param  {[String]} buttonId            button in which ladda will be activated
   */
  sendEmailInvitation: function(form, button) {
    var l = Ladda.create(document.querySelector(button));
    l.start();
    $.post($(form).attr('action'), $(form).serialize())
        .done(function(data) {
            notificationService.successSticky('The invitation was sent successfully');
        })
        .always(function() {
            l.stop();
        })
        .fail(function(data) {
            notificationService.errorSticky(data.responseJSON.email_invitation);
            console.log(data);
        });
  },

  /**
   * Validate form addSiteUser
   * @return  {boolean}            whether is a valid form to send
   */
  FormValidation: function(){
    if($('#id_username').val() === $('#id_username2').val()){
      $('#error_username2').text('');
      return true;
    }
    $('#error_username2').text('Please confirm username');
    return false;
  },

};

function linkSections() {
    notificationService.confirm(function() {
        axios.defaults.headers.common["X-CSRFToken"] = document.getElementsByName('csrfmiddlewaretoken')[0].value;

        $("body").css("cursor", "progress");
        axios({
            method: 'get',
            url: "sectionLink/",
        })
        .then(function (response) {
            $("body").css("cursor", "default");

            let message = 'Graveplots linked to new sections: ' + response.data.section_linked_count + '\<br>';
            if (response.data.section_linked_count>0)
                message += 'With partial overlap: ' + response.data.section_partial_linked_count + '\<br>';
            message += '\<br>Graveplots linked to new subsections: ' + response.data.subsection_linked_count;
            if (response.data.subsection_linked_count>0)
                message += '\<br>With partial overlap: ' + response.data.subsection_partial_linked_count;

            if (response.data.not_saved && response.data.not_saved.length > 0) {
                message += '\<br>';

                response.data.not_saved.forEach(function(msg) {
                    message += '\<br>' + msg;
                });
            }

            notificationService.successStickyTitleAndMessage('Linking Graveplots to Sections/Subsections was successful.',message);
            console.log(response);
        })
        .catch(function (error) {
            $("body").css("cursor", "default");
            notificationService.errorSticky('Linking Graveplots to Sections/Subsections failed.');
            console.log(error.response.data);
        });
    }, 
    function(){
      //do nothing for no callback
    },
    'This will create links between sections/subsections and their contained graveplots.\n\nThis will overwrite any existing section/subsection fields in your graveplots. Do you want to continue?');
  }