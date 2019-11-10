from __future__ import print_function
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

# getting the file of the template

IMG_FILE = 'image.jpg'      # use your own!
# color = input('Would you like white (w) or black (b) slides? ')

SCOPES = (
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/presentations',
)
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
HTTP = creds.authorize(Http())
DRIVE  = discovery.build('drive',  'v3', http=HTTP)
SLIDES = discovery.build('slides', 'v1', http=HTTP)

#replace lyrics
def replaceLyrics(template, color):
    print (template)
    print (color)
    if color == 'b':
        TMPLFILE = 'Indigitous Black'   # use your own!
    else:
        TMPLFILE = 'Indigitous White'   # use your own!
    
    rsp = DRIVE.files().list(q="name='%s'" % TMPLFILE).execute().get('files')[0]
    DATA = {'name': 'Song Lyrics'}
    print('** Copying template %r as %r' % (rsp['name'], DATA['name']))
    DECK_ID = DRIVE.files().copy(body=DATA, fileId=rsp['id']).execute().get('id')

    print('** Get slide objects, search for image placeholder')
    slide = SLIDES.presentations().get(presentationId=DECK_ID,
            fields='slides').execute().get('slides')[0]


    songArtist = template[0].rstrip('\n')
    songName = template[1].rstrip('\n')

    nextLine = template[2].rstrip('\n')
    i = 3
    count = 0
    while i < len(template):
        nextLine = template[i].rstrip('\n')
        i += 1
        lyricsLine = ''
        while nextLine!= '-----' and i < len(template):
            lyricsLine = lyricsLine + '\n' + nextLine
            nextLine = template[i].rstrip('\n')
            i += 1
        #name of new copied Id
        copyId = 'COPY' + str(count)
        #insert index of last slide
        insertIndex = str(count + 3)
        
        SLIDES.presentations().batchUpdate(
            body={'requests': [
                {'duplicateObject': {
                    'objectId': 'g741a72a3e3_4_2',
                    'objectIds': {'g741a72a3e3_4_3': copyId}}},
                {'insertText': {
                    'objectId': copyId,
                    'text': '01',
                    'insertionIndex': 10,}},
                {'updateSlidesPosition': {
                        'slideObjectIds': ['g741a72a3e3_4_2'],
                        'insertionIndex': insertIndex}},
                ]}, presentationId=DECK_ID).execute()


        SLIDES.presentations().batchUpdate(
            body={'requests': [
                {'replaceAllText': {
                    'containsText': {'text': '{{lyrics}}01'},
                    'replaceText': lyricsLine}},
                
                ]}, presentationId=DECK_ID).execute()

        count += 1

#        nextLine = templateFile.readline().rstrip('\n')
#        nextLine = templateFile.readline().rstrip('\n')


        
    
    obj = None
    for obj in slide['pageElements']:
        if obj['shape']['shapeType'] == 'RECTANGLE':
            break

##    print('** Searching for icon file')
##    rsp = DRIVE.files().list(q="name='%s'" % IMG_FILE).execute().get('files')[0]
##    print(' - Found image %r' % rsp['name'])
##    img_url = '%s&access_token=%s' % (
##            DRIVE.files().get_media(fileId=rsp['id']).uri, creds.access_token)

    print('** Replacing placeholder text and icon')
    reqs = [
        {'replaceAllText': {
            'containsText': {'text': '{{Artist}}'},
            'replaceText': songArtist 
        }},
        
        {'replaceAllText': {
            'containsText': {'text': '{{NAME}}'},
            'replaceText': songName
        }},

        #copy slide 2
        
##        {'createImage': {
##            'url': img_url,
##            'elementProperties': {
##                'pageObjectId': slide['objectId'],
##                'size': obj['size'],
##                'transform': obj['transform'],
##            }
##        }},
        {'deleteObject': {'objectId': obj['objectId']}},
        {'deleteObject': {'objectId': 'g741a72a3e3_4_2'}},
    ]
    
    SLIDES.presentations().batchUpdate(body={'requests': reqs},
            presentationId=DECK_ID).execute()

    permissions(DECK_ID)

    print('DONE')
    print('Presentation Link: https://docs.google.com/presentation/d/', DECK_ID, sep='')
    return 'https://docs.google.com/presentation/d/' + DECK_ID

#callback error handling
def callback(request_id, response, exception):
        if exception:
            # Handle error
            print (exception)
        else:
            print ("Permission Id: %s" % response.get('id'))

#change the permissions to anyone can access
def permissions(file_id):    

    batch = DRIVE.new_batch_http_request(callback=callback)
    
##    user_permission = {
##        'type': 'user',
##        'role': 'writer',
##        'emailAddress': email_id
##    }
##    batch.add(DRIVE.permissions().create(
##            fileId=file_id,
##            body=user_permission,
##            fields='id',
##    ))
    domain_permission = {
        'type': 'anyone',
        'role': 'reader',
        #'domain': 'gmail.com'
    }
    batch.add(DRIVE.permissions().create(
            fileId=file_id,
            body=domain_permission,
            fields='id',
    ))
    batch.execute()

# with open('output.txt') as template:
#     lines = template.read().splitlines()
#     replaceLyrics(lines)
