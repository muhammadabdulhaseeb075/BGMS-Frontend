angular.module('bgmsApp.map').service('userActionService', ['interactionService', 'eventService', 'markerService', function(interactionService, eventService, markerService){
	this.interactionStore = {};

	this.drawActionStart = function(){
		var person = interactionService.removeInteractionsByGroup('person');
		var add_grave = interactionService.removeInteractionsByGroup('add_grave');
		if(person)
			this.interactionStore['person'] = person;
		if(add_grave)
			this.interactionStore['add_grave'] = add_grave;
	};

	this.drawActionEnd = function(){
		interactionService.removeInteractionsByGroup('draw');
		var person = this.interactionStore['person'];
		if(person){
			for (var i = person.length - 1; i >= 0; i--) {
				interactionService.pushInteraction(person[i]);
			};
		}
	};

	this.addGraveActionStart = function(){
		var person = eventService.removeEventsByGroup('person');
		var draw = interactionService.removeInteractionsByGroup('draw');
		if(person)
			this.interactionStore['person'] = person;
		if(draw)
			this.interactionStore['draw'] = draw;
	};

	this.addGraveActionEnd = function(){
		interactionService.removeInteractionsByGroup('add_grave');
		var person = this.interactionStore['person'];
		if(person){
			for (var i = person.length - 1; i >= 0; i--) {
				eventService.pushEvent(person[i]);
			};
		}

	};

	this.personFunctionality = function(person){
		interactionService.removeInteractionsByGroup('draw');
		interactionService.removeInteractionsByGroup('add_grave');
	};

	this.layerFunctionality = function(person){
		this.persons[person.id] = person;
	};
	
}]);