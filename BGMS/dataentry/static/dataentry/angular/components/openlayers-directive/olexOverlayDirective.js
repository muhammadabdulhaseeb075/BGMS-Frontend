angular.module('openlayers-directive').directive('olexOverlay', ["$log", "$q", "olMapDefaults", "olHelpers", function($log, $q, olMapDefaults, olHelpers) {

    return {
        restrict: 'E',
        scope: {
            properties: '=olexOverlayProperties'
        },
        replace: false,
        template:   '<div class="resize-class">'+
                        '<div ng-show="properties.message" ng-class="properties.class" ng-bind-html="properties.message"></div>'+
                        '<div ng-show="properties.template" ng-include="properties.template.url" onload="reposition(evt,elem)"></div>'+
                    '</div>',
        require: '^openlayers',
        link: function(scope, element, attrs, controller) {
            // var createOverlay   = olHelpers.createOverlay;
            if(scope.properties){
                if(scope.properties.template && scope.properties.template.scope){
                //adding template variables to scope so that they can be accessed by template
                    var templateScope = scope.properties.template.scope;
                    for(var key in templateScope) {
                        scope[key] = templateScope[key];
                    }
                    // angular.forEach(templateScope, function(variable, key){
                    //     scope[key] = variable;
                    //     // if(key=='memorial_types'){
                    //     //     console.log(key);
                    //     //     console.log(variable);
                    //     // }
                    // });
                    templateScope = null;
                }
                var olScope = controller.getOpenlayersScope();
                var overlayElement = element.children()[0];
                olScope.getMap().then(function(map) {
                    var label = new ol.Overlay({
                        element: overlayElement,
                        autoPan:scope.properties.autoPan,
                        autoPanAnimation: {
                            duration: 250
                        },
                        position: scope.properties.position,
                        stopEvent: true
                    });

                    angular.element(overlayElement).css('visibility','hidden');
                    map.addOverlay(label);
										var div = $(".resize-class");
                    var sensor = new ResizeSensor(div, function(){
                      if(label){
                        var positioning = scope.properties.positioning[0];
                        var offset = scope.properties.offset[positioning];
                        var oldPositioning = scope.properties.positioning[1];

                        if(div.parent('div').height()>(map.getPixelFromCoordinate(label.getPosition())[1]+offset[1])){
                            oldPositioning = scope.properties.positioning[0];
                            positioning = scope.properties.positioning[1];
                            offset = scope.properties.offset[positioning];
                        }
                        if(scope.properties.tooltip){
                            angular.element(overlayElement).removeClass(scope.properties.tooltip[oldPositioning]);
                            angular.element(overlayElement).addClass(scope.properties.tooltip[positioning]);
                        }
                        label.setPositioning(positioning);
                        label.setOffset(offset);
                        angular.element(overlayElement).css('visibility','visible');
                      }
                    });
                    scope.$watchCollection('properties.position', function(newPosition, oldPosition){
                    	label.setPosition(newPosition);
                    });
                    scope.$watchCollection('properties.offset', function(newoffset, oldoffset){
                        // console.log(properties);
                    	console.log('properties.offset:' + newoffset);
                        if(newoffset['top-left'] !== undefined)
                            label.setOffset(newoffset['top-left']);
                    });
                    scope.$on('$destroy', function() {
                        map.removeOverlay(label);
                        sensor.detach($(".resize-class"));
                        sensor = null;
                        if(scope.templateCloseHandler && typeof scope.templateCloseHandler === 'function')
                            scope.templateCloseHandler();
                        label = null;
                    });
                });
            }

        }
    };
}]);