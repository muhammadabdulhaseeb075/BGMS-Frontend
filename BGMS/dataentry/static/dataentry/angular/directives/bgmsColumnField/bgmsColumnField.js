angular.module('bgmsApp.dataentry').directive('bgmsColumnField', [function() {

    return {
        restrict: 'E',
        scope: {
        	column: '=properties'
        },
        templateUrl: jsAngularInterface.staticFilesLocation['bgmsColumnFieldTemplate.html'],
        link: function(scope, element, attrs, controller) {
        	if(scope.column){
            	var columnName = scope.column.name;
            	var columnType = scope.column.type;
        	}
        }
    };
    
}]);