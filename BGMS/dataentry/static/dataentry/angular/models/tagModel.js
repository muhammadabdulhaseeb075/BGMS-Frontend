/**
 * @module
 * @description
 * Model of an Image Tag in a Burial Record
 *  id - unique id of the tag 
 *  extent - {ol.extent} extent of the tag
 */
angular.module('bgmsApp.dataentry').service('tagModel', [function(){	
	return function Tag(params){
		this.id = params.id;
		this.extent = params.extent;
		
		//creating the extent from bounding points
		if(params.extent_points_wkt && params.extent_points_wkt!=''){
			var wktFormatter = new ol.format.WKT();
			//remove projection info
			params.extent_points_wkt = params.extent_points_wkt.substring(params.extent_points_wkt.indexOf(';')+1)
			var extentPoints = wktFormatter.readGeometry(params.extent_points_wkt);
			this.extent = ol.extent.boundingExtent(extentPoints.getCoordinates());
		}
	};	
}]);