//setting timeout interval to match the AdminLte's animation delay, so 
//that map+ui-grid resize happens when the sidebar is completely hidden/shown
var dataentrySidebarTimeout = null;
var dataentrySidebarTimeoutInterval = 500;

$(function(){

	//set initial active link
	   var url = window.location.hash;

	   $('ul.nav a[href="' + url + '"]').parent().addClass('active');
	   $('ul.nav a').filter(function() {
	      return this.href == url;
	   }).parent().parent().parent().addClass('active');

	   $(window).on('hashchange',function(e){ 
		   var url = window.location.hash;
		   if(url.indexOf('?')!=-1)
			   url = url.substring(0, url.indexOf('?'));
		   $('.sidebar-menu').children().removeClass('active');
		   $('ul.nav a[href="' + url + '"]').parent().addClass('active');
	   });
	   
	// Set active link on click
	$('.sidebar-menu > li').children().on('click', function(event){
		var e = $(event.currentTarget);
        e.parent().parent().children().removeClass('active');
        e.parent().addClass("active");
//        debugger;
//        if(window.location.hash==='#/addRecord'){
//        	location.reload();        	
//        }
	});
	
	//fixing the table resize bug on clicking
	$('.sidebar-toggle').on('click', function(event){
		if(dataentrySidebarTimeout){
			window.clearTimeout(dataentrySidebarTimeout);
		}
		dataentrySidebarTimeout = window.setTimeout(function(){
			var bgmsImageViewerController = angular.element('bgms-image-viewer').controller('bgmsImageViewer');
			if(bgmsImageViewerController)
				bgmsImageViewerController.updateMapSize();
			var uiGridController = angular.element('[ui-grid]').controller();
			if(uiGridController && uiGridController.updateUiGrid)
				uiGridController.updateUiGrid();
		}, dataentrySidebarTimeoutInterval);
	});
});
