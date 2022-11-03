angular.module('bgmsApp.map').controller('GraveLinkSidebarController', ['$scope',

function ($scope) {
	// initiate vue app and load GraveLinkSidebar component
	var vueApp = window.initVue('#v-GraveLinkSidebar', 'GraveLinkSidebar');
	$scope.$on('$destroy', function(){
		vueApp.then(function(app){
			app.$el.remove();
			app.$destroy();
		});
		vueApp = null;
	});
}]);
