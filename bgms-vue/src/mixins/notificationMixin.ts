import Vue from 'vue'
import Component from 'vue-class-component'
import PNotify from 'pnotify/dist/es/PNotify.js';
import PNotifyButtons from 'pnotify/dist/es/PNotifyButtons.js';
import PNotifyConfirm from 'pnotify/dist/es/PNotifyConfirm.js';

const STACK_CENTRE = {
  "dir1": "down",
  "firstpos1": (window.innerHeight / 2 - 150),
  "push": 'top'
};

const STACK_BOTTOMRIGHT = {
  "dir1": "up",
  "dir2": "left",
  "firstpos1": 25,
  "firstpos2": 25
};

const STANDARD_NOTIFICATION_PROPERTIES = {
  addClass: "stack-bottomright",
  stack: STACK_BOTTOMRIGHT,
  icons: 'fontawesome5',
  width: '300px'
}

@Component
export default class NotificationMixin extends Vue{

  confirmationOpened: boolean = false;

  /**
   * Vue mounted lifecycle hook
   */
  mounted() {

    // Initiate the required modules for PNotify
    PNotifyButtons;
    PNotifyConfirm;
    PNotify.defaults.icons = 'fontawesome5';
    PNotify.defaults.styling = 'bootstrap3';
  }

  /**
   * @function
   * @description
   * Creates an error notification box using response data (if it exists) and writes log to console
   * @param {string} error - error response from server
   * @param {string} title - title text to be displayed in the notification box
   */
  createHTTPErrorNotificationandLog(error, title){

    let text;

    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      console.log(error.response.data);
      console.log(error.response.status);
      console.log(error.response.headers);

      if (error.response.data && error.response.data.detail)
        text = error.response.data.detail;

    } 
    else if (error.request) {
      // The request was made but no response was received
      // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
      // http.ClientRequest in node.js
      console.log(error.request);
      text = "No response received from server.";
    } 
    else {
      // Something happened in setting up the request that triggered an Error
      console.log('Error', error.message);
      text = error.message;
    }
    
    this.createErrorNotification(title, text, false);
  }

  /**
   * @function
   * @description
   * Creates an error notification box at right bottom of screen
   * @param {string} title - text to be displayed in the notification box
   */
  createErrorNotification(title, text="", hide=false){
    let properties = STANDARD_NOTIFICATION_PROPERTIES;
    properties["title"] = title;
    properties["text"] = text;
    properties["hide"] = hide;

    PNotify.error(properties);
  }
  
  /**
   * @function
   * @description
   * Creates a success notification box at right bottom of screen
   * @param {string} title - text to be displayed in the notification box
   */
  createSuccessNotification(title){
    let properties = STANDARD_NOTIFICATION_PROPERTIES;
    properties["title"] = title;
    properties["text"] = "";
    properties["hide"] = true;

    PNotify.success(properties);
  }


  /**
   * @function
   * @description
   * Creates a warning notification box at right bottom of screen
   * @param {string} title - text to be displayed in the notification box
   */
  createWarningNotification(title){
    let properties = STANDARD_NOTIFICATION_PROPERTIES;
    properties["title"] = title;
    properties["text"] = "";
    properties["hide"] = true;

    PNotify.warning(properties);
  }

  /**
   * 
   * @param text Creates permanent notification at top middle of screen
   * @param cancelButton True if including a cancel button
   * @param cancelCallback 
   */
  createPermanentInfoNotification(text, cancelButton = false, cancelCallback=null, cancelButtonText="Cancel") {
    let notice = PNotify.info({
      title: text,
      icon: false,
      hide: false,
      mobile: {
        swipe_dismiss: false
      },
      addClass: "permanent hideStickerAndCloser alert-info",
      buttons: {
          closer_hover: false,
          sticker: false
      },
      history: {
        history: false
      },
      stack: {
        "dir1": "down",
        "firstpos1": 60
      }
    });

    if (cancelButton) {
      notice.update({
        modules: {
          Confirm: {
            confirm: true,
            buttons: [
              {
                text: cancelButtonText,
                click: (notice) => {
                  notice.close();
                  cancelCallback();
                }
              }
            ]
          }
        }
      });
    }

    return notice;
  }

  /**
   * @function
   * @description
   * Creates a confirmation box in the centre of screen
   * @param {string} title - title to be displayed
   * @param {string} text - text to be displayed
   * @param {function} confirmCallback - function to be called if user clicks confirm
   * @param {function} cancelCallback - function to be called if user clicks cancel
   */
  createConfirmation = function(title, text, confirmCallback, cancelCallback=null, yesLabel: string='Yes', noLabel: string='No'){
    let v = this;

    if(!v.confirmationOpened){
        v.confirmationOpened = true;
      
      let stack = STACK_CENTRE;
      stack["modal"] = true;
      
      PNotify.notice({
        title: title,
        text: text,
        Animate: {
          animate: true,
          inClass: 'zoomInLeft',
          outClass: 'zoomOutRight'
        },
        addClass: 'stack-modal hideStickerAndCloser confirmationNotice',
        icon: 'fas fa-question-circle',
        hide: false,
        modules: {
          Confirm: {
            confirm: true,
            buttons: [{
              text: yesLabel,
              primary: true,
              click: notice => {
                  notice.remove();
                  v.confirmationOpened = false;
                  if(confirmCallback){
                    confirmCallback();
                  }
              }
            },
            {
              text: noLabel,
              click: notice => {
                notice.remove();
                v.confirmationOpened = false;
                if(cancelCallback){
                  cancelCallback();
                }
              }
            }]
          },
          Buttons: {
            closer: false,
            sticker: false,
            stickerHover: false,
            closerHover: false
          },
          History: {
            history: false
          }
        },
        stack: stack
      });
    }
  }

  /**
   * @function
   * @description
   * Creates a confirmation box in the centre of screen
   * @param {string} title - title to be displayed
   * @param {string} text - text to be displayed
   * @param {function} confirmCallback - function to be called if user clicks confirm
   * @param {function} cancelCallback - function to be called if user clicks cancel
   */
  createInfoConfirmation = function(title, text){
      
    let stack = STACK_CENTRE;
    stack["modal"] = true;
    
    PNotify.info({
      title: title,
      text: text,
      Animate: {
        animate: true,
        inClass: 'zoomInLeft',
        outClass: 'zoomOutRight'
      },
      addClass: 'stack-modal hideStickerAndCloser alert-warning',
      hide: false,
      modules: {
        Confirm: {
          confirm: true,
          buttons: [{
            text: 'Ok',
            primary: true,
            click: function(notice) {
              notice.close();
            }
          }]
        },
        Buttons: {
          closer: false,
          sticker: false,
          stickerHover: false,
          closerHover: false
        },
        History: {
          history: false
        }
      },
      stack: stack
    });
  }
}
