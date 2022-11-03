/**
 * @module
 * @description
 * Model of the Image
 *  id - unique id
 *  url - url of the image
 *  comments - comments by the user about the image
 *  bookName - book the image is from
 */
angular.module('bgmsApp.dataentry').service('imageModel', ['$filter', function($filter){
	
	return function Image(params){
		this.id = params.id;
		this.url = params.url;
		this.extent = params.extent;
		this.comments = params.comments;
		this.bookName = params.bookName;
		this.pageNo = params.bookName;
		this.hasTemplate = params.hasTemplate;

		
	    /**
	     * @function
	     * @description
	     * Function to get book name from url
	     */
		this.createBookName = function(){
			var names = this.url.split("/");
			var names = names[names.length-1].split(".");
			var names = names[0].split("_");
			this.bookName = names[1];
		};

		
	    /**
	     * @function
	     * @description
	     * Function to get book number from url
	     */
		this.createPageNo = function(){
			var names = this.url.split("/");
			var names = names[names.length-1].split(".");
			var names = names[0].split("_");
			this.pageNo = names[2];
		};
		
		if(params.bookName)
			this.bookName = params.bookName;
		else
			this.createBookName();
		
		if(params.pageNo)
			this.pageNo = params.pageNo;
		else
			this.createPageNo();

		
	    /**
	     * @function
	     * @description
	     * Function to get object with name:value to post to server
	     */
		this.getImageJSON = function(){
			return {
				"url": this.url,
				"comments": this.comments,
			};
		};
		
		
	}	
	
}]);