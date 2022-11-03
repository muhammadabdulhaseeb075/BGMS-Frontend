import copy
import csv
import re
import traceback

from django.db import transaction
from django.db.models import Q

from bgsite import data_upload_dicts as dud
from bgsite.models import Memorial, Burial, DataUpload, Person, Address, Official, Burial_Official, Death, GravePlot, \
    Section, Subsection, GraveplotStatus, GraveplotState, GraveplotType, GraveOwner, MemorialGraveplot, FeaturesRelationship,\
    GraveDeed, ReservedPlot, ReservePlotState, GraveRef
from main.models import BurialOfficialType, Currency, RelationshipType, PublicPerson, Company, Address as PublicAddress, BurialGroundSite

# Note: I can't get this to work! Keep getting this error: psycopg2.ProgrammingError: relation "bgsite_person" does not exist
# https://stackoverflow.com/questions/51617322/relation-does-not-exist-with-django-uwsgi-spooler-function

# uwsgidecorators is only available on the server
#try:
#    from uwsgidecorators import spool
#except ImportError:
    # create dummy decorator
#    def spool(pass_arguments):
#        def real_decorator(function):
#            return function
#        return real_decorator

ERROR_MESSAGE = "{0}. Error in <b>file '{1}', row {2}, column {3}</b>: {4}"

#@spool(pass_arguments=True)
def _process_data_upload(files, data_upload_record):
    """
    Adds data from CSV file to the database.
    Nested atomic transactions are used so if the upload has errors, it will find all the errors and report back to user everything that needs fixed.
    Hence why every field is added in a seperate transaction.
    """

    grave_record_count = 0
    grave_ownership_record_count = 0
    burial_record_count = 0
    relation_record_count = 0
    error_report = []

    try:
        with transaction.atomic():
            # Everything in this transaction will be rolled back if there is an error. But only after every row has been processed. Hence we get a complete error report.

            for file_type in files:
                file = files[file_type]
                filedata = file.read().decode("latin1").splitlines()
                reader = csv.reader(filedata, dialect='excel', delimiter=',')

                available_fields = None
                header = None
                used_csv_headers = []

                if file_type == "grave":
                    available_fields = dud.graveFields
                elif file_type == "graveOwnership":
                    available_fields = dud.graveOwnershipFields
                elif file_type == "burial":
                    available_fields = dud.burialFields
                elif file_type == "relation":
                    available_fields = dud.relationshipFields

                for csv_row in reader:
                    if not csv_row:
                    # i.e. blank row
                        continue

                    row = []

                    # remove trailing and leading spaces
                    for value in csv_row:
                        row.append(value.strip())

                    if not header:
                        header = row

                        #Get all headers in CSV file and add to list used_csv_headers
                        for field_group in available_fields:
                            for fields in field_group["fields"]:
                                for field in fields:
                                    if field["csv_header"] in header:
                                        used_csv_headers.append(dict(field, **{"table": field_group["table"]}))

                        continue

                    row_dict = dict(zip(header, row))

                    if file_type == "grave":
                        grave_record_count += 1
                        process_grave_row(used_csv_headers, row_dict, error_report, grave_record_count, data_upload_record, file.name)
                    elif file_type == "graveOwnership":
                        grave_ownership_record_count += 1
                        process_grave_ownership_row(used_csv_headers, row_dict, error_report, grave_ownership_record_count, data_upload_record, file.name)
                    elif file_type == "burial":
                        burial_record_count += 1
                        process_burial_row(used_csv_headers, row_dict, error_report, burial_record_count, data_upload_record, file.name)
                    elif file_type == "relation":
                        relation_record_count += 1
                        process_relation_row(row_dict, error_report, relation_record_count, data_upload_record, file.name)

            if error_report:
                # If at least one error has been found, the whole transaction must fail
                raise Exception

            data_upload_record.status = "Successful"
            data_upload_record.record_count = grave_record_count + grave_ownership_record_count + burial_record_count + relation_record_count
            data_upload_record.save()
    except Exception:
        print(traceback.format_exc())
        data_upload_record.status = "Failed"
        data_upload_record.record_count = grave_record_count + grave_ownership_record_count + burial_record_count + relation_record_count
        data_upload_record.report = "\n".join(error_report)
        data_upload_record.save()

