angular.module('bgmsApp.dataentry').service('addBurialRecordService', ['$timeout', '$http', '$q', '$log', 'fieldModel', 'formModel', 'columnModel', 'templateModel', 'imageModel', 'burialRecordService', 'manyToManyFieldService',
  function($timeout, $http, $q, $log, fieldModel, formModel, columnModel, templateModel, imageModel, burialRecordService, manyToManyFieldService){
	
	var view_model = this;

	view_model.columns = {};
	/**
	 * @function
	 * @description
	 * Function to create a form from the received data
	 */
	view_model.createTemplateForm = function(formdata){
		var csrfmiddlewaretoken = formdata.csrfmiddlewaretoken.value;
		var fields = {};
		for(var index in formdata.fields){
			var receivedField = formdata.fields[index];
			if(receivedField.choices){
				// temp fix to remove the http-encoding
				choices = receivedField.choices;
				for(var index in choices){
		  			choices[index].label = choices[index].label.replace(/amp;/g,'');	  
		  			choices[index].value = choices[index].value.replace(/amp;/g,'');
		  			choices[index].label = choices[index].label.replace(/&quot;/g, '"');
		  			choices[index].value = choices[index].value.replace(/&quot;/g, '"');
		  		}
			}
			fields[receivedField.name] = new fieldModel(receivedField);
		}
		var form = new formModel({
			"csrfmiddlewaretoken": csrfmiddlewaretoken,
			"fields": fields
		});
		return form;
	};
	
	view_model.createTemplate = function(templateData){
		var columns = [];
		for(var index=templateData.columns.length-1; index>=0; index--){
			var column = templateData.columns[index];
			var pos = templateData.columns[index]['position'];
			var subcolumns = null;
			if(column.type === 'CombinedColumn'){
				subcolumns = [];
				for(var i=0;i<column.subcolumns.length;i++){
					var subcolumn_position;
					//putting name subcolumns in order of title, firstname, lastname, nickname, birthname
					if(column.subcolumns[i].fieldname === 'title')
	                    subcolumn_position = 0;
	                else if(column.subcolumns[i].fieldname === 'first_names')
	                    subcolumn_position = 1;
	                else if(column.subcolumns[i].fieldname === 'last_name')                    
	                    subcolumn_position = 2;
	                else if(column.subcolumns[i].fieldname === 'other_names')                    
	                    subcolumn_position = 3;
	                else if(column.subcolumns[i].fieldname === 'birth_name')                    
	                    subcolumn_position = 4;
	                else
	                	subcolumn_position = i;
					column.subcolumns[i]["visible"] = true;
					column.subcolumns[i]["position"] = subcolumn_position;
					subcolumns[i] = new columnModel(column.subcolumns[i]);
				}
			}			
			column["visible"] = true;
			column["subcolumns"] = subcolumns;
			column["width"] = 124;
			column["cellTemplate"] = jsAngularInterface.staticFilesLocation['editableRowTemplate.html'];
			columns[pos] = new columnModel(column);
			columns[pos].setField();
		}
  		 var template = new templateModel({
	  		  "id": templateData.id,
  			  "name": templateData.name,
  			  "description": templateData.description,
  			  "burialImage": new imageModel({
  				  "id": templateData.book_name,
  				  "bookName": templateData.book_name,
  				  "pageNo": templateData.book_name
  			  }),
  			  "columns": columns 
  		  });
  		 return template;
	};

	view_model.generateData = function(records, columns){
		var data = [];
		for(var i=0;i<records.length;i++){
			data[i] = view_model.updateRecord(records[i], columns);
		}
		return data;
	};
	
	view_model.clearColumnValues = function(templateColumns){
		//length-2 to account for the last column being the submit buttons
		for (var index=templateColumns.length-2;index>=0;index--){
  			var column = templateColumns[index];
  			column.clearFieldValue();
		}
	};

	view_model.setColumnValues = function(templateColumns, burialRecord, formOptions){
		//length-2 to account for the last column being the submit buttons
  		for (var index=templateColumns.length-2;index>=0;index--){
  			var column = templateColumns[index];
  			var value = burialRecord.getField(column.type, column.modelname, column.fieldname);
  			column.setFieldValue(value, formOptions);
		}
	};
	
	/**
	 * @function
	 * @description
	 * Function that creates a new BurialRecord from column values
	 * @param {Array<Column>} columns - array of columns
	 */
	view_model.createNewRow = function(columns){
		var newRowData = burialRecordService.createBurialRecordFromColumns(columns);
		return newRowData;
	};
	
	view_model.createJsonPostData = function(columns){
		var data = {};
		for (var index=columns.length-2;index>=0;index--){
			if(columns[index].type!='ManyToManyKey')
				angular.extend(data, columns[index].jsonPostData());
		}
		//adding many to many data
		angular.extend(data, manyToManyFieldService.getJsonPostData());
//		debugger;
//		//quickfix for management form error
//		if(data['burial-burial_officials-INITIAL_FORMS']===undefined){
//			data['burial-burial_officials-INITIAL_FORMS']=0;
//			data['burial-burial_officials-MAX_NUM_FORMS']=1000;
//			data['burial-burial_officials-MIN_NUM_FORMS']=0;
//			data['burial-burial_officials-TOTAL_FORMS']=0;
//		}
		return data;
	};
	
	view_model.createBurialRecords = function(records){
		var burialRecords = [];
		for(var index in records){
			burialRecords.push(burialRecordService.createBurialRecord(records[index]));
		}
		return burialRecords;
	};


	/**
	 * @function
	 * @description
	 * Returns the width of the image viewer container
	 * @returns {Array<number>} the width & height of the image viewer in pixels
	 */
	view_model.getImageViewerWidth = function(){
		//height is set to max 300 in in dataentry.css
		return [angular.element('.col-md-12.add-record-50').width(), 300];
	}
	
	/**
	 * @function
	 * @description
	 * Create column fieldObjs from form
	 * @param columns {Array<Column>}
	 * @param form {Object}
	 * @returns {Array<Field>} fields
	 */
	view_model.createFormColumnFieldObjs = function(columns, form){
		var fields = [];
		//initialising manyToManyFieldService
		manyToManyFieldService.initialise(form.fields["burial-burial_officials"]["fieldObjs"], form.fields["burial-burial_officials"]["managementForm"]);

		//excluding last column because it has buttons
		for(var i=columns.length-2;i>=0;i--){
			var column = columns[i];
			var subcolumns = column.subcolumns;
			if(subcolumns){
				//combined column
				for(var j=0;j<subcolumns.length;j++){
					var subcolumn = subcolumns[j];
					var name = subcolumn['modelname']+'-'+subcolumn['fieldname'];
						var position = parseInt(subcolumn['position'], 10);
					form.fields[name]['position'] = position;
					subcolumn.fieldObjs.push(form.fields[name]);
					fields.push(form.fields[name]);
				}
			} else{
				var name = column['modelname']+'-'+column['fieldname'];
				var position = parseInt(column['position'], 10);
				form.fields[name]['position'] = position;
				if(column.type==='SimpleColumn'){
					//simple column
					column.fieldObjs.push(form.fields[name]);
					fields.push(form.fields[name]);		  				
				} else if(column.type==='ManyToManyKey'){
					//many to many column
					var m2m_fields = manyToManyFieldService.addMoreFields(column.throughField);
					column.fieldObjs.push(m2m_fields);
					column.csrfmiddlewaretoken = form['csrfmiddlewaretoken'];
					Array.prototype.push.apply(fields, m2m_fields);
					column.managementFields = form.fields[name]['managementForm'];
				} else{
					//foreign key column
					column.fieldObjs = form.fields[name]['fieldObjs'];
					Array.prototype.push.apply(fields, form.fields[name]['fieldObjs']);
				}
			}
		}
		Array.prototype.push.apply(fields, manyToManyFieldService.managementForm);
  		return fields;
	};
	
}]);