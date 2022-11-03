angular.module('bgmsApp.map').controller('VueDrawingToolsController', ['$scope',

function ($scope) {
	// initiate vue app and load DrawingTools component
	var vueApp;
	window.initVue('#v-VueDrawingToolsController', 'DrawingTools')
	.then(function(app) {
		vueApp = app;

		$scope.$on('$destroy', function(){
			vueApp.$el.remove();
			vueApp.$destroy();
			vueApp = null;
		});
	});
}]);
