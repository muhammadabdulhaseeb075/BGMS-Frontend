angular.module('bgmsApp.map').service('layerGenerator', ['$http', '$q', '$timeout', '$rootScope', 'memorialService', 'layerService', 'layerGroupService', 'styleService', 'MapService',
	function ($http, $q, $timeout, $rootScope, memorialService, layerService, layerGroupService, styleService, MapService) {

		var view_model = this;

		view_model.layerNames = null;

		view_model.geoJSONSourceStore = {};

		/*Functions relating to creating layers and sources*/

		view_model._resolveGeoJSONSourceFromUrl = function (url) {
			$http.get(url).
				success(function (data, status, headers, config) {
					view_model.geoJSONSourceStore[url].resolve(data);
				}).
				error(function (data, status, headers, config) {
					console.log('could not load data from ' + url);
					view_model.geoJSONSourceStore[url].reject('could not load data from ' + url);
				});
		};

		view_model.getGeoJSONSource = function (url) {
			if (!view_model.geoJSONSourceStore[url]) {
				view_model.geoJSONSourceStore[url] = $q.defer();
				view_model._resolveGeoJSONSourceFromUrl(url);
			}
            return view_model.geoJSONSourceStore[url].promise;
		};
	}]);
