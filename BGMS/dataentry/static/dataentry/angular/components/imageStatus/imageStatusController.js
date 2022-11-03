/**
 * Template Creation Controller
 * @constructor
 * @ngInject
 */
angular.module('bgmsApp.dataentry').controller('imageStatusController', ['$window', '$timeout', '$scope', '$http', '$httpParamSerializer', '$filter', '$state', 'imageStatusService', 'imageHistoryModel', 'imageModel', 'notificationHelper', 'uiGridConstants',
  function($window, $timeout, $scope, $http, $httpParamSerializer, $filter, $state, imageStatusService, imageHistoryModel, imageModel, notificationHelper, uiGridConstants) {
    // using view_model instead of this to avoid ambiguity inside functions
    var view_model = this;
    
    view_model.submitLoading = false;

    view_model.csrfmiddlewaretoken = '';

    view_model.imageHistory = [];    
    
    view_model.summary = {};
    
    view_model.historyTable = {
      rowHeight: 50,
      enableFiltering: true,
      columnDefs: [
        {
          field: 'image', 
          displayName: 'Burial Register',
          enableSorting: true,
          enableHiding: false,
          cellTemplate: jsAngularInterface.staticFilesLocation['imageCell.html'],
          sort: {
            direction: uiGridConstants.DESC,
            priority: 0
          },
          sortingAlgorithm: function(a, b) {
            aVal = a.bookName + " " + a.pageNo;
            bVal = b.bookName + " " + b.pageNo;
            return aVal > bVal ? -1 : 1;
          },
          filter: {
            condition: function(searchTerm, cellValue) {
              var actualCellValue = "Book from " + cellValue.bookName + ", page no. " + cellValue.pageNo;
              actualCellValue = actualCellValue.replace('-', '\\-').replace('.', '\\.');
              return actualCellValue.indexOf(searchTerm) >= 0;
            },
            type: uiGridConstants.filter.INPUT,
          },
        },
        {
          field: 'comments', 
          displayName: 'Comments',
          enableSorting: true,
          enableHiding: true,
          enableFiltering: false,
        },
        {
          field: 'status', 
          displayName: 'Status',
          enableSorting: true,
          enableHiding: true,
          filter: {
            condition: uiGridConstants.filter.STARTS_WITH,
            type: uiGridConstants.filter.SELECT,
            selectOptions: [
              { value: "Unprocessed", label: "Unprocessed" },
              { value: "Processing", label: "Processing" },
              { value: "Processed", label: "Processed" },
            ],
          },
        }
      ]
    };

    /**
     * @function
     * @description
     * Function to initialise the imageHistory model and put it into the ui-grid.
     */
    view_model.initialise = function(){
      $http.get('/dataentry/getImageStatus/').
        success(function(data, status, headers, config) {
          
          // Create form
          view_model.csrfmiddlewaretoken = data.csrfmiddlewaretoken;
          view_model.summary["done"] = data.summary.done;
          view_model.summary["remaining"] = data.summary.remaining;
          
          data.imageHistory = $filter('orderBy')(data.imageHistory, 'time', true);
          for (var i = 0; i < data.imageHistory.length; i++) {
            var image = new imageModel(data.imageHistory[i].image);
            view_model.imageHistory.push(new imageHistoryModel({
              "image": image,
              "status": data.imageHistory[i].status,
              "comments": data.imageHistory[i].comments,
              "time": data.imageHistory[i].time,
            }));
            view_model.historyTable.data = view_model.imageHistory;
          }
        }).
        error(function(data, status, headers, config) {
          if (status === 403) {
            //csrf error, reload to redirect to login page
            $window.location.href = location.href.substring(0, location.href.indexOf(location.hostname))+location.host+'/';
          } else {
            console.log(data);
          }
        });
    };
    view_model.initialise(); 
    
    $scope.changeImage = function(row){
    	if(view_model.submitLoading === false){
    	    view_model.submitLoading = true;
    		var formData = {};
    		formData['csrfmiddlewaretoken'] = view_model.csrfmiddlewaretoken;
    		formData['image_id'] = row.image.id;
    		$http({
    		    method: 'POST',
    		    url: '/dataentry/changeToImage/',
    		    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    		    data: $httpParamSerializer(formData)	    
    		}).
    	  	  success(function(data, status, headers, config) {
    	  		$state.go('home', {'imageId': row.image.id});
    	  	  }).
    	  	  error(function(data, status, headers, config) {	
    			  view_model.submitLoading = false;
    			  console.log('failure');
    			  if(status===400)
    				  notificationHelper.createErrorNotification('Could not open image. '+data.message);
    			  else if(status===403){
    				  //csrf error, reload to redirect to login page
    				  $window.location.href = location.href.substring(0, location.href.indexOf(location.hostname))+location.host+'/';
    			  }
    		  });
    	}
    };

  }
]);
