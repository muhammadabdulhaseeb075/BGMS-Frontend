/**
 * Template Creation Controller
 * @constructor
 * @ngInject
 */
angular.module('bgmsApp.dataentry').controller('listTemplatesController', ['$window', '$scope', '$http', '$httpParamSerializer', '$filter', 'templateModel', 'imageModel', 'listTemplatesService', 'notificationHelper',
  function($window, $scope, $http, $httpParamSerializer, $filter, templateModel, imageModel, listTemplatesService, notificationHelper) {
    // using view_model instead of this to avoid ambiguity inside functions
    var view_model = this;
    
    view_model.submitLoading = false;

    view_model.templates = [];

    view_model.csrfmiddlewaretoken = '';

    view_model.templateColumnsUpdate = [];    

	/**
	 * @function
	 * @description
	 * Function to initialise the csrftoken and templates
	 */
    view_model.initialise = function(){
    	$http.get('/dataentry/listTemplates/').
	  	  success(function(data, status, headers, config) {
	  		  //create form
	  		  view_model.csrfmiddlewaretoken = data.csrfmiddlewaretoken;
	  		  view_model.templates = listTemplatesService.cerateTemplates(data.templates);
	  		  for(var index in view_model.templates){
	  			view_model.templates[index].columnOptions = {
	  					columnDefs: view_model.templates[index]['columns']
		  	    };
	  		  }
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
    
//	view_model.submit = function(){
//		var formData = view_model.template.getTemplateJSON();
//		formData['csrfmiddlewaretoken'] = view_model.csrfmiddlewaretoken;
//	    view_model.submitLoading = true;
//		$http({
//		    method: 'POST',
//		    url: '/dataentry/deleteTemplate/',
//		    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
//		    data: $httpParamSerializer(formData)	    
//		}).success(function(data, status, headers, config) {
//		      view_model.submitLoading = false;
//  		  	  console.log('success');
//  		  	  notificationHelper.createSuccessNotification('Successfully created template '+ view_model.template.name+'.');
//	  	  }).
//		  error(function(data, status, headers, config) {
//			  if(status===403){
//				  //csrf error, reload to redirect to login page
//				  $window.location.href = location.href.substring(0, location.href.indexOf(location.hostname))+location.host+'/';
//			  } else{
//				  view_model.submitLoading = false;
//				  console.log('failure');
//		  		  notificationHelper.createErrorNotification('Could not create template.');			  
//			  }
//		  });
//	};    

	/**
	 * @function
	 * @description
	 * Function to delete template from the server by passing template id.
	 */
    view_model.deleteTemplate = function(template){
    	notificationHelper.createConfirmation("Delete Record","Are you sure you want to delete the template "+template.name+"?", 
    		function(){
	    		var formData = {};
	    		formData['csrfmiddlewaretoken'] = view_model.csrfmiddlewaretoken;
	    		formData['template_id'] = template.id;
	    	    view_model.submitLoading = true;
	    		$http({
	    		    method: 'POST',
	    		    url: '/dataentry/deleteTemplate/',
	    		    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
	    		    data: $httpParamSerializer(formData)	    
	    		}).success(function(data, status, headers, config) {
	    		      view_model.submitLoading = false;
	      		  	  console.log('success');
	      		  	  var position = view_model.getPosition('id', template.id, view_model.templates);
	      		  	  view_model.templates.splice(position, 1);
	      		  	  notificationHelper.createSuccessNotification('Successfully deleted template '+ template.name+'.');
	    	  	  }).
	    		  error(function(data, status, headers, config) {
	    			  if(status===403){
	    				  //csrf error, reload to redirect to login page
	    				  $window.location.href = location.href.substring(0, location.href.indexOf(location.hostname))+location.host+'/';
	    			  } else{
		    			  view_model.submitLoading = false;
		    			  console.log('failure');
		    	  		  notificationHelper.createErrorNotification('Could not delete template.');		  
	    			  }
	    		  });
    	});
    };

//    view_model.editTemplate = function(template){
//		var formData = {};
//		formData['csrfmiddlewaretoken'] = view_model.csrfmiddlewaretoken;
//		formData['template_id'] = template.id;
//	    view_model.submitLoading = true;
//		$http({
//		    method: 'POST',
//		    url: '/dataentry/deleteTemplate/',
//		    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
//		    data: $httpParamSerializer(formData)	    
//		}).success(function(data, status, headers, config) {
//		      view_model.submitLoading = false;
//  		  	  console.log('success');
//  		  	  var position = view_model.getPosition('id', template.id, view_model.templates);
//  		  	  view_model.templates.splice(position, 1);
//  		  	  notificationHelper.createSuccessNotification('Successfully deleted template '+ template.name+'.');
//	  	  }).
//		  error(function(data, status, headers, config) {
//			  if(status===403){
//				  //csrf error, reload to redirect to login page
//				  $window.location.href = location.href.substring(0, location.href.indexOf(location.hostname))+location.host+'/';
//			  } else{
//				  view_model.submitLoading = false;
//				  console.log('failure');
//		  		  notificationHelper.createErrorNotification('Could not delete template.');	  
//			  }
//		  });
//    };
  }
]);
