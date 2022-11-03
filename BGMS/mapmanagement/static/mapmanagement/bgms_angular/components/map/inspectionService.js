angular.module('bgmsApp.map').service('inspectionService', ['$q', '$http', 'offlineService',
  function($q, $http, offlineService){
    
    var view_model = this;
    
    // Private Variables
    var CONDITION = {
      1: "Good",
      2: "Reasonable",
      3: "Poor",
    };
    
    // Public Functions
    view_model.create = create;
    
    /**
     * Creates a new inspection from the provided form
     * @param {JQuery} form - The form element
     */
    function create(form) {
      var deferred = $q.defer();
      
      var url = '/mapmanagement/memorialInspection/';
      var formData = form.serialize();
      var image_uri = form.find('#id_image_uri').val();
      
      // If the user has automatic image uploading on and is uploading an image
      if (offlineService.autoImageUpload || !image_uri) {
        
        // Send the data to the server
        $http.post(url, formData, {
          headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        })
          .then(function(response) {
            deferred.resolve(response.data);
          })
          .catch(function(response) {
            deferred.reject(response.data);
          });

      } else {
        
        // Get the data from the form
        var uuid = form.find('[name=uuid]').val();
        var condition = form.find('#id_condition').val();
        var remarks = form.find('#id_remarks').val();
        var action_required = form.find('#id_action_required')[0].checked;
        
        // Create the object to be stored in the database
        var inspection = {
          uuid: uuid,
          url: url,
          data: formData,
          headers: {'Content-Type': 'application/x-www-form-urlencoded'}
        };
        
        // Add the inspection object to the database
        offlineService.addToQueue(inspection)
          .then(function() {
            
            // Fake the response
            deferred.resolve({
              date: new Date().toLocaleDateString(),
              condition: CONDITION[condition],
              remarks: remarks,
              action_required: action_required,
              thumbnail_url: image_uri ? "data:image/jpeg;base64," + image_uri : "", 
            });
            
          })
          .catch(function() {
            deferred.reject();
          });
          
      }
      
      return deferred.promise;
    }
    
  }
]);
