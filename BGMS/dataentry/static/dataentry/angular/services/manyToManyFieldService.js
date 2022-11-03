angular.module('bgmsApp.dataentry').service('manyToManyFieldService', ['fieldModel', function(fieldModel){
	
	var view_model = this;
	
	view_model.fieldObjsArray=null;
	view_model.fieldCount = 0;
	view_model.baseFieldObjs = null;
	view_model.managementForm = null;

	/**
	 * @function
	 * @description
	 * Function to create an empty many-to-many field
	 */
	view_model.initialise = function(fieldObjs, managementForm){
		view_model.fieldObjsArray=[];
		view_model.fieldCount = 0;
		view_model.baseFieldObjs = fieldObjs;
		view_model.managementForm = managementForm;
		view_model.managementForm[0].value = 0;
	}
	
	/**
	 * @function
	 * @description
	 * Function to generate and add more fields to the fieldObjs array for many-to-many fields.
	 */
	view_model.addMoreFields = function(throughField){
		var newFieldset = [];
		for( var j=0;j<view_model.baseFieldObjs.length;j++){
			var nameArray = view_model.baseFieldObjs[j].name.split('-');
			var idArray = view_model.baseFieldObjs[j].id.split('-');
			nameArray[2] = view_model.fieldObjsArray.length;
			idArray[2] = view_model.fieldObjsArray.length;
			var newField = new fieldModel(view_model.baseFieldObjs[j]);
			newField.name = nameArray.join('-');
			newField.id = idArray.join('-');
			if(newField.name.indexOf('burial_official_type')!=-1)
				newField.setValue(throughField);
			else
				newField.setValue('');
			newFieldset.push(newField);
		}
		view_model.fieldObjsArray.push(newFieldset);
		view_model.managementForm[0].value = parseInt(view_model.managementForm[0].value) + 1;
		return newFieldset;
	};
	

	/**
	 * @function
	 * @description
	 * Function to remove additional ManyToMany fields
	 */
	this.removeFields = function(fieldNumber){
		view_model.fieldObjsArray[fieldNumber] = null;;
		view_model.managementForm[0].value = parseInt(view_model.managementForm[0].value) - 1;
	};
	
	/**
	 * @function
	 * @description
	 * Function to remove all ManyToMany fields
	 */
	this.removeAdditionalFields = function(){
		view_model.fieldObjsArray=[];
		view_model.managementForm[0].value = 0;
	};

	
	/**
	 * @function
	 * @description
	 * Function to get many to many json data
	 */
	this.getJsonPostData = function(){
		var data = {};
		var fieldsets = view_model.fieldObjsArray;
		for(var j=0;j<fieldsets.length;j++){
				var fields = fieldsets[j];
				if(fields){
					for( var k in fields){
						var fieldObj = fields[k];
						if(fieldObj)
							data[fieldObj.name] = fieldObj.value;
					}	  				
				}  					
			}
		var fields = view_model.managementForm;
		for(var k=0;k<fields.length;k++){
			var fieldObj = fields[k];
			data[fieldObj.name] = fieldObj.value;
		}	  				  					
		return data;
	}
}]);