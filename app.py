from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/getEmail')
def email():
    return 1

if __name__ == '__main__':
    app.run()