def process_grave_row(used_csv_headers, row_dict, error_report, record_count, data_upload_record, filename):

    current_table = None
    grave_plot_record = None
    duplicate_graveplot = False

    for used_csv_header in used_csv_headers:

        if used_csv_header["table"] is not current_table:
            # We have reached a new table and hence need to create new record
            current_table = used_csv_header["table"]
            new_record = None

            if current_table is "GravePlot":

                if row_dict.get(dud.feature_id):
                    # This will only update an existing feature. It will not create new.

                    graveplot = GravePlot.objects.filter(feature_id=row_dict.get(dud.feature_id))

                    if not graveplot:
                        error_report.append(ERROR_MESSAGE.format(len(error_report)+1, filename, record_count, dud.section, "This GravePlot feature ID cannot be found."))
                    else:
                        new_record = graveplot[0]

                section_field = None
                subsection_field = None

                if (not row_dict.get(dud.section)) and row_dict.get(dud.subsection):
                    # if we're going to have a subsection then we also need a section
                    error_report.append(ERROR_MESSAGE.format(len(error_report)+1, filename, record_count, dud.section, "Cannot have a subsection without a section."))
                    continue

                try:
                    with transaction.atomic():

                        if row_dict.get(dud.section):
                            try:
                                section_field = Section.objects.get(section_name=row_dict.get(dud.section))
                            except Exception:
                                section_field = Section(section_name=row_dict.get(dud.section), created_by=data_upload_record.created_by)
                                section_field.save()

                        if row_dict.get(dud.subsection):
                            try:
                                subsection_field = Subsection.objects.get(subsection_name=row_dict.get(dud.subsection), section=section_field)
                            except Exception:
                                subsection_field = Subsection(subsection_name=row_dict.get(dud.subsection), section=section_field, created_by=data_upload_record.created_by)
                                subsection_field.save()

                except Exception as e:
                    error_report.append(ERROR_MESSAGE.format(len(error_report)+1, filename, record_count, "section or subsection", str(e).strip()))
                    continue

                try:
                    with transaction.atomic():
                        grave_ref = GraveRef.objects.get_or_create_custom(grave_number=row_dict.get(dud.grave_number), section=section_field, subsection=subsection_field)

                        if new_record:
                            # feature id found so just need to update
                            new_record.graveref = grave_ref
                            new_record.save()
                        else:
                            # no feature id
                            new_record, created = GravePlot.objects.get_or_create(graveref=grave_ref)

                            if created:
                                new_record.data_upload = data_upload_record
                                new_record.save()
                            elif new_record.data_upload == data_upload_record:
                                # This is a duplicate graveplot in the csv file, hence only look at the memorial_id and skip everything else
                                duplicate_graveplot = True

                except Exception as e:
                    error_report.append(ERROR_MESSAGE.format(len(error_report)+1, filename, record_count, "grave_number, section or subsection", "These columns must be unique tp a graveplot."))
                    continue

                grave_plot_record = new_record

            elif current_table is "MemorialGraveplot":
                if row_dict.get(dud.memorial_id):
                    # Memorial must already exist. So find it and add it to the record.
                    memorial_record = Memorial.objects.filter(feature_id=row_dict.get(dud.memorial_id))

                    if memorial_record.exists():
                        # add existing memorial record
                        new_record, created = MemorialGraveplot.objects.get_or_create(memorial=memorial_record[0], graveplot=grave_plot_record)

                        # Check if user want persons linked as well. Default is true.
                        if (not dud.link_burials in row_dict) or process_boolean_field(row_dict, {'csv_header': dud.link_burials}, error_report, record_count, filename):
                            # link persons linked to graveplot to the memorial
                            burials = Burial.objects.filter(graveplot=grave_plot_record)

                            for burial in burials:
                                if burial.death:
                                    burial.death.add_memorial(memorial_record[0])
                    else:
                        # memorial not found
                        error_report.append(ERROR_MESSAGE.format(
                            len(error_report)+1, filename, record_count, dud.memorial_id,
                            "Memorial with Feature ID " + row_dict.get(dud.memorial_id) + " cannot be found."))

                # There's nothing more to add to this table. This is a linking table.
                continue

        # Exceptions
        try:
            with transaction.atomic():
                if "boolean" in used_csv_header and not process_boolean_field(row_dict, used_csv_header, error_report, record_count, filename):
                    continue

                if current_table is "GravePlot":

                    # ignore these field as they are needed when creating the row
                    if duplicate_graveplot or used_csv_header["csv_header"] is dud.grave_number or used_csv_header["csv_header"] is dud.section or used_csv_header["csv_header"] is dud.subsection:
                        continue

                    if used_csv_header["csv_header"] is dud.status and row_dict.get(dud.status):
                        try:
                            status_record = GraveplotStatus.objects.get(status=row_dict.get(dud.status))
                        except Exception:
                            status_record = GraveplotStatus(status=row_dict.get(dud.status), created_by=data_upload_record.created_by)
                            status_record.save()

                        new_record.status = status_record
                        new_record.save()
                        continue

                    elif used_csv_header["csv_header"] is dud.state and row_dict.get(dud.state):
                        try:
                            state_record = GraveplotState.objects.get(state=row_dict.get(dud.state))
                        except Exception:
                            state_record = GraveplotState(state=row_dict.get(dud.state), created_by=data_upload_record.created_by)
                            state_record.save()

                        new_record.state = state_record
                        new_record.save()
                        continue

                    elif used_csv_header["csv_header"] is "type" and row_dict.get("type"):
                        try:
                            type_record = GraveplotType.objects.get(type=row_dict.get("type"))
                        except Exception:
                            type_record = GraveplotType(type=row_dict.get("type"), created_by=data_upload_record.created_by)
                            type_record.save()

                        new_record.type = type_record
                        new_record.save()
                        continue

                elif current_table is "MemorialGraveplot":
                    # this is a linking table so there should never be any more data to add.
                    continue

        except Exception as e:
            error_report.append(ERROR_MESSAGE.format(len(error_report)+1, filename, record_count, used_csv_header["csv_header"], str(e).strip()))
            continue

        # Commit new record. Most fields will end up here
        new_record = data_upload_commit_single_field(new_record, used_csv_header["csv_header"], used_csv_header["db_column"], row_dict.get(used_csv_header["csv_header"]), error_report, record_count, filename)


