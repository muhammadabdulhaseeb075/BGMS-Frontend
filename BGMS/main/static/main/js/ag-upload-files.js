
var agUploadFiles = {

  // init
  init: function(endpoint){
    agUploadFiles.initialiseFineUploader(endpoint);
    agUploadFiles.filenameRadioSelected();
  },

  csrfmiddlewaretoken: '',

  uploader: null,


  /**
   * Initialize basic fine-uploader for specific element
   * @return {[type]} [description]
   */
  initialiseFineUploader: function(endpoint){
    console.log("fineUploader....");
    // Core Mode
    // var uploader = new qq.FineUploaderBasic({/* options go here .... */});
    uploader = new qq.FineUploader({
      element: document.getElementById("upload-register-photo"),
      // autoUpload: false,
      template: 'qq-template-gallery',
      request: {
          endpoint: endpoint,
          // mandatory argument to integrate for traditional server
      },
      thumbnails: {
          maxCount: 10,
      },
      validation: {
          allowedExtensions: ['jpeg', 'jpg', 'gif', 'png']
      },
      callbacks: {
        onError: function(id, name, errorReason, xhrOrXdr) {
          notificationService.error(qq.format("Error on file number {}.  {}", id+1, errorReason));
        }
    }
    });
  },

  filenameRadioSelected: function() {
    var element = document.getElementById('page_number');

    if (element) {
      var chkYes = document.getElementById('page_number').checked;
      var value = chkYes ? 'page_number' : 'grave_number';
    }
    
    uploader.setParams({ 'filename_format': value, 'csrfmiddlewaretoken': agUploadFiles.csrfmiddlewaretoken });
  }
};
