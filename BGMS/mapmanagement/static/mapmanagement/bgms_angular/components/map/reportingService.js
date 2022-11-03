angular.module('bgmsApp.map').service('reportingService', ['$q', '$rootScope', '$http',
  function($q, $rootScope, $http){
    
    var view_model = this;
    
    // Public Functions
    view_model.sendBugReport = sendBugReport;
    
    /**
     * Sends a stringified version of the bug to the sysadmin
     * @param {String|*} bug - the bug message
     * @returns {Promise} A promise which resolves if the report is sent successfully
     */
    function sendBugReport(bug) {
      var deferred = $q.defer();
      
      // Stringify the bug
      if(typeof bug !== "string") {
        bug = JSON.stringify(bug); 
      }
      
      var data = {
        'error_message': bug,
      };
      
      $http.post('/mapmanagement/sendReport/', data)
        .then(function() {
          deferred.resolve();
        })
        .catch(function() {
          deferred.reject();
        });
      
      return deferred.promise;
    }
    
  }
]);
