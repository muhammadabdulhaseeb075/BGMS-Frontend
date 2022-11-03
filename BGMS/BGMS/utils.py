import calendar
import datetime
import uuid

from os.path import os

from django.conf import settings
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from mail_templated import send_mail

def get_and_clean_temp_dir(tenant_name):

    root_temp_dir = getattr(settings, 'TEMP_FILES_UPLOAD_PATH')
    timestamp = datetime.datetime.now().strftime('%y%m%d')
    unique_id = str(uuid.uuid4())

    temp_dir = os.path.join(root_temp_dir, tenant_name, timestamp + '-' + unique_id, '')

    # If directory exists clear it out, otherwise create it
    if os.path.isdir(temp_dir):
        for the_file in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, the_file)
            print(file_path)
            try:
                os.remove(file_path)
            except:
                print('Unable to delete old files')
    else:
        os.makedirs(temp_dir)

    return temp_dir


#TODO: Circular reference with def verify_contents(file), better to split in different apps.
def verify_contents(file):
    """
    Checks that the file-upload field data contains a valid image (GIF, JPG,
    PNG, possibly others -- whatever the Python Imaging Library supports).
    TODO: Change this validation when django supports ImageField multiple input
    """
    # import pdb; pdb.set_trace()
    content_type = file.content_type.split('/')[0]
    if content_type in settings.CONTENT_TYPES:
        file_type = file.content_type.split('/')[1]
        if file_type in settings.FILE_TYPES:
            if file.size > settings.MAX_UPLOAD_SIZE:
                return 'File exceed maximum upload file size'
            else:
                from PIL import Image
                try:
                    # load() could spot a truncated JPEG, but it loads the entire
                    # image in memory
                    # import pdb; pdb.set_trace()
                    image = Image.open(file.file)
                    # fullsize_image = PILImage.open(image_file.file)
                    # verify() must be called immediately after the constructor.
                    image.verify()
                except Exception:
                    # Pillow doesn't recognize it as an image.
                    return 'Upload a valid image. The file '+ file.name +' you uploaded was either not an image or a corrupted image.'

        else:
            return 'File type is not supported'
    else:
        return 'File type is not supported'
    return ''


def email_ag_admin(subject, template, extra_context={}):
    """
    Sends an email to Admin.
    subject: String
    template: url to the .tpl File
    extra_context: Dictionary with extra context used by the template
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = settings.EMAIL_AG_ADMIN
    context_basic = {'username': 'AG Admin', 'subject_text': subject}
    context_dict = context_basic.copy()
    context_dict.update(extra_context)

    #Send HTML mail using django templates
    send_mail(template, context_dict, from_email, recipient_list)

def email_non_user(email, subject, template, extra_context={}):
    """
    Sends an email to Admin.
    email: Email account to send msg
    subject: String
    template: url to the .tpl File
    extra_context: Dictionary with extra context used by the template
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    context_basic = {'username': '', 'subject_text': subject}
    context_dict = context_basic.copy()
    context_dict.update(extra_context)

    #Send HTML mail using django templates
    send_mail(template, context_dict, from_email, recipient_list)


