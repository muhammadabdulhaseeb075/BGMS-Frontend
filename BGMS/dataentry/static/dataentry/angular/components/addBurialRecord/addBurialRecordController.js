/**
 * Template Creation Controller
 * @constructor
 * @ngInject
 */
angular.module('bgmsApp.dataentry').controller('addBurialRecordController', ['$window', '$scope', '$http', '$httpParamSerializer', '$timeout', '$state', 'uiGridConstants', 'templateModel', 'imageModel', 'formModel', 'tagModel', 'addBurialRecordService', 'templateCreationService', 'notificationHelper', 'arrayHelperService',
  function($window, $scope, $http, $httpParamSerializer, $timeout, $state, uiGridConstants, templateModel, imageModel, formModel, tagModel, addBurialRecordService, templateCreationService, notificationHelper, arrayHelperService) {
    // using view_model instead of this to avoid ambiguity inside functions
    var view_model = this;

    view_model.templateForm = {};
    view_model.template_name = '';
    view_model.templateChoices = [];
    view_model.book_name = '';
    view_model.image = {};
    view_model.template = {};
    view_model.baseDynamicForm = null;
    view_model.dynamicForm = {};
    view_model.dynamicFormFields = {};
    view_model.csrfmiddlewaretoken = '';
    view_model.records = {};
    view_model.loading = false;   
    view_model.imageViewerWidth = addBurialRecordService.getImageViewerWidth();

    $scope.loadingFormOption = false;
    view_model.formOptions = [];
    
    $scope.isEditing = false;
    
    view_model.tag = new tagModel({});
    view_model.savedTag = null;
    view_model.deletedTag = null;
    
    $scope.$watchCollection('addRecord.tag.extent', function(newTagExtent){
    	if(view_model.gridApi.grid){
    		view_model.gridApi.grid.refresh();
    	}
	});

    view_model.tableOptions = {
		excessColumns: 20,
		rowHeight: 50,
//		minRowsToShow: 4,
	    enableFiltering: false,
	    rowTemplate: jsAngularInterface.staticFilesLocation['rowTemplate.html']
    };
    
    view_model.gridApi = null;
    
    view_model.tableOptions.onRegisterApi = function(gridApi) {
    	view_model.gridApi = gridApi;
    	view_model.gridApi.grid.registerRowsProcessor( view_model.showInput );
    };
    
    
    /**
     * @function
     * @description
     * Loads the image, template choices, book choices and 
     * loads existing burial records into the table.
     * @returns {undefined}
     * 
     */
    view_model.initialise = function(){
    	$http.get('/dataentry/addBurialRecord/').
	  	  success(function(data, status, headers, config) {
	  		if(data.status==='ok'){
	  			//response correctly returned, proceed as normal
		  		view_model.templateForm = addBurialRecordService.createTemplateForm(data);
		  		var choices = view_model.templateForm.fields.templates.choices;
		  		for(var index in choices){
					var bookJson = angular.fromJson(choices[index]['label'].replace(/&quot;/g, '"'));
		  			view_model.templateChoices.push(new templateModel(bookJson));
		  			if(choices[index]['value']===data.fields.templates.value){
		  				view_model.template_name = view_model.templateChoices[index];
		  			}
		  		}
		  		if(choices.length>0){
		  			view_model.getTemplate();
		  		}
		  		view_model.image = new imageModel({
		  			"url": data.image.url.replace(/amp;/g,''),
		  			"comments": view_model.templateForm.fields.comments.value,
		  			"id": data.image.id,
		  			"extent": data.image.extent
		  		});
		  		choices = view_model.templateForm.fields.books.choices;
		  		for(var index in choices){
		  			if(view_model.image.url.indexOf(choices[index]['value'])!=-1){
		  				view_model.book_name = choices[index];
		  			}
		  		}
		  		view_model.records = addBurialRecordService.createBurialRecords(data.records);
	  		} else{
	  			//csrf error, reload to redirect to login page
	  			$window.location.href = location.href.substring(0, location.href.indexOf(location.hostname))+location.host+'/';
	  		}
	  	  }).
		  error(function(data, status, headers, config) {
			  console.log(data);
		  });
    };
    view_model.initialise();
    
    /**
     * @function
     * @description
     * Function to get the values of the column of in the template and create the
     * ui-grid table
     */
    view_model.getTemplate = function(){
    	console.log('changed');
    	$http.get('/dataentry/getTemplate/?template_id='+view_model.template_name.id).
	  	  success(function(data, status, headers, config) {
		  	if(data.status==='ok'){
	  			//response correctly returned, proceed as normal
		  		view_model.template = addBurialRecordService.createTemplate(data.template);
			  	view_model.tableOptions.columnDefs = view_model.template.columns;
			  	view_model.tableOptions.columnDefs.push({ 
			  		name: 'buttons',
			  		displayName: '',
			  		field: 'buttons', 
					width: 140,
			  		cellTemplate: jsAngularInterface.staticFilesLocation['editBurialRecordButton.html'] 
			  	});
			  	view_model.tableOptions.data = view_model.records;//addBurialRecordService.generateData(view_model.records, view_model.template.columns);
			  	var newRow = addBurialRecordService.createNewRow(view_model.template.columns);
			  	if(!view_model.tableOptions.data[0] || !view_model.tableOptions.data[0].isNewRow){
			  		view_model.tableOptions.data.splice(0, 0, newRow);
			  		view_model.tableOptions.data[0].editable = true;
			  		view_model.tableOptions.data[0].isNewRow = true;
			  		view_model.tableOptions.data[0].height = 142;
			  	}		  	
			  	//force showing & hiding of tags
			  	view_model.showInput( view_model.tableOptions.data );
		  		view_model.getFormData();
		  	} else{
	  			//csrf error, reload to redirect to login page
	  			$window.location.href = location.href.substring(0, location.href.indexOf(location.hostname))+location.host+'/';
		  	}
	  	  }).
		  error(function(data, status, headers, config) {
			  notificationHelper.createErrorNotification('There is no template for this book. Please contact your Site Administrator.');
			  console.log(data);
		  });
    };
    
    /**
     * @function
     * @description
     * Function to get all the form fields in burial, death and person and any related models.
     */
    view_model.getFormData = function(){
    	if(!view_model.baseDynamicForm){
        	$http.get('/dataentry/getDynamicForm/').
    	  	  success(function(data, status, headers, config) {
			  	if(data.status==='ok'){
		  			//response correctly returned, proceed as normal
	    	  		console.log(data);
	    	  		view_model.baseDynamicForm = templateCreationService.createTemplateForm(data);
	    	  		var fields = addBurialRecordService.createFormColumnFieldObjs(view_model.template.columns, view_model.baseDynamicForm);
	    	  		view_model.dynamicForm = new formModel({
	    	  			csrfmiddlewaretoken: view_model.baseDynamicForm['csrfmiddlewaretoken'],
	    	  			fields: fields
	    	  		});
			  	} else{
		  			//csrf error, reload to redirect to login page
		  			$window.location.href = location.href.substring(0, location.href.indexOf(location.hostname))+location.host+'/';
			  	}
    	  	  }).
    		  error(function(data, status, headers, config) {
    			  console.log(data);
    	  		  notificationHelper.createErrorNotification('Could not get template info.');
    		  });    	
    	} else {
    		var fields = addBurialRecordService.createFormColumnFieldObjs(view_model.template.columns, view_model.baseDynamicForm);
	  		view_model.dynamicForm.fields = fields;
    	}
    };
    
    /**
     * @function
     * @description
     * Function to submit a new record to the server and update the ui-grid height
     */
	$scope.submitRecord = function(gridrow){
		view_model.loading = true;
		var newRowData = addBurialRecordService.createNewRow(view_model.template.columns);
		var data = addBurialRecordService.createJsonPostData(view_model.template.columns);
		data['csrfmiddlewaretoken'] = view_model.dynamicForm.csrfmiddlewaretoken;
		data['template_id'] = view_model.template.id;
		var geojsonFormatter = new ol.format.GeoJSON({});
		data['tags-top_left_bottom_right'] = geojsonFormatter.writeGeometry(new ol.geom.MultiPoint([ol.extent.getTopLeft(view_model.tag.extent), ol.extent.getBottomRight(view_model.tag.extent)]));
		$http({
		    method: 'POST',
		    url: '/dataentry/getDynamicForm/',
		    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
		    data: $httpParamSerializer(data)	    
		}).success(function(returneddata, status, headers, config) {
			  view_model.loading = false;
			  if(returneddata.status==='ok'){
				  //response correctly returned, proceed as normal
				  newRowData.setField('SimpleColumn', 'person___id', returneddata['person___id']);
				  newRowData.tag = new tagModel({
					  id:returneddata['person___tag_id'],
					  extent: view_model.tag.extent
				  });
				  view_model.savedTag = newRowData.tag;
				  view_model.tag = new tagModel({});
				  view_model.tableOptions.data.push(newRowData);
		  		  notificationHelper.createSuccessNotification('Burial Record Saved.');
		  		  //clearing values on submit
		  		  addBurialRecordService.clearColumnValues(view_model.template.columns);
		  		  //resizing row according to it's actual height
		  		  $timeout(function(){
		  			  var actualHeight = angular.element(angular.element('[ui-grid-row="row"]')[view_model.tableOptions.data.length-2]).height();
			  		  view_model.gridApi.grid.rows[view_model.gridApi.grid.rows.length-1].height = actualHeight;
		  		  });
			  } else{
				  //csrf error, reload to redirect to login page
				  $window.location.href = location.href.substring(0, location.href.indexOf(location.hostname))+location.host+'/';
			  }
	  	  }).
		  error(function(data, status, headers, config) {
			  view_model.loading = false;
			  for(var key in data){
				  for(var index in view_model.dynamicForm.fields){
					  if(view_model.dynamicForm.fields[index]['name']===key){
						  view_model.dynamicForm.fields[index]['error'] = data[key][0];
					  } else{
						  view_model.dynamicForm.fields[index]['error'] = null;
					  }
				  }
			  	console.error('Could not save burial record: ' + key);
			  }
	  		  notificationHelper.createErrorNotification('Could not save burial record.');
		  });
	};

	
    /**
     * @function
     * @description
     * Function to mark image as finished and reload next image
     */
	view_model.finishedImage = function(){
		notificationHelper.createConfirmation("Finish Page","Are you sure this page is finished? You have entered "+(view_model.tableOptions.data.length-1)+" records. Please ensure all records have been entered.", 
			function(){
				var data = {};
				data['csrfmiddlewaretoken'] = view_model.dynamicForm.csrfmiddlewaretoken;
				data['comments'] = view_model.image.comments;
				data['book_name'] = view_model.book_name['value'];
				view_model.loading = true;
				$http({
				    method: 'POST',
				    url: '/dataentry/finishedImage/',
				    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
				    data: $httpParamSerializer(data)	    
				}).success(function(data, status, headers, config) {
					  location.reload();
		  		  	  console.log('success');
	//	  		  	  view_model.loading = false;
			  	  }).
				  error(function(data, status, headers, config) {
					  console.log('failure');
			  		  notificationHelper.createErrorNotification('Could not mark image as finished.');
		  		  	  view_model.loading = false;
				  });
	      	});
		
	};

	
    /**
     * @function
     * @description
     * Function to mark image as skipped and reload next image
     */
	view_model.skipImage = function(){

		notificationHelper.createConfirmation("Skip Page","Are you sure you want to skip this image? You have entered "+(view_model.tableOptions.data.length-1)+" records. This will mean the page is marked as incomplete.", 
			function(){
				var data = {};
				data['csrfmiddlewaretoken'] = view_model.dynamicForm.csrfmiddlewaretoken;
				data['comments'] = view_model.image.comments;
				data['book_name'] = view_model.book_name['value'];
				view_model.loading = true;
				$http({
				    method: 'POST',
				    url: '/dataentry/skipImage/',
				    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
				    data: $httpParamSerializer(data)	    
				}).success(function(data, status, headers, config) {
					  location.reload();
		  		  	  console.log('success');
	//	  		  	  view_model.loading = false;
			  	  }).
				  error(function(data, status, headers, config) {
					  console.log('failure');
			  		  notificationHelper.createErrorNotification('Could not skip image.');
		  		  	  view_model.loading = false;
				  });
	      	});		
	};
  
  /**
   * @function
   * @description
   * Switch to the next image
   */
  view_model.nextImage = function() {
    view_model.loading = true;
    
    var data = {
      csrfmiddlewaretoken: view_model.dynamicForm.csrfmiddlewaretoken,
      book_name: view_model.book_name['value'],
    };
    
    var config = {
      headers: { 
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    };
    
    $http.post('/dataentry/nextImage/', $httpParamSerializer(data), config)
      .then(function(response) {
        console.debug('Got next image:', response);
        location.reload();
        view_model.loading = false;
      })
      .catch(function(response) {
        console.error('Unable to go to next image:', response);
        notificationHelper.createErrorNotification('Couldn\'t go to next image.');
        view_model.loading = false;
      });
  };
  
  /**
   * @function
   * @description
   * Switch to the previous image
   */
  view_model.prevImage = function() {
    view_model.loading = true;
    
    var data = {
      csrfmiddlewaretoken: view_model.dynamicForm.csrfmiddlewaretoken,
      book_name: view_model.book_name['value'],
    };
    
    var config = {
      headers: { 
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    };
    
    $http.post('/dataentry/prevImage/', $httpParamSerializer(data), config)
      .then(function(response) {
        console.debug('Got previous image:', response);
        location.reload();
        view_model.loading = false;
      })
      .catch(function(response) {
        console.error('Unable to go to previous image:', response);
        notificationHelper.createErrorNotification('Couldn\'t go to previous image.');
        view_model.loading = false;
      });
  };
  
    /**
     * @function
     * @description
     * Function to switch to image from another book 
     */
	view_model.changeBook = function(){
		notificationHelper.createConfirmation("Change Book","Are you sure you want to switch to another book?",
			function(){
				var data = {};
				data['csrfmiddlewaretoken'] = view_model.dynamicForm.csrfmiddlewaretoken;
				data['book_name'] = view_model.book_name['value'];
				view_model.loading = true;
				$http({
				    method: 'POST',
				    url: '/dataentry/changeImage/',
				    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
				    data: $httpParamSerializer(data)	    
				}).success(function(data, status, headers, config) {
					  location.reload();
		  		  	  console.log('success');
			  	  }).
				  error(function(data, status, headers, config) {
					  console.log('failure');
			  		  notificationHelper.createErrorNotification('Could not change to book '+view_model.book_name['value']+'.'+' There are no unprocessed images in the book.');
		  		  	  view_model.loading = false;
				  });
	      	});		
	};

    
    /**
     * @function
     * @description
     * Function to save comment when user clicks out of the comment box
     */
	view_model.saveComment = function(){
		var data = {};
		data['csrfmiddlewaretoken'] = view_model.dynamicForm.csrfmiddlewaretoken;
		data['comments'] = view_model.image.comments;
		view_model.loading = true;
		$http({
		    method: 'POST',
		    url: '/dataentry/saveImageComment/',
		    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
		    data: $httpParamSerializer(data)	    
		}).success(function(data, status, headers, config) {
			  if(data.status==='ok'){
				//response correctly returned, proceed as normal
	  		  	  console.log('success');
		  		  notificationHelper.createSuccessNotification('Comment Saved.');
		  		  view_model.loading = false;
			  } else {
				  //csrf error, reload to redirect to login page
				  $window.location.href = location.href.substring(0, location.href.indexOf(location.hostname))+location.host+'/';
			  }
	  	  }).
		  error(function(data, status, headers, config) {
			  console.log('failure');
	  		  notificationHelper.createErrorNotification('Could not save comment.');
  		  	  view_model.loading = false;
		  });
	};

    
    /**
     * @function
     * @description
     * Function to delete a record from the server
     */
	$scope.deleteRecord = function(row){
		notificationHelper.createConfirmation("Delete Record","Are you sure you want to delete this burial record?", 
		  function(){
			console.log(view_model.tag);
			var formData = {};
			formData['csrfmiddlewaretoken'] = view_model.dynamicForm.csrfmiddlewaretoken;
			formData['person_id'] = row.getField('SimpleColumn', 'person', 'id');
			$http({
			    method: 'POST',
			    url: '/dataentry/deleteBurialRecord/',
			    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
			    data: $httpParamSerializer(formData)	    
			}).success(function(data, status, headers, config) {
			      view_model.submitLoading = false;
			      if(data.status==='ok'){
					  //response correctly returned, proceed as normal
		  		  	  console.log('success');
		  		  	  var index = view_model.tableOptions.data.indexOf(row);
		  		  	  view_model.deletedTag = row.tag.id;
		  		  	  view_model.tableOptions.data.splice(index, 1);
		  		  	  notificationHelper.createSuccessNotification('Successfully deleted burial record.');
			      } else{
					  //csrf error, reload to redirect to login page
					  $window.location.href = location.href.substring(0, location.href.indexOf(location.hostname))+location.host+'/';
				  }
		  	  }).
			  error(function(data, status, headers, config) {
				  view_model.submitLoading = false;
				  console.log('failure');
		  		  notificationHelper.createErrorNotification('Could not delete burial record.');
			  });
		});
	};
    
    /**
     * @function
     * @description
     * Function to show the editable fields when editRecord button is clicked.
     */
	$scope.editRecord = function(gridrow){
	    gridrow.height = 154;
		var row = gridrow.entity;
		row.editable = !row.editable;
		view_model.tag = angular.copy(row.tag);
	    view_model.gridApi.core.notifyDataChange( uiGridConstants.dataChange.EDIT );
	    //updating column fields with current values
	    addBurialRecordService.setColumnValues(view_model.template.columns, row, view_model.formOptions);
	};	

    
    /**
     * @function
     * @description
     * Function to submit an edited record to the server and update the ui-grid height
     */
	$scope.submitEditRecord = function(gridrow){
		view_model.loading = true;
		var row = gridrow.entity;
		var newRowData = addBurialRecordService.createNewRow(view_model.template.columns);
		var data = addBurialRecordService.createJsonPostData(view_model.template.columns);
		data['csrfmiddlewaretoken'] = view_model.dynamicForm.csrfmiddlewaretoken;
		data['template_id'] = view_model.template.id;
		data['person-person_id'] = row.getField('SimpleColumn', 'person', 'id');
		//if extent is valid
		if(view_model.tag.extent && view_model.tag.extent.length===4){
			var geojsonFormatter = new ol.format.GeoJSON({});
			data['tags-top_left_bottom_right'] = geojsonFormatter.writeGeometry(new ol.geom.MultiPoint([ol.extent.getTopLeft(view_model.tag.extent), ol.extent.getBottomRight(view_model.tag.extent)]));
			$http({
			    method: 'POST',
			    url: '/dataentry/updateBurialRecord/',
			    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
			    data: $httpParamSerializer(data)	    
			}).success(function(returneddata, status, headers, config) {
				  view_model.loading = false;
			      if(returneddata.status==='ok'){
					  //response correctly returned, proceed as normal
					  newRowData.setField('SimpleColumn', 'person___id', returneddata['person___id']);
					  newRowData.tag = new tagModel({
						  id:returneddata['person___tag_id'],
						  extent: view_model.tag.extent
					  });
					  view_model.savedTag = newRowData.tag;
					  view_model.tag = new tagModel({});
		  		  	  var index = view_model.tableOptions.data.indexOf(row);
		  		  	  view_model.tableOptions.data.splice(index, 1, newRowData);
			  		  notificationHelper.createSuccessNotification('Burial Record Updated.');
			  		  //clearing values on submit
			  		  addBurialRecordService.clearColumnValues(view_model.template.columns);
			  		  //resizing column on save
			  		  $timeout(function(){
			  			  var actualHeight = angular.element(angular.element('[ui-grid-row="row"]')[index-1]).height();
			  			  view_model.gridApi.grid.rows[index].height = actualHeight;
			  		  });
			  		  view_model.baseDynamicForm.fields['tags-top_left_bottom_right'].error = '';
			      } else{
					  //csrf error, reload to redirect to login page
					  $window.location.href = location.href.substring(0, location.href.indexOf(location.hostname))+location.host+'/';
			      }
		  	  }).
			  error(function(data, status, headers, config) {
				  view_model.loading = false;
				  for(var key in data){
					  for(var index in view_model.dynamicForm.fields){
						  if(view_model.dynamicForm.fields[index]['name']===key){
							  view_model.dynamicForm.fields[index]['error'] = data[key][0];
						  } else{
							  view_model.dynamicForm.fields[index]['error'] = null;
						  }
					  }
				  }
				  console.error(data);
		  		  notificationHelper.createErrorNotification('Could not update burial record.');
			  });
		} else{
			 view_model.baseDynamicForm.fields['tags-top_left_bottom_right'].error = 'Image tag needs to be drawn.';
		}
	};	

	
	/**
	 * @description
	 * Function called to cancle editing of existing row.
	 */
	$scope.cancleEdit = function(gridrow){
	    var row = gridrow.entity;
		row.editable = !row.editable;
		view_model.tag = new tagModel({});
		view_model.savedTag = angular.copy(row.tag);
	    view_model.gridApi.core.notifyDataChange( uiGridConstants.dataChange.EDIT );
	    addBurialRecordService.clearColumnValues(view_model.template.columns);
	    //resizing column on cancel
	    $timeout(function(){
	    	var index = view_model.tableOptions.data.indexOf(row);
		    var actualHeight = angular.element(angular.element('[ui-grid-row="row"]')[index-1]).height();
		    gridrow.height = actualHeight;
	    });
	    //clearing save tag error on cancle
		view_model.baseDynamicForm.fields['tags-top_left_bottom_right'].error = '';
	};
	

	/**
	 * @description
	 * Function called to cancle creation of new row.
	 */
	$scope.cancleNewRow = function(gridrow){
		view_model.tag = new tagModel({});
	    addBurialRecordService.clearColumnValues(view_model.template.columns);
	    //clearing save tag error on cancle
		view_model.baseDynamicForm.fields['tags-top_left_bottom_right'].error = '';
	};
	
	/**
	 * @description
	 * Function called when rows are rendered by the ui-grid
	 */
	view_model.showInput = function( renderableRows ){
		if(renderableRows[0]){
			if(renderableRows[0].height!=136)
				renderableRows[0].height=136;
			if(view_model.tag.extent && !view_model.tag.id){
				//if no tag id, it is a new row
				renderableRows[0].visible = true;
			} else{
				renderableRows[0].visible = false;
			}
		}
		if(view_model.tag.extent){
		    $scope.isEditing = true;
		} else{
		    $scope.isEditing = false;
		}
	    return renderableRows;
	  };
	  
	  /**
	   * @description
	   * @function
	   * Called from outside angular to update the ui-grid when the sidebar is hidden.
	   */
	  view_model.updateUiGrid = function(){
		  if(view_model.gridApi)
			  view_model.gridApi.core.handleWindowResize();
	  };
	  
  }
]);
