grave_number = "grave_number"
ownership_register = "ownership_register"
section = "section"
subsection = "subsection"
full_name = "full_name"
first_names = "first_names"
last_name = "last_name"
impossible_date = "impossible_date"
birth_date = "birth_date"
birth_date_day = "birth_date_day"
birth_date_month = "birth_date_month"
birth_date_year = "birth_date_year"
profession = "profession"
first_line = "first_line"
second_line = "second_line"
town = "town"
county = "county"
postcode = "postcode"
country = "country"
current = "current"
date_of_death = "date_of_death"
death_date = "death_date"
date_of_death_day = "date_of_death_day"
date_of_death_month = "date_of_death_month"
date_of_death_year = "date_of_death_year"
burial_date = "burial_date"
burial_date_day = "burial_date_day"
burial_date_month = "burial_date_month"
burial_date_year = "burial_date_year"
official_title = "official_title"
official_first_names = "official_first_names"
official_last_name = "official_last_name"
official_type = "official_type"
parish = "parish"
event_name = "event_name"
event_description = "event_description"
religion = "religion"
memorial_id = "memorial_id"
link_burials = "link_burials"
memorials = "memorials"
memorial = "memorial"
feature_id = "feature_id"
status = "status"
state = "state"
ownership_order = "ownership_order"
impossible_date_day = "impossible_date_day"
impossible_date_month = "impossible_date_month"
impossible_date_year = "impossible_date_year"
purchase_date = "purchase_date"
purchase_date_day = "purchase_date_day"
purchase_date_month = "purchase_date_month"
purchase_date_year = "purchase_date_year"
order_date = "order_date"
order_date_day = "order_date_day"
order_date_month = "order_date_month"
order_date_year = "order_date_year"
impossible_order_date_day = "impossible_order_date_day"
impossible_order_date_month = "impossible_order_date_month"
impossible_order_date_year = "impossible_order_date_year"
cost = "cost"
cost_currency = "cost_currency"
feature_1_id = "feature_1_id"
feature_2_id = "feature_2_id"
relationship = "relationship"
deed_reference = "deed_reference"
owner_from_date = "owner_from_date"
owner_from_date_day = "owner_from_date_day"
owner_from_date_month = "owner_from_date_month"
owner_from_date_year = "owner_from_date_year"
owner_to_date = "owner_to_date"
owner_to_date_day = "owner_to_date_day"
owner_to_date_month = "owner_to_date_month"
owner_to_date_year = "owner_to_date_year"
cremation_date = "cremation_date"
cremation_date_day = "cremation_date_day"
cremation_date_month = "cremation_date_month"
cremation_date_year = "cremation_date_year"
impossible_cremation_date_day = "impossible_cremation_date_day"
impossible_cremation_date_month = "impossible_cremation_date_month"
impossible_cremation_date_year = "impossible_cremation_date_year"

