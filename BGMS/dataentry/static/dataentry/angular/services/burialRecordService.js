angular.module('bgmsApp.dataentry').service('burialRecordService', ['burialRecordModel', 'tagModel', function(burialRecordModel, tagModel){
	
	var view_model = this;
	
	/**
	 * @description
	 * Function to create a new BurialRecord from a row of downloaded data
	 * @param {Array<Object>} columns - array of Column objects
	 * @returns {Object<BurialRecord>} - newly created burial record
	 */
	view_model.createBurialRecord = function(data){
		var newBurialRecord = new burialRecordModel();
		for( var index in data ){
			var cell = data[index];
			if(cell.constructor === Array){
				//if array, it is a many to many column
				newBurialRecord.manyToManyKeys[index] = cell;
			} else if(cell.constructor === Object){
				//if object it is a foreign key or combined column or tag
				var isCombinedColumn = Object.keys(cell).pop().indexOf('___')!=-1;
				var isTag = index.indexOf('person___tag')!=-1;
				if(isTag){
					newBurialRecord.tag = new tagModel(cell);					
				} else if(isCombinedColumn){
					newBurialRecord.combinedColumns[index] = cell;					
				}
				else{//is foreign key
					newBurialRecord.foreignKeys[index] = cell;					
				}
			} else{
				//object is a simple key either part
				newBurialRecord.simpleKeys[index] = cell;
			}
		}
		return newBurialRecord;
	};

	/**
	 * @function
	 * @description
	 * Function that creates a new BurialRecord from column values
	 * @param {Array<Column>} columns - array of columns
	 */
	view_model.createBurialRecordFromColumns = function(columns){
		var newBurialRecord = new burialRecordModel();
		for (var index=columns.length-2;index>=0;index--){
			var column = columns[index];
			if(column.type==='SimpleColumn'){
				newBurialRecord.simpleKeys[column.name] = column.columnValue()[column.name];
			}
			else if(column.type==='CombinedColumn'){
				newBurialRecord.combinedColumns[column.name] = column.columnValue()[column.name];
			}
			else if(column.type==='ForeignKey'){
				newBurialRecord.foreignKeys[column.name] = column.columnValue()[column.name];
			}
			else if(column.type==='ManyToManyKey'){
				if(!newBurialRecord.manyToManyKeys[column.modelname+'___'+column.fieldname])
					newBurialRecord.manyToManyKeys[column.modelname+'___'+column.fieldname] = [];
				Array.prototype.push.apply(newBurialRecord.manyToManyKeys[column.modelname+'___'+column.fieldname], column.columnValue()[column.name]);
			}
		}
		return newBurialRecord;
	};
	
}]);