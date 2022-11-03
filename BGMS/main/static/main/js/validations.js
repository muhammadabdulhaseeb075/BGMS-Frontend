
// function validateCheckbox(submitElementSelector){
//   // l = Ladda.create(document.querySelector(submitElementSelector));
//   // l.start();
//   var isChecked = document.getElementById("disclaimerCheckbox");
//   if(isChecked.checked){
//     document.getElementById('error_checkbox').style.display = 'none';
//     return true;
//   }else{
//     document.getElementById('error_checkbox').style.display = 'block';
//     // l.stop();
//     return false;
//   }
// }

/**
 *
 * Validation for Select site page and login page
 * @class PublicValidation
 */
var PublicEntry = (function () {
    // isChecked: boolean;
    /**
     * Creates an instance of PublicValidation.
     * @memberOf PublicValidation
     */
    function PublicEntry() {
        // this.isChecked = false;
    }
    /**
     *
     * Validates disclaimer checkbox before sending the form
     * @param {string} submitElementSelector
     * @returns {boolean}
     *
     * @memberOf PublicValidation
     */
    PublicEntry.prototype.validateCheckbox = function (submitElementSelector) {
        // l = Ladda.create(document.querySelector(submitElementSelector));
        // l.start();
        var isChecked = document.getElementById("disclaimerCheckbox");
        if (isChecked.checked) {
            document.getElementById('error_checkbox').style.display = 'none';
            return true;
        }
        else {
            document.getElementById('error_checkbox').style.display = 'block';
            // l.stop();
            return false;
        }
    };
    /**
     * Verify the site is known before redirecting
     *
     * @param {string} formElem
     * @param {string} buttonElem
     *
     * @memberOf PublicEntry
     */
    PublicEntry.prototype.redirectSite = function (formElem, buttonElem) {
        var l = Ladda.create(document.querySelector(buttonElem));
        l.start();
        var action = $(formElem).attr('action');
        $(formElem).attr('action', '');

        // http://stackoverflow.com/questions/5750696/how-to-get-a-cross-origin-resource-sharing-cors-post-request-working
        // TODO: Change structure view to receive form.
        // $.ajax({
        //     url: "http://localhost:8079/students/add/",
        //     type: "POST",
        //     crossDomain: true,
        //     data: JSON.stringify(somejson),
        //     dataType: "json",
        //     success: function (response) {
        //         var resp = JSON.parse(response)
        //         alert(resp.status);
        //     },
        //     error: function (xhr, status) {
        //         alert("error");
        //     }
        // });

        $.post('/redirect/', $(formElem).serialize())
            .done(function (data) {
            if(data.site_url !== ''){
                // notificationService.success('Username exists!');
                window.location = data.site_url;
            }else{
                document.getElementById('error_unknownsite').style.display = 'block';
            }
            // console.log(data);
            // console.log(data.site_url);

        })
            .always(function () {
            l.stop();
        })
            .fail(function (data) {
            document.getElementById('error_unknownsite').style.display = 'block';
            // console.log(data);
        });        
    };
    return PublicEntry;
}());
var publicEntry = new PublicEntry();
