angular.module('bgmsApp.dataentry').service('templateCreationService', ['formModel', 'fieldModel', 'columnModel', 'arrayHelperService', function(formModel, fieldModel, columnModel, arrayHelperService){
	
	var view_model = this;

	view_model.template = {};

    view_model.columnOptions = {
   		enableColumnResizing: true
    };
    
    view_model.rowOptions = {
	    enableRowSelection: true,
	    enableSelectAll: true,
	    selectionRowHeaderWidth: 35,
	    enableFiltering: true,
//    	rowTemplate: '<div grid="grid"><div ng-repeat="(colRenderIndex, col) in colContainer.renderedColumns track by col.colDef.name" class="ui-grid-cell" ng-class="{ \'ui-grid-row-header-cell\': col.isRowHeader, \'custom\': true }" ui-grid-cell></div></div>',
   		columnDefs: [
   		       {
   		    	   field: 'displayName', 
   		    	   displayName: 'Column Name',
   		    	   enableFiltering: true,
   		       	   enableSorting: false,
   		       	   enableHiding: false
   		       },
   		 ]
    };

	view_model._getPosition = function(name, array){
        for(var index in array){
        	if(array[index] === name)
        		return index;
        }
        return -1;
	};

	/**
	 * @function
	 * @description
	 * Creates an array of Column objects. If columnValues are present, it is based on an 
	 * existing template, otherwise it is for a new template.
	 * @param {Array<Object>}columnChoices - all columns
	 * @param {Array<Object>} columnValues - the columns in the based-on template
	 * @returns {Array<Column>} array of created columns
	 */
	view_model.createColumns = function(columnChoices){
		var columns = [];
		for(var index=0, len=columnChoices.length; index<len; index++){
			var columnJson = angular.fromJson(columnChoices[index]['label'].replace(/&quot;/g, '"'));
			visible = false;
			columnJson['position'] = index;
			columnJson['visible'] = visible;
			columns[index] = new columnModel(columnJson);
			columns[index].setMenu();
		}
		return columns;
	};
	
	/**
	 * @function
	 * @description
	 * Function to create a Form object
	 */
	view_model.createTemplateForm = function(formdata){
		var csrfmiddlewaretoken = formdata.csrfmiddlewaretoken.value;
		var fields = {};
		for(var index in formdata.fields){
			var receivedField = formdata.fields[index];
			if(receivedField.choices){
				var choices = receivedField.choices;
				for(var j in choices){
		  			choices[j].label = choices[j].label.replace(/amp;/g,'');	  
		  			choices[j].value = choices[j].value.replace(/amp;/g,'');				
		  		}
			}
			if(receivedField.type==='ForeignKey'){
				var foreignKeys = formdata['foreign_keys'][receivedField.name];
				var fieldObjs = [];
				for(var j in foreignKeys){
					var foreignField = new fieldModel(foreignKeys[j]);
					fieldObjs.push(foreignField);
					fields[foreignKeys[j].name] = foreignField;
		  		}
				fields[receivedField.name] = {"fieldObjs":fieldObjs,
												"type": receivedField.type};
			}
			else if(receivedField.type==='ManyToManyKey'){
				var manyToManyKeys = formdata['many_to_many_keys'][receivedField.name];
				var fieldObjs = [], managementForm = [];
				for(var j in manyToManyKeys['form_fields']){
					var manyToManyField = new fieldModel(manyToManyKeys['form_fields'][j]);
					fieldObjs.push(manyToManyField);
					fields[manyToManyKeys['form_fields'][j].name] = manyToManyField;
		  		}
				for(var j in manyToManyKeys['management_form']){
					var manyToManyField = new fieldModel(manyToManyKeys['management_form'][j]);
					managementForm.push(manyToManyField);
					fields[manyToManyKeys['management_form'][j].name] = manyToManyField;
		  		}
				fields[receivedField.name] = {"fieldObjs":fieldObjs,
												"managementForm": managementForm,
												"type": receivedField.type};
			}
			else {
				fields[receivedField.name] = new fieldModel(receivedField);
			}
		}
		var form = new formModel({
			"csrfmiddlewaretoken": csrfmiddlewaretoken,
			"fields": fields
		});
		return form;
	};
	

	/**
	 * @function
	 * @description
	 * Updates the template column if it has not already been updated
	 * @param {Column} column - the column object which has been moved
	 * @param {number} originalPosition
	 * @param {number} newPosition
	 * @returns {undefined}
	 */
	view_model.moveColumn = function(column, originalPosition, newPosition){
 		 var templateColumns = view_model.template.columns;
 		 var maxVisiblePosition = arrayHelperService.getObjectPosition('visible', false, view_model.template.columns)[0]-1;
 		 //bugfix to ensure last column doesn't go below hidden columns when it is visible
 		 if(column.visible===true && originalPosition<=maxVisiblePosition && newPosition>maxVisiblePosition)
 			newPosition = maxVisiblePosition;
 		 var newColumn = templateColumns[newPosition];
 		 if(column != newColumn){
 			 var old = templateColumns.splice(originalPosition,1)[0]; 
 	 		 templateColumns.splice(newPosition,0,old);  
 	 		 column.position = newPosition;
 		 } 		 
	};
	

	/**
	 * @function
	 * @description
	 * Hides a column and moves it to the bottom of the columns list, or
	 * shows a column and moves it to the right hand side of the column list
	 * @param {Column} column - the column object which needs to be moved
	 * @returns {number} column position
	 */
	view_model.setColumnVisibility = function(column){
 		 var templateColumns = view_model.template.columns;
 		 var oldPosition = arrayHelperService.getObjectPosition('name', column.name, view_model.template.columns)[0];
 		 var newPosition = null;
 		 if(column.visible){
 			newPosition = arrayHelperService.getObjectPosition('visible', false, view_model.template.columns)[0];
 			if(oldPosition<newPosition){
 				newPosition = oldPosition;
 			}
 			else if(newPosition===-1){
 				//bugfix to stop last column swapping place when all columns are visible
 				//and it is hidden and reshown
 				newPosition = oldPosition; 		 				
 			}		
 		 } else{
 			newPosition = view_model.template.columns.length-1;
 		 }
 		view_model.moveColumn(column, oldPosition, newPosition);
 		return newPosition;
	};


	/**
	 * @function
	 * @description
	 * Sorts the given array of columns into the correct position
	 * @param {Array<Column>} columns - the array of column object which needs to be sorted
	 * @returns {undefined}
	 */
	view_model.updateColumns = function(columns){
 		 var templateColumns = view_model.template.columns;
 		 for(var index = 0; index<columns.length; index++){
 			 var newPosition = columns[index]['position'];
 			 var oldPosition = arrayHelperService.getObjectPosition('id', columns[index]['id'], templateColumns)[0];
 			 var column = templateColumns[oldPosition];
 			 if(column){
 		    	//updating display names
 	 			 column.displayName = columns[index]['displayname'];
 				 if(newPosition!=oldPosition){
 					 view_model.moveColumn(column, oldPosition, newPosition);
 				 }
 			 } 
 		 }
	};
	
	/**
	 * @function
	 * @description
	 * Returns the width & height of the image viewer container
	 * @returns {Array<number>} the width of the image viewer in pixels
	 */
	view_model.getImageViewerWidth = function(){
		//height is set to 400 in dataentry.css
		return [angular.element('.burialImage').width(), 400];
	}
	
	/**
	 * @function
	 * @description
	 * Returns the default name for the template: either book name if it doesn't already exist, or
	 * bookName(n) if it does.
	 * @param {String} bookName - name of current book
	 * @param {Array<String>}namelist - list of existing names
	 */
	view_model.getDefaultTemplateName = function(bookName, nameChoices){
		var newName = bookName;
		var nameArray = angular.element.map(nameChoices, function(el) { 
			if(el.label.indexOf(bookName)!=-1)
				return el.label;
		});
		if(nameArray.length>0){
			//generate new name
			newName = bookName;
		}
		return newName;
	};
	
	/**
	 * @function
	 * @description
	 * Sets the style for image choices
	 */
	view_model.changeBurialImageDropdownStyle = function(images){
		for(var i=0;i<images.length;i++){
			if(images[i].hasTemplate){
				var element = angular.element('[label="Book from '+images[i].bookName+'"]');
				element.removeClass('hasTemplateFalse');
				element.addClass('hasTemplateTrue');
			} else{
				angular.element('[label="Book from '+images[i].bookName+'"]').addClass('hasTemplateFalse');
			}
		}
	};
}]);