def process_grave_ownership_row(used_csv_headers, row_dict, error_report, record_count, data_upload_record, filename):

    current_table = None

    ignore_address = False

    grave_deed = None
    address_records = []
    person_record = None
    company_record = None
    address_suffix = ''

    for used_csv_header in used_csv_headers:
        if used_csv_header["table"] is not current_table:
            # We have reached a new table and hence need to create new record
            current_table = used_csv_header["table"]
            new_record = None

            if current_table is "GraveDeed":

                # get linked graveplot if it exists
                graveplot, report = get_graveplot(row_dict.get(dud.grave_number), row_dict.get(dud.section), row_dict.get(dud.subsection), used_csv_headers)

                if not graveplot:
                    # graveplot has not been found
                    error_report.append(ERROR_MESSAGE.format(len(error_report)+1, filename, record_count, "grave_number, section and/or subsection", report))
                    break

                if row_dict.get(dud.deed_reference):
                    new_record, created = GraveDeed.objects.get_or_create(deed_reference=row_dict.get(dud.deed_reference), graveplot=graveplot)
                else:
                    new_record, created = GraveDeed.objects.get_or_create(deed_reference__isnull=True, graveplot=graveplot)

                if created:
                    new_record.data_upload = data_upload_record
                    new_record.save()

                grave_deed = new_record

            elif current_table.startswith("Address"):
                # There could be up to 5 different addresses

                address_suffix = current_table[-2:]

                if (row_dict.get(dud.first_line + address_suffix)
                        or row_dict.get(dud.second_line + address_suffix)
                        or row_dict.get(dud.town + address_suffix)
                        or row_dict.get(dud.county + address_suffix)
                        or row_dict.get(dud.postcode + address_suffix)
                        or row_dict.get(dud.country + address_suffix)):
                    new_record = PublicAddress.objects.create(first_line="", current=True)
                    address_records.append(new_record)
                    ignore_address = False
                else:
                    ignore_address = True

            elif current_table is "PublicPerson":
                new_record = PublicPerson.objects.create(from_data_upload=True)
                new_record.clients.add(BurialGroundSite.get_client())

                if address_records:
                    new_record.addresses.add(*address_records)

                new_record.save()
                person_record = new_record

            elif current_table is "Company":
                # ignore if no company name exists
                if row_dict.get('company_name'):
                    new_record = Company.objects.create(from_data_upload=True)
                    new_record.clients.add(BurialGroundSite.get_client())

                    if address_records:
                        new_record.addresses.add(*address_records)

                    new_record.save()

                    # if person data exists, link them to company rather than deed directly
                    if person_record:
                        new_record.persons.add(person_record)
                        new_record.save()

                    company_record = new_record

            elif current_table is "GraveOwner":

                # deed records are essential
                if not grave_deed:
                    error_report.append(ERROR_MESSAGE.format(len(error_report)+1, filename, record_count, used_csv_header["csv_header"], "Grave deed data is required."))
                    continue

                if company_record:
                    new_record = GraveOwner.objects.create(deed=grave_deed, owner=company_record, data_upload=data_upload_record)
                elif person_record:
                    new_record = GraveOwner.objects.create(deed=grave_deed, owner=person_record, data_upload=data_upload_record)
                else:
                    new_record = GraveOwner.objects.create(deed=grave_deed, data_upload=data_upload_record)

        # Exceptions
        try:
            with transaction.atomic():
                if "boolean" in used_csv_header and not process_boolean_field(row_dict, used_csv_header, error_report, record_count, filename):
                    continue

                if current_table.startswith("Address"):
                    if ignore_address:
                        continue
                    elif used_csv_header["csv_header"].startswith('from_date') and row_dict.get('from_date' + address_suffix):
                        new_record, valid = process_full_date(
                            row_dict.get('from_date' + address_suffix), new_record, 'from_date' + address_suffix, 'from_date_day', 'from_date_month', 'from_date_year',
                            error_report, record_count, filename, 'from_date_day', 'from_date_month', 'from_date_year')
                        if not valid:
                            # this date is invalid and should not be saved
                            continue
                    elif used_csv_header["csv_header"].startswith('to_date') and row_dict.get('to_date' + address_suffix):
                        new_record, valid = process_full_date(
                            row_dict.get('to_date' + address_suffix), new_record, 'to_date' + address_suffix, 'to_date_day', 'to_date_month', 'to_date_year',
                            error_report, record_count, filename, 'to_date_day', 'to_date_month', 'to_date_year')
                        if not valid:
                            # this date is invalid and should not be saved
                            continue

                elif current_table is "GraveOwner":

                    if used_csv_header["csv_header"] is dud.owner_from_date and row_dict.get(dud.owner_from_date):
                        new_record, valid = process_full_date(row_dict.get(dud.owner_from_date), new_record, dud.owner_from_date, dud.owner_from_date_day, dud.owner_from_date_month, dud.owner_from_date_year, error_report, record_count, filename, dud.owner_from_date_day, dud.owner_from_date_month, dud.owner_from_date_year)
                        if not valid:
                            # this date is invalid and should not be saved
                            continue
                    elif used_csv_header["csv_header"] is dud.owner_to_date and row_dict.get(dud.owner_to_date):
                        new_record, valid = process_full_date(row_dict.get(dud.owner_to_date), new_record, dud.owner_to_date, dud.owner_to_date_day, dud.owner_to_date_month, dud.owner_to_date_year, error_report, record_count, filename, dud.owner_to_date_day, dud.owner_to_date_month, dud.owner_to_date_year)
                        if not valid:
                            # this date is invalid and should not be saved
                            continue
                    elif used_csv_header["csv_header"] is dud.grave_number or used_csv_header["csv_header"] is dud.section or used_csv_header["csv_header"] is dud.subsection:
                        # don't need to add these fields into this table (will already have been done when creating the record)
                        continue

                elif current_table is "PublicPerson":
                    if used_csv_header["csv_header"] is dud.full_name and row_dict.get(dud.full_name):
                        new_record = split_full_name(row_dict.get(used_csv_header["csv_header"]), new_record)
                        continue

                elif current_table is "GraveDeed":
                    if used_csv_header["csv_header"] is dud.purchase_date and row_dict.get(dud.purchase_date):
                        new_record, valid = process_full_date(row_dict.get(dud.purchase_date), new_record, dud.purchase_date, dud.purchase_date_day, dud.purchase_date_month, dud.purchase_date_year, error_report, record_count, filename, dud.purchase_date_day, dud.purchase_date_month, dud.purchase_date_year)
                        if not valid:
                            # this date is invalid and should not be saved
                            continue

                    elif used_csv_header["csv_header"] is dud.cost_currency and row_dict.get(dud.cost_currency):
                        currency_type = None
                        try:
                            currency_type = Currency.objects.get(name=row_dict.get(dud.cost_currency))
                        except Exception:
                            currency_type = None
                            error_report.append(ERROR_MESSAGE.format(len(error_report)+1, filename, record_count, dud.memorial_id, "Currency type does not exist. Do you need to add it to the Currency table?"))

                        new_record.cost_currency = currency_type
                        new_record.save()
                        continue

                    elif used_csv_header["csv_header"] is dud.cost and row_dict.get(dud.cost):
                        # cost gets split into seperate fields
                        individual_number_strings = map(int, re.findall(r"\d+", row_dict.get(dud.cost)))
                        individual_numbers = [int(x) for x in individual_number_strings]

                        if len(individual_numbers) > 4 or (currency_type and len(individual_numbers) > 2 and not currency_type.subunit2_name):
                            error_report.append(ERROR_MESSAGE.format(len(error_report)+1, filename, record_count, dud.memorial_id, "Cost is not in the correct format."))
                        elif individual_numbers:
                            new_record.cost_unit = individual_numbers[0]

                            if len(individual_numbers) > 1:
                                new_record.cost_subunit = individual_numbers[1]
                            else:
                                new_record.cost_subunit = None

                            if len(individual_numbers) > 3:
                                # last unit can be a decimal e.g. half penny
                                new_record.cost_subunit2 = float(str(individual_numbers[2])+"."+str(individual_numbers[3]))
                            elif len(individual_numbers) > 2:
                                new_record.cost_subunit2 = individual_numbers[2]
                            else:
                                new_record.cost_subunit2 = None
                        else:
                            new_record.cost_unit = None

                        new_record.save()
                        continue

                elif (current_table is "Company" and not company_record) or (current_table is "PublicPerson" and not person_record):
                    continue

        except Exception as e:
            error_report.append(ERROR_MESSAGE.format(len(error_report)+1, filename, record_count, used_csv_header["csv_header"], str(e).strip()))
            continue

        # Commit new record. Most fields will end up here
        new_record = data_upload_commit_single_field(new_record, used_csv_header["csv_header"], used_csv_header["db_column"], row_dict.get(used_csv_header["csv_header"]), error_report, record_count, filename)

