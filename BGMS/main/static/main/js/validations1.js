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
        $.post($(formElem).attr('action'), $(formElem).serialize())
            .done(function (data) {
            // if(data.url !== ''){
            //     notificationService.success('Username exists!');
            //     window.location.href = data.url;
            // }else{
            //     notificationService.error('Username does not exist');
            // }
            console.log('redirecting..');
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
//# sourceMappingURL=validations1.js.map