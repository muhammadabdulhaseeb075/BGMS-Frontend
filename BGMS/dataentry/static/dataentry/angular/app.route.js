angular.module('bgmsApp').config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {
  $urlRouterProvider.otherwise("/addRecord");
  //
  // Now set up the states
  $stateProvider
  .state('home', {
    	url: "/addRecord",
      templateUrl: jsAngularInterface.staticFilesLocation['addBurialRecord.html']
    })
    .state('list', {
      	url: "/listTemplates",
        templateUrl: jsAngularInterface.staticFilesLocation['listTemplates.html']
    })
    .state('create', {
      	url: "/createTemplate",
      	controller: 'templateCreationController',
      	controllerAs: 'creator',
        templateUrl: jsAngularInterface.staticFilesLocation['createTemplate.html']
    })      
    .state('edit', {
      	url: "/editTemplate?templateId",
      	controller: 'templateCreationController',
      	controllerAs: 'creator',
        templateUrl: jsAngularInterface.staticFilesLocation['createTemplate.html']
    })    
    .state('imageStatus', {
      	url: "/imageStatus",
      	controller: 'imageStatusController',
      	controllerAs: 'imageStatus',
        templateUrl: jsAngularInterface.staticFilesLocation['imageStatus.html']
    })
    .state('userActivity', {
      	url: "/userActivity",
      	controller: 'userActivityController',
      	controllerAs: 'userActivity',
        templateUrl: jsAngularInterface.staticFilesLocation['userActivity.html']
    })
}]);