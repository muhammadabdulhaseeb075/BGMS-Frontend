var prettyPhotoTemplate = {

  getTemplate: function(){
    $("a[rel^='prettyPhoto']").prettyPhoto({
  		markup: '<div class="pp_pic_holder"> \
  			<div class="ppt">&nbsp;</div> \
  			<div class="pp_top"> \
  				<div class="pp_left"></div> \
  				<div class="pp_middle"></div> \
  				<div class="pp_right"></div> \
  			</div> \
  			<div class="pp_content_container"> \
  				<div class="pp_left"> \
  				<div class="pp_right"> \
  					<div class="pp_content"> \
  						<div class="pp_loaderIcon"></div> \
  						<div class="pp_fade"> \
  							<a href="#" id="ppex_top" class="pp_expand" title="Contract the image">Contract</a> \
  							<a class="pp_close" href="#">Close</a> \
  							<div class="pp_hoverContainer"> \
  								<a class="pp_next" href="#">next</a> \
  								<a class="pp_previous" href="#">previous</a> \
  							</div> \
  							<div id="pp_full_res"></div> \
  							<div class="pp_details"> \
  								<a href="#" class="pp_expand" title="Expand the image">Expand</a> \
  								<div class="pp_nav"> \
  									<a href="#" class="pp_arrow_previous">Previous</a> \
  									<p class="currentTextHolder">0/0</p> \
  									<a href="#" class="pp_arrow_next">Next</a> \
  								</div> \
  								<p class="pp_description"></p> \
  							</div> \
  						</div> \
  					</div> \
  				</div> \
  				</div> \
  			</div> \
  			<div class="pp_bottom"> \
  				<div class="pp_left"></div> \
  				<div class="pp_middle"></div> \
  				<div class="pp_right"></div> \
  			</div> \
  		</div> \
  		<div class="pp_overlay"></div>',
  	  allowPanImageInExpand: false,
  	  deeplinking: false,
  		clicking: false,
  		previousX: undefined,
  		previousY: undefined,
      // allow_resize: false,
  		addDragAndDropSupportForScrollingTo: function(selector, clicking){
  			var vm = this;
  			$('.pp_pic_holder.pp_default').mousedown(function(e) {
  				//console.log('mousedown');
  					e.preventDefault();
  					vm.previousX = e.clientX;
  					vm.previousY = e.clientY;
  					vm.clicking = true;
  			});
  			$(document).mouseup(function() {
  				//console.log('clicking:'+clicking);
  					vm.clicking = false;
  			});
  			$('.pp_pic_holder.pp_default').mousemove(function(e) {
  				//console.log('mousemove');
  				// $('div.pp_default .pp_next:hover').addClass('.grab');
  				// $('div.pp_default .pp_previous:hover').addClass('.grab');
  				// 		$('div.pp_default .pp_next:hover').addClass('.grabbing');
  				// 		$('div.pp_default .pp_previous:hover').addClass('.grabbing');
  				//TODO: Add support to IE with class .grab and .grabbing
  				$('div.pp_default .pp_hoverContainer').css('cursor','-webkit-grab');
  					if (vm.clicking) {
  							e.preventDefault();
  							$('div.pp_default .pp_hoverContainer').css('cursor','-webkit-grabbing');
  							var directionX = (vm.previousX - e.clientX) > 0 ? 1 : -1;
  							var directionY = (vm.previousY - e.clientY) > 0 ? 1 : -1;
  							//$("#scroll").scrollLeft($("#scroll").scrollLeft() + 10 * directionX);
  							//$("#scroll").scrollTop($("#scroll").scrollTop() + 10 * directionY);
  							$(selector).scrollLeft($(selector).scrollLeft() + (vm.previousX - e.clientX));
  							$(selector).scrollTop($(selector).scrollTop() + (vm.previousY - e.clientY));
  			//				$('.pp_close').css('right',$(selector).scrollLeft()*-1);
  							// $('.pp_close').css('top',$(selector).scrollTop());
  							vm.previousX = e.clientX;
  							vm.previousY = e.clientY;
  					}
  			});
  			$('.pp_pic_holder.pp_default').mouseleave(function(e) {
  				//console.log('mouseleave');
  					vm.clicking = false;
  			});
  		},
  		changepicturecallback: function(){
  			//remove missing images from list
  			for (k = 0; k<modalBurialDetails.failToLoadImages.length; k++){
  				for(i = 0; i< pp_images.length; i++){
  					if((pp_images[i].split('memorials/')[1] && modalBurialDetails.failToLoadImages[k].split('memorials/')[1] &&
  		      		  pp_images[i].split('memorials/')[1].split('?')[0] === modalBurialDetails.failToLoadImages[k].split('memorials/')[1].split('?')[0])
  		      		  || (pp_images[i].indexOf(modalBurialDetails.failToLoadImages[k])>-1)){
  						pp_images.splice(i,1);
  					}
  				}
  			}

  			//remove missing images from gallery
  			$(".pp_gallery img").each(function() {
  		      if(this.src.indexOf("/images/") > -1){
  		      	for (var i in modalBurialDetails.failToLoadImages){
  		      		if((this.src.split('memorials/')[1] && modalBurialDetails.failToLoadImages[i].split('memorials/')[1] &&
  		      		  this.src.split('memorials/')[1].split('?')[0] === modalBurialDetails.failToLoadImages[i].split('memorials/')[1].split('?')[0])
  		      		  || (this.src.indexOf(modalBurialDetails.failToLoadImages[i])>-1)){
  		      			$(this).parent().parent().remove();
  		      		}
  		      	}
  		      }
  		    });


  			//hide previous and next buttons when there is only one image
  			if(pp_images.length === 1){
  				$('.pp_next').hide();
  				$('.pp_previous').hide();
  			} else{
  				//disable changePage when expanded
  				// .pp_contract class means image is already expanded
  				if($('a.pp_expand').length===0){
  					$('.pp_next').hide();
  					$('.pp_previous').hide();
  				} else {
  					$('.pp_next').show();
  					$('.pp_previous').show();
  				}
  			}

  			// allow horizontal scrollbar when expand image
  			// .pp_contract class means image is already expanded
  			if($('a.pp_expand').length===0){
  				//add horizontal scrolling support for full screen images
  				//hide close button at the top and add an additional expand/contract button
  				$('.pp_close').hide();
          $('.pp_details .pp_contract').hide();
  				$('#ppex_top').show();
  				$('#ppex_top').removeClass('pp_expand').addClass('pp_contract');

  				if(imgPreloader.width > screen.width){
  					$('.pp_pic_holder.pp_default').addClass('pp_pic_holder100');
  					$('.pp_content_container').addClass('pp_pic_holder100');
  					$('.pp_content_container').css("overflow","scroll");
  					$('#ppex_top').css("position","fixed");
  					$('#ppex_top').css("top","0px");
            $('#ppex_top').css("right","0px");
            /* initial property not supported in Internet Explorer
            $('.pp_pic_holder.pp_default').css("overflow-x","initial");
    				$('.pp_pic_holder.pp_default').css("overflow-y","initial");
            */
  					$('.pp_pic_holder.pp_default').css("overflow-x","visible");
  					$('.pp_pic_holder.pp_default').css("overflow-y","visible");
  					//hide frame for full screen images
  					$('.pp_top').hide();
  					this.addDragAndDropSupportForScrollingTo('.pp_content_container', this.clicking);
  				}else{
  					if(imgPreloader.height > window.innerHeight){
  						// $('html').css('overflow-y','auto');
  						// addDragAndDropSupportForScrollingTo('body', this.clicking);
  						// $('.pp_content_container').addClass('pp_pic_holder100');
  						$('.pp_content_container').css("overflow","scroll");
  						$('.pp_content_container').css("height",(window.innerHeight - 40)+"px");
  						$('#ppex_top').css("position","fixed");
  						$('#ppex_top').css("top","0px");
  						$('#ppex_top').css("right",((screen.width - imgPreloader.width)/2)+"px");
              $('.pp_top').hide();
  						this.addDragAndDropSupportForScrollingTo('.pp_content_container', this.clicking);
  					}
  				}
  				this.allowPanImageInExpand = true;
  			} else{
  				//hide scrollbar and remove custom class
          $('.pp_content_container').find('.pp_contract').removeClass('pp_contract').addClass('pp_expand');
  				$('#ppex_top').removeClass('pp_expand').addClass('pp_contract');
  				$('.pp_close').show();
  				$('#ppex_top').hide();
  				$('.pp_pic_holder.pp_default').css("overflow-x","auto");
  				$('.pp_pic_holder.pp_default').css("overflow-y","hidden");
  				$('.pp_pic_holder.pp_default').removeClass('pp_pic_holder100');
  				$('.pp_content_container').removeClass('pp_pic_holder100');
          /* initial property not supported in Internet Explorer
  				$('.pp_content_container').css("overflow","initial");
          */
          $('.pp_content_container').css("overflow","visible");
  				$('.pp_close').css("position","absolute");
  				$('.pp_close').css("top","-20px");
  				$('html').css('overflow-y','hidden');
          $('html').css('overflow-x','hidden');
  				$('body').scrollTop(0);
  				$('.pp_close').css('right',0);
  				$('.pp_top').show();
  				this.allowPanImageInExpand = false;
  			}
  		}
  	});
  },

};
