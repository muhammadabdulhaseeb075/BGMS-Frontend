angular.module('bgmsApp.dataentry', [
  'ngRoute',
  'bsTable',
//  'ngAnimate', 
//  'ngTouch', 
//  'ngMessages',
  'ui.grid', 
  'ui.grid.moveColumns', 
  'ui.grid.selection',
  'ui.grid.resizeColumns',
  'ui.grid.autoResize',
  'openlayers-directive']);

angular.module('bgmsApp.dataentry').filter('orderObjectBy', function(){
	 return function(input, attribute) {
	    if (!angular.isObject(input)) return input;

	    var array = [];
	    for(var objectKey in input) {
	        array.push(input[objectKey]);
	    }

	    array.sort(function(a, b){
	        a = parseInt(a[attribute]);
	        b = parseInt(b[attribute]);
	        return a - b;
	    });
	    return array;
	 }
	});