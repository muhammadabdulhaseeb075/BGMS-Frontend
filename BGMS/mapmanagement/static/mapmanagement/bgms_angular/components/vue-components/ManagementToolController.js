angular.module('bgmsApp.map').controller('ManagementToolController', ['$scope',

function ($scope) {
	// initiate vue app and load ManagementTool component
	// Note: this is always open.
	window.initVue('#v-ManagementTool', 'ManagementTool');
}]);
