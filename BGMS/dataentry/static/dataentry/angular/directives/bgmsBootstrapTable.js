angular.module('bgmsApp.dataentry').directive('bgmsUpdateTable', [function() {

    return {
        restrict: 'E',
        scope: {
        	options:'=options'
        },
        link: function(scope, element, attrs, controller) {
        	var table = element.siblings('table');
        	scope.$watchCollection('options.columns', function(newColumns){
//        		var displayColumns = angular.element(element).getOptions().columns;
        		var options = table.bootstrapTable('getOptions');
        		options.columns = newColumns;
        		table.bootstrapTable('refreshOptions', options);
        	});
        	
        	scope.$watchCollection('options.data', function(newData){
//        		angular.element(element).getData().
        	});
        	
        	scope.$watchCollection('options.methods', function(newMethods){
        		
        	});
        }
    };
    
}]);