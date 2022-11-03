angular.module('bgmsApp.dataentry').directive('bgmsPanzoom', [function() {

    return {
        restrict: 'E',
        scope: {
        	options: '=panzoomOptions',
        	imageSrc: '=imageSrc'
        },
        templateUrl: jsAngularInterface.staticFilesLocation['bgmsPanzoomTemplate.html'],
        link: function(scope, element, attrs, controller) {
//        	var options = scope.options;       	
        	
    		var panzoom = angular.element(".panzoom");
    		panzoom.panzoom({
    			minScale: 1
    		});
    		panzoom.on('mousewheel.focal', function( e ) {
                e.preventDefault();
                var delta = e.delta || e.originalEvent.wheelDelta;
                var zoomOut = delta ? delta < 0 : e.originalEvent.deltaY > 0;
                panzoom.panzoom('zoom', zoomOut, {
                  increment: 0.1,
                  animate: false,
                  focal: e
                });
            });

            scope.$watch('imageSrc', function(newSrc, oldSrc){
           	 	console.log(newSrc);
//	           	var canvas = document.getElementById('bgmsPanzoomCanvas'),
//	            ctx = canvas.getContext('2d'),
//	            image = document.getElementById('bgmsPanzoomImage');
//	           	image.onload = function(evt) {
//	           		ctx.drawImage(image, 0, 0, this.width, this.height);
//	           	};
//	           	image.src = newSrc;
            });
    		
    		
        	
        	 scope.$on('$destroy', function() {
                 //handle destruction
             });
        }
    };
}]);