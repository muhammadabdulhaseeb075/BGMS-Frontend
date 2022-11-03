angular.module('bgmsApp.map').controller('VueLayersToolbarController', ['$scope',

function ($scope) {
	// initiate vue app and load LayersToolbar component
	var vueApp;
	window.initVue('#layersAccordion', 'LayersToolbar')
	.then(function(app) {
		vueApp = app;

		$scope.$on('$destroy', function(){
			vueApp.$el.remove();
			vueApp.$destroy();
			vueApp = null;
		});
	});
}]);