"""
List of fields that can be included in a data upload:
"desc": description of the field or group of related fields
"table": name of the database table the field belongs to
"fields": one or more fields belonging to group. This value contains a list of field lists. Lists of lists will be alternative fields. I.e. you can include one of full_name or last_name.
    Field lists:
    "csv_header": what the header should be in the csv file. THIS MUST BE UNIQUE!
    "db_column": name of column in table which this field belongs to.

Note: these fields must be grouped by table and in the order in which that they should be added to the database.
"""
graveFields = [
    # GRAVEPLOT TABLE
    {"desc": "Feature ID for linking to existing graveplot feature", "table": "GravePlot", 
        "fields": [[{"csv_header": feature_id, "db_column": feature_id}]]},

    {"desc": "Grave identifier (not all fields required, but included fields must be unique)", "table": "GravePlot", 
        "fields": [[
            {"csv_header": "grave_number", "db_column": "grave_number"}, 
            {"csv_header": "section", "db_column": "section"}, 
            {"csv_header": "subsection", "db_column": "subsection"}]]},
    
    {"desc": "Grave's status (e.g. private, common, invalid)", "table": "GravePlot", 
        "fields": [[{"csv_header": status, "db_column": status}]]},
   
    {"desc": "Grave's state (e.g. occupied, empty, full)", "table": "GravePlot", 
        "fields": [[{"csv_header": state, "db_column": state}]]},
    
    {"desc": "Grave's type (e.g. earthen grave, brick grave)", "table": "GravePlot", 
        "fields": [[{"csv_header": "type", "db_column": "type"}]]},
    
    {"desc": "Grave's size", "table": "GravePlot", 
        "fields": [[
            {"csv_header": "size", "db_column": "size"},
            {"csv_header": "size_units", "db_column": "size_units"}]]},
    
    {"desc": "Grave's depth", "table": "GravePlot", 
        "fields": [[
            {"csv_header": "depth", "db_column": "depth"},
            {"csv_header": "depth_units", "db_column": "depth_units"}]]},
    
    {"desc": "Perpetual (blank or yes/y/true/1 or no/n/false/0)", "table": "GravePlot", 
        "fields": [[{"csv_header": "perpetual", "db_column": "perpetual", "boolean": True}]]},
    
    {"desc": "Consecrated (blank or yes/y/true/1 or no/n/false/0)", "table": "GravePlot", 
        "fields": [[{"csv_header": "consecrated", "db_column": "consecrated", "boolean": True}]]},
    
    {"desc": "Comment on memorial", "table": "GravePlot", 
        "fields": [[{"csv_header": "memorial_comment", "db_column": "memorial_comment"}]]},

    {"desc": "Remarks on the grave", "table": "GravePlot", 
        "fields": [[{"csv_header": "grave_remarks", "db_column": "grave_remarks"}]]},
    
    # MemorialGraveplot TABLE
    {"desc": "Memorial ID for linking grave to existing memorial feature", "table": "MemorialGraveplot", 
        "fields": [[{"csv_header": memorial_id, "db_column": memorial}]]},
    {"desc": "Option to also link grave's burials to memorial (default true) (blank or yes/y/true/1 or no/n/false/0)", "table": "MemorialGraveplot", 
        "fields": [[{"csv_header": link_burials, "db_column": link_burials, "boolean": True}]]},
]

