/**
 * @module
 * @description
 * Model of a Form Field in a template
 *  id - html id
 *  name - html name
 *  type - type of the field - text, select or multiple-checkbox
 *  choices - select choices
 *  value - initial value
 */
angular.module('bgmsApp.dataentry').service('fieldModel', [function(){
	return function Field(params){
		this.id = params.id;
		this.name = params.name;
		this.label = params.label;
		this.maxlength = params.maxlength;
		this.type = params.type;
		this.choices = params.choices;
		this.value = params.value;
		this.position = params.position;
		this.error = params.error;
		
		/**
		 * @function
		 * @description
		 * Sets the field value and clears previous errors.
		 */
		this.setValue = function(value){
			if(this.type==='CheckboxInput' && typeof(value)!='boolean'){
				if(value==='True')
					value = true;
				else
					value = false;
			} else if(this.type==='NumberInput' && typeof(value)!='number'){
				value = parseInt(value);
				if(isNaN(value))
					value='';
			} 
			this.value = value;
			this.error = null;
		};
		
	};
	
}]);