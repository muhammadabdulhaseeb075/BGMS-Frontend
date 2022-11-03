/** @module Search People */

var searchSection = {

  showAdvanceSearch: true,
  // showBorderContainer: true,
  openned: false,

  resizeResults: function() {
    var mapSearch = document.getElementById("mapSearch").value;
    //217px is the distance from the top to the begining of the table results, includes total results, (not any more: filter height is now dynamic) and titles.
    var distanceFromTop = 217; 
    //Filter height
    distanceFromTop += $('.sidebar-form.sidebar-offcanvas.input-group').height();
    if(mapSearch == "True"){
      if ((window.innerHeight - distanceFromTop) <= $('#table-search-sorter tbody').height()) {
        $('#table-search-sorter tbody').css('max-height', window.innerHeight - distanceFromTop + 'px');
        $('.collapse-menu-results').height($('.collapse-menu-results .bootstrap-table').height() + $('#table-search-sorter tbody').height());
      } else {
        $('#table-search-sorter tbody').css('max-height', '200px');
        if ($('#table-search-sorter tbody').length != 0){
            $('.collapse-menu-results').height($('.collapse-menu-results .bootstrap-table').height() + $('#table-search-sorter tbody').height());
        }
      }
    }else{
      if(!searchSection.showAdvanceSearch){
        $('#table-search-sorter tbody').css('max-height', 'calc(70vh - 300px)');
      }else{
        $('#table-search-sorter tbody').css('max-height', 'calc(90vh - 300px)');
      }
      if ($('#table-search-sorter tbody').length != 0){
          $('.collapse-menu-results').height($('.collapse-menu-results .bootstrap-table').height() + $('#table-search-sorter tbody').height());
      }
    }

  },

  showOrHideAdvancedSearch: function() {
    if (searchSection.showAdvanceSearch) {
      $('#advanced-search-section').show();
      searchSection.showAdvanceSearch = false;
      $('#advanced-search-button-text').text('Less ');
      $('#advanced-search-button-icon').removeClass('glyphicon-chevron-down');
      $('#advanced-search-button-icon').addClass('glyphicon-chevron-up');
    } else {
      $('#advanced-search-section').hide();
      searchSection.showAdvanceSearch = true;
      $('#advanced-search-button-text').text('More ');
      $('#advanced-search-button-icon').removeClass('glyphicon-chevron-up');
      $('#advanced-search-button-icon').addClass('glyphicon-chevron-down');
    }
    var mapSearch = document.getElementById("mapSearch").value;
    if(mapSearch == "False"){
      searchSection.resizeResults();
    }
  },

  // showOrHideBorderContainer: function() {
  //   if(searchSection.showBorderContainer){
  //     // $('#container-left-menu').css('border','2px solid #999999');
  //     searchSection.showBorderContainer = false;
  //   }else{
  //     // $('#container-left-menu').css('border','0px');
  //     searchSection.showBorderContainer = true;
  //   }
  // },

  handleSearchBox: function() {
    if($('#search').hasClass('in')){
      $('#search').collapse('toggle');
      searchSection.openned = true;
    }else{
      if(searchSection.openned){
        $('#search').collapse('toggle');
        searchSection.openned = false;
      }
    }
  },

  clearSearhForm: function() {
    $('#search-form')[0].reset();
    $('#search-form').find('*').removeClass('floating-label-form-group-with-value');
    $(".search-results-div").empty();
    $('#burial_date_range').hide();
    $('.collapse-menu-results').height(0);
  },

  resetFloatingLabel: function(e) {
    if ($(this).val() == "" || $(this).val() == 'yyyy') {
      $(this).parent().removeClass("floating-label-form-group-with-value");
    }
  },

  init: function(){
    //Mask for input dates files
    $("#id_burial_date").mask("99/99/9999", {
      placeholder: "dd/mm/yyyy"
    });
    $("#id_burial_date_to").mask("99/99/9999", {
      placeholder: "dd/mm/yyyy"
    });
    $("#id_year_burial_date").mask("9999", {
      placeholder: "yyyy"
    });
    $("#id_year_burial_date_to").mask("9999", {
      placeholder: "yyyy"
    });

    $('#specific-date-check').change(function() {
      if ($(this).is(":checked")) {
        $('#burial_date_range').show();
        $('#year_burial_date_range').hide();
        $("#id_year_burial_date").val('');
        $('#id_year_burial_date').parent().removeClass("floating-label-form-group-with-value");
        $("#id_year_burial_date_to").val('');
        $('#id_year_burial_date_to').parent().removeClass("floating-label-form-group-with-value");
      } else {
        $('#burial_date_range').hide();
        $('#year_burial_date_range').show();
      }
    });

    //Disable floating label manually due to the input mask
    $("#id_year_burial_date").bind("propertychange change click keyup input paste", this.resetFloatingLabel);
    $("#id_year_burial_date").focusout(this.resetFloatingLabel);
    $("#id_year_burial_date_to").bind("propertychange change click keyup input paste", this.resetFloatingLabel);
    $("#id_year_burial_date_to").focusout(this.resetFloatingLabel);

    //Initialize form validation search form
    $('.search-form').validate({
      errorElement: "span",
      rules: {
        age: {min: 0, max: 150, digits: true},
        age_to: {min: 0, max: 150, digits: true},
      }
    });

    $('#burial_date_range input').datepicker({
      format: 'dd/mm/yyyy',
      keyboardNavigation: false,
      forceParse: false,
      autoclose: true
    });

    $('.death_date').on('changeDate', function(ev) {
      $(this).datepicker('hide');
      $(this).parent().addClass("floating-label-form-group-with-focus");
      $(this).parent().addClass("floating-label-form-group-with-value");
    });
  },

  formatterBurialDate: function(value, row){
      if (row['burial_date']) {
        return this.formatDate(row['burial_date']);
      } else {
        return '-';
      }
  },

  formatDate: function(value){
    if (value && value != "None") {
      let dateArray = value.split("-");
      return (parseInt(dateArray[2]) ? parseInt(dateArray[2]) : 'day') + ' ' + (parseInt(dateArray[1]) ? this.integerMonthToShort(parseInt(dateArray[1])) : 'month') + ' ' + (parseInt(dateArray[0]) ? parseInt(dateArray[0]) : 'year');
    } 
    else {
      return '-';
    }
  },

  integerMonthToShort: function(monthAsNumber) {
    let months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

    let returnValue = months[monthAsNumber-1];

    if (returnValue)
      return returnValue;
    else
      return 'MMM';
  },

  formatterAgeYears: function(value, row){
    if(!row['age_years'] && (row['age_months']>0 ||
        row['age_weeks']>0 || row['age_days']>0 ||
        row['age_hours']>0 || row['age_minutes']>0)){
        return '< 1';
    } else {
        return row['age_years'];
    }
  },

  resetFiltersTableResult: function(){
      $('#table-search-sorter').trigger('sortReset');
  }
}
