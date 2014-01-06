from flask import Flask, render_template, request
from pymongo import MongoClient
import simplejson
from random import randint
import os

client = MongoClient("localhost", 27017)
db = client.events

app = Flask(__name__)

'''
    Really hacky function to get back the correct collection depending on email.
    If the user sends an email to x+myapp@something.com it will return a collectoin as db.x
'''
def getCol(event):
    print event
    if event == 'pennapps':
        return db.pennapps
    elif event == 'hckru':
        return db.hackru
    elif event == 'mhacks':
        return db.mhacks
    elif event == 'test':
        return db.test
    elif event == 'stew':
        return db.stew
@app.route('/')
def index():
    print 'test2'
    return render_template('index.html')


@app.route('/<event>')
def getImage(event):
    print event
    collection = getCol(str(event))
    find = collection.find({"images": {'$exists': True}})
    if find.count() == 0:
        return "nothing here yet"
    else:
        for item in find:
            imageUrl = 'static/images/' + str(event) + '/' + str(randint(0, item['images'])) + '.jpg'
    return render_template('event.html', imageUrl=imageUrl)


@app.route('/parse', methods=['POST'])
def parse():
    print "HTTP/1.1 200 OK"

    envelope = simplejson.loads(request.form.get('envelope'))
    print envelope['to']
    print envelope['from']
    envelope['to'] = str(envelope['to'])[3:len(envelope['to']) - 3]
    event = str(envelope['to']).split('+')[0].lower()
    print envelope['to']
    print envelope['from']
    print envelope
    print int(request.form.get('attachments', 0))
    if int(request.form.get('attachments', 0)) >= 1:
        attachment = request.files.get('attachment1')
    else:
        return 'No attachment found'

    collection = getCol(event)
    print collection
    print envelope['from']
    print 'her'
    find = collection.find({"emails": {'$exists': True}})
    if find.count() != 0:
        for item in find:
            emails = item['emails']
            if not envelope['from'] in emails:
                emails.append(envelope['from'])
                collection.save({'_id': item['_id'], 'emails': emails})
            print item
    else:
        collection.insert({'emails': [envelope['from']]})
        print 'found nothing'

    print 'her'
    count = -1
    find = collection.find({"images": {'$exists': True}})
    if find.count() != 0:
        for item in find:
            count = item['images'] + 1
            collection.update({'_id': item['_id']}, {'$inc': {"images": 1}}, False)
            print item
    else:
        collection.insert({'images': 0})
        count = 0
        print 'found nothing'
    directoryRoot = 'static/images/' + event
    if not os.path.exists(directoryRoot):
        os.makedirs(directoryRoot)
    f = open('static/images/' + event + '/' + str(count) + '.jpg', 'w')
    f.write(attachment.read())
    f.close()

    print "HTTP/1.1 200 OK"
    return "HTTP/1.1 200 OK"

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