def password_reset_notify(user_name, user_email, auth, message):
    """
    Sends a basic notification email to a given users password authorizer.
    user: the email address of the user who requested reset.
    auth: the email address of the person who authorizes their reset link.
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    context = {'username': 'Administrator',
                'subject_text': 'Password Reset Notification',
                'user_name': user_name if user_name else 'A user',
                'user_email': user_email,
                'message': message}

    template = "mail_templated/pw_reset_notify.tpl"

    #Send HTML mail using django templates
    send_mail(template, context, from_email, auth)


def date_elements_to_full_date(day, month, year):
    """
    Takes three date elements a puts them into a date field.
    If date elelments do not form a valid date, a similar, valid date is created
    and is marked as being an impossible date.
    """

    impossible_date = False

    # fields must be string rather than integers
    if day and isinstance(day, int):
        day = str(day)
    if month and isinstance(month, int):
        month = str(month)
    if year and isinstance(year, int):
        year = str(year)

    # if this is a non existant date
    if ((not day or (str.isdigit(day) and int(day) == 0)) 
    and (not month or (str.isdigit(month) and int(month) == 0)) 
    and (not year or (str.isdigit(year) and int(year) == 0))):
        return [None, impossible_date]

    # if there is a missing day or month substitute it with a 1
    if not day or not day.isdigit() or int(day) == 0:
        day = 1
        impossible_date = True
    else:
        day = int(day)

    if not month or not month.isdigit() or int(month) == 0:
        month = 1
        impossible_date = True
    else:
        month = int(month)
        # if the date doesn't match the month, set to max
        if (month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12) and day > 31:
            day = 31
            impossible_date = True
        elif (month == 4 or month == 6 or month == 9 or month == 11) and day > 30:
            day = 30
            impossible_date = True
        elif month == 2 and day > 29 and year and calendar.isleap(int(year)):
            day = 29
            impossible_date = True
        elif month == 2 and day > 28 and year and not calendar.isleap(int(year)):
            day = 28
            impossible_date = True
    
    if not year:
        year = 1
        impossible_date = True
        
    return [datetime.datetime(year=int(year), month=month, day=day), impossible_date]

""" Search functions """

def scorer(match, db_value):
    """Custom scorer that returns a tuple of (match_score, sorting_score).
    match_score is used for score_cutoff, and sorting_score is used to order the list."""
    db_value = db_value.strip().strip('-')
    match_score = fuzz.QRatio(match, db_value)
    sorting_score = match_score
    if (match_score<100) and ((' ' in db_value) or ('-'in db_value)):
        whitspace_list = []
        if (' ' in db_value) and ('-'in db_value):
            hyphen_list = db_value.split('-')
            for string in hyphen_list:
                whitspace_list.extend(string.split())
        elif(' ' in db_value):
            whitspace_list = db_value.split()
        elif('-'in db_value):
            whitspace_list = db_value.split('-')
        for string in whitspace_list:
            temp_ratio = fuzz.QRatio(match, string)
            if temp_ratio>match_score:
                match_score = temp_ratio
                sorting_score = temp_ratio-0.01 * (whitspace_list.index(string)+1)
    return (match_score, sorting_score)

def sort_list_by_score(searched_list, key_list):
    """Returns list with accumulate scores for the same person from the fuzzy search between two fuzzy results"""
    # sorting the combined list by person id

    def sort_key(result):
        return_key = []
        for key in key_list:
            return_key.append(result[0][key])
        return return_key

    searched_list.sort(key=lambda result:(sort_key(result)))
    sorted_list = []
    previous_result = None
    for current_result in searched_list:
        add_result = True
        if previous_result is not None:
            add_result = False
            for key in key_list:
                if current_result[0][key] != previous_result[0][key]:
                    add_result = True
                    break

        if not add_result:
            # update previous person's score in sorted_list
            previous_result = sorted_list.pop()
            updated_score = (previous_result[1][0] + current_result[1][0],
                                                    previous_result[1][1] + current_result[1][1])
            sorted_list.append((previous_result[0], updated_score))
            # update previous_result
            previous_result = (previous_result[0], updated_score)
        else:
            # add person and score to sorted_list
            sorted_list.append(current_result)
            # update previous_result
            previous_result = current_result
    # sort result by the updated scores
    sorted_list.sort(key=(lambda tup: tup[1][1]), reverse=True)
    return sorted_list

def fuzzy_search(match, key, searched_list):
    """DRY method to execute basic fuzzy search"""
    return process.extract(match, searched_list, scorer=scorer, processor=(lambda person:person[key] if person[key] else ''), limit=len(searched_list))

def fuzzy_search_fullname(first_names, last_name, queryresult, fuzzy_value, key_list):
    """Returns a list of persons based on fuzzy matching of first_name, last_name returning people with the higher score as a whole"""
    persons_last_name = []
    fuzziness = fuzzy_value

    if fuzziness == 100:
        """ If fuzziness is 100 then do an exact filter """
        if(last_name):
            last_name = last_name.strip().strip("'")
            queryresult = queryresult.filter(last_name__icontains=last_name)

        if(first_names):
            first_names = first_names.strip().strip("'")
            queryresult = queryresult.filter(first_names__icontains=first_names)

        return queryresult
    else:
        """ If fuzziness is less than 100 then do fuzzy search """
        if(last_name):
            last_name = last_name.strip()
        # for double-barrel names in search, increase matching score - currently increasing from 60% to 75%
            fuzziness = fuzzy_value
            if (' ' in last_name) or ('-'in last_name):
                fuzziness = fuzzy_value/1.25
            persons_last_name = fuzzy_search(last_name, 'last_name', queryresult)
            persons_last_name = list(filter(lambda person_score: person_score[1][0] >= fuzziness, persons_last_name))
            if(first_names):
                #set the queryset for first name search as the last names search result
                queryresult = [person[0] for person in persons_last_name]

        if(first_names):
            first_names = first_names.strip()
        # for double-barrell names in search, increase matching score - currently increasing from 60% to 75%
            fuzziness = fuzzy_value
            if (' ' in first_names) or ('-'in first_names):
                fuzziness = fuzzy_value/1.25
            persons_first_name = fuzzy_search(first_names, 'first_names', queryresult)
            persons_first_name = list(filter(lambda person_score: person_score[1][0] >= fuzziness, persons_first_name))
            # multipliers to score to increase weighting of last name
            if(last_name):
                persons_first_name = [(person[0], (person[1][0]*0.45, person[1][1]*0.45)) for person in persons_first_name]
                persons_last_name = [(person[0], (person[1][0]*0.55, person[1][1]*0.55)) for person in persons_last_name]
            persons_last_name.extend(persons_first_name)

        sorted_result = sort_list_by_score(persons_last_name, key_list)
        sorted_result = list(filter(lambda person_score: person_score[1][0] >= fuzziness, sorted_result))
        #print(sorted_result)
        result = [person[0] for person in sorted_result]

    return result

def rename_queryset_value(values_queryset, name_dict):
    """Renames the fields (called by old_name) in the values queryset to new_name"""
    for values_dict in values_queryset:
        for old_name, new_name in name_dict.items():
            if old_name in values_dict:
                values_dict[new_name] = values_dict.pop(old_name)
    return values_queryset


def get_display_name_from_firstnames_lastname(first_names, last_name):
    ''' Formats first names and last name into single string.
    -All first names after the first are abbreviated to initial.
    -Last name is upper case. '''

    return_name = ''

    if not first_names and not last_name:
        return 'UNKNOWN'

    if first_names:
        first_names_list = first_names.split()

        return_name = first_names_list[0]

        if len(first_names_list) > 1:
            # if more than one name, shorten to initial only
            first_names_iter = iter(first_names_list)
            next(first_names_iter)
            for first_name in first_names_iter:
                return_name += ' ' + first_name[:1]

        if last_name:
            return_name += ' '

    if last_name:
        # capitalise last name
        return_name += last_name.upper()

    return return_name