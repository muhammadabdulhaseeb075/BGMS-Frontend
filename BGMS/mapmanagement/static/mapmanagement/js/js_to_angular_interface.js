
var jsAngularInterface = {
	mapController: null,
	addGraveController: null,
	personController: null,
	memorialService: null,
	staticFilesLocation: {},

	getMapController: function(){
		if(!this.mapController)
			this.mapController = angular.element(document.querySelector(constants.MAP_ELEMENT_SELECTOR)).controller();
		return this.mapController;
	},
	getAddGraveController: function(){
		if(!this.addGraveController)
			this.addGraveController = angular.element(document.querySelector(constants.ADD_GRAVE_ELEMENT_SELECTOR)).controller();
		return this.addGraveController;
	},
	getPersonController: function(){
		if(!this.personController)
			this.personController = angular.element(document.querySelector(constants.PERSON_ELEMENT_SELECTOR)).controller();
		return this.personController;
	},
	showHoverDetails: function(personId){
		this.getPersonController().showSearchHover(personId);
	},
	hidePersonDetails: function(coordinates, personId){
		// this.getPersonController().hideClickDetails();
		this.getPersonController().hideHoverDetails();
	},
	hidePersonClickDetails: function(coordinates, personId){
		this.getPersonController().hideClickDetails();
	},
	setStaticFilesLocation: function(staticFilesUrl){
		this.getMapController().setStaticFilesLocation(staticFilesUrl);
	},
};
