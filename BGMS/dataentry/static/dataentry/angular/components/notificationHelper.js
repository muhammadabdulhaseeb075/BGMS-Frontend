angular.module('bgmsApp.dataentry').service('notificationHelper', ['$rootScope', function($rootScope){

	var view_model = this;

    view_model.stack_bottomright = {
    	      "dir1": "up",
    	      "dir2": "left",
    	      "firstpos1": 25,
    	      "firstpos2": 25
    	    };

    view_model.stack_centre = {
            "dir1": "down",
            "dir2": "right",
            "firstpos1": ($(window).height() / 2 - 150),
            "firstpos2": ($(window).width() / 2 - 150)
          };

    view_model.confirmationOpened = false;

	/**
	 * @function
	 * @description
	 * Creates a prompt in the centre of screen
	 * @param {string} title - title to be displayed
	 * @param {string} text - text to be displayed
	 * @param {function} confirmCallback - function to be called if user clicks confirm
	 * @param {function} cancleCallback - function to be called if user clicks cancel
	 */
	view_model.createPrompt = function(title, text, confirmCallback, cancleCallback){
		if(!view_model.confirmationOpened){
		    view_model.confirmationOpened = true;
			new PNotify({
		          title: title,
		          text: text,
		          icon: 'glyphicon glyphicon-question-sign',
		          hide: false,
		          confirm: {
		        	prompt: true,
		            buttons: [{
		              text: 'Save',
		              click: function(notice, value) {
		                 notice.remove();
		                 view_model.confirmationOpened = false;
		                 if(confirmCallback){
		                 	 $rootScope.$apply(function(){
		                    	 confirmCallback(value);
		                 	 });
		                 }
		              }
		            }, {
		              text: 'Cancel',
		              click: function(notice) {
		                notice.remove();
		                view_model.confirmationOpened = false;
		                if(cancleCallback){
		                	$rootScope.$apply(function(){
		                    	cancleCallback();
		                	});
		                }
		              }
		            }]
		          },
		          buttons: {
		            closer: false,
		            sticker: false
		          },
		          history: {
		            history: false
		          },
		          stack: view_model.stack_centre
		        });
		}
	};

	/**
	 * @function
	 * @description
	 * Creates a confirmation box in the centre of screen
	 * @param {string} title - title to be displayed
	 * @param {string} text - text to be displayed
	 * @param {function} confirmCallback - function to be called if user clicks confirm
	 * @param {function} cancleCallback - function to be called if user clicks cancel
	 */
	view_model.createConfirmation = function(title, text, confirmCallback, cancleCallback){
		if(!view_model.confirmationOpened){
		    view_model.confirmationOpened = true;
			new PNotify({
		          title: title,
		          text: text,
		          icon: 'glyphicon glyphicon-question-sign',
		          hide: false,
		          confirm: {
		            confirm: true,
		            buttons: [{
		              text: 'Yes',
		              click: function(notice) {
		                 notice.remove();
		                 view_model.confirmationOpened = false;
		                 if(confirmCallback){
		                 	 $rootScope.$apply(function(){
		                    	 confirmCallback();
		                 	 });
		                 }
		              }
		            }, {
		              text: 'No',
		              click: function(notice) {
		                notice.remove();
		                view_model.confirmationOpened = false;
		                if(cancleCallback){
		                	$rootScope.$apply(function(){
		                    	cancleCallback();
		                	});
		                }
		              }
		            }]
		          },
		          buttons: {
		            closer: false,
		            sticker: false
		          },
		          history: {
		            history: false
		          },
		          stack: view_model.stack_centre
		        });
		}
	};

	/**
	 * @function
	 * @private
	 * @description
	 * Creates a notification with the specified text at right bottom of the screen
	 * @param {string} title - text to be displayed in the notification box
	 * @param {string} type - type of box to create: 'success' or 'error'
	 */
	view_model._createNotification = function(title, type){
		new PNotify({
	        title: title,
	        type: type,
	        addclass: "stack-bottomright",
	        stack: view_model.stack_bottomright,
	        mouse_reset: false
	    });
	};

	/**
	 * @function
	 * @description
	 * Creates an error notification box at right bottom of screen
	 * @param {string} title - text to be displayed in the notification box
	 */
	view_model.createErrorNotification = function(title){
		view_model._createNotification(title, 'error');
	};

	/**
	 * @function
	 * @description
	 * Creates a success notification box at right bottom of screen
	 * @param {string} title - text to be displayed in the notification box
	 */
	view_model.createSuccessNotification = function(title){
		view_model._createNotification(title, 'success');
	};

}]);