graveOwnershipFields = [
    #GRAVEDEED TABLE
    {"desc": "Grave identifier (not all fields required, but included fields must be unique)", "table": "GraveDeed", 
        "fields": [[
            {"csv_header": grave_number, "db_column": grave_number}, 
            {"csv_header": section, "db_column": section},
            {"csv_header": subsection, "db_column": subsection}]]},

    {"desc": "Ownership register, the date range related to the owner", "table": "GraveDeed",
            "fields": [[{"csv_header": ownership_register, "db_column": ownership_register}]]},

    {"desc": "Deed reference", "table": "GraveDeed", 
        "fields": [[{"csv_header": deed_reference, "db_column": deed_reference}]]},

    {"desc": "Cost of grave (currency must exist in main_currency)", "table": "GraveDeed", 
        "fields": [
            [{"csv_header": cost_currency, "db_column": cost_currency},
            {"csv_header": cost, "db_column": ""}],
            [{"csv_header": cost_currency, "db_column": cost_currency},
            {"csv_header": "cost_unit", "db_column": "cost_unit"},
            {"csv_header": "cost_subunit", "db_column": "cost_subunit"},
            {"csv_header": "cost_subunit2", "db_column": "cost_subunit2"}]]},

    {"desc": "Grave's purchase date (invalid dates allowed) (purchase_date must be in YYYY-MM-DD format)", "table": "GraveDeed",
        "fields": [[{"csv_header": purchase_date, "db_column": purchase_date}],
            [{"csv_header": purchase_date_day, "db_column": impossible_date_day}, 
            {"csv_header": purchase_date_month, "db_column": impossible_date_month}, 
            {"csv_header": purchase_date_year, "db_column": impossible_date_year}]]},

    {"desc": "Grave's tenure (options: blank, 'PERPETUAL', 'FIXED')", "table": "GraveDeed",
        "fields": [[{"csv_header": "tenure", "db_column": "tenure"}]]},

    {"desc": "Grave's tenure (in years)", "table": "GraveDeed",
        "fields": [[{"csv_header": "tenure_years", "db_column": "tenure_years"}]]},

    {"desc": "Remarks about grave ownership", "table": "GraveDeed",
        "fields": [[{"csv_header": "remarks", "db_column": "remarks"}]]},

    # ADDRESS TABLE 1
    {"desc": "Owner's address 1", "table": "Address_1", 
        "fields": [[
            {"csv_header": 'first_line_1', "db_column": first_line}, 
            {"csv_header": 'second_line_1', "db_column": second_line},
            {"csv_header": 'town_1', "db_column": town}, 
            {"csv_header": 'county_1', "db_column": county},
            {"csv_header": 'postcode_1', "db_column": postcode}, 
            {"csv_header": 'country_1', "db_column": country},
            {"csv_header": 'current_1', "db_column": current, "boolean": True}]]},
    
    {"desc": "Address 1 from date (invalid dates allowed) (from_date must be in YYYY-MM-DD format)", "table": "Address_1",
        "fields": [[{"csv_header": 'from_date_1', "db_column": 'from_date'}],
            [{"csv_header": 'from_date_day_1', "db_column": 'from_date_day'}, 
            {"csv_header": 'from_date_month_1', "db_column": 'from_date_month'}, 
            {"csv_header": 'from_date_year_1', "db_column": 'from_date_year'}]]},
    
    {"desc": "Address 1 to date (invalid dates allowed) (to_date must be in YYYY-MM-DD format)", "table": "Address_1",
        "fields": [[{"csv_header": 'to_date_1', "db_column": 'to_date'}],
            [{"csv_header": 'to_date_day_1', "db_column": 'to_date_day'}, 
            {"csv_header": 'to_date_month_1', "db_column": 'to_date_month'}, 
            {"csv_header": 'to_date_year_1', "db_column": 'to_date_year'}]]},

    # ADDRESS TABLE 2
    {"desc": "Owner's address 2", "table": "Address_2", 
        "fields": [[
            {"csv_header": 'first_line_2', "db_column": first_line}, 
            {"csv_header": 'second_line_2', "db_column": second_line},
            {"csv_header": 'town_2', "db_column": town}, 
            {"csv_header": 'county_2', "db_column": county},
            {"csv_header": 'postcode_2', "db_column": postcode}, 
            {"csv_header": 'country_2', "db_column": country},
            {"csv_header": 'current_2', "db_column": current, "boolean": True}]]},
    
    {"desc": "Address 2 from date (invalid dates allowed) (from_date must be in YYYY-MM-DD format)", "table": "Address_2",
        "fields": [[{"csv_header": 'from_date_2', "db_column": 'from_date'}],
            [{"csv_header": 'from_date_day_2', "db_column": 'from_date_day'}, 
            {"csv_header": 'from_date_month_2', "db_column": 'from_date_month'}, 
            {"csv_header": 'from_date_year_2', "db_column": 'from_date_year'}]]},
    
    {"desc": "Address 2 to date (invalid dates allowed) (to_date must be in YYYY-MM-DD format)", "table": "Address_2",
        "fields": [[{"csv_header": 'to_date_2', "db_column": 'to_date'}],
            [{"csv_header": 'to_date_day_2', "db_column": 'to_date_day'}, 
            {"csv_header": 'to_date_month_2', "db_column": 'to_date_month'}, 
            {"csv_header": 'to_date_year_2', "db_column": 'to_date_year'}]]},

    # ADDRESS TABLE 3
    {"desc": "Owner's address 3", "table": "Address_3", 
        "fields": [[
            {"csv_header": 'first_line_3', "db_column": first_line}, 
            {"csv_header": 'second_line_3', "db_column": second_line},
            {"csv_header": 'town_3', "db_column": town}, 
            {"csv_header": 'county_3', "db_column": county},
            {"csv_header": 'postcode_3', "db_column": postcode}, 
            {"csv_header": 'country_3', "db_column": country},
            {"csv_header": 'current_3', "db_column": current, "boolean": True}]]},
    
    {"desc": "Address 3 from date (invalid dates allowed) (from_date must be in YYYY-MM-DD format)", "table": "Address_3",
        "fields": [[{"csv_header": 'from_date_3', "db_column": 'from_date'}],
            [{"csv_header": 'from_date_day_3', "db_column": 'from_date_day'}, 
            {"csv_header": 'from_date_month_3', "db_column": 'from_date_month'}, 
            {"csv_header": 'from_date_year_3', "db_column": 'from_date_year'}]]},
    
    {"desc": "Address 3 to date (invalid dates allowed) (to_date must be in YYYY-MM-DD format)", "table": "Address_3",
        "fields": [[{"csv_header": 'to_date_3', "db_column": 'to_date'}],
            [{"csv_header": 'to_date_day_3', "db_column": 'to_date_day'}, 
            {"csv_header": 'to_date_month_3', "db_column": 'to_date_month'}, 
            {"csv_header": 'to_date_year_3', "db_column": 'to_date_year'}]]},

    # ADDRESS TABLE 4
    {"desc": "Owner's address 4", "table": "Address_4", 
        "fields": [[
            {"csv_header": 'first_line_4', "db_column": first_line}, 
            {"csv_header": 'second_line_4', "db_column": second_line},
            {"csv_header": 'town_4', "db_column": town}, 
            {"csv_header": 'county_4', "db_column": county},
            {"csv_header": 'postcode_4', "db_column": postcode}, 
            {"csv_header": 'country_4', "db_column": country},
            {"csv_header": 'current_4', "db_column": current, "boolean": True}]]},
    
    {"desc": "Address 4 from date (invalid dates allowed) (from_date must be in YYYY-MM-DD format)", "table": "Address_4",
        "fields": [[{"csv_header": 'from_date_4', "db_column": 'from_date'}],
            [{"csv_header": 'from_date_day_4', "db_column": 'from_date_day'}, 
            {"csv_header": 'from_date_month_4', "db_column": 'from_date_month'}, 
            {"csv_header": 'from_date_year_4', "db_column": 'from_date_year'}]]},
    
    {"desc": "Address 4 to date (invalid dates allowed) (to_date must be in YYYY-MM-DD format)", "table": "Address_4",
        "fields": [[{"csv_header": 'to_date_4', "db_column": 'to_date'}],
            [{"csv_header": 'to_date_day_4', "db_column": 'to_date_day'}, 
            {"csv_header": 'to_date_month_4', "db_column": 'to_date_month'}, 
            {"csv_header": 'to_date_year_4', "db_column": 'to_date_year'}]]},

    # ADDRESS TABLE 5
    {"desc": "Owner's address 5", "table": "Address_5", 
        "fields": [[
            {"csv_header": 'first_line_5', "db_column": first_line}, 
            {"csv_header": 'second_line_5', "db_column": second_line},
            {"csv_header": 'town_5', "db_column": town}, 
            {"csv_header": 'county_5', "db_column": county},
            {"csv_header": 'postcode_5', "db_column": postcode}, 
            {"csv_header": 'country_5', "db_column": country},
            {"csv_header": 'current_5', "db_column": current, "boolean": True}]]},
    
    {"desc": "Address 5 from date (invalid dates allowed) (from_date must be in YYYY-MM-DD format)", "table": "Address_5",
        "fields": [[{"csv_header": 'from_date_5', "db_column": 'from_date'}],
            [{"csv_header": 'from_date_day_5', "db_column": 'from_date_day'}, 
            {"csv_header": 'from_date_month_5', "db_column": 'from_date_month'}, 
            {"csv_header": 'from_date_year_5', "db_column": 'from_date_year'}]]},
    
    {"desc": "Address 5 to date (invalid dates allowed) (to_date must be in YYYY-MM-DD format)", "table": "Address_5",
        "fields": [[{"csv_header": 'to_date_5', "db_column": 'to_date'}],
            [{"csv_header": 'to_date_day_5', "db_column": 'to_date_day'}, 
            {"csv_header": 'to_date_month_5', "db_column": 'to_date_month'}, 
            {"csv_header": 'to_date_year_5', "db_column": 'to_date_year'}]]},

    # PERSON TABLE
    {"desc": "Owner person's title", "table": "PublicPerson", "fields": [[{"csv_header": "title", "db_column": "title"}]]},

    {"desc": "Owner person's name", "table": "PublicPerson",
        "fields": [
            [{"csv_header": first_names, "db_column": first_names}, 
            {"csv_header": last_name, "db_column": last_name}], 
            [{"csv_header": full_name, "db_column": ""}]]},

    {"desc": "Owner person's email", "table": "PublicPerson", "fields": [[{"csv_header": "person_email", "db_column": "email"}]]},
    
    {"desc": "Owner person's phone number", "table": "PublicPerson", "fields": [[{"csv_header": "person_phone_number", "db_column": "phone_number"}]]},
    
    {"desc": "Owner person's phone number 2", "table": "PublicPerson", "fields": [[{"csv_header": "person_phone_number_2", "db_column": "phone_number_2"}]]},

    {"desc": "Remarks on the owner person", "table": "PublicPerson", 
        "fields": [[{"csv_header": "person_remarks", "db_column": "remarks"}]]},

    # COMPANY TABLE
    {"desc": "Owner company's name", "table": "Company", "fields": [[{"csv_header": "company_name", "db_column": "name"}]]}, 

    {"desc": "Owner company's email", "table": "Company", "fields": [[{"csv_header": "company_email", "db_column": "email"}]]},
    
    {"desc": "Owner company's phone number", "table": "Company", "fields": [[{"csv_header": "company_phone_number", "db_column": "phone_number"}]]},
    
    {"desc": "Owner company's phone number 2", "table": "Company", "fields": [[{"csv_header": "company_phone_number_2", "db_column": "phone_number_2"}]]},

    {"desc": "Remarks on the owner company", "table": "Company", 
        "fields": [[{"csv_header": "company_remarks", "db_column": "remarks"}]]},

    # GRAVEOWNER TABLE
    {"desc": "Ownership order (e.g. 1=1st owner, 2=2nd owner)", "table": "GraveOwner", 
        "fields": [[{"csv_header": ownership_order, "db_column": ownership_order}]]},
    
    {"desc": "Date became owner (invalid dates allowed) (owner_date must be in YYYY-MM-DD format)", "table": "GraveOwner",
        "fields": [[{"csv_header": owner_from_date, "db_column": owner_from_date}],
            [{"csv_header": owner_from_date_day, "db_column": owner_from_date_day}, 
            {"csv_header": owner_from_date_month, "db_column": owner_from_date_month}, 
            {"csv_header": owner_from_date_year, "db_column": owner_from_date_year}]]},
    
    {"desc": "Date ended being an owner (invalid dates allowed) (owner_date must be in YYYY-MM-DD format)", "table": "GraveOwner",
        "fields": [[{"csv_header": owner_to_date, "db_column": owner_to_date}],
            [{"csv_header": owner_to_date_day, "db_column": owner_to_date_day}, 
            {"csv_header": owner_to_date_month, "db_column": owner_to_date_month}, 
            {"csv_header": owner_to_date_year, "db_column": owner_to_date_year}]]},
    
    {"desc": "Active owner (default is true) (blank or yes/y/true/1 or no/n/false/0)", "table": "GraveOwner", 
        "fields": [[{"csv_header": "active_owner", "db_column": "active_owner", "boolean": True}]]},
    
    {"desc": "Remarks about grave owner", "table": "GraveOwner", 
        "fields": [[{"csv_header": "owner_remarks", "db_column": "remarks"}]]},
]

