'''
Created on 27 Jul 2015

@author: achickermane
'''
import sys
import psycopg2
import csv
from _datetime import date


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
            if row['Burial No.']:
                row['Photo'] ='{0}/images/memorials/'.format(schema)+ row['Photo']+'.jpg'
                cursor.execute('''(select image.id from {0}.bgsite_image as image where image.url like %s)'''.format(schema), (row['Photo'],))
                image_id = cursor.fetchone()[0]
                cursor.execute('''SELECT memorial.memorial_id FROM {0}.bgsite_memorial_images as memorial WHERE memorial.image_id = %s
                                    ;'''.format(schema), (image_id,))
                memorial_id = cursor.fetchone()[0]
                death_memorial_link_query = '''INSERT INTO {0}.bgsite_death_memorials (death_id, memorial_id) 
                                           with t1 as (SELECT %s as death_id, %s as memorial_id)
                                           SELECT t1.death_id, t1.memorial_id from t1 WHERE NOT EXISTS (
                                    SELECT death_id FROM {0}.bgsite_death_memorials WHERE death_id = %s and 
                                memorial_id = %s);'''.format(schema)
                cursor.execute(death_memorial_link_query, (int(row['Burial No.']), memorial_id, int(row['Burial No.']), memorial_id,))
                
                connection.commit()
    
#     except:
#         print("Unable to connect to database.")

if __name__ == '__main__':
    main(sys.argv)