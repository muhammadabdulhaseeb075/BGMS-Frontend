/**
 * @module
 * @description
 * Model of a Form Field in a template
 *  csrfmiddlewaretoken - csrf token
 *  fields - json dictionary of fieldModel
 */
angular.module('bgmsApp.dataentry').service('formModel', [function(){
	return function Form(params){
		this.csrfmiddlewaretoken = params.csrfmiddlewaretoken;
		if(params.fields)
			this.fields = params.fields;
		else
			this.fields = {};
		
		this.getSerialisedParameters = function(){
			var data = {};
			data['csrfmiddlewaretoken'] = this.csrfmiddlewaretoken;
			for (var index in this.fields){
				var fieldName = this.fields[index][name];
				data[fieldName] = this.fields[index]['value'];
			}
			return data;
		}
	};	
}]);