burialFields = [
    # ADDRESS TABLE
    {"desc": "Person's address", "table": "Address", 
        "fields": [[
            {"csv_header": first_line, "db_column": first_line}, 
            {"csv_header": second_line, "db_column": second_line},
            {"csv_header": town, "db_column": town}, 
            {"csv_header": county, "db_column": county},
            {"csv_header": postcode, "db_column": postcode}, 
            {"csv_header": country, "db_column": country}]]},

    # PERSON TABLE
    {"desc": "Person's title", "table": "Person", "fields": [[{"csv_header": "title", "db_column": "title"}]]},

    {"desc": "Person's name", "table": "Person",
        "fields": [
            [{"csv_header": first_names, "db_column": first_names}, 
            {"csv_header": last_name, "db_column": last_name}], 
            [{"csv_header": full_name, "db_column": ""}]]},
    
    {"desc": "Person's birth name", "table": "Person", 
        "fields": [[{"csv_header": "birth_name", "db_column": "birth_name"}]]},

    {"desc": "Person's other names", "table": "Person", 
        "fields": [[{"csv_header": "other_names", "db_column": "other_names"}]]},
    
    {"desc": "Person's birth date (invalid dates allowed) (birth_date must be in YYYY-MM-DD format)", "table": "Person",
        "fields": [[{"csv_header": birth_date, "db_column": birth_date}],
            [{"csv_header": birth_date_day, "db_column": impossible_date_day}, 
            {"csv_header": birth_date_month, "db_column": impossible_date_month}, 
            {"csv_header": birth_date_year, "db_column": impossible_date_year}]]},

    {"desc": "Person's gender", "table": "Person", 
        "fields": [[{"csv_header": "gender", "db_column": "gender"}]]},
    
    {"desc": "Person description", "table": "Person", 
        "fields": [[{"csv_header": "person_description", "db_column": "description"}]]},
    
    {"desc": "Person's profession", "table": "Person", 
        "fields": [[{"csv_header": profession, "db_column": profession}]]},

    # DEATH TABLE
    {"desc": "Memorial ID for linking to existing memorial feature", "table": "Death", 
        "fields": [[{"csv_header": memorial_id, "db_column": memorials}]]},

    {"desc": "Event relating to death", "table": "Death", 
        "fields": [[
            {"csv_header": event_name, "db_column": event_name},
            {"csv_header": event_description, "db_column": event_description}]]},

    {"desc": "Person's age", "table": "Death", 
        "fields": [[
            {"csv_header": "age_years", "db_column": "age_years"}, 
            {"csv_header": "age_months", "db_column": "age_months"},
            {"csv_header": "age_weeks", "db_column": "age_weeks"}, 
            {"csv_header": "age_days", "db_column": "age_days"},
            {"csv_header": "age_hours", "db_column": "age_hours"},
            {"csv_header": "age_minutes", "db_column": "age_minutes"}]]},

    {"desc": "Parish related to where the person was buried", "table": "Death", 
        "fields": [[{"csv_header": parish, "db_column": parish}]]},
        
    {"desc": "Religion", "table": "Death", 
        "fields": [[{"csv_header": religion, "db_column": religion}]]},
    
    {"desc": "Person's date of death (invalid dates allowed) (date_of_death must be in YYYY-MM-DD format)", "table": "Death",
        "fields": [[{"csv_header": date_of_death, "db_column": death_date}],
            [{"csv_header": date_of_death_day, "db_column": impossible_date_day}, 
            {"csv_header": date_of_death_month, "db_column": impossible_date_month}, 
            {"csv_header": date_of_death_year, "db_column": impossible_date_year}]]},
    
    {"desc": "Cause of death", "table": "Death", 
        "fields": [[{"csv_header": "cause_of_death", "db_column": "death_cause"}]]},
    
    # GRAVEPLOT TABLE
    {"desc": "Grave identifier (not all fields required, but included fields must be unique)", "table": "GravePlot", 
        "fields": [[
            {"csv_header": "grave_number", "db_column": "grave_number"}, 
            {"csv_header": "section", "db_column": "section"}, 
            {"csv_header": "subsection", "db_column": "subsection"}]]},

    # RESERVEDPLOT TABLE
    {"desc": "Reserved person (blank or yes/y/true/1 or no/n/false/0)", "table": "ReservedPlot", 
        "fields": [[{"csv_header": "reservation", "db_column": "", "boolean": True}]]},
    
    # BURIAL TABLE
    {"desc": "Serial number of entry in physical book", "table": "Burial", 
        "fields": [[{"csv_header": "burial_number", "db_column": "burial_number"}]]},
    
    {"desc": "Burial date (invalid dates allowed) (burial_date must be in YYYY-MM-DD format)", "table": "Burial",
        "fields": [[{"csv_header": burial_date, "db_column": burial_date}],
            [{"csv_header": burial_date_day, "db_column": impossible_date_day}, 
            {"csv_header": burial_date_month, "db_column": impossible_date_month}, 
            {"csv_header": burial_date_year, "db_column": impossible_date_year}]]},
    
    {"desc": "Order date (invalid dates allowed) (order_date must be in YYYY-MM-DD format)", "table": "Burial",
        "fields": [[{"csv_header": order_date, "db_column": order_date}],
            [{"csv_header": order_date_day, "db_column": impossible_order_date_day}, 
            {"csv_header": order_date_month, "db_column": impossible_order_date_month}, 
            {"csv_header": order_date_year, "db_column": impossible_order_date_year}]]},
    
    {"desc": "Cremated (blank or yes/y/true/1 or no/n/false/0)", "table": "Burial", 
        "fields": [[{"csv_header": "cremated", "db_column": "cremated", "boolean": True}]]},
    
    {"desc": "Cremation certificate number", "table": "Burial", 
        "fields": [[{"csv_header": "cremation_certificate_no", "db_column": "cremation_certificate_no"}]]},
    
    {"desc": "Cremation date (invalid dates allowed) (cremation_date must be in YYYY-MM-DD format)", "table": "Burial",
        "fields": [[{"csv_header": cremation_date, "db_column": cremation_date}],
            [{"csv_header": cremation_date_day, "db_column": impossible_cremation_date_day}, 
            {"csv_header": cremation_date_month, "db_column": impossible_cremation_date_month}, 
            {"csv_header": cremation_date_year, "db_column": impossible_cremation_date_year}]]},
    
    {"desc": "Interred (blank or yes/y/true/1 or no/n/false/0)", "table": "Burial", 
        "fields": [[{"csv_header": "interred", "db_column": "interred", "boolean": True}]]},
    
    {"desc": "Depth in ft/m/cm", "table": "Burial", 
        "fields": [[
            {"csv_header": "depth", "db_column": "depth"},
            {"csv_header": "depth_units", "db_column": "depth_units"}]]},

    {"desc": "Depth position", "table": "Burial", 
        "fields": [[{"csv_header": "depth_position", "db_column": "depth_position"}]]},

    {"desc": "Additional information not specified elsewhere", "table": "Burial", 
        "fields": [[{"csv_header": "burial_remarks", "db_column": "burial_remarks"}]]},
    
    {"desc": "Comments", "table": "Burial", 
        "fields": [[{"csv_header": "comments", "db_column": "user_remarks"}]]},
    
    {"desc": "Location or situation of the grave", "table": "Burial", 
        "fields": [[{"csv_header": "situation", "db_column": "situation"}]]},
    
    {"desc": "Register recording burial name/code", "table": "Burial", 
        "fields": [[{"csv_header": "register", "db_column": "register"}]]},
    
    {"desc": "Page number in register recording burial name/code", "table": "Burial", 
        "fields": [[{"csv_header": "register_page", "db_column": "register_page"}]]},
    
    {"desc": "Registration number", "table": "Burial", 
        "fields": [[{"csv_header": "registration_number", "db_column": "registration_number"}]]},
    
    # OFFICIAL TABLE
    {"desc": "Official's name", "table": "Official", 
        "fields": [[
            {"csv_header": official_title, "db_column": "title"},
            {"csv_header": official_first_names, "db_column": first_names},
            {"csv_header": official_last_name, "db_column": last_name}]]},

    # OFFICIALBURIALTYPE TABLE
    {"desc": "Official's type (e.g. 'Registrar', 'Ceremony performed by', 'Certificate issued by'", "table": "Burial_Official", 
        "fields": [[{"csv_header": official_type, "db_column": official_type}]]}
]
relationshipFields = [
    # FEATURESRELATIONSHIP TABLE
    {"desc": "Grave number for 1st feature (must be unique)", "table": "FeaturesRelationship", 
        "fields": [[{"csv_header": feature_1_id, "db_column": ""}]]},
    {"desc": "Grave number for 2nd feature (must be unique) (can contin multiple seperated by commas)", "table": "FeaturesRelationship", 
        "fields": [[{"csv_header": feature_2_id, "db_column": ""}]]},
    {"desc": "Relationship type (must be in main_relationshiptype", "table": "FeaturesRelationship", 
        "fields": [[{"csv_header": relationship, "db_column": relationship}]]}
]