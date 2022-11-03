/** @module Person details */
/**Require basemodal.js*/

var modalBurialDetails = {

  enableFields: function(formsElementClass) {
    $(formsElementClass).find('*').not('.non-editable').removeAttr('readonly');
    $(formsElementClass).find('*').not('.non-editable').removeAttr('DISABLED');
    $(formsElementClass).parent().find('.field-to-hide').hide();
    $(formsElementClass).parent().find('.field-to-show').show();
    $(formsElementClass).removeClass('read-only-form');
    //Add selectize hibrid textbox and select for year select
    $(formsElementClass).find('.impossible-date select').selectize();
    $(formsElementClass).find('.impossible-date select').hide();
    $(formsElementClass).find('.impossible-date div.selectize-control').show();
    if(formsElementClass == "#BurialForm"){
      modalBurialDetails.getAndShowBurialOfficialsSelect();
      modalBurialDetails.burialOfficialsPosition[""]={};
      try{
      $('#flexslider-burial-official').flexslider("stop");
      $('#flexslider-burial-official').flexslider(0);
      }catch(err){
        //has not been created
      }
    }
    // if(formsElementClass.startsWith("#MemorialForm")){ Not supported by IE
    if(formsElementClass.indexOf('#MemorialForm') == 0){
      $("#flexslider-memorial").resize();
      if($('form[id^="MemorialForm"]').length <= 3){
        $("#flexslider-memorial").parent().addClass('form-section-selected');
      }else{
        $(formsElementClass).parent().addClass('form-section-selected');
      }
    }else{
      $(formsElementClass).closest('div[class^="col-"]').addClass('form-section-selected');
    }

    baseModal.removeTextAreaClass();
  },

  disableFields: function(formsElementClass, fromSave) {
    if(modalBurialDetails.hasFormBeenEdited[formsElementClass] == true && !fromSave){
      modalBurialDetails.saveChangesNotification(
        function(){
          modalBurialDetails.saveChanges(formsElementClass);
          modalBurialDetails.hasFormBeenEdited[formsElementClass] = false;
          if(formsElementClass == "#BurialForm"){
            modalBurialDetails.hasFormBeenEdited['#BurialFormCounter'] = 0;
          }
          modalBurialDetails.disableFieldsAll(formsElementClass, true); //simulates click on save button
        },
        function(){
          modalBurialDetails.hasFormBeenEdited[formsElementClass] = false;
          if(formsElementClass == "#BurialForm"){
            modalBurialDetails.hasFormBeenEdited['#BurialFormCounter'] = 0;
          }
          modalBurialDetails.disableFieldsAll(formsElementClass, fromSave);
        }
      );
    }else{
      modalBurialDetails.disableFieldsAll(formsElementClass, fromSave);
    }
  },

  saveChangesNotification: function(yesCallback, noCallback){
    new PNotify({
      title: messages.burialDetails.saveChanges.confirmation.title,
      text: messages.burialDetails.saveChanges.confirmation.text,
      icon: 'glyphicon glyphicon-question-sign',
      hide: false,
      confirm: {
        confirm: true,
        buttons: [{
          text: 'Yes',
          click: function(notice) {
             notice.remove();
             yesCallback();
          }
        }, {
          text: 'No',
          click: function(notice) {
            notice.remove();
            noCallback();
          }
        }]
      },
      buttons: {
        closer: false,
        sticker: false
      },
      history: {
        history: false
      },
      stack: {"dir1": "down","dir2": "right","firstpos1": ($(window).height() / 2 - 150),"firstpos2": ($(window).width() / 2 - 150)}
    });
  },

  saveChanges: function(formsElementClass){
    if(formsElementClass == "#DeathPersonForm"){
      person.submitDetailsForm('/datamatching/personEdit/', '#DeathPersonForm', '#savePersonDetailsButton');
    }else{
        if(formsElementClass == "#BurialForm"){
          person.submitDetailsForm('/datamatching/burialEdit/', '#BurialForm', '#saveBurialDetailsButton');
        }
    }
  },

  disableFieldsAll: function(formsElementClass, fromSave) {
    $(formsElementClass).find('input[type="text"]').prop('readonly', true);
    $(formsElementClass).find('input[type="checkbox"]').prop('disabled', true);
    $('#BurialForm').find('select').prop('disabled', true);
    $(formsElementClass).parent().find('.field-to-hide').show();
    $(formsElementClass).parent().find('.field-to-show').hide();
    $(formsElementClass).addClass('read-only-form');
    $(formsElementClass).closest('div[class^="col-"]').removeClass('form-section-selected');
    $(formsElementClass).find('.impossible-date select').show();
    $(formsElementClass).find('.impossible-date div.selectize-control').hide();
    //Adding a new person
    if($('#id_id_person').val() == ""){
      $('.editDetailPersonForm').show();
      $('#flexslider-memorial .editDetailPersonForm').hide();
    }
    if(formsElementClass == "#BurialForm"){
      $('#id_burial_remarks_disable').text($('#id_burial_remarks').val());
      $('#id_user_remarks_disable').text($('#id_user_remarks').val());
      $('#flexslider-burial-official').flexslider("play");
      if(!fromSave){
        modalBurialDetails.cleanBurialOfficialsSelect();
      }else{
        burialOfficialForm.updateFlexsliderBurialOfficialOld(modalBurialDetails.burialOfficialsPosition);
      }
      baseModal.handleTextAreaClass();
    }
    // if(formsElementClass.startsWith("#MemorialForm")){
    if(formsElementClass.indexOf('#MemorialForm') == 0){
      $("#flexslider-memorial").resize();
      $(formsElementClass).parent().removeClass('form-section-selected');
    }
  },

  failToLoadImages: [],
  failToLoadImagesBurial: [],
  burialOfficialsRemoved: [],
  currentBurialOfficialSlide: 0,
  burialOfficialsPosition: {}, //Position in slider by key: burial_official_id , val: position
  burialOfficials: {},
  hasFormBeenEdited: {
    '#BurialForm' : false,
    '#BurialFormCounter' : 0,
    '#MemorialForm' : false,
    '#DeathPersonForm' : false,
  },

  getAllBurialOfficials: function(handleData){
    // if(Object.keys(modalBurialDetails.burialOfficials).length == 0){
      $.get("/mapmanagement/getBurialOfficials/")
  		    	.done(function(data){
              bolist = $.parseJSON(data);
              modalBurialDetails.burialOfficials = bolist;
              return handleData(modalBurialDetails.burialOfficials);
            })
            .fail(function(data){
              new PNotify({
                      title: messages.burialDetails.getAllBurialOfficials.error.title,
                      type: 'error',
                      addclass: "stack-bottomright",
                      stack: person.stack_bottomright,
                      mouse_reset: false
                    });
              return handleData({});
            });
    // }else{
    //   return handleData(modalBurialDetails.burialOfficials);
    // }
  },

  getAndShowBurialOfficialsSelect: function(){
      modalBurialDetails.getAllBurialOfficials(function(bolist){
           var selectizeBo =  $('#burialOfficialsSelect').selectize({
              valueField: 'id',
              labelField: 'last_name',
              searchField: ['first_names','last_name'],
              sortField: 'score',
              maxItems: 100,
              options: bolist,
              optgroupField: 'optgroup',
              optgroups: [
                  {value: 'top', label: 'Recently used'},
                  {value: 'all', label: 'All'}
              ],
              render: {
                optgroup_header: function(data, escape) {
                    return '<div class="optgroup-header">' + escape(data.label) + '</div>';
                },
                item: function(item, escape){
                  return '<div>'
                  + item.last_name + ",&nbsp;" + item.first_names
                  + '</div>';
                },
                option: function(item, escape) {
                    return '<div>'
                    + item.last_name + ",&nbsp;" + item.first_names + "&nbsp;(" + item.title + ")"
                    + '</div>';
                }
              },
              onItemAdd: function(value, $item){
                if(!modalBurialDetails.containsBurialOfficial(value)){
                  var nonBo = false;
                  for (var i=0; i<$('#id_burialOfficial-TOTAL_FORMS').val(); i++){
                    if($('#id_burialOfficial-'+i+'-official_id').val() == ""){
                      nonBo = true;
                    }
                  }

                  var cloneResult = modalBurialDetails.cloneFormSet('.burial-official','burialOfficial', false);
                  var cleanNewElement = modalBurialDetails.cleanCloneResult(cloneResult.newElement);
                  var lastId = cloneResult.total;

                  $('#flexslider-burial-official').data('flexslider').addSlide(cleanNewElement, 0);
                  modalBurialDetails.cleanNamesClones('#flexslider-burial-official');

                  if(nonBo){
                    $('#flexslider-burial-official').data('flexslider').removeSlide(1);
                    modalBurialDetails.cleanNamesClones('#flexslider-burial-official');
                  }

                  for(var i = 0; i < bolist.length; i++){
                    if (bolist[i]['id'] == value){
                      $('#id_burialOfficial-'+(lastId-1)+'-official_first_names').val(bolist[i]['first_names']);
                      $('#id_burialOfficial-'+(lastId-1)+'-official_last_name').val(bolist[i]['last_name']);
                      $('#id_burialOfficial-'+(lastId-1)+'-official_types  option:first-child').attr("selected", "selected");
                      $('#id_burialOfficial-'+(lastId-1)+'-official_title').val(bolist[i]['title']);
                      $('#id_burialOfficial-'+(lastId-1)+'-official_id').val(bolist[i]['id']);
                    }
                  }
                  $('#flexslider-burial-official').data('flexslider').flexslider(0);
                  modalBurialDetails.addValueBurialOfficial(value);
                }
              },
              after: function(slider) {
                modalBurialDetails.currentBurialOfficialSlide = slider.currentSlide;
              },
              onItemRemove: function(value){
                // var element = $("#flexslider-burial-official :input[value='"+value+"']").attr('name');
                // var position = element.split('-')[1];
                var position = modalBurialDetails.burialOfficialsPosition[$('#id_id_person').val()][value];
                // modalBurialDetails.removeBurialOfficial(position,"burialOfficial");
                total = $('#flexslider-burial-official').data('flexslider').count;
                if(total == 1){
                  $('#flexslider-burial-official').find('input').each(function() {
                      $(this).val('');
                  });
                }else{
                  $('#flexslider-burial-official').data('flexslider').removeSlide(modalBurialDetails.burialOfficialsPosition[$('#id_id_person').val()][value]);
                }
                modalBurialDetails.deleteValueBurialOfficial(value);
              },
            });

            //Add label to selectize if burial officials already related to burial
            var initialSize = 0;
            var valTemp = "";
            var valsTemp = [];
            if(modalBurialDetails.burialOfficialsPosition[$('#id_id_person').val()] === undefined){
              modalBurialDetails.burialOfficialsPosition[$('#id_id_person').val()] = {} //initialize dictionary for person form
              initialSize = $('#flexslider-burial-official').data('flexslider').count;
              for (var i=0; i<initialSize; i++){
                valTemp = $($('#flexslider-burial-official').data('flexslider').slides[i]).find('input[id$=official_id]').val()
                // valTemp = $('#id_burialOfficial-'+i+'-official_id').val();
                if(valTemp != ""){
                  modalBurialDetails.burialOfficialsPosition[$('#id_id_person').val()][valTemp] = i;
                  valsTemp.push(valTemp);
                }
              }
            }else{
              valsTemp = Object.keys(modalBurialDetails.burialOfficialsPosition[$('#id_id_person').val()]);
            }
            selectizeBo[0].selectize.setValue(valsTemp);

            //if valsTemp.length > 0 burial officials already related then this change to the input selectize does not have to count
            if(valsTemp.length > 0){
              modalBurialDetails.hasFormBeenEdited['#BurialFormCounter'] = 0;
              modalBurialDetails.hasFormBeenEdited['#BurialForm'] = false;
            }

            //Burial officials in input work as tabs with the flexslider
            selectizeBo[0].selectize.$input.next().click(function(event){
              var _this = this;
              var ev = event;
              var values = $('#burialOfficialsSelect')[0].selectize.getValue();
              for (i=0;i<values.length;i++){
                if($("div[data-value='"+values[i]+"']").hasClass('active')){
                  $('#flexslider-burial-official').data('flexslider').flexslider(modalBurialDetails.burialOfficialsPosition[$('#id_id_person').val()][values[i]]);
                  continue;
                }
              }
            });
      });
  },

  cleanBurialOfficialsSelect: function(){
    //clean selectize
    if(modalBurialDetails.burialOfficialsPosition[$('#id_id_person').val()] === undefined){
      delete modalBurialDetails.burialOfficialsPosition[""];
    }else{
      delete modalBurialDetails.burialOfficialsPosition[$('#id_id_person').val()];
    }
    //clean flexslider and add originals
    if($("#flexslider-burial-official").data('flexslider') != undefined){
      while ($("#flexslider-burial-official").data('flexslider').count > 0){
          $("#flexslider-burial-official").data('flexslider').removeSlide(0);
      }
      for(i = 0; i<burialOfficialForm.flexsliderBurialOfficialOld.size(); i++){
        $("#flexslider-burial-official").data('flexslider').addSlide(burialOfficialForm.flexsliderBurialOfficialOld[i]);
      }
      $('#flexslider-burial-official').data('flexslider').flexslider(0);
    }
  },

  updatePersonIdtoBurialOfficialsDictionary: function(id_id_person){
    if (modalBurialDetails.burialOfficialsPosition[id_id_person] === undefined || Object.keys(modalBurialDetails.burialOfficialsPosition[id_id_person]).length == 0)
      modalBurialDetails.burialOfficialsPosition[id_id_person] = modalBurialDetails.burialOfficialsPosition[''];
  },

  cloneFormSet: function(selector, type, insertHtml) {
    var newElement;
    if($(selector).size() > 1){
      newElement = $(selector).eq(1).clone(true);
    }else{
      newElement = $(selector).first().clone(true);
    }
    var total = $('#id_' + type + '-TOTAL_FORMS').val();
    newElement.find('input').each(function() {
        var name = $(this).attr('name').replace(/-[0-9]+-/g,'-' + total + '-');
        var id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });
    newElement.find('select').each(function() {
        var name = $(this).attr('name').replace(/-[0-9]+-/g,'-' + total + '-');
        var id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });
    newElement.find('label').each(function() {
        var newFor = $(this).attr('for').replace(/-[0-9]+-/g,'-' + total + '-');
        $(this).attr('for', newFor);
    });
    var newid = newElement.attr('id').replace(/-[0-9]+/g,'-' + total);
    newElement.attr('id', newid);
    newElement.find('button').attr('onclick','modalBurialDetails.removeBurialOfficial('+total+',"burialOfficial")')
    total++;
    $('#id_' + type + '-TOTAL_FORMS').val(total);
    if(insertHtml)
      $(selector).last().after(newElement);
    return {total: total, newElement: newElement };
  },

  cleanCloneResult: function(element){
    var newId = element.attr('id').replace('_clone','')
    element.attr('id', newId);
    // element.find('input').each(function() {
    //     var newIdInput =  $(this).attr('id').replace('_clone','');
    //     $(this).attr('id', newId);
    // });
    var newClass = element.attr('class').replace('clone','')
    element.attr('class', newClass);
    return element;
  },

  cleanNamesClones: function(element){
    $(element).find('input').each(function() {
        var d = $(this).attr('id').length - '_clone'.length;
        if( d >= 0 && $(this).attr('id').lastIndexOf('_clone') === d){
          $(this).attr('name','');
        }
    });
    $(element).find('select').each(function() {
      var d = $(this).attr('id').length - '_clone'.length;
      if( d >= 0 && $(this).attr('id').lastIndexOf('_clone') === d){
        $(this).attr('name','');
      }
    });
  },

  removeFormSet: function(selector, type, position){
    var total = $('#id_' + type + '-TOTAL_FORMS').val();
    for ( var i = 0; i < $(selector).length; i++ ) {
      $($(selector)[i]).find('input').each(function() {
          var name = $(this).attr('name').replace(/-[0-9]+-/g,'-' + i + '-');
          var id = 'id_' + name;
          $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
      });
      $($(selector)[i]).find('label').each(function() {
          var newFor = $(this).attr('for').replace(/-[0-9]+-/g,'-' + i + '-');
          $(this).attr('for', newFor);
      });
      var newid = $($(selector)[i]).attr('id').replace(/-[0-9]+/g,'-' + i);
      $($(selector)[i]).attr('id', newid);
    }
    total--;
    $('#id_' + type + '-TOTAL_FORMS').val(total);
  },

  removeBurialOfficial: function(officialPosition, type){
    modalBurialDetails.burialOfficialsRemoved.push($('#id_burialOfficial-'+officialPosition+'-official_id').val());
    total = $('#flexslider-burial-official').data('flexslider').count;
    val = "";
    if($('#id_burialOfficial-'+officialPosition+'-official_id').val() != null)
      val = $('#id_burialOfficial-'+officialPosition+'-official_id').val();
    $('#burialOfficialsSelect')[0].selectize.removeItem(val, true);
  },

  getBurialOfficialsKeys: function(){
    var keys = [];
    for(var k in modalBurialDetails.burialOfficialsPosition[$('#id_id_person').val()]) keys.push(k);
    return keys;
  },

  containsBurialOfficial: function(value){
    for(var k in modalBurialDetails.burialOfficialsPosition[$('#id_id_person').val()]){
      if (k == value)
        return true;
    }
    return false;
  },

  addValueBurialOfficial: function(value){
    for(var k in modalBurialDetails.burialOfficialsPosition[$('#id_id_person').val()])
      modalBurialDetails.burialOfficialsPosition[$('#id_id_person').val()][k] = modalBurialDetails.burialOfficialsPosition[$('#id_id_person').val()][k] + 1;
    modalBurialDetails.burialOfficialsPosition[$('#id_id_person').val()][value] = 0;
  },

  deleteValueBurialOfficial: function(value){
    positionToDelete = modalBurialDetails.burialOfficialsPosition[$('#id_id_person').val()][value];
    for(var k in modalBurialDetails.burialOfficialsPosition[$('#id_id_person').val()]){
      if(modalBurialDetails.burialOfficialsPosition[$('#id_id_person').val()][k] > positionToDelete){
        modalBurialDetails.burialOfficialsPosition[$('#id_id_person').val()][k] = modalBurialDetails.burialOfficialsPosition[$('#id_id_person').val()][k] - 1;
      }
    }
    delete modalBurialDetails.burialOfficialsPosition[$('#id_id_person').val()][value];
  },

  validator: '',

  isANewPerson: function(){
    //edit_button will not exist if this is an 'unknown grave'
    var result = $('#id_id_person').val() === "" && $('#edit_buttons').length > 0;
    return result;
  },

  hasErrors: function(){
    return modalBurialDetails.validator.errorList.length > 0;
  },

  isInEditMode: function(){
    return $('#id_modalBurialDetails input:not([readonly]):not([type="hidden"]):not([disabled]):not([type="file"])').size() > 0;
  },

  validateClosingModal: function(){
    isEditMode = this.isInEditMode();
    isEmptyNewPerson = (this.isANewPerson() && !person.isEmptyForm("#DeathPersonForm") && !person.isEmptyForm('#BurialForm')) ? true : false;

    if(isEditMode && !isEmptyNewPerson){
      new PNotify({
  	        title: messages.burialDetails.validateClosingModal.title,
            text: messages.burialDetails.validateClosingModal.text,
  	        // type: type,
  	        addclass: "stack-bottomright",
  	        stack: {"dir1": "up","dir2": "left","firstpos1": 25,"firstpos2": 25},
  	        mouse_reset: false
  	  });
      return false;
    }else{
      modalBurialDetails.cleanBurialOfficialsSelect();
      $('#id_modalBurialDetails_all').remove();
      return true;
    }
  },

  open: function(data){
    if(data.indexOf('loginModal') > -1){
      location.reload();
    }else{
      $('body').append(data);
      $('#id_modalBurialDetails').modal({
        keyboard: false
      });
      $('#id_modalBurialDetails').one('shown.bs.modal', function (e) {
        $("#flexslider-memorial").resize();
      });
    }
  },

  /**
   * Delete memorial image by uuid
   * @param  {[type]} url /mapmanagement/deleteMemorialImages/(uuid: Image.id)
   */
  deleteMemorialImages: function(url, form, uuidImage){

    notificationService.confirm(
      function(){
        //set uuid image to send in form
        $('#id_memorial_image_id_delete').val(uuidImage);
        //init ladda on thumbnail that is being deleted
        var l = Ladda.create(document.querySelector('#thumb-'+uuidImage));
        l.start();

        $.post(url, $(form).serialize())
          .done(function(data){
            console.log(data);
            //remove thumbnail due it was succesfully deleted
            $('#thumb-'+uuidImage).parent().remove();
            //Reload prettyphoto template to remove photo just deleted from carousel
            prettyPhotoTemplate.getTemplate();

            //clean temp uuid to delete in case multiple images in carousel
            $('#id_memorial_image_id_delete').removeAttr('value');

            new PNotify({
              title: messages.memorialImages.delete.success.title,
              type: 'success',
              addclass: "stack-bottomright",
              stack: person.stack_bottomright,
              mouse_reset: false
            });
          })
          .always(function() {
            l.stop();
          })
          .fail(function(data){
            console.log(data.responseText);
            new PNotify({
              title: messages.memorialImages.delete.fail.title,
              type: 'error',
              addclass: "stack-bottomright",
              stack: person.stack_bottomright,
              mouse_reset: false
            });
          });
      },
      function(){
        //do nothing
      },
      messages.memorialImages.delete.confirmation.text
    );
  },

  clearFields: function(formElementSelector){
    var elements = $(formElementSelector).find('input');
    $('#id_id_person').val(''); //In case was called from reserved plot form
		for (i = 0; i < elements.size(); i++) {
			if(elements[i].type == 'text'){
				if(elements[i].value !== ""){
					elements[i].value = "";
				}
			}else{
				if(elements[i].type == "checkbox"){
					elements[i].checked = false;
				}
			}
		}
		var selects = $(formElementSelector).find('select');
		for (i = 0; i < selects.size(); i++) {
			if(selects[i].value !== "0" && selects[i].selectize !== undefined){
				selects[i].selectize.setValue(0);
			}else{
        selects[i].value = 0;
      }
		}
		var textarea = $(formElementSelector).find('textarea');
		for (i = 0; i < textarea.size(); i++) {
				textarea[i].value = "";
		}
  },

  hideOptionsAfterSave: function(){
    $('.hide-after-save').hide();
  },

};

