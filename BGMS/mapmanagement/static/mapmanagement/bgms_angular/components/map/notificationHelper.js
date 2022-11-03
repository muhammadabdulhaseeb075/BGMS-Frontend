angular.module('bgmsApp.map').service('notificationHelper', ['$rootScope', function($rootScope){

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
            "firstpos2": ($(window).width() / 2 - 150),
						"push": 'top'
          };

    view_model.confirmationOpened = false;

	/**
	 * @function
	 * @description
	 * Creates a confirmation box in the centre of screen
	 * @param {string} title - title to be displayed
	 * @param {string} text - text to be displayed
	 * @param {function} confirmCallback - function to be called if user clicks confirm
	 * @param {function} cancelCallback - function to be called if user clicks cancel
	 */
	view_model.createConfirmation = function(title, text, confirmCallback, cancelCallback){
		if(!view_model.confirmationOpened){
				view_model.confirmationOpened = true;
			
			let stack = view_model.stack_centre;
			stack["modal"] = true;
			
			new PNotify({
		          title: title,
		          text: text,
							Animate: {
								animate: true,
								inClass: 'zoomInLeft',
								outClass: 'zoomOutRight'
							},
							addclass: 'stack-modal',
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
		                if(cancelCallback){
		                	$rootScope.$apply(function(){
												cancelCallback();
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
		          stack: stack
		        });
		}
	};

	/**
	 * @function
	 * @description
	 * Creates a notification containing a progress bar
	 * @param {string} title - text to be displayed in the notification box
	 * @param {function} beforeCallback - function to be called before notification opens
	 * @returns {PNotify} - the progress notification itself
	 */
	view_model.createProgressNotification = function(title, beforeCallback) {
		return new PNotify({
			title: title,
			text: '<div class="progress progress-striped active" style="margin:0"><div class="progress-bar" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0"><span class="sr-only">0%</span></div></div>',
			icon: 'glyphicon glyphicon-refresh fa-spin',
			hide: false,
			buttons: {
				closer: true,
				sticker: false,
			},
			history: {
				history: false,
			},
			addclass: "stack-bottomright",
			stack: view_model.stack_bottomright,
			mouse_reset: false,
			before_open: beforeCallback,
		});
	};

	/**
	 * @function
	 * @description
	 * Creates a notification box in the centre of screen that requires user to acknowledge
	 * @param {string} title - title to be displayed
	 * @param {string} text - text to be displayed
	 */
	view_model.createInfoNotification = function(title, text){
		PNotify.prototype.options.confirm.buttons = [];

			new PNotify({
        title: title,
        text: text,
        icon: 'glyphicon glyphicon-question-info-sign',
        hide: false,
				type: 'notice',
		    confirm: {
		      confirm: true,
		      buttons: [{
		        text: 'Ok',
		        primary: true,
		        click: function(notice) {
		          notice.remove();
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
	};

	/**
	 * @function
	 * @private
	 * @description
	 * Creates a notification with the specified text at right bottom of the screen
	 * @param {string} title - text to be displayed in the notification box
	 * @param {string} type - type of box to create: 'success' or 'error'
	 */
	view_model._createNotification = function(title, type, text=""){
		new PNotify({
					title: title,
					text: text,
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
	view_model.createErrorNotification = function(title, text=""){
		view_model._createNotification(title, 'error', text);
	};

	/**
	 * @function
	 * @description
	 * Creates a success notification box at right bottom of screen
	 * @param {string} title - text to be displayed in the notification box
	 */
	view_model.createSuccessNotification = function(title, text=''){
		view_model._createNotification(title, 'success', text);
	};

	/**
	 * @function
	 * @description
	 * Creates a warning notification box at right bottom of screen
	 * @param {string} title - text to be displayed in the notification box
	 */
	view_model.createWarningNotification = function(title){
		view_model._createNotification(title, 'default');
	};

	/**
	 * @function
	 * @description
	 * Adds a notification that the user cannot dismiss
	 * @param {string} title - title to be displayed in the notification box
	 * @param {string} [text=''] - text to be displayed in the notification box
	 */
	view_model.createPermanentNotification = function(title, text) {

		// Set default value
		text = text || "";

		return new PNotify({
			title: title,
			text: text,
			hide: false,
			buttons: {
				closer: false,
				sticker: false
			},
			mobile: {
				swipe_dismiss: false
			},
			addclass: "stack-bottomright permanent",
			stack: view_model.stack_bottomright,
			icon: false,
		});
	};

	/**
	 * @function
	 * @description
	 * Removes the provided notification
	 * @param {PNotify} notification - the notification to remove
	 */
	view_model.removePermanentNotification = function(notification) {
		if(notification.remove) {
			notification.remove();
		}
	};

	/**
	 * @function
	 * @description
	 * Adds an info notification that the user cannot dismiss
	 * @param {string} [text=''] - text to be displayed in the notification box
	 */
	view_model.createPermanentInfoNotification = function(text) {

		return new PNotify({
			title: text,
			hide: false,
			type: 'info',
			buttons: {
				closer: false,
				sticker: false
			},
			mobile: {
				swipe_dismiss: false
			},
			history: {
				history: true
			},
			addclass: "permanent",
			stack: {
				"dir1": "down",
				"dir2": "right",
				"firstpos1": 60,
				"firstpos2": ($(window).width() / 2 - 150)
			},
			icon: false
		});
	}

	/**
	 * @function
	 * @description
	 * Removes the provided notification
	 * @param {PNotify} notification - the notification to remove
	 */
	view_model.removePermanentInfoNotification = function(notification) {

		if(notification.remove) {
			notification.remove();
		}
	};

}]);
