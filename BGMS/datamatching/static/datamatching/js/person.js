var person = {

	destinationElementSelector: null,

	initialiseUploadImage: function(url, formElementSelector, submitElementSelector, url2, formElementSelector2){
		try{
		var l = Ladda.create(document.querySelector(submitElementSelector));
		} catch(err){}
		var formelement = '';
		if(formElementSelector2 == null){
			formelement = formElementSelector;
		}else{
			formelement = formElementSelector2;
		}
		$(formelement).fileupload({
				autoUpload: false,
		    dataType: 'json',
		    multipart: true,
		    replaceFileInput: false,
		    maxFileSize: 5000000, // 5 MB
				//acceptFileTypes: /(\.|\/)(jpe?g|png)$/i,
				// previewMaxWidth: 100,
        // previewMaxHeight: 100,
        // previewCrop: true,
	      add:  function (e, data) {
					var goUpload = true;
					var uploadFile = data.files[0];
					if (!(/\.(jpg|jpeg|png)$/i).test(uploadFile.name)) {
							new PNotify({
                    title: messages.burialDetails.fileUpload.validationFileType.title,
                    type: 'error',
										addclass: "stack-bottomright",
                    stack: person.stack_bottomright,
										mouse_reset: false
                	});
							goUpload = false;
					}
					if (uploadFile.size > 5000000) { // 5mb
							new PNotify({
									title: messages.burialDetails.fileUpload.validationFileSize.title,
									type: 'error',
									addclass: "stack-bottomright",
									stack: person.stack_bottomright,
									mouse_reset: false
								});
							goUpload = false;
					}
					if (goUpload == true) {
						$(submitElementSelector).attr('onclick','');
						$(submitElementSelector).unbind('click')
								.on('click', null, null, function (submitEvent) {
								try{
								l = Ladda.create(document.querySelector(submitElementSelector));
								l.start();
								} catch(err){}

								if(url2 != null && formElementSelector2 != null){
									person.submitNewDetailsForm(url, formElementSelector, url2, formElementSelector2, submitElementSelector, data);
								}else{
									data.formData = $(formElementSelector).serializeArray();
									person.submitDetailsForm(url, formElementSelector, submitElementSelector, data);
								}
								// data.submit();
								});
					}
					return false;
	      },
		    done: function (e, data) {
		    		new PNotify({
                    title: messages.burialDetails.fileUpload.success.title,
                    type: 'success',
										addclass: "stack-bottomright",
                    stack: person.stack_bottomright,
										mouse_reset: false
                	});
						person.doneAfterSubmitForm(data, formElementSelector);
						modalBurialDetails.disableFields(formElementSelector, true);
						if (formElementSelector2 != null)
							modalBurialDetails.disableFields(formElementSelector2, true);
					try{
		    	l.stop();
					} catch(err){}
        	},
        	fail: function (e, data) {
		    		new PNotify({
                    title: messages.burialDetails.fileUpload.fail.title,
                    type: 'error',
										addclass: "stack-bottomright",
                    stack: person.stack_bottomright,
										mouse_reset: false
                	});
        		l.stop();
	    		console.log(data.responseText);
        	}
		});
	},

	submitSearchForm: function(url, formElementSelector, destinationElementSelector, buttonId){
		//console.time('submitSearchForm');
		//clear previous search popup if it is open
		// jsAngularInterface.hidePersonClickDetails();
		if(person.validateDates()){
			//submit ajax-ly to avoid reloading page
			$(formElementSelector).unbind('submit').submit(function(event){
			    event.preventDefault();
			    var l = Ladda.create(document.querySelector(buttonId));
		 		l.start();
			    $.post(url, $(formElementSelector).serialize())
			    	.done(function(data){
							if(data.data == null){ //Session expired
								location.reload();
							}else{
							//console.timeEnd('submitSearchForm');
				    		$(destinationElementSelector).html(data.data);
								searchSection.resizeResults();
							}
			    	})
			    	.always(function() { l.stop(); })
			    	.fail(function(data){
			    		$(destinationElementSelector).text('Unable to find the person.');
			    		//clearing previous search
			    		console.log(data.responseText)
			    	});
			});
		}

	},

	validateDates: function(){
		var yearFrom = $('#id_year_burial_date').val();
		var yearTo = $('#id_year_burial_date_to').val();
		if(yearFrom != ''){
			$('#id_burial_date').val('01/01/'+yearFrom);
			$('#id_burial_date').parent().addClass("floating-label-form-group-with-value");
			if(yearTo != ''){
				$('#id_burial_date_to').val('31/12/'+yearTo);
				$('#id_burial_date_to').parent().addClass("floating-label-form-group-with-value");
			}else{
				$('#id_burial_date_to').val('31/12/'+yearFrom);
				$('#id_burial_date_to').parent().addClass("floating-label-form-group-with-value");
			}
		}else{
			if(!$('#specific-date-check').is(":checked")){
				$('#id_burial_date').val('');
				$('#id_burial_date_to').val('');
			}
		}
		return true;

	},

	clearSearchForm: function(){
		jsAngularInterface.hidePersonClickDetails();
	},

	isEmptyForm: function(formElementSelector){
		var elements = $(formElementSelector).find('input');
		for (i = 0; i < elements.size(); i++) {
			if(elements[i].type == 'text'){
				if(elements[i].value != ""){
					return true;
				}
			}else{
				if(elements[i].type == "checkbox"){
					if($(elements[i]).is(':checked')){
						return true;
					}
				}
			}
		}
		var selects = $(formElementSelector).find('select');
		for (i = 0; i < selects.size(); i++) {
			if(selects[i].value != 0){
				return true;
			}
		}
		return false;
	},

	stack_bottomright: {"dir1": "up", "dir2": "left", "firstpos1": 25, "firstpos2": 25},

	doneAfterSubmitForm: function(data, formElementSelector){

		//in case the form was sent by jquery.uploadFile
		if(data.result){
			data = data.result;
		}

		var oldAvailablePlotId = data['old_plot_id'];
		var personGeoJSON = data['person_feature'];
		var oldLayer = data['old_layer'];
		var burial_image = data['burial_image'];
		if(personGeoJSON){
				$("input[name$='person_id']").val(data['person_feature']['id']);
				//update burial officials dictionary with person_id
				modalBurialDetails.updatePersonIdtoBurialOfficialsDictionary(data['person_feature']['id']);
				//Refresh age field
				var newAge = '';
				if(personGeoJSON['age_years'] != null && personGeoJSON['age_years'] != 0)
					newAge += personGeoJSON['age_years'] + ' years ';
				if(personGeoJSON['age_months'] != null && personGeoJSON['age_months'] != 0)
					newAge += personGeoJSON['age_months'] + ' months ';
        if(personGeoJSON['age_weeks'] != null && personGeoJSON['age_weeks'] != 0)
          newAge += personGeoJSON['age_weeks'] + ' weeks ';
				if(personGeoJSON['age_days'] != null && personGeoJSON['age_days'] != 0)
					newAge += personGeoJSON['age_days'] + ' days ';
				if(personGeoJSON['age_hours'] != null && personGeoJSON['age_hours'] != 0)
					newAge += personGeoJSON['age_hours'] + ' hours ';
          if(personGeoJSON['age_minutes'] != null && personGeoJSON['age_minutes'] != 0)
            newAge += personGeoJSON['age_minutes'] + ' minutes ';
				$('#id_age_str').val(newAge);
		}

		//Refresh burial record image
		if(burial_image){
			$('#id_burial_image_url').attr('href',burial_image['image_url']);
			$('#id_burial_thumbnail_url').attr('src',burial_image['thumbnail_url']);
		}

		modalBurialDetails.hideOptionsAfterSave();
	},

	submitDetailsForm: function(url, formElementSelector, buttonId, dataFileUpload){
		var l = Ladda.create(document.querySelector(buttonId));
		l.start();
		if(modalBurialDetails.hasErrors()){
			l.stop();
			new PNotify({
							title: messages.burialDetails.saveChanges.hasErrors.title,
							text: messages.burialDetails.saveChanges.hasErrors.text,
							type: 'error',
							addclass: "stack-bottomright",
							stack: person.stack_bottomright,
							mouse_reset: false
						});
		}else{
			if(!person.isEmptyForm(formElementSelector)){
				l.stop();
				new PNotify({
								title: messages.burialDetails.saveChanges.isEmptyForm.title,
								text: messages.burialDetails.saveChanges.isEmptyForm.text,
								type: 'error',
								addclass: "stack-bottomright",
								stack: person.stack_bottomright,
								mouse_reset: false
							});

			}else{
				if(dataFileUpload == null){
						$.post(url, $(formElementSelector).serialize())
					    	.done(function(data){
					    		person.doneAfterSubmitForm(data, formElementSelector);
									modalBurialDetails.disableFields(formElementSelector, true);
					    		new PNotify({
			                    title: messages.burialDetails.saveChanges.success.title,
			                    type: 'success',
													addclass: "stack-bottomright",
			                    stack: person.stack_bottomright,
													mouse_reset: false
			                	});
					    	})
					    	.always(function() { l.stop(); })
					    	.fail(function(data){
					    		new PNotify({
			                    title: messages.burialDetails.saveChanges.fail.title,
			                    type: 'error',
													addclass: "stack-bottomright",
			                    stack: person.stack_bottomright,
													mouse_reset: false
			                	});
					    	});
					}else{
						dataFileUpload.submit();
					}
			}
		}
	},

	submitNewDetailsForm: function(urlPerson, formElementSelectorPerson, urlBurial, formElementSelectorBurial, buttonId, dataBurial){
		var l = Ladda.create(document.querySelector(buttonId));
		l.start();
		if(modalBurialDetails.hasErrors()){
			l.stop();
			new PNotify({
							title: messages.burialDetails.saveChanges.hasErrors.title,
							text: messages.burialDetails.saveChanges.hasErrors.text,
							type: 'error',
							addclass: "stack-bottomright",
							stack: person.stack_bottomright,
							mouse_reset: false
						});
		}else{
			var isEmptyForm = !person.isEmptyForm(formElementSelectorPerson);
			if(isEmptyForm){
				l.stop();
				new PNotify({
								title: messages.burialDetails.saveChanges.isEmptyForm.title,
								text: messages.burialDetails.saveChanges.isEmptyForm.text,
								type: 'error',
								addclass: "stack-bottomright",
								stack: person.stack_bottomright,
								mouse_reset: false
							});
			}else{
				//POST person details
				$.post(urlPerson, $(formElementSelectorPerson).serialize())
				    	.done(function(data){
								person.doneAfterSubmitForm(data, formElementSelectorPerson);
								$('#id_id_person').val(data['person_feature']['id']);
								modalBurialDetails.disableFields(formElementSelectorPerson, true);
								l.stop();
								new PNotify({
									title: messages.burialDetails.saveChanges.success.title,
									type: 'success',
									addclass: "stack-bottomright",
									stack: person.stack_bottomright,
									mouse_reset: false
								});

								const pData = data['person_feature']
										
								// event will link new person to matched memorial
								jQuery(document).trigger('personSelectedForLinking', { newPerson: true,
									first_names: pData['first_names'], last_name: pData['last_name'], personId:pData['id'], age_years: pData['age_years'], age_months: pData['age_months'], age_weeks: pData['age_weeks'], age_days: pData['age_days'], age_hours: pData['age_hours'], age_minutes: pData['age_minutes'] });

								// close the modal form
								$('#id_modalBurialDetails').modal('hide')
				    	})
				    	.fail(function(data){
								l.stop();
				    		new PNotify({
		                    title: messages.burialDetails.saveChanges.fail.title,
		                    type: 'error',
												addclass: "stack-bottomright",
		                    stack: person.stack_bottomright,
												mouse_reset: false
		                	});
				    	});
			}
		}
	},

	showHoverDetails: function(personId){
		jsAngularInterface.showHoverDetails(personId);
	},

	hideHoverDetails: function(){
		jsAngularInterface.hidePersonDetails();
	},
	/*,
	updateMapSize:function(){
		jsAngularInterface.updateMapSize();
	}*/

};
