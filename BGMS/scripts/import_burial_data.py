'''
Created on 27 Jul 2015

@author: achickermane
'''
import sys
import psycopg2
import csv
from _datetime import date
import math


def main(args): 
    
    def get_date(year, month, day):
        if year == '':
            return None
        if month == '':
            month = 1
        if day == '':
            day = 1
        return date(int(year), int(month), int(day))
    
    def is_impossible_date(year, month, day):
        if (year == '') | (month == '') | (day == ''):
            return True
        else:
            return False
        
    def is_interred(buried):
        if buried.lower()=='burial':
            return True
        else:
            return False
        
    def convert_to_int(value, null_as_zero=False):
        value=value.strip()
        if value=='':
            if null_as_zero:
                return 0
            else:
                return None
        else:
            try:
                return int(value)
            except:
                if null_as_zero:
                    return 0
                else:
                    return None
            
    def calculate_years_months(years, months):
        if (months) and (months>12):
            years = years+int(math.floor(months/12))
            months = months%12
        return (years, months,)
    
    # set variable from command line args
    db_param = args[1].split()
    database = db_param[0]
    schema = db_param[1]
    user = db_param[2]
    password = db_param[3]
    host = 'dbdemo.c2sriuehqiis.eu-west-1.rds.amazonaws.com'
    port = '5432'
    
    csv_file = args[2]
    print(csv_file)
    
    # Obtain a database connection  
    connection = None
