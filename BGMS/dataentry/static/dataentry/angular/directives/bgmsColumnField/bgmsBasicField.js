angular.module('bgmsApp.dataentry').directive('bgmsBasicField', [function() {

    return {
        restrict: 'E',
        templateUrl: jsAngularInterface.staticFilesLocation['bgmsBasicFieldTemplate.html'],
        link: function(scope, element, attrs, controller) {
        }
    };
    
}]);