/**
 * @module
 * @description
 * Model of Image History
 *  image{imageModel} - image object
 *  comments - the latest comment about the image
 *  time - the latest timestamp of when the image was accessed
 *  status - state of image - processing, processed or unprocessed
 */
angular.module('bgmsApp.dataentry').service('imageHistoryModel', ['$filter', function($filter){
	
	return function ImageHistory(params){
		this.image = params.image;
		this.comments = params.comments;
		this.time = params.time;
		this.status = params.status;	
	}	
	
}]);