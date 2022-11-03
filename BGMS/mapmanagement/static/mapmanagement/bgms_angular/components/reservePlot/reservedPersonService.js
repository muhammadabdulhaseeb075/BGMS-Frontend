/**
 * @module reservedPersonService
 *
 * @description
 * This model contains the reserved Person details.
 *
 */
angular.module('bgmsApp.map').service('reservedPersonService', ['$http','modalHelperService', function($http, modalHelperService){

  var view_model = this;

  /**
   * Storage for reserved persons
   * @type {array}
   * Sample:
   * [ 
        grave_plot__uuid: [uuid]
        grave_plot_id: [uuid]
        person__first_names: [string]
        person__last_name: [string]
        person__other_names: [string]
        person_id: [uuid]
        origin__feature_type: [Feature_code]
     ]
   */
  view_model.reservedPersons = [];

  /**
   * Return Origin for reserved Person
   * @return {[string]}
   */
  view_model.getOrigin = function (rp) {
    return rp.origin__feature_type;
  };

  /**
   * Get request to retrieve reserved persons
   * @param  {[String]} url [description]
   * @return {[type]}     [description]
   */
  view_model.loadReservedPersonsFromGeoJson = function(){
        $http.get('/mapmanagement/getReservedPersons/').
        success(function(data, status, headers, config) {
  			var reserved_persons = data.reserved_persons;
        console.log(reserved_persons);
        view_model.reservedPersons = data.reserved_persons;
        //TODO: refresh layer to reserved_plot

  			// for(var i=0;i<features.length;i++){
				// var personDetails = features[i];
				// if(personDetails['id'] != null){
				// 	view_model.addPerson(personDetails['id'], personDetails['memorial_id'],
				// 		personDetails['first_names'], personDetails['last_name'],
				// 		(personDetails['burial_date'] === null)? 'Unknown':new Date(personDetails['burial_date']),
				// 		personDetails['age_years'], personDetails['age_months'],
				// 		personDetails['age_weeks'], personDetails['age_days'],
				// 		personDetails['age_hours']);
				// }
			  // }
        }).
        error(function(data, status, headers, config) {
            console.log('could not load data from '+ config.url);
        });
  };
  
  view_model.removeReservedPerson = function(person_id){

    for(let i = 0; i<view_model.reservedPersons.length; i++){
      if(view_model.reservedPersons[i].person_id === person_id){
        view_model.reservedPersons.splice(i, 1);
        break;
      }
    }

  };

  /**
   * Return array with reserved persons found by plot
   * @param  {[string]} graveplotUuid [id plot]
   * @return {[array]}
   */
  view_model.getPersonsReservedByPlotId = function(graveplotUuid){
    var prbp = [];
    for(var i = 0; i<view_model.reservedPersons.length; i++){
      if(view_model.reservedPersons[i].grave_plot__uuid === graveplotUuid){
        prbp.push(view_model.reservedPersons[i]);
      }
    }
    return prbp;
  };

}]);