def process_burial_row(used_csv_headers, row_dict, error_report, record_count, data_upload_record, filename):

    current_table = None

    ignore_address = False
    ignore_official = False

    this_is_a_reservation = False

    address_record = None
    person_record = None
    death_record = None
    burial_record = None
    official_record = None
    burial_official_record = None

    for used_csv_header in used_csv_headers:

        if current_table is "Burial" and this_is_a_reservation:
            # ignore burial table is this is a reservation
            continue

        if used_csv_header["table"] is not current_table:
            # We have reached a new table and hence need to create new record
            current_table = used_csv_header["table"]
            new_record = None

            if current_table is "Address":
                if (row_dict.get(dud.first_line) or row_dict.get(dud.second_line) or row_dict.get(dud.town) or row_dict.get(dud.county) or row_dict.get(dud.postcode) or row_dict.get(dud.country)):
                    new_record = Address(first_line="")
                    new_record.save()
                    address_record = new_record
                else:
                    ignore_address = True

            elif current_table is "Person":
                new_record = Person(data_upload=data_upload_record)

                if address_record:
                    new_record.residence_address = address_record

                new_record.save()

                person_record = new_record

            elif current_table is "Death":
                if not person_record:
                    # death record needs a person record
                    person_record = Person.objects.create()

                new_record = Death(person=person_record)

                if address_record:
                    new_record.address = address_record

                new_record.save()

                death_record = new_record

            elif current_table is "ReservedPlot":
                # if current field is 'reservation' and field contains a value and the value is truthy
                if used_csv_header["csv_header"] is 'reservation' and row_dict.get('reservation') and process_boolean_field(row_dict, used_csv_header, error_report, record_count, filename) and row_dict.get('reservation'):

                    this_is_a_reservation = True

                    if not person_record:
                        # no person fields have been included
                        error_report.append(ERROR_MESSAGE.format(len(error_report)+1, filename, record_count, "reservation", "No 'person' fields have been included."))

                    graveplot = None

                    try:
                        # get linked graveplot if it exists
                        graveplot, report = get_graveplot(row_dict.get(dud.grave_number), row_dict.get(dud.section), row_dict.get(dud.subsection), used_csv_headers)

                        if not graveplot:
                            raise Exception
                    except Exception as e:
                        print(traceback.format_exc())
                        # graveplot has not been found
                        error_report.append(ERROR_MESSAGE.format(len(error_report)+1, filename, record_count, "grave_number, section and/or subsection", report))

                    new_record = ReservedPlot(person=person_record, grave_plot=graveplot, state=ReservePlotState.objects.get(state='reserved'))
                    new_record.save()

            elif current_table is "Burial":
                if not this_is_a_reservation:
                    if not death_record:
                        if not person_record:
                            # burial record needs a death record
                            person_record = Person.objects.create()

                        # burial record needs a death record
                        death_record = Death.objects.create(person=person_record)

                    graveplot = None

                    if row_dict.get(dud.grave_number):
                        # get linked graveplot if it exists
                        graveplot, report = get_graveplot(row_dict.get(dud.grave_number), row_dict.get(dud.section), row_dict.get(dud.subsection), used_csv_headers)

                        if not graveplot:
                            # graveplot has not been found
                            error_report.append(ERROR_MESSAGE.format(len(error_report)+1, filename, record_count, "grave_number, section and/or subsection", report))

                    new_record = Burial(death=death_record, graveplot=graveplot)
                    new_record.save()

                    burial_record = new_record

                else:
                    # ignore burial table is this is a reservation
                    continue

            elif current_table is "Official":
                # See if an official already exists
                # Note: we could use get_or_create, but I want to add the fields seperately for error reporting
                if row_dict.get(dud.official_title):
                    official_record = Official.objects.filter(title=row_dict.get(dud.official_title))
                else:
                    official_record = Official.objects.filter(Q(title__isnull=True) | Q(title=""))

                if row_dict.get(dud.official_first_names):
                    official_record = Official.objects.filter(first_names=row_dict.get(dud.official_first_names))
                else:
                    official_record = Official.objects.filter(Q(first_names__isnull=True) | Q(first_names=""))

                if row_dict.get(dud.official_last_name):
                    official_record = Official.objects.filter(last_name=row_dict.get(dud.official_last_name))
                else:
                    official_record = Official.objects.filter(Q(last_name__isnull=True) | Q(last_name=""))

                if official_record:
                    new_record = official_record[0]
                    ignore_official = True

                else:
                    new_record = Official()

                new_record.save()

                official_record = new_record

                burial_official_record = Burial_Official(official=official_record, burial=burial_record)
                burial_official_record.save()

            elif current_table is "Burial_Official":
                if not burial_official_record:
                    continue
                else:
                    new_record = burial_official_record

        # Exceptions
        try:
            with transaction.atomic():

                if current_table is "ReservedPlot" or (
                        "boolean" in used_csv_header and not process_boolean_field(row_dict, used_csv_header, error_report, record_count, filename)):
                    continue

                if current_table is "Address":
                    if ignore_address:
                        continue

                elif current_table is "Burial":
                    if ignore_official:
                        continue

                    if used_csv_header["csv_header"] is dud.burial_date and row_dict.get(dud.burial_date):
                        new_record, valid = process_full_date(row_dict.get(dud.burial_date), new_record, dud.burial_date, dud.burial_date_day, dud.burial_date_month, dud.burial_date_year, error_report, record_count, filename)
                        if not valid:
                            # this date is invalid and should not be saved
                            continue

                    elif used_csv_header["csv_header"] is dud.order_date and row_dict.get(dud.order_date):
                        new_record, valid = process_full_date(row_dict.get(dud.order_date), new_record, dud.order_date, dud.order_date_day, dud.order_date_month, dud.order_date_year, error_report, record_count, filename, dud.impossible_order_date_day, dud.impossible_order_date_month, dud.impossible_order_date_year)
                        if not valid:
                            # this date is invalid and should not be saved
                            continue

                    elif used_csv_header["csv_header"] is dud.cremation_date and row_dict.get(dud.cremation_date):
                        new_record, valid = process_full_date(row_dict.get(dud.cremation_date), new_record, dud.cremation_date, dud.cremation_date_day, dud.cremation_date_month, dud.cremation_date_year, error_report, record_count, filename, dud.impossible_cremation_date_day, dud.impossible_cremation_date_month, dud.impossible_cremation_date_year)
                        if not valid:
                            # this date is invalid and should not be saved
                            continue

                elif current_table is "GravePlot":
                    continue

                elif current_table is "Person":

                    if used_csv_header["csv_header"] is dud.birth_date and row_dict.get(dud.birth_date):
                        new_record, valid = process_full_date(row_dict.get(dud.birth_date), new_record, dud.birth_date, dud.birth_date_day, dud.birth_date_month, dud.birth_date_year, error_report, record_count, filename)
                        if not valid:
                            # this date is invalid and should not be saved
                            continue

                    elif used_csv_header["csv_header"] is dud.full_name and row_dict.get(dud.full_name):
                        new_record = split_full_name(row_dict.get(used_csv_header["csv_header"]), new_record)
                        continue
                    elif used_csv_header["csv_header"] is dud.profession and row_dict.get(dud.profession):
                        # profession is not a foreign key
                        existing_profession = dud.profession

                        if existing_profession:
                            row_dict[dud.profession] = existing_profession
                        else:
                            new_profession = dud.profession
                            new_profession.save()
                            row_dict[dud.profession] = new_profession

                elif current_table is "Death":

                    if used_csv_header["csv_header"] is dud.date_of_death and row_dict.get(dud.date_of_death):
                        new_record, valid = process_full_date(row_dict.get(dud.date_of_death), new_record, dud.date_of_death, dud.date_of_death_day, dud.date_of_death_month, dud.date_of_death_year, error_report, record_count, filename)
                        if not valid:
                            # this date is invalid and should not be saved
                            continue

                    elif used_csv_header["csv_header"] is dud.parish and row_dict.get(dud.parish):
                        new_record.add_parish(row_dict.get(dud.parish))
                        new_record.save()
                        continue

                    elif (used_csv_header["csv_header"] is dud.event_name and row_dict.get(dud.event_name)) or used_csv_header["csv_header"] is dud.event_description and row_dict.get(dud.event_description):
                        # create a new event if needed
                        name = None
                        description = None

                        if used_csv_header["csv_header"] is dud.event_name and row_dict.get(dud.event_name):
                            #check if a description exists and if so, wait for that
                            if row_dict.get(dud.event_description):
                                continue
                            else:
                                name = row_dict.get(dud.event_name)

                        elif used_csv_header["csv_header"] is dud.event_description and row_dict.get(dud.event_description):
                            #check if a name exists and if so, use it
                            if row_dict.get(dud.event_name):
                                name = row_dict.get(dud.event_name)

                            description = row_dict.get(dud.event_description)

                        new_record.add_event(name, description)
                        new_record.save()
                        continue

                    elif used_csv_header["csv_header"] is dud.religion and row_dict.get(dud.religion):
                        new_record.add_religion(row_dict.get(dud.religion))
                        new_record.save()
                        continue

                    elif used_csv_header["csv_header"] is dud.memorial_id:
                        if row_dict.get(dud.memorial_id):
                            # Memorial must already exist. So find it and add it to the record.
                            memorial_record = Memorial.objects.filter(feature_id=row_dict.get(dud.memorial_id))

                            if memorial_record:
                                # add existing memorial record
                                new_record = data_upload_commit_single_field(new_record, dud.memorial_id, dud.memorials, memorial_record, error_report, record_count, filename)
                            else:
                                # memorial not found
                                error_report.append(ERROR_MESSAGE.format(len(error_report)+1, filename, record_count, dud.memorial_id, "Memorial with Feature ID " + row_dict.get(dud.memorial_id) + " cannot be found."))

                        continue

                elif current_table is "Burial_Official" and used_csv_header["csv_header"] is dud.official_type and row_dict.get(dud.official_type):
                    # This table contains burial_official_type (foreign key) and official_type. I don't know why.
                    # Need to search for the foreign key and return error if it is not found or add it to Burial_Official if it is found.
                    burial_official_type_record = BurialOfficialType.objects.filter(official_type=row_dict.get(dud.official_type))

                    if not burial_official_type_record:
                        error_report.append(ERROR_MESSAGE.format(len(error_report)+1, filename, record_count, used_csv_header["csv_header"], "The official type '" + row_dict.get(dud.official_type) + "' is not recognised."))
                        continue
                    else:
                        new_record = data_upload_commit_single_field(new_record, "burial_official_type", "burial_official_type", burial_official_type_record[0], error_report, record_count, filename)
                        # This also saves the same data to official_type

        except Exception as e:
            error_report.append(ERROR_MESSAGE.format(len(error_report)+1, filename, record_count, used_csv_header["csv_header"], str(e).strip()))
            continue

        # Commit new record. Most fields will end up here
        new_record = data_upload_commit_single_field(new_record, used_csv_header["csv_header"], used_csv_header["db_column"], row_dict.get(used_csv_header["csv_header"]), error_report, record_count, filename)


