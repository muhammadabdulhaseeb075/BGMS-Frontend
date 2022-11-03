angular.module('openlayers-directive').directive('olexLabelFeature', [function($timeout) {

  function labelFeature(scope, element, attrs, controller) {
    console.log(element);
  }

  return {
    restrict: 'EA',
    link: labelFeature
  };
}]);
