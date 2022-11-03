angular.module('bgmsApp.map').controller('VueOtherToolsController', ['$scope',

function ($scope) {
	// initiate vue app and load OtherTools component
	var vueApp;
	window.initVue('#v-VueOtherToolsController', 'OtherTools')
	.then(function(app) {
		vueApp = app;

		$scope.$on('$destroy', function(){
			vueApp.$el.remove();
			vueApp.$destroy();
			vueApp = null;
		});
	});
}]);