#     try:
    connection = psycopg2.connect(database=database, host=host, port=port, user=user, password=password)
    cursor = connection.cursor()

    # Open CSV file for reading
    with open(csv_file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Cells need to be cleaned of multiple whitespace
            if row['ID']:
                # Only write rows with actual data, do not count row id
                # & entered by in the assessment (first & second columns in row)
        #         if any(newrow[2:]):
                # First create person
                address_id = None
                if hasattr(row, 'Abode'):
                    address_insert_query = '''insert into {0}.bgsite_address (first_line) 
                                                with t3 as (SELECT %(address)s as address) 
                                                SELECT t3.address from t3 WHERE NOT EXISTS (
                                        SELECT address.first_line FROM {0}.bgsite_address as address WHERE address.first_line LIKE %(address)s
                                    );'''.format(schema)
                    cursor.execute(address_insert_query, {'address': row['Abode']})
                    cursor.execute('''SELECT address.id FROM {0}.bgsite_address as address WHERE address.first_line LIKE %(address)s;'''.format(schema), {'address': row['Abode']})
                    address_id = cursor.fetchone()[0]
                nickname = ''
                if 'Nickname(s)' in row:
                    nickname = row['Nickname(s)']
                person_insert_query = '''INSERT INTO {0}.bgsite_person (first_names, other_names, last_name, impossible_date, 
                                        impossible_date_day, impossible_date_month, impossible_date_year, residence_address_id)
                                        values(%(first_names)s, %(other_names)s, %(last_name)s, %(impossible_date)s, %(impossible_date_day)s, 
                                        %(impossible_date_month)s, %(impossible_date_year)s, %(residence_address_id)s) RETURNING id;'''.format(schema)
                cursor.execute(person_insert_query, {'first_names':row['First Name(s)'], 
                                                     'other_names':nickname, 
                                                     'last_name':row['Last Name'], 
                                                     'impossible_date': is_impossible_date(row['Date of Birth (Year)'],row['Date of Birth (Month)'],row['Date of Birth (Day)']),
                                                     'impossible_date_day': convert_to_int(row['Date of Birth (Day)']), 
                                                     'impossible_date_month': convert_to_int(row['Date of Birth (Month)']),
                                                     'impossible_date_year': convert_to_int(row['Date of Birth (Year)']),
                                                     'residence_address_id':address_id})
                person_id = cursor.fetchone()[0]
                death_insert_query = '''INSERT INTO {0}.bgsite_death (person_id, age_years, age_months, age_weeks, 
                                            age_days, age_hours, death_date, impossible_date, impossible_date_day,
                                            impossible_date_month, impossible_date_year, death_cause)
                                            values(%(person_id)s, %(age_years)s, %(age_months)s, %(age_weeks)s, 
                                            %(age_days)s, %(age_hours)s, %(death_date)s, %(impossible_date)s, 
                                            %(impossible_date_day)s, %(impossible_date_month)s, %(impossible_date_year)s, 
                                            %(death_cause)s);'''.format(schema)
                null_as_zero=False
                if (row['Age (Years)']!='')|(row['Age (Months)']!='')|(row['Age (Weeks)']!='')|(row['Age (Days)']!='')|(row['Age (Hours)']!=''):
                    null_as_zero=True
                years = convert_to_int(row['Age (Years)'],null_as_zero)
                months = convert_to_int(row['Age (Months)'],False)
                years_months = calculate_years_months(years,months)
                years = years_months[0]
                months = years_months[1]
                cursor.execute(death_insert_query, {'person_id': person_id, 
                                                    'age_years': years, 
                                                    'age_months': months, 
                                                    'age_weeks': convert_to_int(row['Age (Weeks)'],False), 
                                                    'age_days': convert_to_int(row['Age (Days)'],False), 
                                                    'age_hours': convert_to_int(row['Age (Hours)'],False), 
                                                    'death_date': get_date(row['Date of Death (Year)'], row['Date of Death (Month)'],row['Date of Death (Day)']), 
                                                    'impossible_date': is_impossible_date(row['Date of Death (Year)'],row['Date of Death (Month)'],row['Date of Death (Day)']),
                                                    'impossible_date_day': convert_to_int(row['Date of Death (Day)']),
                                                    'impossible_date_month': convert_to_int(row['Date of Death (Month)']),
                                                    'impossible_date_year': convert_to_int(row['Date of Death (Year)']), 
                                                    'death_cause': row['Cause of death']})
                image_insert_query = '''INSERT INTO {0}.bgsite_image(image_state_id, image_type_id, url)
                                WITH t1 AS (SELECT state.id as state_id from public.main_imagestate as state where state.image_state = 'unprocessed' ),
                                    t2 AS (SELECT img_type.id as state_type from public.main_imagetype as img_type where img_type.image_type = 'burial_record' ),
                                    t3 as (SELECT %(url)s as image_path)
                                SELECT t1.state_id, t2.state_type, t3.image_path from t1,t2,t3
                                WHERE NOT EXISTS (
                                    SELECT image.url FROM {0}.bgsite_image as image WHERE image.url LIKE %(url)s
                                );'''.format(schema)
                if not row['Image file name'].endswith('.jpg'):
                    row['Image file name'] = row['Image file name']+'.jpg'
                cursor.execute(image_insert_query, {'url': '{0}/images/burial_records/'.format(schema)+row['Image file name']})
                cursor.execute('SELECT image.id as image_id from {0}.bgsite_image as image where (image.url LIKE %(url)s)'.format(schema), {'url':'{0}/images/burial_records/'.format(schema)+row['Image file name']})
                image_id = cursor.fetchone()[0]
                thumbnail_insert_query = '''INSERT INTO {0}.bgsite_thumbnail(image_id, url) 
                    WITH t1 as (SELECT %(image_id)s as image_id,%(url)s as url)
                    SELECT t1.image_id, t1.url from t1
                     WHERE NOT EXISTS (
                                    SELECT image.image_id FROM {0}.bgsite_thumbnail as image WHERE image.image_id = %(image_id)s
                                )'''.format(schema)
                cursor.execute(thumbnail_insert_query, {'image_id': image_id, 'url': ('{0}/thumbnails/burial_records/'.format(schema)+row['Image file name'])})
                burial_insert_query = '''INSERT INTO {0}.bgsite_burial (burial_number, burial_date, impossible_date, impossible_date_day,
                                            impossible_date_month, impossible_date_year, interred, burial_remarks, user_remarks, death_id, burial_record_image_id, requires_investigation)
                                            VALUES ( %(burial_number)s, %(burial_date)s, %(impossible_date)s, %(impossible_date_day)s, %(impossible_date_month)s, 
                                            %(impossible_date_year)s, %(interred)s, %(burial_remarks)s, %(user_remarks)s, %(death_id)s, %(burial_record_image_id)s, 
                                            %(requires_investigation)s) RETURNING id;'''.format(schema)
                cursor.execute(burial_insert_query, {'burial_number': row['No.'], 
                                                     'burial_date': get_date(row['When Buried (Year)'],row['When Buried (Month)'],row['When Buried (Day)']), 
                                                     'impossible_date': is_impossible_date(row['When Buried (Year)'],row['When Buried (Month)'],row['When Buried (Day)']),
                                                     'impossible_date_day': convert_to_int(row['When Buried (Day)']), 
                                                     'impossible_date_month': convert_to_int(row['When Buried (Month)']), 
                                                     'impossible_date_year': convert_to_int(row['When Buried (Year)']), 
                                                     'interred': is_interred(row['Cremation or Burial?']), 
                                                     'burial_remarks': row['Other'], 
                                                     'user_remarks': row['Notes'], 
                                                     'death_id': person_id, 
                                                     'burial_record_image_id': image_id, 
                                                     'requires_investigation': False})
                burial_id = cursor.fetchone()[0]
                official_insert_query = '''INSERT INTO {0}.bgsite_official (title, first_names, last_name) 
                                           with t3 as (SELECT %(title)s as title, %(first_names)s as first_names, 
                                           %(last_name)s as last_name) 
                                            SELECT t3.title, t3.first_names, t3.last_name from t3 WHERE NOT EXISTS (
                                    SELECT image.title FROM {0}.bgsite_official as image WHERE image.title LIKE %(title)s
                                    and image.first_names LIKE %(first_names)s and image.last_name LIKE %(last_name)s);'''.format(schema)
                name_split = row['By whom the Ceremony was Performed'].split()
                last_name = ''
                if len(name_split)>0:
                    last_name = name_split.pop()
                first_names = ''.join(name_split)
                if (first_names!='') | (last_name!='') | (row['Position/Profession of who Performed the Ceremony']!=''):
                    cursor.execute(official_insert_query, {'title': row['Position/Profession of who Performed the Ceremony'],
                                                           'first_names': first_names,
                                                           'last_name': last_name})
                
                    official_type_insert_query = '''INSERT INTO {0}.bgsite_burialofficialtype (official_type) 
                                           with t3 as (SELECT %(official_type)s as official_type) 
                                            SELECT t3.official_type from t3 WHERE NOT EXISTS (
                                    SELECT image.official_type FROM {0}.bgsite_burialofficialtype 
                                    as image WHERE image.official_type LIKE %(official_type)s);'''.format(schema)
                    cursor.execute(official_type_insert_query, {'official_type': 'Ceremony Performed by'})                       
                    cursor.execute('''SELECT id FROM {0}.bgsite_burialofficialtype WHERE official_type LIKE %(official_type)s;'''.format(schema), {'official_type': 'Ceremony Performed by'})
                    official_type_id = cursor.fetchone()[0]
                    cursor.execute('''SELECT image.id FROM {0}.bgsite_official as image WHERE image.title LIKE %(title)s
                                    and image.first_names LIKE %(first_names)s and image.last_name LIKE %(last_name)s;'''.format(schema),
                                                 {'title': row['Position/Profession of who Performed the Ceremony'], 
                                                  'first_names': first_names, 
                                                  'last_name': last_name})
                    official_id = cursor.fetchone()[0]
                    burial_official_insert_query = '''INSERT INTO {0}.bgsite_burialofficial (official_id, official_type_id) 
                                           with t1 as (SELECT %(official_id)s as official_id, %(official_type_id)s as official_type_id)
                                           SELECT t1.official_id, t1.official_type_id from t1 WHERE NOT EXISTS (
                                    SELECT image.official_id, image.official_type_id FROM {0}.bgsite_burialofficial 
                                    as image WHERE image.official_id = %(official_id)s and image.official_type_id = %(official_type_id)s);'''.format(schema)
                    cursor.execute(burial_official_insert_query, {'official_id': official_id, 'official_type_id': official_type_id})
                    cursor.execute('''SELECT id FROM {0}.bgsite_burialofficial WHERE 
                                        official_id = %(official_id)s and official_type_id = %(official_type_id)s'''.format(schema), 
                                        {'official_id': official_id, 'official_type_id': official_type_id})
                    burialofficial_id = cursor.fetchone()[0]
                    burial_burial_officials_insert_query = '''INSERT INTO {0}.bgsite_burial_burial_officials (burial_id, burialofficial_id)
                                            VALUES(%(burial_id)s,%(burialofficial_id)s);'''.format(schema)
                    cursor.execute(burial_burial_officials_insert_query, {'burial_id': burial_id, 'burialofficial_id': burialofficial_id})
                if row['Grave ID']:
                    memorial_insert_query = '''insert into {0}.bgsite_memorial (feature_id, uuid, user_generated) 
                                            with t3 as (SELECT %(feature_id)s as feature_id, %(user_generated)s as user_generated) 
                                            SELECT t3.feature_id, uuid_generate_v4(), t3.user_generated from t3 WHERE NOT EXISTS (
                                    SELECT image.feature_id FROM {0}.bgsite_memorial as image WHERE feature_id = %(feature_id)s
                                );'''.format(schema)
                    cursor.execute(memorial_insert_query, {'feature_id': int(row['Grave ID']),'user_generated': False})
                    cursor.execute('''SELECT image.id FROM {0}.bgsite_memorial as image WHERE image.feature_id = %s;'''.format(schema), (row['Grave ID'],))
                    memorial_id = cursor.fetchone()[0]
                    death_memorial_link_query = '''INSERT INTO {0}.bgsite_death_memorials (death_id, memorial_id) 
                                           with t1 as (SELECT %(death_id)s as death_id, %(memorial_id)s as memorial_id)
                                           SELECT t1.death_id, t1.memorial_id from t1 WHERE NOT EXISTS (
                                    SELECT death_id FROM {0}.bgsite_death_memorials WHERE death_id = %(death_id)s and 
                                memorial_id = %(memorial_id)s);'''.format(schema)
                    cursor.execute(death_memorial_link_query, {'death_id': person_id, 'memorial_id': memorial_id})
            connection.commit()
    
#     except:
#         print("Unable to connect to database.")

if __name__ == '__main__':
    main(sys.argv)