"""
Minimal REST API for BACAS. Implements authentication and request for deceased by section and grave ref. 
Implemented as functions so this file can be run/tested in interactive mode. Can easily make it OOP if multiple API sites make it necessary/useful. 
(All other available methods are available in the commented out section.)
Token expiry is handled by requesting every it request but cacheing the authentication response. Handles all necessary cases with minimal code.
Only POST requests are cached. Currently that is only the authentication methods. 
GET request caching also tested but not used for demo to reduce side effects. Can also create a separate cache with different settings for GET reuests if desired.
Usename/Password and URL are hard coded but are intended to be easily pulled from DB.
"""

# Install the Python Requests library:
# `pip install requests`
# `pip install requests-cache`

import requests
import requests_cache #caches requests in an sql_lite db 
import json
import time #used for timing requests for debugging

#import logging
#logging.basicConfig(level='DEBUG')
#logging.getLogger('requests_cache').setLevel('DEBUG')

#These variables should be stored in the DB and retrieved as necessary
bacas_base_url = "https://bacasapi.cardiff.gov.uk/bacascoreapi/api/"
bacas_password = "*Atl4nt1cB4c45*"
bacas_username = "Atlantic"

#Initialize the cache. Token expires every twelve hours so expiry must be less than that. (Probably half that for all edge cases.)
requests_cache.install_cache('bacas_cache', backend='sqlite', expire_after=21600, allowable_methods=('POST')) #set cache for six hours. only cache post methods for authentication.
#requests_cache.install_cache('bacas_cache', backend='sqlite', expire_after=21600, allowable_methods=('GET', 'POST')) #set cache for six hours. cache all requests.


"""
Returns the current token for the BACAS API. Rather than handle token expiry we just cache the request.
Calls: bacas_authenticate to do the actual rest request
Uses: base)uel, username, password variables currently hard coded above
"""
def bacas_get_token():
    #print("Starting bacas_gettoken.")
    json = bacas_authenticate()
    token = json['token'] #should validate this
    print('Token: ' + token)    
    return token

"""
/api/Users/authenticate
POST https://bacasapi.cardiff.gov.uk/bacascoreapi/api/Users/authenticate/   
"""
def bacas_authenticate(): #Authenticates via the bacas rest api using username & password variables.          
    try:
        now = time.ctime(int(time.time()))        
        response = requests.post(
            url= bacas_base_url + "Users/authenticate/",
            headers={
                "Content-Type": "application/json-patch+json",
                "Accept": "text/plain",
            },
            data=json.dumps({
                "password": bacas_password,
                "username": bacas_username,
                "token": "",
                "firstName": "",
                "id": 0,
                "role": "",                                
                "lastName": ""
            })
        )
        print("Time: " + now + "/ Used Cache: " + str(response.from_cache))
        return response.json()      
    except requests.exceptions.RequestException:
        print('HTTP Request failed')
        return {}

""" 
Gets a list of deceased given a bacas section_id and a bacas grave_ref. These are mapped to out IDs vis the bgsite_graveref table.
"""
def bacas_get_deceased(section_id, grave_ref):
    try:
        now = time.ctime(int(time.time()))               
        #token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiTWFwcyIsIm5iZiI6MTY0NTgyMDg5MSwiZXhwIjoxNjQ2NDI1NjkxLCJpYXQiOjE2NDU4MjA4OTF9.liecgNpYNLoLkiu2o6wiagBhhik3-hrOSI_bwiqWjg8'
        token = bacas_get_token()
        #print('Token: ' + str(token))        
        #url= bacas_base_url + "Graves/Section/" + str(section_id) + "/" + str(grave_ref) + "/"
        response = requests.get(
            url= bacas_base_url + "Graves/Section/" + str(section_id) + "/" + str(grave_ref) + "/",
            headers={
                "Accept": "text/plain",
                "Authorization": "Bearer " + str(token),
            },
        )
        print("Time: " + now + "/ Used Cache: " + str(response.from_cache))
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        if response.status_code == 401:
            print('Authentication Error. Check Token?')
            return {}
        elif response.status_code == 200:
            json = response.json()        
            return bacas_modify_deceased_json(json)
        else :
            return {}
        
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


def bacas_modify_deceased_json(original_json):
    for deceased in original_json['deceaseds']:
        deceased['person_id'] = deceased.pop('deceasedId')
        deceased['death_date'] = deceased.pop('dateOfDeath')
        deceased['age_years'] = deceased.pop('age')
        #deceased['death_date'] = deceased.pop('dateOfDeath')
        deceased['display_name'] = deceased['foreNames'] + " " + deceased['surname']
    return original_json['deceaseds'] 