def process_relation_row(row_dict, error_report, record_count, data_upload_record, filename):

    if row_dict.get(dud.feature_1_id) and row_dict.get(dud.feature_2_id):
        # both of these column must be included and valid

        # feature2 gets split into seperate features
        individual_feature2_ids = row_dict.get(dud.feature_2_id).split(",")
        # remove whitespace
        individual_feature2_ids = [x.strip() for x in individual_feature2_ids]

        for feature2_id in individual_feature2_ids:

            try:
                grave_ref = GraveRef.objects.get(grave_number=row_dict.get(dud.feature_1_id), section=None, subsection=None)
                feature1 = GravePlot.objects.filter(graveref=grave_ref)[0]
            except Exception:
                feature1 = None
                error_report.append(ERROR_MESSAGE.format(len(error_report)+1, filename, record_count, dud.feature_1_id, "Feature 1 cannot be found."))

            try:
                grave_ref = GraveRef.objects.get(grave_number=row_dict.get(dud.feature2_id), section=None, subsection=None)
                feature2 = GravePlot.objects.filter(graveref=grave_ref)[0]
            except Exception:
                feature2 = None
                error_report.append(ERROR_MESSAGE.format(len(error_report)+1, filename, record_count, dud.feature_2_id, "Feature 2 (" + feature2_id + ") cannot be found."))

            if feature1 and feature2:
                try:
                    with transaction.atomic():
                        new_record = FeaturesRelationship(feature_1_content_object=feature1, feature_2_content_object=feature2, data_upload=data_upload_record)

                        if row_dict.get(dud.relationship):
                            # find the relationship record
                            try:
                                relationship_type = RelationshipType.objects.get(type=row_dict.get(dud.relationship))
                            except Exception:
                                relationship_type = None
                                error_report.append(ERROR_MESSAGE.format(len(error_report)+1, filename, record_count, dud.relationship, "Relationship type does not exist. Do you need to add it to the RelationshipType table?"))

                            new_record.relationship = relationship_type
                        new_record.save()
                except Exception as e:
                    error_report.append(ERROR_MESSAGE.format(len(error_report)+1, filename, record_count, dud.feature_1_id + " or " + dud.feature_2_id + " or " + dud.relationship, str(e).strip()))
    else:
        error_report.append(ERROR_MESSAGE.format(len(error_report)+1, filename, record_count, dud.feature_1_id + " & " + dud.feature_2_id, "Both 'feature_1_id' and 'feature_2_id' are compulsory."))


