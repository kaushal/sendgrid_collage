from flask import Flask, render_template, request
import simplejson

app = Flask(__name__)


@app.route('/')
def index():
    print 'test2'
    return render_template('index.html')


@app.route('/parse', methods=['POST'])
def parse():
    print "HTTP/1.1 200 OK"
    envelope = simplejson.loads(request.form.get('envelope'))
    print envelope
    print int(request.form.get('attachments', 0))
    if int(request.form.get('attachments', 0)) >= 1:
        attachment = request.files.get('attachment%1')
    else:
        return

    print attachment.read()
    return 'test'

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
