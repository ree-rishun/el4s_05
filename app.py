from flask import Flask

app = Flask(__name__)


@app.route('/genre')
def genre():
    return 'Hello World!'


@app.route('/music')
def music_select():
    return 'test'


if __name__ == '__main__':
    app.run()
