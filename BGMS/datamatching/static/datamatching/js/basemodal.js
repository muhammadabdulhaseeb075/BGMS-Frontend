/** @module Base Modal */

var baseModal = {

  /**
   * Initialize form after document ready
   */
  initModal: function(){

    //Create custom prettyphoto
    prettyPhotoTemplate.getTemplate();

	  //remove missing images from list
    $('form[id^=MemorialForm] img').on( "error", function() {
      //console.error('error(function()');
      if(this.src.indexOf("/memorials/") > -1){
        modalBurialDetails.failToLoadImages.push(this.src);
        $(this).parent().parent().remove();
      }else{
        $(this).attr('src', $(this).parent().attr('href'));
      }
    });

    $("#BurialForm img").on( "error", function() {
      modalBurialDetails.failToLoadImagesBurial.push(this.src);
      if(this.src.indexOf("icons/noimage.jpg") > -1){
        $(this).parent().parent().hide();
        $(this).parent().parent().remove();
      }else{
        try{
          var noimagePath = "https://s3-eu-west-1.amazonaws.com/bgms/images/icons/noimage.jpg";
          this.src = noimagePath;
          modalBurialDetails.failToLoadImages.push(noimagePath);
          $(this).parent().attr('href', noimagePath);
        }catch(err){
          $(this).parent().parent().remove();
        }
      }
    });

    //Check if is a new person
    if (modalBurialDetails.isANewPerson()) {
      modalBurialDetails.enableFields('#DeathPersonForm.burial-details-form-editable');
      modalBurialDetails.enableFields('#BurialForm');
      $('.editDetailPersonForm').hide();
      $('div[id^=memorial_image_input]').hide();
      $('#BurialForm').parent().find('.field-to-show.ladda-button').hide();
      $('#DeathPersonForm').parent().find('.field-to-show.ladda-button').not(document.getElementById("savePersonDetailsButton")).hide();

      //Get action wheter is a new person or a new person based on reserved person
      var urlPersonForm = baseModal.getNewPersonFormAction();

      $('#savePersonDetailsButton').attr('onclick','person.submitNewDetailsForm("'+urlPersonForm+'", "#DeathPersonForm", "/datamatching/burialEdit/", "#BurialForm", "#savePersonDetailsButton")');
      person.initialiseUploadImage( urlPersonForm, '#DeathPersonForm', '#savePersonDetailsButton', '/datamatching/burialEdit/', '#BurialForm');

      baseModal.showClearButton();

    }
    else{
      for(var i=0; i<$('.left-form-section').find('form').size(); i++){
        person.initialiseUploadImage($($('.left-form-section').find('form')[i])
          .attr('action'), '#'+$($('.left-form-section').find('form')[i]).attr('id'), '#'+$($('.left-form-section')
          .find('button[id^=saveMemorialDetailsButton]')[i]).attr('id'));
      }
      person.initialiseUploadImage( '/datamatching/burialEdit/', '#BurialForm', '#saveBurialDetailsButton');
    }

    //Add mask to dates of death and date of birth
    $("#id_death_date").mask("99/99/9999", {
      placeholder: "dd/mm/yyyy"
    });
    $("#id_birth_date").mask("99/99/9999", {
      placeholder: "dd/mm/yyyy"
    });

    //Hook up the slider for memorials
    var flexsliderMemorial = $('#flexslider-memorial').flexslider({
      animation: "slide",
      // directionNav: false
      // selector: ".slides > div > li",
      start: function(slider){
        $("#flexslider-memorial").resize();
      }
    });
    //Hook up the slider for burial officials
    var flexsliderBO = $('#flexslider-burial-official').flexslider({
      animation: "slide",
      // directionNav: false
      // selector: ".slides > div > li",
      start: function(slider){
        $("#flexslider-burial-official").resize();
      }
    });
    //create copy to maintain original burial officials
    burialOfficialForm.flexsliderBurialOfficialOld = jQuery.extend(true, {}, flexsliderBO.data('flexslider').slides);
      // $('#flexslider-burial-official')

    //Initialize form validation
    modalBurialDetails.validator = $('.burial-details-form').validate({
      // errorPlacement: function(error, element) {
  		// 	// Append error within linked label
  		// 	$( element ).parent().append( error );
  		// },
		  errorElement: "span",
      rules: {
        age_years: {min: 0, max: 150, digits: true},
        age_months: {min: 0, max: 36, digits: true},
        age_days: {min: 0, max: 365, digits: true},
        age_hours: {min: 0, max: 99, digits: true},
        age_minutes: {min: 0, max: 59, digits: true},
      }
    });

    //changes to add memorial headpoint and featureId
    $("input[name='graveplot_polygon_feature']").val(jsAngularInterface['graveplot_polygon_feature']);
    //Clean graveplot_polygon_feature variable for next time opening modal person
    jsAngularInterface['graveplot_polygon_feature'] = '';


    $(".btn-file input[id^=id_memorial]").on('change', function() {
      if (this.files.length > 0) {
        $(this).parent().parent().find('span[id^=nameMemorialImage]').text(this.files[0].name);
      }
    });
    $("#id_burial_image_input").on('change', function() {
      if (this.files.length > 0) {
        $(this).parent().parent().find('span[id^=nameBurialImage]').text(this.files[0].name);
      }
    });

    //Initialize dropdownlist burial official types
    $('.choice-field').change(function(){
      idField = $(this).attr('id');
      idField = idField.substring(0, idField.length - 1);
      $('#'+idField).val($('option:selected', this).text());
    });

    //Closing modal
    $('#id_modalBurialDetails').on('hide.bs.modal', function() {
      return modalBurialDetails.validateClosingModal();
    });

    //
    $("#DeathPersonForm").on("change", function() {
        modalBurialDetails.hasFormBeenEdited['#DeathPersonForm'] = true;
    });
    $("#BurialForm").on("change", function() {
        modalBurialDetails.hasFormBeenEdited['#BurialFormCounter'] += 1;
        if(modalBurialDetails.hasFormBeenEdited['#BurialFormCounter'] > 0)
          modalBurialDetails.hasFormBeenEdited['#BurialForm'] = true;
    });

    //Add class allow scrollbar in case there was a hidden modal behind
    $('#id_modalBurialDetails').on('shown.bs.modal', function (e) {
      $('body').addClass('modal-open');
    });

    //Change text area style in case empty
    baseModal.handleTextAreaClass();

  },

  /**
   * Get action whether is a new person or a new person based on reserved person
   * @return {String} url action for person form
   */
  getNewPersonFormAction: function(){
    return "/datamatching/personEdit/";
  },

  /**
   *  Change text area style in case empty
   *  or
   *  Remove text area style in case non empty
   */
  handleTextAreaClass: function(){
    $( "textarea" ).each(function( index ) {
      if($( this ).val() === ''){
        $(this).addClass('empty-textarea');
      }else{
        $(this).removeClass('empty-textarea');
      }
    });
  },

  /**
   *  Remove text area style to be normal textarea
   */
  removeTextAreaClass: function(){
    $( "textarea" ).each(function( index ) {
      $(this).removeClass('empty-textarea');
    });
  },

  /**
   * Show clear button when entering a new burial record only
   * Excludes convert to burial from reservation plot
   * @return {undefined}
   */
  showClearButton: function() {
    $('.btn-clear-fields').show();
  },

};
