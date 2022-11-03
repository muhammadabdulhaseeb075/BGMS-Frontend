angular.module('bgmsApp.map').controller('MemorialCaptureSidebarController', ['$scope',

function ($scope) {
	// initiate vue app and load MemorialCaptureSidebar component
	var vueApp = window.initVue('#v-MemorialCaptureSidebar', 'MemorialCaptureSidebar');
	$scope.$on('$destroy', function(){
		vueApp.then(function(app){
			app.$el.remove();
			app.$destroy();
		});
		vueApp = null;
	});
}]);
