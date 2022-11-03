angular.module('bgmsApp.dataentry').controller('userActivityController', ['$window', '$http', '$filter', '$state', 'userActivityModel', 'imageModel', 'uiGridConstants',
  function($window, $http, $filter, $state, userActivityModel, imageModel, uiGridConstants) {
    
    var view_model = this;
    
    // Public Functions
    view_model.initialise = initialise
    
    // Public Variables
    view_model.submitLoading = false;
    view_model.csrfmiddlewaretoken = '';
    view_model.table = {
      rowHeight: 75,
      enableFiltering: true,
      columnDefs: [
        {
          field: 'image.bookName', 
          displayName: 'Book',
          enableSorting: true,
          enableHiding: false,
          filter: {
            condition: uiGridConstants.filter.STARTS_WITH,
            type: uiGridConstants.filter.INPUT,
          },
          maxWidth: 100,
        }, {
          field: 'image.pageNo',
          displayName: 'Page',
          enableSorting: true,
          enableHiding: false,
          enableFiltering: false,
          maxWidth: 75,
        }, {
          field: 'userFullName', 
          displayName: 'Name',
          enableSorting: true,
          enableHiding: false,
          filter: {
            condition: uiGridConstants.filter.CONTAINS,
            type: uiGridConstants.filter.INPUT,
          },
        }, {
          field: 'time',
          cellFilter: 'date:"dd/MM/yyyy, h:mm a"',
          type: 'date',
          displayName: 'Date',
          enableSorting: true,
          enableHiding: true,
          enableFiltering: false,
          sort: {
            direction: uiGridConstants.DESC,
            priority: 0
          }
        }, {
          field: 'status',
          displayName: 'Status',
          enableSorting: true,
          enableHiding: true,
          filter: {
            condition: uiGridConstants.filter.STARTS_WITH,
            type: uiGridConstants.filter.SELECT,
            selectOptions: [
              { value: "In use", label: "In use" },
              { value: "Skipped", label: "Skipped" },
              { value: "Done", label: "Done" },
              { value: "Viewed", label: "Viewed" },
              { value: "Created", label: "Created" },
              { value: "Updated", label: "Updated" },
            ],
          },
          maxWidth: 100,
        }, {
          field: 'comments',
          displayName: 'Comments',
          enableSorting: true,
          enableHiding: true,
          enableFiltering: false,
          minWidth: 200,
          width: '40%',
          cellClass: 'comment-cell'
        },
      ]
    };
    
    /**
     * Initialise the page
     */
    function initialise() {
      $http.get('/dataentry/getUserActivity/')
        .then(function(response) {
          var data = response.data;
          
          // Create form
          view_model.csrfmiddlewaretoken = data.csrfmiddlewaretoken;
          
          // Loop through data, add it to table
          for (var i = 0; i < data.userActivity.length; i++) {
            var activity = data.userActivity[i];
            
            var image = new imageModel(activity.image);
            console.debug(image);
            view_model.table.data.push(new userActivityModel({
              id: activity.id,
              userId: activity.user.id,
              userName: activity.user.name,
              userFirstName: activity.user.first_name,
              userLastName: activity.user.last_name,
              comments: activity.comments,
              time: new Date(activity.time),
              status: activity.status,
              image: image,
            }));
          }
          
        })
        .catch(function(response) {
          if (response.status === 403) {
            $window.location.href = location.href.substring(0, location.href.indexOf(location.hostname)) + location.host + '/';
          } else {
            console.error('Unable to get user activity:', response);
          }
        });
    };
    view_model.initialise(); 
    
    
  }
]);