# Commits a single field to the database. If it fails it rolls back the transaction and writes to error_report.
def data_upload_commit_single_field(record, field_csv, field_db, value, error_report, record_count, filename):
    """ Commit a single field to the database """

    if type(value) != bool and (not field_db.startswith("first_line")) and (not value or value == ''):
        # Blank csv fields are read as empty strings. This will make them null.
        # first_line is exception as it is not null but can be blank.
        value = None

    try:
        with transaction.atomic():
            modified_record = copy.copy(record)
            setattr(modified_record, field_db, value)
            modified_record.save()
            return modified_record
    except Exception as e:
        error_report.append(ERROR_MESSAGE.format(len(error_report)+1, filename, record_count, field_csv, str(e).strip()))
        return record

def process_full_date(input_date, new_record, date_field_csv, day_field, month_field, year_field, error_report, record_count, filename, impossible_day_field=dud.impossible_date_day, impossible_month_field=dud.impossible_date_month, impossible_year_field=dud.impossible_date_year):
    """
    Produces error if date is in wrong format.
    Splits date up and saves in seperate fields.
    Model will use seperate date fields to populate full date and impossible date boolean

    True: if valid date that still needs saved.
    False: if invalid date that may have a modified version saved.
    """

    return_value = True

    try:
        year, month, day = input_date.split('-')
    except Exception:
        error_report.append(ERROR_MESSAGE.format(len(error_report)+1, filename, record_count, date_field_csv, "Date is in the wrong format. It must be formatted as (yyyy-mm-dd)."))
        return [new_record, False]

    new_record = data_upload_commit_single_field(new_record, year_field, impossible_year_field, year, error_report, record_count, filename)
    new_record = data_upload_commit_single_field(new_record, month_field, impossible_month_field, month, error_report, record_count, filename)
    new_record = data_upload_commit_single_field(new_record, day_field, impossible_day_field, day, error_report, record_count, filename)

    return [new_record, return_value]

