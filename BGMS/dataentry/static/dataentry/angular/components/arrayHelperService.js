angular.module('bgmsApp.dataentry').service('arrayHelperService', [function(){

	var view_model = this;	

	/**
	 * @function
	 * @description Function returning an array of index positions of a given array
	 * 		of objects where the key:value pair.
	 * @param {string} key - any property name
	 * @param {string} value - the value to search for
	 * @returns {Array<number>} Array of indices of the events matching the key:value pair
	 */
	this.getObjectPosition = function(key, value, array){
		if(!key || !array)
			return null;
 		var positions = [-1];
        var i = 0;
        angular.forEach(array, function(obj, index) {
            if(obj[key] === value){
                positions[i++] = index;
            }
        });
        return positions;
	};

	
	view_model.getPosition = function(name, array){
        for(var index in array){
        	if(array[index] === name)
        		return index;
        }
        return -1;
	};

}]);