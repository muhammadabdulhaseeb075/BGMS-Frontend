/**
 * @description
 * Helper service to handle the opening and closing of modals created outside AngularJS.
 * TODO: fix the use of external vanillaJS object modalBurialDetails
 */
angular.module('bgmsApp.map').service('modalHelperService', ['$rootScope', function($rootScope){

	var view_model = this;

	//default true: means any modal can be opened
	//when false: modals wont open, allowing only one modal at the time
  view_model.modalOpened = true;

    /**
     * @function
     * @description
     * Function called to open modal outside AngularJS
     */
	view_model.openModal = function(data){
		
		if(data.indexOf('loginModal') > -1){
      location.reload();
    }else{
      $('body').append(data);
      $('#id_modalBurialDetails').modal({
        keyboard: false
      });
      $('#id_modalBurialDetails').one('shown.bs.modal', function (e) {
        $("#flexslider-memorial").resize();
      });
    }

		view_model.modalOpened = true;
    document.body.style.cursor = 'default';
		//calling apply because jquery is used to update view outside AngularJS
		if(!$rootScope.$$phase)
			$rootScope.$apply();
	};

	/**
	 * Function callback when modal is closed
	 * TODO: multiple arguments
	 */
	view_model.onCloseModal = function(callback, argument){
        $('#id_modalBurialDetails').one('hide.bs.modal', function (e) {
			$('#id_modalBurialDetails').remove();
        	callback(argument);
    		//calling apply because jquery is used to update view outside AngularJS
    		if(!$rootScope.$$phase)
    			$rootScope.$apply();
        });
	};


}]);
