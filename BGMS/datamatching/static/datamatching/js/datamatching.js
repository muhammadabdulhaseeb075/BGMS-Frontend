var memorialModule = {

  /**
   * Trigger event that call Vue function that will link selected person to memorial
   * @param {*} first_names 
   * @param {*} last_name 
   * @param {*} personId 
   */
  linkMemorial: function(first_names, last_name, personId, age){
		jQuery(document).trigger('personSelectedForLinking', { 
      first_names: first_names, last_name: last_name, personId: personId, age_years: age });
  },

  //open person details modal
  showCompleteDetails: function(id){
    // TODO: add restriction to open the modal only one time
		// if(modalHelperService.modalOpened){
		// 	modalHelperService.modalOpened = false;
		$('body').css('cursor','progress');
		$.get('/datamatching/personDetails?id='+id).
        success(function(data, status, headers, config) {
              modalBurialDetails.open(data);
              // view_model.modalOpened = true;
              $('body').css('cursor','auto');
        }).
        error(function(data, status, headers, config) {
          console.log('could not load data');
          console.log(data);
          // modalHelperService.modalOpened = true;
          $('body').css('cursor','auto');
        });
			// }
	},

  showEmptyPersonDetails: function(){
    // TODO: add restriction to open the modal only one time
    // if (modalHelperService.modalOpened) {
    //   modalHelperService.modalOpened = false;
        $('body').css('cursor','progress');
        $.get('/datamatching/addPerson/').
        success(function(data, status, headers, config) {
          modalBurialDetails.open(data);
          $('body').css('cursor','auto');
        }).
        error(function(data, status, headers, config) {
          // modalHelperService.modalOpened = true;
          console.log('could not load data');
          $('body').css('cursor','auto');
        });
    // }
  },

  successNotification(title) {
    new PNotify({
      title: title,
      type: 'success',
      addclass: "stack-bottomright",
      stack: person.stack_bottomright,
      mouse_reset: false
    });
  },

  failNotification(title) {
    new PNotify({
      title: title,
      type: 'error',
      addclass: "stack-bottomright",
      stack: person.stack_bottomright,
      mouse_reset: false
    });
  },

	// auto fill search form using memorial inscriptions
	inscriptionSearch: function(firstNames, lastName, age) {
		$('#id_first_names').val(firstNames);
		$('#id_last_name').val(lastName);

		if (age) {
			if ($('#advanced-search-section').css("display") === "none") {
				searchSection.showOrHideAdvancedSearch();
			}
			$('#id_age').val(age);
		}
		else {
			$('#id_age').val('');
		}
		$('#id_age_to').val('');

		$('#searchForm').click();
	}
}