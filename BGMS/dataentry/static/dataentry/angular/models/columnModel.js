/**
 * @module
 * @description
 * Model of a Column Field in a template
 *  modelname - name of the django model it belongs to
 *  fieldname - django fieldname
 *  name - modelname___fieldname, used for uniquely identifying a column
 *  dispalyName - display name of the column
 *  defaultDisplayName - the default displayname of the columns to revert to
 *  position - position in template
 *  visible - select choices
 *  fieldObj - 
 */
angular.module('bgmsApp.dataentry').service('columnModel', ['fieldModel', 'notificationHelper', 'uiGridConstants', 'manyToManyFieldService', function(fieldModel, notificationHelper, uiGridConstants, manyToManyFieldService){	
	return function Column(params){
		if(params.modelname || params.fieldname){
			this.modelname = params.modelname;
			this.fieldname = params.fieldname;
			this.name = params.modelname+'___'+params.fieldname;
			if(params.through)
				this.name = params.modelname+'___'+params.fieldname+'___'+params.through;
//			this.field = params.modelname+'***'+params.fieldname;
		}
		this.id = params.id;
		this.minWidth = 100;
		this.enableColumnMenu = false;
		this.defaultDisplayName = params.name;
		this.displayName = params.displayname;
		this.throughField = params.through;
		this.position = params.position;
		this.visible = params.visible;
		this.cellTemplate = params.cellTemplate;
		this.subcolumns = params.subcolumns;
		this.type = params.type;
		if(params.fieldObjs){
			if(this.type==='ManyToManyKey')
				this.fieldObjs = [params.fieldObjs];
			else 
				this.fieldObjs = params.fieldObjs;
		}
		else
			this.fieldObjs = [];
		this.managementFields = params.managementFields;
		
		this.addProfession = false;
		this.addReligion = false;
		this.addEvent = false;
		this.addParish = false;

		/**
		 * @function
		 * @description
		 * Function to retrieve field from the BurialRecordModel object.
		 */
		this.setField = function(){
			console.log(this.type);
			this.field = 'getField("'+this.type+'", "'+this.modelname+'", "'+this.fieldname+'")';
		};
		
		/**
		 * @function
		 * @description
		 * Function to add Edit Name and Hide Column options to the menu .
		 */
		this.setMenu = function(){
			this.enableColumnMenu = true;
			this.enableFiltering = false;
			this.enableSorting = false;
	       	this.menuItems = [
	           {
	              title: 'Edit Name',
	              icon: 'ui-grid-icon-info-circled',
	              action: function($event) {
	            	  var column = this.context.col.colDef;
	            	  var grid =  this.grid;
	            	  notificationHelper.createPrompt("Change Display Name: "+column.displayName, 
		            	  "Use the box below to enter the column name that matches the image column name in the register.", function(newName){
		            		  column.displayName = newName;
		            		  grid.api.core.notifyDataChange( uiGridConstants.dataChange.COLUMN );
		            	  });
	              }
	            }
	  		];
		};
		
		/**
		 * @function
		 * @description
		 * Function to generate and add more fields to the fieldObjs array for many-to-many fields.
		 */
		this.addMoreFields = function(){
			var isFieldEmpty = true;
			var currentField = this.fieldObjs[this.fieldObjs.length-1];
			for( var j=0;j<currentField.length;j++){
				if(currentField[j].value!='' && currentField[j].type!='HiddenInput'){
					isFieldEmpty = false;
					break;
				}				
			}
			if(!isFieldEmpty){
				var newFieldset = manyToManyFieldService.addMoreFields(this.throughField);
				this.fieldObjs.push(newFieldset);
			}
		};
		
		/**
		 * @function
		 * @description
		 * Function to remove additional ManyToMany fields
		 */
		this.removeAdditionalFields = function(){
			var currentField = this.fieldObjs[0];
			for(var i=1;i<this.fieldObjs.length;i++){
				var fieldNo = this.fieldObjs[i][0].name.split('-')[2];
				manyToManyFieldService.removeFields(fieldNo);
				this.fieldObjs[i] = null;
			}
			this.fieldObjs = [currentField];
		};

		/**
		 * @function
		 * @description
		 * Function to set the field value for the fields in the fieldObjs array
		 * for many-to-many fields, combined fields, simple fields and foreign-key fields.
		 */
		this.setFieldValue = function(value, formOptions){
		    if(this.type==='SimpleColumn'){
				var fieldObj = this['fieldObjs'][0];
				fieldObj.setValue(value);
  			} else if(this.type==='CombinedColumn'){
  				var subcolumns = this.subcolumns;
  				for(var j in subcolumns){
  					var subcolumn = subcolumns[j];
  	  				var fieldObj = subcolumn['fieldObjs'][0];
					fieldObj.setValue(value[subcolumn.modelname+'___'+subcolumn.fieldname]);
  				}
  			} else if(this.type==='ForeignKey'){
                var fields = this['fieldObjs'];
                for(var j in fields){
                    var fieldObj = fields[j];
                    var subcolumnName = fieldObj.name.split('-').pop();
                    fieldObj.setValue(value[subcolumnName]);

                    if(this.name==='person___profession') {
                      fieldObj.choices = formOptions.professionOptions;
                    }
                    else if(this.name==='death___religion') {
                      fieldObj.choices = formOptions.religionOptions;
                    }
                    else if(fieldObj.name==='death-event-name') {
                      fieldObj.choices = formOptions.eventOptions;
                    }
                    else if(this.name==='death___parish') {
                      fieldObj.choices = formOptions.parishOptions;
                    }
                }
  			} else if(this.type==='ManyToManyKey'){
  				this.removeAdditionalFields();
  				var fieldsets = [];
  				for(var i=0;i<value.length;i++){
  					if(value[i]['burial_official_type']===this.throughField)
  						fieldsets.push(value[i]);
  				}
  				for(var j=0;j<fieldsets.length;j++){
  					if(j>0)
  						this.addMoreFields();
  					var valueSet = fieldsets[j];
  					var currentFieldset = this.fieldObjs[j];
  					for(var k=0;k<currentFieldset.length;k++){
  						var fieldObj = currentFieldset[k];
  	  	  				var subcolumnName = fieldObj.name.split('-').pop();
  	  	  				fieldObj.setValue(valueSet[subcolumnName]);  	
  					}	  	
  				}
  			}
		};
		
		/**
		 * @function
		 * @description
		 * Function to clear the field value for the fields in the fieldObjs array
		 * for many-to-many fields, combined fields, simple fields and foreign-key fields.
		 */
		this.clearFieldValue = function(resetFlags=true){
			if(this.type==='SimpleColumn'){
				var fieldObj = this['fieldObjs'][0];
				fieldObj.setValue('');
  			} else if(this.type==='CombinedColumn'){
  				var subcolumns = this.subcolumns;
  				for(var j in subcolumns){
  					var subcolumn = subcolumns[j];
  	  				var fieldObj = subcolumn['fieldObjs'][0];
					fieldObj.setValue('');
  				}
  			} else if(this.type==='ForeignKey'){
  	  			var fields = this['fieldObjs'];
  	  			for(var j=0;j<fields.length;j++){
  	  				var fieldObj = fields[j];
					fieldObj.setValue('');  	  				
  	  			}
  			} else if(this.type==='ManyToManyKey'){
  				this.removeAdditionalFields();
  				var fieldsets = this['fieldObjs'];
  				for( var j in fieldsets){
  					var fields = fieldsets[j];
  					for( var k=0;k<fields.length;k++){
  						var fieldObj = fields[k];
  						if(fieldObj.name.indexOf('burial_official_type')!=-1)
  							fieldObj.setValue(this.throughField);
  						else
  							fieldObj.setValue('');  	
  					}	  				  					
  				}
				}
				
				if (resetFlags)
					this.resetFlags();
		};

		/**
		 * Resets the flags
		 */
		this.resetFlags = function() {
			this.addProfession = false;
			this.addReligion = false;
			this.addEvent = false;
			this.addParish = false;
		}
		
		/**
		 * @function
		 * @description
		 * Function to set the error.
		 */
		this.setFieldError = function(error){
			if(this.type==='SimpleColumn'){
				var fieldObj = this['fieldObjs'][0];
				fieldObj.error = error;
  			} else if(this.type==='CombinedColumn'){
  				var subcolumns = this.subcolumns;
  				for(var j in subcolumns){
  					var subcolumn = subcolumns[j];
  	  				var fieldObj = subcolumn['fieldObjs'][0];
  					fieldObj.error = error;
  				}
  			} else if(this.type==='ForeignKey'){
  	  			var fields = this['fieldObjs'];
  	  			for(var j in fields){
  	  				var fieldObj = fields[j];
  					fieldObj.error = error;			
  	  			}
  			} else if(this.type==='ManyToManyKey'){
  				this.removeAdditionalFields();
  				var fieldsets = this['fieldObjs'];
  				for( var j in fieldsets){
  					var fields = fieldsets[j];
  					for( var k in fields){
  						var fieldObj = fields[k];
  						fieldObj.error = error;
  					}	  				  					
  				}
  			}
		};
		
		/**
		 * @function
		 * @description
		 * Function to get the json post data as an object in the fieldname: value format
		 */
		this.jsonPostData = function(){
			var data = {};
			if(this.type==='SimpleColumn'){
				var fieldObj = this['fieldObjs'][0];
				data[fieldObj.name] = fieldObj.value;
  			} else if(this.type==='CombinedColumn'){
  				var subcolumns = this.subcolumns;
  				for(var j in subcolumns){
  					var subcolumn = subcolumns[j];
  	  				var fieldObj = subcolumn['fieldObjs'][0];
  					data[fieldObj.name] = fieldObj.value;
  				}
  			} else if(this.type==='ForeignKey'){
  	  			var fields = this['fieldObjs'];
  	  			for(var j in fields){
  	  				var fieldObj = fields[j];
  					data[fieldObj.name] = fieldObj.value;
  	  			}
  			} else if(this.type==='ManyToManyKey'){
  				var fieldsets = this['fieldObjs'];
  				for( var j =0;j<fieldsets.length;j++){
  					var fields = fieldsets[j];
  					for( var k in fields){
  						var fieldObj = fields[k];
  						if(fieldObj)
  							data[fieldObj.name] = fieldObj.value;
  					}	  				  					
  				}
  				var fields = this['managementFields'];
				for( var k=0;k<fields.length;k++){
					var fieldObj = fields[k];
					data[fieldObj.name] = fieldObj.value;
				}	  				  					
  			}
			return data;
		};
		
		/**
		 * @function
		 * @description
		 * Function to get the field value of the column
		 */
		this.columnValue = function(){
			var data = {};
			if(this.type==='SimpleColumn'){
				var fieldObj = this['fieldObjs'][0];
				data[this.name] = fieldObj?fieldObj.value:'';
  			} else if(this.type==='CombinedColumn'){
  				var subcolumns = this.subcolumns;
  				data[this.name] = {};
  				for(var j in subcolumns){
  					var subcolumn = subcolumns[j];
  	  				var fieldObj = subcolumn['fieldObjs'][0];
  	  				data[this.name][subcolumn.name] = fieldObj?fieldObj.value:'';
  				}
  			} else if(this.type==='ForeignKey'){
  	  			var fields = this['fieldObjs'];
  				data[this.name] = {};
  	  			for(var j in fields){
  	  				var fieldObj = fields[j];
  	  				data[this.name][fieldObj.name.split('-').pop()] = fieldObj?fieldObj.value:'';
  	  			}
  			} else if(this.type==='ManyToManyKey'){
  				var fieldsets = this['fieldObjs'];
  				data[this.name] = [];
  				for( var j=0;j<fieldsets.length;j++){
  					data[this.name][j] = {}
  					var fields = fieldsets[j];
  					for( var k=0; k<fields.length;k++){
  						var fieldObj = fields[k];
  						data[this.name][j][fieldObj.name.split('-').pop()] = fieldObj?fieldObj.value:'';
  					}	  				  					
  				}
  			}
			return data;
		};
		
	};
	
}]);