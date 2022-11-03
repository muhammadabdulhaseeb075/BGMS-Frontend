angular.module('bgmsApp.map').service('interactionService', function(){

	/* 
	Map interactions are represented by an object of the type
		{
			group: 'if it belongs to a user action eg draw, layerswitch, personselect etc'
			type: 'olInteractionType'
			parameters: {param_name: param_value}
			handlers: {handler_function_name: handler_function}
		}

		Only one interaction of a given type is usually honored by openlayers.
		Currently supporting the following interactions:
			pointer - 
			draw
			select
			modify
	*/

	this.getInteractions = function(){
		return window.MapInteractions;
	};

	this.getInteractionByType = function(interactionType){
        try{
            return this.getInteractions()[this.getInteractionPositionInStack('type', interactionType)[0]];
        }
        catch(e){
            console.log('interaction of type'+interactionType+' could not be found');
            return;
        }
	};

	this.pushInteraction = function(interaction){
		jQuery(document).trigger('pushInteraction', interaction);
	};

	this.removeInteractionsByGroup = function(interactionGroup){
		jQuery(document).trigger('removeInteractionsByGroup', interactionGroup);
	};


});