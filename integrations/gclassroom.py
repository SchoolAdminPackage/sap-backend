from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


SCOPES = "https://www.googleapis.com/auth/classroom.rosters https://www.googleapis.com/auth/classroom.profile.emails https://www.googleapis.com/auth/classroom.profile.photos https://www.googleapis.com/auth/classroom.courses"
#'https://www.googleapis.com/auth/classroom.courses'

CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Classroom API Python Quickstart'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'classroom.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Classroom API.

    Creates a Classroom API service object and prints the names of the first
    10 courses the user has access to.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('classroom', 'v1', http=http)
    
    course = {
        'name': '10th Grade Biology',
        'section': 'Period 2',
        'descriptionHeading': 'Welcome to 10th Grade Biology',
        'description': """We'll be learning about about the structure of living
                     creatures from a combination of textbooks, guest
                     lectures, and lab work. Expect to be excited!""",
        'room': '301',
        'ownerId': 'me',
        'courseState': 'PROVISIONED'
    }
        
    results = service.courses().list(pageSize=10).execute()
    a = service.courses()
    b = a.create(body=course)
    c = b.execute()
    courses = results.get('courses', [])

    if not courses:
        print('No courses found.')
    else:
        print('Courses:')
        for course in courses:
            print(course['name'])


def initialize_integration(sapi):
    @sapi.event('global.createClass')
    def createClass(className):
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('classroom', 'v1', http=http)
    
        course = {
            'name': className,
            'section': 'Period 2',
            'descriptionHeading': 'Welcome to 10th Grade Biology',
            'description': """We'll be learning about about the structure of living
                         creatures from a combination of textbooks, guest
                         lectures, and lab work. Expect to be excited!""",
            'room': '301',
            'ownerId': 'me',
            'courseState': 'PROVISIONED'
        }
        
        results = service.courses().list(pageSize=10).execute()
        a = service.courses()
        b = a.create(body=course)
        c = b.execute()    
    
    #
    # @sapi.event('global.createAssignment')
    # def createAssignment(assignmentName):
    #     assignment = {}