def process_boolean_field(row_dict, used_csv_header, error_report, record_count, filename):
    b_value = row_dict[used_csv_header["csv_header"]]

    if b_value and type(b_value) is not bool:
        b_value = b_value.lower()
        if b_value == "yes" or b_value == "y" or b_value == "true" or b_value == "1":
            row_dict[used_csv_header["csv_header"]] = True
        elif b_value == "no" or b_value == "n" or b_value == "false" or b_value == "0":
            row_dict[used_csv_header["csv_header"]] = False
        else:
            error_report.append(ERROR_MESSAGE.format(len(error_report)+1, filename, record_count, used_csv_header["csv_header"], "Value must be yes/y/true/1 or no/n/false/0."))
            return False
        return True

def get_graveplot(grave_number, section, subsection, used_csv_headers):
    graveplot = None
    report = None
    include_section = any(d['csv_header'] == dud.section for d in used_csv_headers)
    include_subection = any(d['csv_header'] == dud.subsection for d in used_csv_headers)
    grave_ref = None

    # need to include section
    if grave_number and include_section:
        # if section is not None then find record
        if section:
            try:
                section_record = Section.objects.get(section_name=section)
            except Exception:
                return [None, "Section has not been found"]
        else:
            section_record = None

        # need to include subection
        if include_subection:
            # if subsection is not None then find record
            if subsection:
                try:
                    subsection_record = Subsection.objects.get(subsection_name=subsection, section=section_record)
                except Exception:
                    return [None, "Subsection has not been found"]
            else:
                subsection_record = None

            grave_ref = GraveRef.objects.filter(grave_number=grave_number, section=section_record, subsection=subsection_record)
        else:
            grave_ref = GraveRef.objects.filter(grave_number=grave_number, section=section_record, subsection=None)
    elif grave_number:
        grave_ref = GraveRef.objects.filter(grave_number=grave_number, section=None, subsection=None)

    if grave_ref and grave_ref.exists():
        graveplot = GravePlot.objects.filter(graveref=grave_ref[0])

        if not graveplot.exists():
            # graveplot has not been found
            graveplot = None
            report = "Graveplot has not been found."
        else:
            graveplot = graveplot[0]
    else:
        report = "Grave reference has not been found."

    return [graveplot, report]

def split_full_name(fullname, new_record):
    """ Full_name must be split up """

    name_array = fullname.rsplit(' ', 1)

    modified_record = copy.copy(new_record)

    if len(name_array) is 2:
        modified_record.first_names = name_array[0]
        modified_record.last_name = name_array[1]
    else:
        modified_record.last_name = name_array[0]

    modified_record.save()
    return modified_record

#@spool(pass_arguments=True)
def _process_delete_data_upload(data_upload_record):
    """
    Deletes all records created during specified data upload.
    Atomic transaction is used so if there is an error nothing will be deleted.
    """

    try:
        newdata_upload_record = DataUpload(
            file_name=data_upload_record.file_name, status="Deleted", created_by=data_upload_record.created_by, record_count=data_upload_record.record_count)

        with transaction.atomic():
            # Everything in this transaction will be rolled back if there is an error.

            # Cascading delete means all data that was added in this upload will be deleted
            data_upload_record.delete()

        newdata_upload_record.save()
        newdata_upload_record.date = data_upload_record.date
        newdata_upload_record.save()

    except Exception:
        print(traceback.format_exc())
        data_upload_record.status = "Delete Failed"
        data_upload_record.save()
