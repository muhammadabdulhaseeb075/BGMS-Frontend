angular.module('bgmsApp.map').service('featureOverlayService', function(){
	/*
		FeatureOverlays represented by object of type:
	*/

	var view_model = this;

	view_model.getFeatureOverlayStore = function(){
			return window.MapFeatureOverlayStore;
	};

	view_model.addFeatureOverlay = function(featureOverlay){
		jQuery(document).trigger('addFeatureOverlay', featureOverlay);

		// If param is a string, then it contains name of feature overlay.
		// Otherwise it's an object.
		if (typeof(featureOverlay) === 'string')
			return view_model.getFeatureOverlayStore()[featureOverlay];
		else
			return view_model.getFeatureOverlayStore()[featureOverlay.name];
	};

	view_model.removeFeatureOverlayByName = function(featureOverlayName){
			delete view_model.getFeatureOverlayStore()[featureOverlayName];
	};

	view_model.getFeatureOverlay = function(overlayName){
		return view_model.getFeatureOverlayStore()[overlayName];
	};
	
	view_model.removeAllFeaturesInGroup = function(groupName){
		jQuery(document).trigger('removeAllFeaturesInGroup', groupName);
	};
});
