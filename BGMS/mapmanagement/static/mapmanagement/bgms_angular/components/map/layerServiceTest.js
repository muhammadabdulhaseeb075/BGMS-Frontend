//"use strict";
//
//describe("layer api service", function () {
//  var layerService, httpBackend;
//
//  beforeEach(module("reddit"));
//
//  beforeEach(inject(function (_ledditService_, $httpBackend) {
//    layerService = _layerService_;
//    httpBackend = $httpBackend;
//  }));
//
//  it("should add layer", function () {
//    // httpBackend.whenGET("http://api.reddit.com/user/yoitsnate/submitted.json").respond({
//    //     data: {
//    //       children: [
//    //         {
//    //           data: {
//    //             subreddit: "golang"
//    //           }
//    //         },
//    //         {
//    //           data: {
//    //             subreddit: "javascript"
//    //           }
//    //         },
//    //         {
//    //           data: {
//    //             subreddit: "golang"
//    //           }
//    //         },
//    //         {
//    //           data: {
//    //             subreddit: "javascript"
//    //           }
//    //         }
//    //       ]
//    //     }
//    // });
//    layerService.addLayer('baseLayer', 'Layer').then(function(subreddits) {
//      expect(subreddits).toEqual(["golang", "javascript"]);
//    });
//    httpBackend.flush();
//  });
//
//});