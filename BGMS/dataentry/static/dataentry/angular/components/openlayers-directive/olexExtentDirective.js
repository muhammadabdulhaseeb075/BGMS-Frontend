angular.module('openlayers-directive').directive('olexMapExtent', [function() {
	//extending openlayers-directive to add set extent of map
	return {
	   	restrict: "E",
        scope: {
            parameters: '=olexExtentProperties'
        },
        replace: false,
        require: '^openlayers',
	   	link: function( scope, element, attrs, controller) {
	   		controller.getOpenlayersScope().getMap().then(function(map){
	   		 //TODO: if scope.parameters.ignoreIfInView is set, dont change extent if current view has extent in it
	   			scope.$watch('parameters', function(newExtent){
	   				console.log('extent changed');
	   				if(newExtent)
							map.getView().fit(newExtent);
	   			});
	   		});
	   		scope.$on('$destroy', function() {
	   			// do we need to do anything here?
	   		});
   		}
   	}
}]);
