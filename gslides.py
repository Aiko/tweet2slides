from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import sys

SCOPES = "https://www.googleapis.com/auth/presentations"

store = file.Storage('credentials.json')
creds = store.get()

if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
    print('Fetched credentials.')
else:
    print('Got credentials')

service = build('slides', 'v1', http=creds.authorize(Http()))
i = 0


def init():
    return service.presentations().create()


def new_slide(ppt, tweet):
    q = [
        {
            'createSlide': {
                'objectId': f'pageBoi_{i}',
                'slideLayoutReference': {
                    'predefinedLayout': 'TITLE_AND_TWO_COLUMNS'
                }
            },
            'placeholderIdMappings': [{
                'layoutPlaceholder': {'type': 'TITLE', 'index': 0},
                'objectId': f'titleBoi_{i}'
            }]
        }, {
            'insertText': {
                'objectId': f'titleBoi_{i}',
                'text': tweet['time']
            }
        }, {
            'createShape': {
                'objectId': f'tweetBoi_{i}',
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': f'pageBoi_{i}',
                    'size': {
                        'height': {'magnitude': 200, 'unit': 'PT'},
                        'width': {'magnitude': 400, 'unit': 'PT'}
                    },
                    'transform': {
                        'scaleX': 1, 'scaleY': 1, 'translateX': 400, 'translateY': 100, 'unit': 'PT'
                    }
                }
            }
        }, {
            'insertText': {
                'objectId': f'tweetBoi_{i}', 'text': tweet['text']
            }
        }, {
            'createShape': {
                'objectId': f'engagementBoi_{i}',
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': f'pageBoi_{i}',
                    'size': {
                        'height': {'magnitude': 350, 'unit': 'PT'},
                        'width': {'magnitude': 400, 'unit': 'PT'}
                    },
                    'transform': {
                        'scaleX': 1, 'scaleY': 1, 'translateX': 400, 'translateY': 400, 'unit': 'PT'
                    }
                }
            }
        }, {
            'insertText': {
                'objectId': f'engagementBoi_{i}',
                'text': f'{tweet["retweets"]} retweets, {tweet["favorites"]} favorites'
            }
        }
    ]
    i += 1
    s = service.presentations().batchUpdate(presentationId=ppt.get(
        'presentationId'), body={'requests': q}).execute()
    return s.get('replies')[0].get('createSlide').get('objectId')
