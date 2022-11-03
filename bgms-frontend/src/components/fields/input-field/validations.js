import isEmpty from "validator/lib/isEmpty";
import _inRange from "lodash/inRange";
import {DateTime} from "luxon";


export default {
    required: (value) => !isEmpty(value, { ignore_whitespace: false }),
    timeRange: (value) => {
        if( value ) {
            const dateToBeComparedInMillis = DateTime.fromFormat(value, "T").toMillis();
            const initialRange = DateTime.fromFormat("8:00", "T").toMillis();
            const endRange = DateTime.fromFormat("17:31", "T").toMillis();
            return _inRange(dateToBeComparedInMillis, initialRange, endRange);
        }
        return false;

    }
};
