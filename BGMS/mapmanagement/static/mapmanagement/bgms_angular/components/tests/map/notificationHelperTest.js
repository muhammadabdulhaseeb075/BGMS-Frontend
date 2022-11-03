"use strict";

describe("notification helper service", function () {
  var notificationHelper, $compile, $rootScope, scope;

  beforeEach(module("bgmsApp"));
//  beforeEach(module("bgmsApp.map"));

  beforeEach(inject(function (_notificationHelper_, _$compile_, _$rootScope_) {
	  notificationHelper = _notificationHelper_;
	  $compile = _$compile_;
	  $rootScope = _$rootScope_;
	  scope = $rootScope.$new();
  }));
  
  // testing createConfirmation function
  it("should call scope.apply on success callback of confirmation", function () {
	  notificationHelper.createConfirmation('Confirmation Needed','Do you want to do something?', 
		function(){
		  console.log('success callback');
	  	  expect($rootScope.$$phase).toBe("$apply");
	  	},
	  	null);
	  //clicking first button ie yes
  	  var element = jQuery('.ui-pnotify-container button').first();
  	  element.click();
  });

  it("should call scope.apply on success callback of confirmation", function () {
	  notificationHelper.createConfirmation('Confirmation Needed','Do you want to delete the plot?', 
		null,
	  	function(){
			  console.log('failure callback');
		  	  expect($rootScope.$$phase).toBe("$apply");
	  });
	  //clicking second button ie n
	  var element = jQuery('.ui-pnotify-container button').last();
	  element.click();
  });
});