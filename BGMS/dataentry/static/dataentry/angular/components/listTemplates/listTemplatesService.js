angular.module('bgmsApp.dataentry').service('listTemplatesService', ['templateModel', 'columnModel', 'imageModel', 
  function(templateModel, columnModel, imageModel){

	var view_model = this;

	/**
	 * @function
	 * @description
	 * Function to generate columns from response data
	 */
	view_model.createColumns = function(columnChoices){
		var columns = [];
		for(var index=columnChoices.length-1; index>=0; index--){
			columns[index] = new columnModel({
				"fieldname": columnChoices[index]['fieldname'],
				"modelname": columnChoices[index]['fieldname'],
				"displayname": columnChoices[index]['displayname'],
				"visible": true,
				"position": index
			});
		}
		return columns;
	};

	/**
	 * @function
	 * @description
	 * Function to create templates from the response data
	 */
	view_model.cerateTemplates = function(templateData){
		var templates = [];
		for(var index in templateData){
			templates[index] = new templateModel({
				'id': templateData[index]['id'],
				'name': templateData[index]['name'],
				'description': templateData[index]['description'],
				'burialImage': new imageModel({
		  			  url: templateData[index]['burial_image'],
		  			  id: templateData[index]['burial_image']
		  		  }),
				'columns': view_model.createColumns(templateData[index]['columns'])
			});
		}
		return templates;
	};
	
}]);