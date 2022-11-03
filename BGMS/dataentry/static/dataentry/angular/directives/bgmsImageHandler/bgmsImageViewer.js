angular.module('bgmsApp.dataentry').directive('bgmsImageViewer', [function() {

	return {
        restrict: 'E',
        scope: {
        	image: '=image',
        	width: '=width',
        	imageIdForTags: '=imageIdForTags',
            addTag: '=addTag',
            removeTag: '=removeTag'
        },
        transclude: true,
        templateUrl: jsAngularInterface.staticFilesLocation['imageViewer.html'],
        controllerAs: 'viewer',
        controller: 'imageViewerController',        
        link: function(scope, element, attrs, controller) {        	
        	 scope.$on('$destroy', function() {
                 //handle destruction
             });
        }
    };
}]);