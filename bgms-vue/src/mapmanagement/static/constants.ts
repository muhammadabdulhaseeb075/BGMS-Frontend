// default column widths for forms within management tool
const LABEL_COLUMN_CLASSES = 'col-xs-4 control-label';
const FIELD_COLUMN_CLASSES = 'col-xs-8 no-padding';

// Width of the management tool
// Note: these must match constants in sass file
const TOOL_WIDTH: number = 170;
const TOOL_WIDTH_NARROW: number = 25;
const TOOL_CONTENT_WIDTH: number = 303;
const TOOL_BORDER_WIDTH: number = 4;

export default {
  LABEL_COLUMN_CLASSES: LABEL_COLUMN_CLASSES,
  FIELD_COLUMN_CLASSES: FIELD_COLUMN_CLASSES,
  TOOL_WIDTH: TOOL_WIDTH,
  TOOL_BORDER_WIDTH: TOOL_BORDER_WIDTH,
  TOOL_WIDTH_NARROW: TOOL_WIDTH_NARROW,
  TOOL_CONTENT_WIDTH: TOOL_CONTENT_WIDTH,
};

export const SUBBUTTONNAMES = {
  OWNERSHIPSUBBUTTONS: "ownershipSubbuttons",
  RESERVATIONSUBBUTTONS: "reservationSubbuttons",
  BURIALSUBBUTTONS: "burialSubbuttons",
  SURVEYSUBBUTTONS: "surveySubbuttons",
  PERSONSUBBUTTONS: "personSubbuttons"
}

export enum SEARCH_TYPE_ENUM { burial = 'burial', reservation = 'reservation', owner = 'owner', grave = 'grave' }