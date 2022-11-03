angular.module('bgmsApp.dataentry').directive('bgmsImageTagger', [function() {
    return {
        restrict: 'E',
        require: ['^bgmsImageViewer'],
        scope: {
        	'imageTag': '=imageTag'
        },
        templateUrl: jsAngularInterface.staticFilesLocation['imageTagger.html'],
        controller: 'imageTaggerController',
        controllerAs: 'tagger',
        link: function(scope, element, attrs, controller) {        	
        	 scope.$on('$destroy', function() {
                 //handle destruction
             });
        }
    };
}]);