enum PERSON_BURIAL_OPTIONS { person, burial }

enum FEATURE_TYPES { memorial = 'memorial', grave = 'grave' }

/** Router names **/
const MEMORIAL_MANAGEMENT_PATH = 'memorialmanagement';
enum MEMORIAL_MANAGEMENT_CHILD_ROUTES {
  persons = 'persons', 
  addPerson = 'addPerson', 
  memorialDetails= 'memorialDetails', 
  memorialGeometry= 'memorialGeometry',
  linkedGraves = 'linkedGraves', 
  photos = 'photos',
  attributes = 'memorialAttributes',
  surveys = 'memorialSurveys'
}

const GRAVE_MANAGEMENT_PATH = 'gravemanagement';
enum GRAVE_MANAGEMENT_CHILD_ROUTES {
  burials = 'burials', 
  addBurial = 'addBurial', 
  reservations = 'reservations', 
  addReservation = 'addReservation', 
  convertReservation = 'convertReservation',
  deleteReservation = 'deleteReservation',
  graveDetails= 'graveDetails',
  graveGeometry= 'graveGeometry',
  linkedMemorials = 'linkedMemorials', 
  graveOwnershipOption = 'graveOwnershipOption', 
  graveOwnership = 'graveOwnership', 
  graveowner = 'graveowner',
  newGraveOwner = 'newGraveOwner',
  attributes = 'graveAttributes',
  surveys = 'graveSurveys' }

const BURIAL_PERSON_MANAGEMENT_PATH = 'burialpersonmanagement';
enum BURIAL_PERSON_MANAGEMENT_CHILD_ROUTES { 
  person = 'burialPerson' }

const PERSON_MANAGEMENT_PATH = 'personmanagement';
enum PERSON_MANAGEMENT_CHILD_ROUTES { 
  personownership = 'personownership',
  personNextOfKinTo = 'personNextOfKinTo',
  persondetails = 'persondetails',
  persondetailsaddress = 'persondetailsaddress' }

  const COMPANY_MANAGEMENT_PATH = 'companymanagement';
  enum COMPANY_MANAGEMENT_CHILD_ROUTES { 
    companyownership = 'companyownership', 
    companydetails = 'companydetails',
    companydetailsaddress = 'companydetailsaddress' }

  const FEATURE_MANAGEMENT_PATH = 'featuremanagement';
  enum FEATURE_MANAGEMENT_CHILD_ROUTES {
    attributes = 'featureAttributes',
    surveys = 'surveys' }

export default {
  PERSON_BURIAL_OPTIONS: PERSON_BURIAL_OPTIONS,
  FEATURE_TYPES: FEATURE_TYPES,

  MEMORIAL_MANAGEMENT_PATH: MEMORIAL_MANAGEMENT_PATH,
  MEMORIAL_MANAGEMENT_CHILD_ROUTES: MEMORIAL_MANAGEMENT_CHILD_ROUTES,

  BURIAL_PERSON_MANAGEMENT_PATH: BURIAL_PERSON_MANAGEMENT_PATH,
  BURIAL_PERSON_MANAGEMENT_CHILD_ROUTES: BURIAL_PERSON_MANAGEMENT_CHILD_ROUTES,

  GRAVE_MANAGEMENT_PATH: GRAVE_MANAGEMENT_PATH,
  GRAVE_MANAGEMENT_CHILD_ROUTES: GRAVE_MANAGEMENT_CHILD_ROUTES,

  PERSON_MANAGEMENT_PATH: PERSON_MANAGEMENT_PATH,
  PERSON_MANAGEMENT_CHILD_ROUTES: PERSON_MANAGEMENT_CHILD_ROUTES,

  COMPANY_MANAGEMENT_PATH: COMPANY_MANAGEMENT_PATH,
  COMPANY_MANAGEMENT_CHILD_ROUTES: COMPANY_MANAGEMENT_CHILD_ROUTES,

  FEATURE_MANAGEMENT_PATH: FEATURE_MANAGEMENT_PATH,
  FEATURE_MANAGEMENT_CHILD_ROUTES: FEATURE_MANAGEMENT_CHILD_ROUTES
};

export type PERSON_BURIAL_OPTIONS_ENUM = PERSON_BURIAL_OPTIONS;

export type FEATURE_TYPES_ENUM = FEATURE_TYPES;

export interface FEATURES_DATA {
  readonly featureID: string;
  readonly layerName: string;
}