/**
 * Decorator for openlayers directive
 * Watch defaults, therefore extent can be set in the map creation
 */
angular.module('openlayers-directive').config(['$provide', function($provide){
  $provide.decorator('openlayersDirective', ['$delegate', 'olHelpers', 'olMapDefaults', function($delegate, olHelpers, olMapDefaults){
    var directive = $delegate[0];

    var link = directive.link;

    directive.compile = function() {
      return function(scope, element, attrs) {

      scope.$watch('defaults.view.extent', function(){
	      if(scope.defaults.view.extent.length !== 0){
	        console.log("going to create map...");
	        link(scope, element, attrs);
	      }
      });//FIN watch
      };
    };

    return $delegate;
  }]);
}]);
