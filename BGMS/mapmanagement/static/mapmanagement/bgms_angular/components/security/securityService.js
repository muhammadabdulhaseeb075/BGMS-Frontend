angular.module('bgmsApp.map').service('securityService', ['$http', '$q', function($http, $q){

  var view_model = this;
  this.group_required_value = null;
  this.groups = null;
  view_model.username = $q.defer();

	view_model.group_required = function(group_names){

    $http.get("/bgsite/group_required/", { 'params': { 'group_names': JSON.stringify(group_names) }}).
    success(function(data, status, headers, config) {
      // alert(data.group_required);
      view_model.group_required_value.resolve(data.group_required);
    }).
    error(function(data, status, headers, config) {
      console.log('could not load data' + data);
      view_model.username.reject('');
      return false;
    });
	};

  view_model.get_group_required_value = function (group_names) {
    if(!view_model.group_required_value){
        view_model.group_required_value = $q.defer();
        view_model.group_required(group_names);
    }
    return view_model.group_required_value.promise;
  };

  view_model.get_groups = function () {
    return $http.get('/bgsite/user_groups/');
  }

  view_model.getUserName = function(){
    return view_model.username.promise;
  };

  view_model.setUserName = function(username){
      view_model.username.resolve(username);
  };

}]);
