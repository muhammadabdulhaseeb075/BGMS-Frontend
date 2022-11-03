/**
 * @module
 * @description
 * Model of a Burial Record in the table
 *  simpleKeys - Json dict of all simple keys as 'modelname___fieldname': key
 *  combinedColumns - Json dict of all combined columns as 'modelname___fieldname': key
 *  foreignKeys - Json dict of all foreign keys as 'modelname___fieldname': key
 *  manyToManyKeys - Json dict of many to many keys as 'modelname___fieldname': [
 *  	'subfieldname': subfieldvalue,
 *  	.
 *  	.
 *  	.
 *  ]
 */
angular.module('bgmsApp.dataentry').service('burialRecordModel', ['$http', '$window', '$httpParamSerializer', 'fieldModel', 'notificationHelper', function($http, $window, $httpParamSerializer, fieldModel, notificationHelper){	
	return function BurialRecord(){
		var self = this;
		this.simpleKeys = {};
		this.combinedColumns = {};
		this.foreignKeys = {};
		this.manyToManyKeys = {};
		this.tag = undefined;

		/**
		 * @function
		 * @description
		 * Returns the field value 
		 */
		this.getField = function(columnType, columnModelname, columnFieldName, subcolumnName, index){
			var columnName = columnModelname + '___' + columnFieldName;
			if(columnType==="SimpleColumn"){
				return this.simpleKeys[columnName];
			} else if(columnType==="CombinedColumn"){
				if(subcolumnName)
					return this.combinedColumns[columnName][subcolumnName];
				else
					return this.combinedColumns[columnName];
			} else if(columnType==="ManyToManyKey"){
				if(index && subcolumnName)
					return this.manyToManyKeys[columnName][index][subcolumnName];
				else if(index)
					return this.manyToManyKeys[columnName][index];
				else
					return this.manyToManyKeys[columnName];
			} else if(columnType==="ForeignKey"){
				if(subcolumnName)
					return this.foreignKeys[columnName][subcolumnName];
				else
					return this.foreignKeys[columnName];
			}
		};
		
		/**
		 * @function
		 * @description
		 * Sets the field value 
		 */
		this.setField = function(columnType, columnName, value, subcolumnName, index){
			if(columnType==="SimpleColumn"){
				this.simpleKeys[columnName] = value;
			} else if(columnType==="CombinedColumn"){
				if(subcolumnName)
					this.combinedColumns[columnName][subcolumnName] = value;
				else
					this.combinedColumns[columnName] = value;
			} else if(columnType==="ManyToManyKey"){
				if(index && subcolumnName)
					this.manyToManyKeys[columnName][index][subcolumnName] = value;
				else if(index)
					this.manyToManyKeys[columnName][index] = value;
				else
					this.manyToManyKeys[columnName] = value;
			} else if(columnType==="ForeignKey"){
				if(subcolumnName)
					this.foreignKeys[columnName][subcolumnName] = value;
				else
					this.foreignKeys[columnName] = value;
			}
		};

		/**
		 * @function
		 * @description
		 * Checks if the field should be displayed or if it is empty
		 */
		this.doesFieldExist = function(columnType, columnModelname, columnFieldName, subcolumnName, index){
			var field = this.getField(columnType, columnModelname, columnFieldName, subcolumnName, index);
			if(field===0 || field==='0' || field==='' || field===null || field===undefined)
				return false;
			else
				return true;
		};

		/**
		 * @function
		 * @description
		 * Checks if the field should be displayed, has zero value or is empt
		 */
		this.doesFieldExistOrHasZeroValue = function(columnType, columnModelname, columnFieldName, subcolumnName, index){
			const field = this.getField(columnType, columnModelname, columnFieldName, subcolumnName, index);
			if( field==='' || field===null || field===undefined)
				return false;
			else
				return true;
		};



		/**
		 * @function
		 * @description
		 * Converts numeric month to mon
		 */
		this.getFieldMonth = function(columnType, columnModelname, columnFieldName, subcolumnName){
			var field = this.getField(columnType, columnModelname, columnFieldName, subcolumnName);
			switch(parseInt(field)){
				case 1: return 'Jan';
				case 2: return 'Feb';
				case 3: return 'Mar';
				case 4: return 'Apr';
				case 5: return 'May';
				case 6: return 'Jun';
				case 7: return 'Jul';
				case 8: return 'Aug';
				case 9: return 'Sep';
				case 10: return 'Oct';
				case 11: return 'Nov';
				case 12: return 'Dec';
				default: return '-';
			}
		};

		
		/**
		 * @function
		 * @description
		 * Deletes the burial official from the server by passing person id and  official id.
		 */
		this.removeManyToManyField = function(columnType, columnModelname, columnFieldName, csrfmiddlewaretoken, index){
			var burialOfficial = this.getField(columnType, columnModelname, columnFieldName)[index];			
			notificationHelper.createConfirmation("Delete Burial Official","Are you sure you want to remove "+
					burialOfficial['title']+" "+burialOfficial['first_names']+" "+burialOfficial['last_name']+
					"from this burial record?", 
			  function(){
				var formData = {};
				formData['csrfmiddlewaretoken'] = csrfmiddlewaretoken;
				formData['person_id'] = self.getField('SimpleColumn', 'person', 'id');
				formData['official_id'] = burialOfficial['id'];
				$http({
				    method: 'POST',
				    url: '/dataentry/deleteBurialOfficial/',
				    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
				    data: $httpParamSerializer(formData)	    
				}).success(function(data, status, headers, config) {
					if(data.status==='ok'){
						  //response correctly returned, proceed as normal
			  		  	  console.log('success');
			  		  	  self.getField(columnType, columnModelname, columnFieldName).splice(index, 1);
			  		  	  notificationHelper.createSuccessNotification('Successfully deleted burial official.');
					} else{
					  //csrf error, reload to redirect to login page
					  $window.location.href = location.href.substring(0, location.href.indexOf(location.hostname))+location.host+'/';
					}
			  	  }).
				  error(function(data, status, headers, config) {
					  console.log('failure');
			  		  notificationHelper.createErrorNotification('Could not delete burial official.');
				  });
			});
		};
		
	};
	
}]);