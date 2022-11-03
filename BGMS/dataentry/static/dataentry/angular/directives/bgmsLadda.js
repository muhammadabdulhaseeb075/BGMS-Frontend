angular.module('bgmsApp.dataentry').directive('bgmsLadda', [function() {

    return {
        restrict: 'A',
        scope: {
        	isLoading: '=bgmsLadda'
        },
        link: function(scope, element, attrs, controller) {
        	var l = Ladda.create(element[0]);
        	scope.$watch('isLoading', function(loading){
//           	 	console.log(loading);
        		if(loading){
	        		l.start();
	        	} else{
        			l.stop();
	        	}
        	})
        	
        }
    };
    
}]);