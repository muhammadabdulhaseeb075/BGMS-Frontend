import moment from 'moment';

/**
 * Format date with space between names and last name in uppercase
 * @param firstNames 
 * @param lastName 
 */
export function formatName(firstNames, lastName) {

  let name = firstNames ? firstNames : '';
  
  if (lastName) {
    if (name)
      name += ' ';

    name += lastName.toUpperCase();
  }
  
  return name;
}

/**
 * Format date
 * @param value The date
 * @returns The formatted date (dd MMM yyyy) or '-'
 */
export function formatDate(value){
  if (value && value != "None") {
    let dateArray = value.split("-");
    return (parseInt(dateArray[2]) ? parseInt(dateArray[2]) : 'day') + ' ' + (parseInt(dateArray[1]) ? integerMonthToShort(parseInt(dateArray[1])) : 'month') + ' ' + (parseInt(dateArray[0]) ? parseInt(dateArray[0]) : 'year');
  } 
  else {
    return '-';
  }
}

/**
 * Retruns date string from three date fields
 * @param day 
 * @param month 
 * @param year 
 */
export function individualDateFieldsToSingleDate(day, month, year) {
  let date = '';

  if (day)
    date = day;
  
  if (month) {
    date += date ? ' ' : '';
    date += integerMonthToShort(month);
  }
  
  if (year) {
    date += date ? ' ' : '';
    date += year;
  }

  return date;
}
  
/**
 * Maps a month number to month abbreviation
 * @param monthAsNumber 
 */
function integerMonthToShort(monthAsNumber: number): string {
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

  let returnValue = months[monthAsNumber-1];

  if (returnValue)
    return returnValue;
  else
    return 'MMM';
}

/**
 * I.e. 2019-09-11T15:15
 */
export const SERVER_DATE_MOMENT_FORMAT = "YYYY-MM-DDTHH:mm";

/**
 * I.e. 11 Sep 2019
 */
export const DISPLAY_DATE_MOMENT_FORMAT = "D MMM YYYY";

/**
 * I.e. Wednesday 11 Sep 2019
 */
export const DISPLAY_DATE_WITH_DAYNAME_MOMENT_FORMAT = "dddd " + DISPLAY_DATE_MOMENT_FORMAT;

/**
 * I.e. 3:15pm
 */
export const DISPLAY_TIME_MOMENT_FORMAT = "h:mma";

/**
 * I.e. 11 Sep 2019 3:15pm
 */
export const DISPLAY_DATETIME_WITH_DAYNAME_MOMENT_FORMAT = DISPLAY_DATE_WITH_DAYNAME_MOMENT_FORMAT + " " + DISPLAY_TIME_MOMENT_FORMAT;

/**
 * Convert JS date object to a displayable date
 * @param datetime 
 * @returns {string} Returns date formatted for displaying
 */
export function getDisplayDate(datetime: Date, includeDayName: boolean = true): string {
  let momentDatetime = moment(datetime);

  if (includeDayName) {
    return momentDatetime.format(DISPLAY_DATE_WITH_DAYNAME_MOMENT_FORMAT);
  }

  return momentDatetime.format(DISPLAY_DATE_MOMENT_FORMAT);
}

/**
 * Convert time part of JS date object to a displayable time
 * @param datetime 
 * @returns {string} Returns time formatted for displaying
 */
export function getDisplayTimeFromDatetime(datetime: Date): string {
  return getDisplayTime(datetime.getHours(), datetime.getMinutes());
}

/**
 * Convert hours and minutes to a displayable time
 * @param hours
 * @param minutes
 * @returns {string} Returns time formatted for displaying
 */
export function getDisplayTime(hours: number, minutes: number): string {
  const time = moment(hours + ":" + minutes, "HH:mm");
  return time.format(DISPLAY_TIME_MOMENT_FORMAT)
}

/**
 * @param date { day, month, year }
 * @returns Date as a string for saving (yyyy-mm-dd)
 */
export function dateFieldsToStringForSaving(date: { day, month, year }) {
  if (date.day && date.month && date.year)
    return date.year + '-' + date.month + '-' + date.day;
  else
    return null;
}

/**
 * Format the age so it is in years
 * @param {number} years
 * @param {number} months
 * @param {number} weeks
 * @param {number} days
 * @param {number} hours
 * @return The age in years or < 0
 */
export function formatAgeYears(years: number, months: number, weeks: number, days: number, hours: number, minutes: number) {
  if(!years && (months>0 ||
      weeks>0 || days>0 ||
      hours>0 || minutes>0)){
      return '< 1';
  } else {
      return years;
  }
}
  
export function getRoundedAge(years: number, months: number, weeks: number, days: number, hours: number, minutes: number){
  let age = { age:'Unknown', units:'' };
  
  if(years){
    age.age = String(years);
    age.units = "year";
  } 
  else if(months){
    age.age = String(months);
    age.units = "month";
  } 
  else if(weeks){
    age.age = String(weeks);
    age.units = "week";
  } 
  else if(days){
    age.age = String(days);
    age.units = "day";
  } 
  else if(hours){
    age.age = String(hours);
    age.units = "hour";
  }
  else if(minutes){
    age.age = String(minutes);
    age.units = "minute";
  }

  if(age.age!='Unknown' && age.age!='1')
    age.units+='s';

  return age;
}

/**
 * Recursive function for changing all undefined number fields to nulls
 * (Currently when number input is blank, v-model.number turns into a string. 
 * This is a bug in Vue that might be fixed in Vue 3.)
 * @param data
 */
export function makeUndefinedNumbersNull(data) {
  for (let key in data) {

    if (typeof data[key] === 'object') {
      // if object, we need to check each child key
      makeUndefinedNumbersNull(data[key]);
    }

    // Determine if this field is a number field. If it is, make it null.
    if (key.indexOf('_date_day') !== -1 || key.indexOf('_date_month') !== -1 || key.indexOf('_date_year') !== -1 || key.indexOf('age_') !== -1 || key==='tenure_years') {
      if (!data[key])
        data[key] = null;
    }
  }

  return data;
}

/**
 * Format address fields into a single string (short)
 * @param firstLine 
 * @param town 
 * @param postcode 
 */
export function formatAddress(firstLine, town, postcode) {
  let address = firstLine ? firstLine : '';
  
  if (town) {
    if (address)
      address += ', ';

    address += town;
  }
  
  if (postcode) {
    if (address)
      address += ', ';

    address += postcode.toUpperCase();
  }
  
  return address;
}

/**
 * Validate email address
 * @param email
 */
export function validateEmailAddress(email) {
  
  const re = new RegExp(/^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/);
  return re.test(String(email).toLowerCase());
}