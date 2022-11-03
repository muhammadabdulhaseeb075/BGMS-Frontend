/**
 * @module
 * @description
 * Model of the Template
 *  id - unique id
 *  name - url of the image
 *  description - description
 *  burialImage - Image
 *  columns - array of Columns
 */
angular.module('bgmsApp.dataentry').service('templateModel', ['$filter', function($filter){
	
	return function Template(params){			
		this.id = params.id;	
		this.name = params.name;
		this.bookName = params.bookName;
		this.description = params.description;
		this.burialImage = params.burialImage;
		if(!params.columns)
			this.columms = [];
		else
			this.columns = params.columns;
		
		this.removeColumn = function(columnPosition){
			return this.columns.splice(columnPosition, 1);
		};

		
	    /**
	     * @function
	     * @description
	     * Function to get object to post to the server
	     */
		this.getTemplateJSON = function(){
			var columns = [];
			for (var index=0;index<this.columns.length;index++){
				if(this.columns[index].visible === true)
					columns.push(this.columns[index].id);
			}
			return {
				"name": this.name,
				"description": this.description,
				"burial_image": this.burialImage.id,
				"columns": columns
			};
		};
		

		/**
		 * @function
		 * @description
		 * Function to return the (column_id, displayName) tuple for all
		 * columns in the template. as a JSON string.
		 * @returns {String} JSON String
		 */
		this.getColumnDisplayNamesJson = function(){
			var columns = {};
			for(var index=0;index<this.columns.length;index++){
				if(this.columns[index].visible === true)
					columns[this.columns[index].id] = this.columns[index].displayName;
			}
			return angular.toJson(columns);
		};
	}	
	
}]);