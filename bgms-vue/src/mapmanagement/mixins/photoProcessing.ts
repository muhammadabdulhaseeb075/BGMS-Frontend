import Vue from 'vue'
import Component from 'vue-class-component'
import { messages } from '@/global-static/messages.js';
import Compressor from 'compressorjs';

@Component
export default class PhotoProcessing extends Vue{

  vueInstance;

  /**
   * Compresses the photo and upload.
   * @param {any} e
   */
  processPhoto(e:any) {
    let v = this.vueInstance;
    let memorial = v.$store.state.MemorialSidebar.memorial;

    v.photoProcessing = true;

    if (v.stopSidebarClose) {
      v.stopSidebarClose(true)
    }

    let fileUploaderInput = v.$refs.fileUploaderInput as HTMLInputElement;
    let cameraUploaderInput = v.$refs.cameraUploaderInput as HTMLInputElement;

    let files = e.target.files || e.dataTransfer.files;
    if (!files.length)
      return;

      let j = 0;

    for(let i = 0;i<files.length;i++){
      this.compressPhoto(files[i])
      .then(result => {
        let reader = new FileReader();

        // Handle the compressed image file
        reader.onload = function(e) {
          // work out if this is the final photo to be processed. (This function is not neccessarily called in order of i.)
          j++;
          let final = j===files.length;

          v.processPhotoPart2(reader.result, memorial, final);

          if (final) {
            fileUploaderInput.value = null;
            cameraUploaderInput.value = null;
          }
        };
        reader.readAsDataURL(result as Blob);
      })
      .catch(err => {
        console.log(err);
        v.notificationHelper.createErrorNotification(messages.memorialImages.upload.fail.title);
        v.photoProcessing = false;

        if (i===(files.length-1)) {
          fileUploaderInput.value = null;
          cameraUploaderInput.value = null;
        }
      });
    }
  }

  compressPhoto(file, imageQuality = null, imageMaxLength = 4000) {
    let v = this;

    return new Promise((resolve, reject) => { 

      if (file.size < 1572864)
            resolve(file);

      let quality = imageQuality;
      
      if (!quality) {
        if (file.size < 2621440 )
          quality = 0.8
        else if (file.size < 3145728  )
          quality = 0.7
        else
          quality = 0.6
      }

      let maxLength = imageMaxLength;

      new Compressor(file, { maxWidth: maxLength, maxHeight: maxLength, quality: quality, checkOrientation: true,
        success(result) {
          if (result.size < 1572864)
            resolve(result);
          else 
            v.compressPhoto(result, quality, maxLength * 0.9)
            .then(result => {
              resolve(result);
            })
            .catch(err => {
              reject(err);
            });
        },
        error(err) {
          reject(err);
        }
      });
    });
  }
}
