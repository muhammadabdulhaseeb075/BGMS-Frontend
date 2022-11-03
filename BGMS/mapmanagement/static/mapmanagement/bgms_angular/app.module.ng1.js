//goog.require('bgmsApp.map');

/**
 * Angular module
 * @export
 */
bgmsApp = angular.module('bgmsApp', [ 'ngResource',
    'ui.bootstrap', 'bgmsApp.map' ]);

angular.module('bgmsApp').config(['$resourceProvider', 
		function($resourceProvider) {
			$resourceProvider.defaults.stripTrailingSlashes = false;
		}]).config(['$sceDelegateProvider', '$httpProvider',
		function($sceDelegateProvider, $httpProvider) {

      var whiteList = [ 'self',
        jsAngularInterface.mainPartialFileLocation + '**',
      ];

      if (jsAngularInterface.vueDistLocation)
        // Only used in development, allows angular to access webpack dev server files
        whiteList.push(jsAngularInterface.vueDistLocation + '**');

      // do not continue until mainPartialFileLocation has a value (it will always have a value)
      if (!jsAngularInterface.mainPartialFileLocation) {
        var interval = setInterval(function() {
          if (jsAngularInterface.mainPartialFileLocation) {
            $sceDelegateProvider.resourceUrlWhitelist(whiteList);
            clearInterval(interval);
          }
        }, 50);
      }
      else
        $sceDelegateProvider.resourceUrlWhitelist(whiteList);

      let token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
      $httpProvider.defaults.headers.post["X-CSRFToken"] = token;
		}]);

angular.module('bgmsApp').filter('orderByGroupHierarchy', function() {
  return function(items, field, reverse) {
    var filtered = [];
    filtered.sort(function (a, b) {
        return (a[field] > b[field] ? 1 : -1);
      });
    angular.forEach(items, function(item) {
      filtered.push(item);
    });
    if(reverse) filtered.reverse();
    return filtered;
  };
});