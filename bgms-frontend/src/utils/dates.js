import { DateTime } from "luxon";

export function convertTimeToTwelveHourFormat (timeInTwentyFourHourFormat){
    return DateTime.fromFormat(timeInTwentyFourHourFormat, "T").toFormat("h:mm a");
};

export function convertTimeToTwentyFourHourFormat(timeInTwelveHourFormat){
    return DateTime.fromFormat(timeInTwelveHourFormat, "t" ).toLocaleString(DateTime.TIME_24_SIMPLE);
};