"""
# Install the Python Requests library:
# `pip install requests`
import requests

def send_request():
    # /api/MainLocations
    # GET https://bacasapi.cardiff.gov.uk/bacascoreapi/api/MainLocations/

    try:
        response = requests.get(
            url="https://bacasapi.cardiff.gov.uk/bacascoreapi/api/MainLocations/",
            headers={
                "Accept": "text/plain",
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiTWFwcyIsIm5iZiI6MTY0NDI1OTE2NywiZXhwIjoxNjQ0ODYzOTY3LCJpYXQiOjE2NDQyNTkxNjd9.VvT5-hb2Dt2Zv3UaKDTWBPL1TJV65GE7cDB5saP22YE",
            },
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


# Install the Python Requests library:
# `pip install requests`

import requests
import json


def send_request():
    # /api/MainLocations/{cemeteryid}
    # GET https://bacasapi.cardiff.gov.uk/bacascoreapi/api/MainLocations/3

    try:
        response = requests.get(
            url="https://bacasapi.cardiff.gov.uk/bacascoreapi/api/MainLocations/3",
            headers={
                "Accept": "text/plain",
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiTWFwcyIsIm5iZiI6MTY0NDI1OTE2NywiZXhwIjoxNjQ0ODYzOTY3LCJpYXQiOjE2NDQyNTkxNjd9.VvT5-hb2Dt2Zv3UaKDTWBPL1TJV65GE7cDB5saP22YE",
            },
            data=json.dumps({

            })
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


# Install the Python Requests library:
# `pip install requests`

import requests


# Install the Python Requests library:
# `pip install requests`

import requests


def send_request():
    # /api/Graves
    # GET https://bacasapi.cardiff.gov.uk/bacascoreapi/api/graves/section/2

    try:
        response = requests.get(
            url="https://bacasapi.cardiff.gov.uk/bacascoreapi/api/graves/section/2",
            headers={
                "Accept": "text/plain",
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiTWFwcyIsIm5iZiI6MTY0NDI1OTE2NywiZXhwIjoxNjQ0ODYzOTY3LCJpYXQiOjE2NDQyNTkxNjd9.VvT5-hb2Dt2Zv3UaKDTWBPL1TJV65GE7cDB5saP22YE",
            },
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


# Install the Python Requests library:
# `pip install requests`

import requests


def send_request():
    # /api/Graves/{graveid}
    # GET https://bacasapi.cardiff.gov.uk/bacascoreapi/api/Graves/115056/

    try:
        response = requests.get(
            url="https://bacasapi.cardiff.gov.uk/bacascoreapi/api/Graves/115056/",
            headers={
                "Accept": "text/plain",
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiTWFwcyIsIm5iZiI6MTY0NDI1OTE2NywiZXhwIjoxNjQ0ODYzOTY3LCJpYXQiOjE2NDQyNTkxNjd9.VvT5-hb2Dt2Zv3UaKDTWBPL1TJV65GE7cDB5saP22YE",
            },
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


# Install the Python Requests library:
# `pip install requests`

import requests


def send_request():
    # /api/Graves/Section/{sectionid}
    # GET https://bacasapi.cardiff.gov.uk/bacascoreapi/api/Graves/Section/358/

    try:
        response = requests.get(
            url="https://bacasapi.cardiff.gov.uk/bacascoreapi/api/Graves/Section/358/",
            headers={
                "Accept": "text/plain",
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiTWFwcyIsIm5iZiI6MTY0NDI1OTE2NywiZXhwIjoxNjQ0ODYzOTY3LCJpYXQiOjE2NDQyNTkxNjd9.VvT5-hb2Dt2Zv3UaKDTWBPL1TJV65GE7cDB5saP22YE",
            },
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


# Install the Python Requests library:
# `pip install requests`

import requests


def send_request():
    # /api/Sections
    # GET https://bacasapi.cardiff.gov.uk/bacascoreapi/api/Sections/

    try:
        response = requests.get(
            url="https://bacasapi.cardiff.gov.uk/bacascoreapi/api/Sections/",
            headers={
                "Accept": "text/plain",
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiTWFwcyIsIm5iZiI6MTY0NDI1OTE2NywiZXhwIjoxNjQ0ODYzOTY3LCJpYXQiOjE2NDQyNTkxNjd9.VvT5-hb2Dt2Zv3UaKDTWBPL1TJV65GE7cDB5saP22YE",
            },
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


# Install the Python Requests library:
# `pip install requests`

import requests


def send_request():
    # /api/Sections/Cemetery/{cemeteryid}
    # GET https://bacasapi.cardiff.gov.uk/bacascoreapi/api/Sections/Cemetery/3/

    try:
        response = requests.get(
            url="https://bacasapi.cardiff.gov.uk/bacascoreapi/api/Sections/Cemetery/3/",
            headers={
                "Accept": "text/plain",
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiTWFwcyIsIm5iZiI6MTY0NDI1OTE2NywiZXhwIjoxNjQ0ODYzOTY3LCJpYXQiOjE2NDQyNTkxNjd9.VvT5-hb2Dt2Zv3UaKDTWBPL1TJV65GE7cDB5saP22YE",
            },
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


# Install the Python Requests library:
# `pip install requests`

import requests


def send_request():
    # /api/Sections/{sectionid}
    # GET https://bacasapi.cardiff.gov.uk/bacascoreapi/api/Sections/192/

    try:
        response = requests.get(
            url="https://bacasapi.cardiff.gov.uk/bacascoreapi/api/Sections/192/",
            headers={
                "Accept": "text/plain",
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiTWFwcyIsIm5iZiI6MTY0NDI1OTE2NywiZXhwIjoxNjQ0ODYzOTY3LCJpYXQiOjE2NDQyNTkxNjd9.VvT5-hb2Dt2Zv3UaKDTWBPL1TJV65GE7cDB5saP22YE",
            },
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')

"""
