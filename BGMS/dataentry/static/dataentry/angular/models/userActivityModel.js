/**
 * @module
 * @description
 * Model of User Activity
 *  userId{number} - user id
 *  userFirstName{string} - user's first name
 *  userLastName{string} - user's last name
 *  comments - the comment about the image
 *  time - the timestamp of when the image was accessed
 *  status - state of image - processing, processed or unprocessed
 */
angular.module('bgmsApp.dataentry').service('userActivityModel', ['$filter', function($filter){
	
	return function UserActivity(params){
		this.id = params.id;	
		this.userId = params.userId;
		this.userName = params.userName;
		this.userFirstName = params.userFirstName;
		this.userLastName = params.userLastName;
		this.userFullName = params.userFirstName + " " + params.userLastName;
		this.comments = params.comments;
		this.time = params.time;
		this.status = params.status;	
		this.image = params.image;
	}	
	
}]);