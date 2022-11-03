//"use strict";
//
//describe("modal helper service", function () {
//  var modalHelperService;
//  var $compile, $rootScope, scope, element;
//
//  beforeEach(module("bgmsApp"));
////  beforeEach(module("bgmsApp.map"));
//
//  beforeEach(inject(function (_$rootScope_, _$compile_, _modalHelperService_) {
//	  modalHelperService = _modalHelperService_;
//	  $rootScope = _$rootScope_;
//	  $compile = _$compile_;
//	  scope = $rootScope.$new();
//	      element = angular.element(
//	              '<div id="id_modalBurialDetails" class="modal fade" tabindex="-1" role="dialog">'+
//	              '</div>'
//	    		  );
//	      element = $compile(element)(scope);
//	      scope.$digest();
//  }));
//  
//  afterEach(inject(function($rootScope) {
////      $rootScope.$apply();
//  }));
//
//  //testing openModal function
////  update: cannot be tested until library file order is sorted
////  it("should open the modal and modalOpened should be true", function () {
////	  modalHelperService.openModal('test');
////	  var modal = $("#id_modalBurialDetails").data('bs.modal');
////	  expect(modal).toNotEqual(undefined);
////  });
////
////  //testing onCloseModal 
//  it("should be called when modal is dismissed", function () {
//	  $(element).modal({
//	        keyboard: false
//	      });
//	  expect(modal).toNotEqual(undefined);
//	  modalHelperService.onCloseModal(function(a){
//		  console.log('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$');
//		  expect(a).toEqual('called');
//	  }, 'called');
//	  $('#id_modalBurialDetails').modal('hide');
//  });
//  
//});