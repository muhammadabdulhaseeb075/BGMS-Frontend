/**
 * Template Creation Controller
 * @constructor
 * @ngInject
 */
angular.module('bgmsApp.dataentry').controller('templateCreationController', ['$window', '$scope', '$http', '$httpParamSerializer', '$filter', '$timeout', '$stateParams', 'uiGridConstants', 'templateModel', 'imageModel', 'templateCreationService', 'notificationHelper', 'arrayHelperService', 
  function($window, $scope, $http, $httpParamSerializer, $filter, $timeout, $stateParams, uiGridConstants, templateModel, imageModel, templateCreationService, notificationHelper, arrayHelperService) {
    // using view_model instead of this to avoid ambiguity inside functions
    var view_model = this;
    
    view_model.submitLoading = false;
    
    view_model.imageViewerWidth = templateCreationService.getImageViewerWidth();

    view_model.form = {};

    view_model.templateId = $stateParams.templateId;
    
    view_model.template = templateCreationService.template;
    
    view_model.baseTemplate = null;
    
    view_model.columnOptions = templateCreationService.columnOptions; 
    view_model.columnApi = null;
    view_model.rowOptions = templateCreationService.rowOptions;
    view_model.rowApi = null;
    
    view_model.columnOptions.onRegisterApi = function(gridApi) {
    	view_model.columnApi = gridApi;
    	gridApi.colMovable.on.columnPositionChanged($scope,function(colDef, originalPosition, newPosition){
    		templateCreationService.moveColumn(colDef, originalPosition, newPosition);
	    });
    	gridApi.core.on.columnVisibilityChanged( $scope, function (column) {
    		view_model.rowApi.selection.toggleRowSelection(column.colDef);
    	});
	};    
	
    view_model.rowOptions.onRegisterApi = function (gridApi) {
    	view_model.rowApi = gridApi;
	    gridApi.selection.on.rowSelectionChanged($scope,function(row){
    		//setting Column visibility to false
	    	var column = row.entity;
	    	column.visible=row.isSelected;
    		//bugfix to ensure that doing hide column and restore doesn't move it 
    		//back to it's old place and break the order between table and checklist
    		var position = templateCreationService.setColumnVisibility(column);
    		var length = view_model.columnApi.grid.moveColumns.orderCache.length;
    		var cachedPosition = arrayHelperService.getObjectPosition('colDef', column, view_model.columnApi.grid.moveColumns.orderCache)[0];
			if(column.visible===true && cachedPosition!=-1)
    			view_model.columnApi.colMovable.moveColumn(cachedPosition, position);
	    	view_model.columnApi.core.notifyDataChange(uiGridConstants.dataChange.COLUMN);
	    });
	    gridApi.selection.on.rowSelectionChangedBatch($scope,function(rows){
	    	for(var index in rows){
	    		row = rows[index];
	    		row.entity.visible=row.isSelected;
	    	}
	    	view_model.columnApi.core.notifyDataChange(uiGridConstants.dataChange.COLUMN);
	    });
	};

	/**
	 * @function
	 * @description
	 * Function to initialise the template_form, columns and the ui-grid for
	 * the column and row tables
	 */
    view_model.initialise = function(){
    	var url = '/dataentry/createTemplate/';
    	if(view_model.templateId)
    		url = '/dataentry/editTemplate/?template_id='+view_model.templateId
    	$http.get(url).
	  	  success(function(data, status, headers, config) {
	  		  //create form
	  		  view_model.form = templateCreationService.createTemplateForm(data);	  
	  		  //create columns
	  		  var columnValues, columns;
	  		  columns = templateCreationService.createColumns(view_model.form.fields.columns.choices);
  			  //create Burial Images
	  		  var templateImage, images = [];
	  		  for(var index in view_model.form.fields.burial_image.choices){
	  			var imageValues = angular.fromJson(view_model.form.fields.burial_image.choices[index].label.replace(/&quot;/g, "\""));
	  			if(!imageValues["has_template"]){
					var imageValue = new imageModel({
						  url: imageValues['url'],
						  extent: imageValues['extent'],
						  id: view_model.form.fields.burial_image.choices[index].value,
						  hasTemplate: imageValues['has_template']
					  });
	  				images.push(imageValue);
					if(data.fields.burial_image.value===imageValue.id)
						templateImage = imageValue;
				}
	  		  }
	  		  if(!templateImage)
	  			templateImage = images[0];
	  		  view_model.form.fields.burial_image.choices = images;
	  		  //getting default name for template
	  		  if(!view_model.templateId)
	  			 view_model.form.fields.name.value = templateCreationService.getDefaultTemplateName(templateImage.bookName, view_model.form.fields.base_template.choices);
	  		  //create template
	  		  view_model.template = new templateModel({
	  			  "name": view_model.form.fields.name.value, 
	  			  "description": view_model.form.fields.description.value, 
	  			  "burialImage": templateImage,
	  			  "columns": columns 
	  		  });
	  		  templateCreationService.template = view_model.template;
	  		  //initialise templateColumnsTable columns 
	  		  view_model.columnOptions.columnDefs = columns;
	  		  //initialise base_template for edit template
	  		  if(view_model.templateId){
	  			  var baseChoices = view_model.form.fields.base_template.choices;
	  			  for(var i=0;i<baseChoices.length;i++){
	  				  if(baseChoices[i]['value']===view_model.form.fields.base_template.value){
			  			  view_model.baseTemplate = baseChoices[i];
			  			  view_model.changeTemplate();
			  			  break;
	  				  }	  				  
	  			  }
	  		  }
	  		  //initialise templateRowsTable rows 
	  		  view_model.rowOptions.data = columns;
	  		//setting different styles for image dropdown
	  		$timeout(function(){
	  			templateCreationService.changeBurialImageDropdownStyle(view_model.form.fields.burial_image.choices);
	  		});	  		  
	  	  }).
		  error(function(data, status, headers, config) {
			  if(status===403){
				  //csrf error, reload to redirect to login page
				  $window.location.href = location.href.substring(0, location.href.indexOf(location.hostname))+location.host+'/';
			  } else{
				  console.log(data);	  
			  }
		  });
    };	  
    view_model.initialise();  

	/**
	 * @function
	 * @description
	 * Function to generate a default template name when the image is changed.
	 */
    view_model.changeImage = function(){
		//getting default name for template
		view_model.template.name = templateCreationService.getDefaultTemplateName(view_model.template.burialImage.bookName, view_model.form.fields.base_template.choices);
    };

	/**
	 * @function
	 * @description
	 * Function to change template columns based on the base template
	 */
    view_model.changeTemplate = function(choice){
    	console.log('changed');
    	//resetting display names
  		for(var index=0;index<view_model.template.columns.length;index++){
  			view_model.template.columns[index]['displayName'] = view_model.template.columns[index]['defaultDisplayName'];
  		}
    	view_model.rowApi.core.notifyDataChange(uiGridConstants.dataChange.ALL);
    	if(view_model.baseTemplate){
        	$http.get('/dataentry/getTemplate/?template_id='+view_model.baseTemplate.value).
    	  	  success(function(data, status, headers, config) {
    	  		if(data.status==='ok'){
    	  			//response correctly returned, proceed as normal
        	  		view_model.rowApi.selection.clearSelectedRows();
        	  		templateCreationService.updateColumns(data.template.columns);
        	    	view_model.columnApi.core.notifyDataChange(uiGridConstants.dataChange.COLUMN);
    		  		$timeout(function(){
    		  			for(var index in data.template.columns){
    		  				//show only columns that are not compulsary
    		  				if(data.template.columns[index].is_compulsary!=true)
    		  					view_model.rowApi.selection.selectRowByVisibleIndex(index);
        		  		}
        			  	notificationHelper.createSuccessNotification('Successfully loaded columns from template '+ view_model.baseTemplate.label+'.');
    		  		});
        	    	
    	  		} else{
    	  			//csrf error, reload to redirect to login page
    	  			$window.location.href = location.href.substring(0, location.href.indexOf(location.hostname))+location.host+'/';
    	  		}
    	  	  }).
    		  error(function(data, status, headers, config) {
    			  console.log(data);
    	  		  notificationHelper.createErrorNotification('Could not load columns from template '+ view_model.baseTemplate.label+'.');
    		  });
    	} else {
    		view_model.rowApi.selection.clearSelectedRows();
    	}
    };

	/**
	 * @function
	 * @description
	 * Helper function to get the position of an object in an array
	 */
    view_model.getPosition = function(key, value, array){
        //optimise this
        var positions = [-1];
        var i = 0;
        angular.forEach(array, function(marker, index) {
            if(marker[key] === value){
                positions[i++] = index;
            }
        });
        return positions;
    };

	/**
	 * @function
	 * @description
	 * Function to save a new template to the server
	 */
	view_model.submit = function(){
		var formData = view_model.template.getTemplateJSON();
		formData['csrfmiddlewaretoken'] = view_model.form['csrfmiddlewaretoken'];
		formData['column_displaynames'] = view_model.template.getColumnDisplayNamesJson();
	    view_model.submitLoading = true;
		$http({
		    method: 'POST',
		    url: '/dataentry/createTemplate/',
		    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
		    data: $httpParamSerializer(formData)	    
		}).success(function(data, status, headers, config) {
		      view_model.submitLoading = false;
			  for(var index in view_model.form.fields){
				  view_model.form.fields[index].error = undefined;
			  }
  		  	  console.log('success');
  		  	  //add current template to base template list
  		  	  view_model.form.fields.base_template.choices.push({
  		  		  'value': data['template_id'],
  		  		  'label': view_model.template.name
  		  	  });
  		  	  //clear template on success
  		  	  view_model.template.name='';
  		  	  view_model.template.description='';
  		  	  view_model.baseTemplate = null;
  		      //set current burialImage hasTemplate to 'true'
  		  	  view_model.template.burialImage.hasTemplate = true;
  	  		  //setting different styles for image dropdown
  		  	  $timeout(function(){
  		  		templateCreationService.changeBurialImageDropdownStyle(view_model.form.fields.burial_image.choices);
  		  	  });  	  		  
  	  		  //set template_image to first book without a template
  		  	  var images = view_model.form.fields.burial_image.choices;
  		  	  for(var i=0;i<images.length;i++){
  		  		  if(!images[i].hasTemplate){
  		  			view_model.template.burialImage = images[i];
  		  		  	  view_model.changeImage();  		  			  
  		  		  }
  		  	  }
  		  	  //clear columns
			  view_model.rowApi.selection.clearSelectedRows();
	  		  notificationHelper.createSuccessNotification('Successfully created template '+ view_model.template.name+'.');
//	  		});
	  	  }).
		  error(function(data, status, headers, config) {
			  if(status===403){
				  //csrf error, reload to redirect to login page
				  $window.location.href = location.href.substring(0, location.href.indexOf(location.hostname))+location.host+'/';
			  } else{
				  view_model.submitLoading = false;
				  for(var index in view_model.form.fields){
					  view_model.form.fields[index].error = undefined;
				  }
				  for(var index in data){
					  view_model.form.fields[index].error = data[index][0];
				  }
				  console.log('failure');
		  		  notificationHelper.createErrorNotification('Could not create template.');  
			  }
		  });
	};    

	/**
	 * @function
	 * @description
	 * Function to save an edited template to the server
	 */
	view_model.updateTemplate = function(){
		var formData = view_model.template.getTemplateJSON();
		formData['csrfmiddlewaretoken'] = view_model.form['csrfmiddlewaretoken'];
		formData['column_displaynames'] = view_model.template.getColumnDisplayNamesJson();
		formData['id'] = view_model.templateId;
	    view_model.submitLoading = true;
		$http({
		    method: 'POST',
		    url: '/dataentry/editTemplate/',
		    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
		    data: $httpParamSerializer(formData)	    
		}).success(function(data, status, headers, config) {
		      view_model.submitLoading = false;
  		  	  console.log('success');
  		  	  notificationHelper.createSuccessNotification('Successfully updated template '+ view_model.template.name+'.');
	  	  }).
		  error(function(data, status, headers, config) {
			  if(status===403){
				  //csrf error, reload to redirect to login page
				  $window.location.href = location.href.substring(0, location.href.indexOf(location.hostname))+location.host+'/';
			  } else{
				  view_model.submitLoading = false;
				  for(var index in view_model.form.fields){
					  view_model.form.fields[index].error = undefined;
				  }
				  for(var index in data){
					  view_model.form.fields[index].error = data[index][0];
				  }
				  console.log('failure');
		  		  notificationHelper.createErrorNotification('Could not update template.');  
			  }
		  });
	};      

	  /**
	   * @description
	   * @function
	   * Calle from outside angular to update the ui-grid when the sidebar is hidden.
	   */
	  view_model.updateUiGrid = function(){
		  if(view_model.columnApi)
			  view_model.columnApi.core.handleWindowResize();
		  if(view_model.rowApi)
			  view_model.rowApi.core.handleWindowResize();
	  };
  }
]);
