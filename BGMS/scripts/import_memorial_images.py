'''
Created on 27 Jul 2015

@author: achickermane
'''
import sys
import psycopg2
import csv
from _datetime import date
import uuid


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
        
    def convert_to_int(value):
        if value=='':
            return None
        else:
            try:
                return int(value)
            except:
                return None
    
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
            
            # Only write rows with actual data, do not count row id
            # & entered by in the assessment (first & second columns in row)
    #         if any(newrow[2:]):
            # First create person
            if row['Grave ID'] and row['Photo']:
                image_insert_query = '''INSERT INTO {0}.bgsite_image(image_state_id, image_type_id, url)
                                WITH t1 AS (SELECT state.id as state_id from public.main_imagestate as state where state.image_state = 'unprocessed' ),
                                    t2 AS (SELECT img_type.id as state_type from public.main_imagetype as img_type where img_type.image_type = 'memorial' ),
                                    t3 as (SELECT %s as image_path)
                                SELECT t1.state_id, t2.state_type, t3.image_path from t1,t2,t3 WHERE NOT EXISTS (
                                    SELECT image.url FROM {0}.bgsite_image as image WHERE image.url LIKE %s
                                );'''.format(schema)
                if not row['Photo'].endswith('.jpg'):
                    row['Photo'] = row['Photo']+'.jpg'
                image ='{0}/images/memorials/'.format(schema)+ row['Photo']
                thumbnail ='{0}/thumbnails/memorials/'.format(schema)+ row['Photo']
                cursor.execute(image_insert_query, (image, image,))
                cursor.execute('''SELECT id FROM {0}.bgsite_image WHERE url LIKE %s;'''.format(schema), (image,))
                image_id = cursor.fetchone()[0]
                thumbnail_insert_query = '''INSERT INTO {0}.bgsite_thumbnail(image_id, url) 
                    WITH t1 as (SELECT %s as image_id,%s as url)
                    SELECT t1.image_id, t1.url from t1
                     WHERE NOT EXISTS (
                                    SELECT image.image_id FROM {0}.bgsite_thumbnail as image WHERE image.image_id = %s
                                )'''.format(schema)
                cursor.execute(thumbnail_insert_query, (image_id,thumbnail,image_id,))
#                 memorial_insert_query = '''insert into {0}.bgsite_memorial (feature_id,description, uuid, user_generated) 
#                                             with t3 as (SELECT %s as feature_id, %s as description, %s as user_generated) 
#                                             SELECT t3.feature_id, t3.description, uuid_generate_v4(), t3.user_generated from t3 WHERE NOT EXISTS (
#                                     SELECT image.feature_id FROM {0}.bgsite_memorial as image WHERE feature_id = %s
#                                 );'''.format(schema)
#                 cursor.execute(memorial_insert_query, (int(row['Grave ID']), row['Notes'], False, int(row['Grave ID'])))
                cursor.execute('''SELECT image.id FROM {0}.bgsite_memorial as image WHERE image.feature_id = %s;'''.format(schema), (row['Grave ID'],))
                memorial_id = cursor.fetchone()[0]
                if not memorial_id:
                    memorial_insert_query = '''insert into {0}.bgsite_memorial (feature_id,description, uuid, user_generated) 
                                            with t3 as (SELECT %s as feature_id, %s as description, %s as user_generated) 
                                            SELECT t3.feature_id, t3.description, uuid_generate_v4(), t3.user_generated from t3 WHERE NOT EXISTS (
                                    SELECT image.feature_id FROM {0}.bgsite_memorial as image WHERE feature_id = %s
                                );'''.format(schema)
                    cursor.execute(memorial_insert_query, (int(row['Grave ID']), row['Notes'], False, int(row['Grave ID'])))
                    cursor.execute('''SELECT image.id FROM {0}.bgsite_memorial as image WHERE image.feature_id = %s;'''.format(schema), (row['Grave ID'],))
                    memorial_id = cursor.fetchone()[0]
                memorial_images_insert_query = '''INSERT INTO {0}.bgsite_memorial_images (memorial_id, image_id) 
                                           with t1 as (SELECT %s as memorial_id, %s as image_id)
                                           SELECT t1.memorial_id, t1.image_id from t1;'''.format(schema)
                cursor.execute(memorial_images_insert_query, (memorial_id,image_id,))
                
                connection.commit()
    
#     except:
#         print("Unable to connect to database.")

if __name__ == '__main__':
    main(sys.argv)