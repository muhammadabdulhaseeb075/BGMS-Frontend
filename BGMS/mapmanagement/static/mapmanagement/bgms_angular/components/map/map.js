//goog.provide('bgmsApp.map');

angular.module('bgmsApp.map', [
  'ngRoute',]);


angular.module('bgmsApp.map').config(['$compileProvider', function ($compileProvider) {
  
  // Allow angular to link to data:image/ URLs
  $compileProvider.aHrefSanitizationWhitelist(/^\s*(https?|ftp|mailto|tel|file|data):/);
  
}]);