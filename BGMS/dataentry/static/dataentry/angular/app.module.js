/**
 * Angular module
 * @export
 */
bgmsApp = angular.module('bgmsApp', [ 'ui.router', 'ngResource',
		'ui.bootstrap', 'bgmsApp.dataentry' ]);

angular.module('bgmsApp').config(['$resourceProvider', 
		function($resourceProvider) {
			$resourceProvider.defaults.stripTrailingSlashes = false;
		}]).config(['$sceDelegateProvider', '$httpProvider',
		function($sceDelegateProvider, $httpProvider) {
			$sceDelegateProvider.resourceUrlWhitelist([ 'self',
          jsAngularInterface.mainPartialFileLocation + '**' ]);

      let token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
      $httpProvider.defaults.headers.post["X-CSRFToken"] = token;
		}]);