var burialOfficialForm = {

  currentIdNew: 999,

  flexsliderBurialOfficialOld: [],

  updateFlexsliderBurialOfficialOld: function(newfbo){
    //create copy to maintain original burial officials
    burialOfficialForm.flexsliderBurialOfficialOld = jQuery.extend(true, {}, $('#flexslider-burial-official').data('flexslider').slides);
  },

  addNew: function(){
    var nonBo = false;
    if(Object.keys(modalBurialDetails.burialOfficialsPosition[$('#id_id_person').val()]).length == 0){
      nonBo = true;
    }

    var cloneResult = modalBurialDetails.cloneFormSet('.burial-official','burialOfficial', false);
    var cleanNewElement = modalBurialDetails.cleanCloneResult(cloneResult.newElement);
    var lastId = cloneResult.total;

    $('#flexslider-burial-official').data('flexslider').addSlide(cleanNewElement, 0);
    modalBurialDetails.cleanNamesClones('#flexslider-burial-official');

    if(nonBo){
      $('#flexslider-burial-official').data('flexslider').removeSlide(1);
      modalBurialDetails.cleanNamesClones('#flexslider-burial-official');
    }

    $('#id_burialOfficial-'+(lastId-1)+'-official_first_names').val("");
    $('#id_burialOfficial-'+(lastId-1)+'-official_last_name').val("");
    $('#id_burialOfficial-'+(lastId-1)+'-official_types').val(1);
    $('#id_burialOfficial-'+(lastId-1)+'-official_title').val("");
    $('#id_burialOfficial-'+(lastId-1)+'-official_id').val("");

    $('#flexslider-burial-official').data('flexslider').flexslider(0);
    modalBurialDetails.addValueBurialOfficial(burialOfficialForm.currentIdNew + 1);
  },

};
