(function($) {
  $(document).ready(function () {
    console.log($.fn.jquery);
  });
}(django.jQuery));

var csrftoken = document.getElementsByName("csrfmiddlewaretoken");

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function addCSRFTokenToHeader() {
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken[0].value);
      }
    }
  });
}

// do not continue until mainPartialFileLocation has a value (it will always have a value)
if (csrftoken.length===0) {
  var interval = setInterval(function() {
    csrftoken = document.getElementsByName("csrfmiddlewaretoken");
    if (csrftoken.length>0) {
      addCSRFTokenToHeader();
      clearInterval(interval);
    }
  }, 50);
}
else
  addCSRFTokenToHeader();

// increment id and name for element
function changeNameAndID(element, from, to) {
  var old_name = $(element).attr('name');
  var old_id = $(element).attr('id');
  
  //var re = new RegExp(from + '([^,]*)$/,'\ and$1', "g");

  if (old_name) {
    var index = old_name.lastIndexOf(from);
    $(element).attr('name', old_name.substring(0, index) + to + old_name.substring(index + String(from).length));
    //$(element).attr('name', old_name.substr(0, old_name.lastIndexOf(from)) + to);
  }
    //$(element).attr('name', old_name.replace(re, to));
  if (old_id) {
    var index = old_id.lastIndexOf(from);
    $(element).attr('id', old_id.substring(0, index) + to + old_id.substring(index + String(from).length));
    //$(element).attr('id', old_id.substr(0, old_id.lastIndexOf(from)) + to);
    //$(element).attr('id', old_id.replace(re, to));
  }
}

// increment ids for children inputs
function increment_form_ids(el, from, to) {
  $(':input', $(el)).each(function(i,e){
    changeNameAndID(e, from, to);
  })
}

// add inline form
function add_inline_form(id, hierarchy) {
  var empty = $('#survey_template_fields-2-empty');
  var fieldTable = empty.parents('.inline-related').find('table > tbody');
  var count = fieldTable.children().length;
  var copy = empty.clone(true);

  // change name and id
  changeNameAndID(copy, 'empty', count-2);

  // modify classes
  copy.removeClass("row1 row2 empty-form");
  copy.addClass("dynamic-survey_template_fields-2");
  copy.addClass("row"+((count % 2) == 0 ? 1 : 2));

  // set values
  if (id)
    copy.find('select').val(id); // select field
  if (hierarchy)
    copy.find('.vIntegerField').val(hierarchy); // set hierarchy

  // insert delete option (otherwise missing)
  var del = copy.find('.delete');
  del.append('<div><a class="inline-deletelink" href="javascript:void(0)">Remove</a></div>');
  del.click(function() {
    copy.remove();
    var fields = fieldTable.find('.dynamic-survey_template_fields-2');
    $.each(fields, function(index, value) {
      var originalPrefix = fields[index].id.match(/\d+$/);
      changeNameAndID(fields[index], originalPrefix, index);
      increment_form_ids(fields[index], originalPrefix, index);
    });

    $('input#id_survey_template_fields-2-TOTAL_FORMS').val($('input#id_survey_template_fields-2-TOTAL_FORMS').val()-1);
  });

  copy.insertBefore(empty);

  // change name and id of child elements
  increment_form_ids(empty.prev(), '__prefix__', count-2);

  // modify total forms count
  $('input#id_survey_template_fields-2-TOTAL_FORMS').val(count-1);

  return false;
}

var moveSelection = function(move_func, from, to) {
  move_func(from, to);
  SelectFilter.refresh_icons('id_feature_codes');
};

(function($) {
  $(document).ready(function () {
    
    // event to fix id
    var hyperlink = $('#survey_template_fields-2-empty').parents('.inline-related').find('.add-row a');
    hyperlink.click(function(e) {
      var newElement = $('#survey_template_fields-2-empty').prev()[0];
      changeNameAndID(newElement, newElement.id.match(/\d+$/)[0], $('input#id_survey_template_fields-2-TOTAL_FORMS').val()-1);
    });

    // event fired when select changes
    $("#id_master_templates").on('change', function(e) {
      e.preventDefault();
      console.log($(this).val());

      if ($(this).val()) {

        // remove all current template fields
        $('#survey_template_fields-2-empty').parents('.inline-related').find('.dynamic-survey_template_fields-2').remove();

        $.getJSON("/survey/masterTemplate/",{ id: $(this).val() }, function(result) {
          // set name field
          $('input[name="name"]').val(result.name);

          // set feature codes
          if (result.feature_codes) {
            moveSelection(SelectBox.move_all, 'id_feature_codes_to', 'id_feature_codes_from');
            var featureCodeIDs = result.feature_codes.map(function(a) { return a.id });
            $('#id_feature_codes_from').val(featureCodeIDs);
            moveSelection(SelectBox.move, 'id_feature_codes_from', 'id_feature_codes_to');
          }

          // add template fields
          $.each(result.fields, function( index, value ) {
            add_inline_form(value.id, value.hierarchy);
          });
        });
      }
    });
  })
}(django.jQuery))