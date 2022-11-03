/** @module
 *  Notifications service
 *  Requires: PNotify library
 *            messages.js
 */

var notificationService = {
  

  stack_bottomright: {"dir1": "up", "dir2": "left", "firstpos1": 25, "firstpos2": 25},
  stack_center: {"dir1": "down","dir2": "right","firstpos1": ($(window).height() / 2 - 150),"firstpos2": ($(window).width() / 2 - 150)},
  
  /**
   * Server error optional custom msj
   */
  error: function(msg) {
    var error_msg = typeof msg !== 'undefined' ? msg : "Update Unsuccessful";
    new PNotify({
          title: error_msg,
          type: 'error',
          addclass: "stack-bottomright",
          stack: notificationService.stack_bottomright,
          mouse_reset: false
        });
  },
  
  /**
   * Server error optional custom msj
   */
  errorSticky: function(msg) {
    var error_msg = typeof msg !== 'undefined' ? msg : "Update Unsuccessful";
    new PNotify({
      title: error_msg,
      type: 'error',
      addclass: "stack-bottomright",
      stack: notificationService.stack_bottomright,
      mouse_reset: false,
      hide: false
    });
  },
  

  /**
   * warning custom msj
   */
  warning: function(msj) {
    new PNotify({
          title: msj,
          // type: 'error',
          addclass: "stack-bottomright",
          stack: notificationService.stack_bottomright,
          mouse_reset: false
        });
  },

  /**
   * success custom msj
   */
  success: function(msj) {
    new PNotify({
          title: msj,
          type: 'success',
          addclass: "stack-bottomright",
          stack: notificationService.stack_bottomright,
          mouse_reset: false
        });
  },

  /**
   * success custom msj
   */
  successSticky: function(msj) {
    new PNotify({
      title: msj,
      type: 'success',
      addclass: "stack-bottomright",
      stack: notificationService.stack_bottomright,
      mouse_reset: false,
      hide: false
    });
  },

  /**
   * success custom title and msj
   */
  successStickyTitleAndMessage: function(title, msj) {
    new PNotify({
      title: title,
      text: msj,
      type: 'success',
      addclass: "stack-bottomright",
      stack: notificationService.stack_bottomright,
      mouse_reset: false,
      hide: false
    });
  },

  /**
   * Confirmation: Yes or No
   */
  confirm: function(yesCallback, noCallback, text){
    new PNotify({
      title: 'Confirmation needed',
      text: text,
      icon: 'glyphicon glyphicon-question-sign',
      hide: false,
      confirm: {
        confirm: true,
        buttons: [{
          text: 'Yes',
          click: function(notice) {
             notice.remove();
             yesCallback();
          }
        }, {
          text: 'No',
          click: function(notice) {
            notice.remove();
            noCallback();
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
      stack: notificationService.stack_center,
    });
  },
  
};