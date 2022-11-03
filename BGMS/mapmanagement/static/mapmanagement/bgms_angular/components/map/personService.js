/**
 * @module personService
 *
 * @description
 * This model contains all the persons buried in the site.
 *
 */
angular.module('bgmsApp.map').service('personService', ['memorialService', '$http', '$q', function(memorialService, $http, $q){

	/**
	 * Constructor to create a new person
	 * @class Person
	 * @classdesc Defining the person constructor to use as the model
	 * @param {string} id - unique id, corresponds to id on the server
	 * @param {Array<uuids>} memorial_ids - id of the memorial geometries in the geoJson
	 * @param {string} first_names - first names
	 * @param {string} last_name - last name
	 * @param {Date} burial_date - date of burial from the burial record
	 * @param {number} age_years - age of death (years)
	 * @param {number} age_months - age of death (months)
	 * @param {number} age_weeks - age of death (weeks)
	 * @param {number} age_days - age of death (days)
	 * @param {number} age_hours - age of death (hours)
	 * @param {number} age_minutes - age of death (minutes)
	 *
	 */
	function Person(id, memorial_id, first_names, last_name, burial_date, age_years, age_months, age_weeks, age_days, age_hours, age_minutes){
		this.id = id;
//		this.memorial_id = memorial_id;
		this.memorial_ids = [memorial_id];
		this.first_names = first_names;
		this.last_name = last_name;
		this.burial_date = burial_date;
		this.age_years = age_years;
		this.age_months = age_months;
		this.age_weeks = age_weeks;
		this.age_days = age_days;
    this.age_hours = age_hours;
    this.age_minutes = age_minutes;

		if (this.memorial_ids)
			this.memorials = [memorialService.getMemorialById(memorial_id)];
		else
			this.memorials = undefined;

		this.update = function(personJSON){
			if(personJSON['memorial_id'])
				this.memorial_id = personJSON['memorial_id'];
			if(personJSON['first_names']!== undefined)
				this.first_names = personJSON['first_names'];
			if(personJSON['last_name']!==undefined)
				this.last_name = personJSON['last_name'];
			if(personJSON['burial_date']!==undefined)
				this.burial_date = (personJSON['burial_date'] === null)? 'Unknown':new Date(personJSON['burial_date']);
			if(personJSON['age_years']!==undefined)
				this.age_years = personJSON['age_years'];
			if(personJSON['age_months']!==undefined)
				this.age_months = personJSON['age_months'];
			if(personJSON['age_weeks']!==undefined)
				this.age_weeks = personJSON['age_weeks'];
			if(personJSON['age_days']!==undefined)
				this.age_days = personJSON['age_days'];
			if(personJSON['age_hours']!==undefined)
				this.age_hours = personJSON['age_hours'];
      if(personJSON['age_minutes']!==undefined)
        this.age_minutes = personJSON['age_minutes'];
		};

		this.has_age = function(){
			if(this.age_years || this.age_months || this.age_weeks || this.age_days || this.age_hours || this.age_minutes)
				return true;
			else
				return false;
		};

		this.has_burial_date = function(){
			if (this.burial_date === 'Unknown')
				return false;
			else
				return true;
		};

		this.get_rounded_age = function(){
			age = {age:'Unknown'};
			if(this.age_years){
				age.age = this.age_years;
				age.units = "year";
			} else if(this.age_months){
				age.age = this.age_months;
				age.units = "month";
			} else if(this.age_weeks){
				age.age = this.age_weeks;
				age.units = "week";
			} else if(this.age_days){
				age.age = this.age_days;
				age.units = "day";
			} else if(this.age_hours){
				age.age = this.age_hours;
				age.units = "hour";
			} else if(this.age_minutes){
				age.age = this.age_minutes;
				age.units = "minute";
			}
			if(age.age!='Unknown' && age.age!=1)
				age.units+='s';
			return age;
		};

		this.get_rounded_age_shortened = function(){
			age = this.get_rounded_age();
			if(age.units){
				if(age.units == 'years')
					age.units = 'yrs';
				else if(age.units == 'year')
					age.units = 'yr';
				else if(age.units == 'months')
					age.units = 'mons'
				else if(age.units == 'month')
					age.units = 'mon'
				else if(age.units == 'weeks')
					age.units = 'wks'
				else if(age.units == 'week')
					age.units = 'wk'
				else if(age.units == 'hours')
					age.units = 'hrs';
				else if(age.units == 'hour')
					age.units = 'hr';
			}
			return age;
		};

//		this.getMemorial = function(){
//			if(this.memorial === undefined)
//				this.memorial = memorialService.getMemorialById(this.memorial_id);
//			return this.memorial;
//		};

		this.getMemorials = function(){
//			if(this.memorials === undefined){
				this.memorials = [];
				for (var index in this.memorial_ids){
					var memorial = memorialService.getMemorialById(this.memorial_ids[index]);
					if(memorial)
						this.memorials.push(memorial);
				}
//			}
			return this.memorials;
		};

		this.addMemorial = function(memorial_id){
			this.memorial_ids.push(memorial_id);
			if(this.memorials)
				this.memorials.push(memorialService.getMemorialById(memorial_id));
		};
	}

	var view_model = this;

	let currentPersonID = null;
	let currentPerson = null;

	/**
	 * @param {*} personId Person ID
	 * @returns Single person object
	 */
	view_model.getPersonById = function(personID) {
		let deferred = $q.defer();
		view_model.getPersonsByIds([personID])
		.then(function (persons) {
			deferred.resolve(persons[0]);
		})
		.catch(function () {
			deferred.reject();
		});

		return deferred.promise;
	}

	/**
	 * @param {*} personIds Array containing at least one Person ID
	 * @returns array of Person objects to match given IDs
	 */
	view_model.getPersonsByIds = function(personIds){
		let deferred = $q.defer();
		
		// if the memorialid has not actually changed and isn't being reloaded
		if (JSON.stringify(currentPersonID) === JSON.stringify(personIds)) {
			// if data is still loading in a previous request, wait until it has finished populating the data
			if (currentPerson === 'loading') {
				let intervalID = setInterval(function() {
					if (currentPerson !== 'loading') {
						clearInterval(intervalID);
						deferred.resolve(currentPerson);
					}
				}, 100);
			}
			else
				deferred.resolve(currentPerson);
		}
		else {
			currentPersonID = personIds;
			currentPerson = 'loading';
			$http.get('/mapmanagement/getPersonByID/', {params: { personIds: JSON.stringify(personIds) }}).
			success(function(data, status, headers, config) {
				var personsResult = data.persons;
				let persons = [];
				for(let item in personsResult){
					const personGroup = personsResult[item];
					const person = personGroup[0];
					if(person['id'] != null){
						let personObject = new Person(person.id, person.memorial_id, person.first_names, person.last_name, person.burial_date, person.age_years, person.age_months, person.age_weeks, person.age_days, person.age_hours, person.age_minutes);

						// if same person belongs to multiple memorials
						if (personGroup.length > 1) {
							for (let i=1;i<personGroup.length;i++) {
								personObject.addMemorial(personGroup[i].memorial_id);
							}
						}

						persons.push(personObject);
					}
				}
				currentPerson = persons;
				deferred.resolve(persons);

			}).
			error(function(data, status, headers, config) {
				deferred.reject();
				console.log('could not load data from /mapmanagement/getPersonByID/');
			});
		}

		return deferred.promise;
	};

	view_model.currentMemorialID = null;
	let currentMemorialPersons;
	let currentKnownMemorials = [];

	/**
	 * @param {*} memorial_ids Array containing at least one graveplot.uuid for plots with people
	 * @returns array of Person objects for persons related to given memorial_ids
	 */
	view_model.getPersonsByMemorialIds = function(memorial_ids){
		let deferred = $q.defer();
		// if the memorialid has not actually changed
		if (JSON.stringify(view_model.currentMemorialID) === JSON.stringify(memorial_ids)) {
			// if data is still loading in a previous request, wait until it has finished populating the data
			if (currentMemorialPersons === 'loading') {
				let intervalID = setInterval(function() {
					if (currentMemorialPersons !== 'loading') {
						clearInterval(intervalID);
						deferred.resolve({ persons: currentMemorialPersons, knownMemorials: currentKnownMemorials });
					}
				}, 100);
			}
			else
				deferred.resolve({ persons: currentMemorialPersons, knownMemorials: currentKnownMemorials });
		}
		else {
			view_model.currentMemorialID = memorial_ids;
			currentKnownMemorials = [];
			currentMemorialPersons = 'loading';
			$http.get('/mapmanagement/getPersonByMemorialID/', {params: { memorialId: JSON.stringify(memorial_ids) }}).
			success(function(data, status, headers, config) {
				var personsResult = data.persons;
				let persons = [];
				for(var i=0;i<personsResult.length;i++){
					var personDetails = personsResult[i];
					if(personDetails['id'] != null){
						let person = new Person(personDetails['id'], personDetails['memorial_id'], personDetails['first_names'], personDetails['last_name'], (personDetails['burial_date'] === null)? 'Unknown': view_model.showYearIfImpossibleMonthIsNotDefined(personDetails), personDetails['age_years'], personDetails['age_months'], personDetails['age_weeks'], personDetails['age_days'], personDetails['age_hours'], personDetails['age_minutes']);
						persons.push(person);

						if (currentKnownMemorials.indexOf(personDetails['memorial_id']) === -1)
							currentKnownMemorials.push(personDetails['memorial_id'])
					}
				}
				currentMemorialPersons = persons;
				deferred.resolve({ persons: persons, knownMemorials: currentKnownMemorials });
			}).
			error(function(data, status, headers, config) {
				deferred.reject();
				console.log('could not load data from /mapmanagement/getPersonByMemorialID/');
			});
		}

		return deferred.promise;
	};

	view_model.showYearIfImpossibleMonthIsNotDefined = function (person){
  	let YEAR = 0;
    if(!person['impossible_date_month'] && person['burial_date']){
      return person.burial_date.split('-')[YEAR];
    } else {
      return new Date((person['burial_date'] +" 00:00:00"))
    }
  }
}]);
