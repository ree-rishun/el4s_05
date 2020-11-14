from flask import Flask
from firestoreDb import db

app = Flask(__name__)


@app.route('/genre')
def genre():
    genres = db.collection('genres').get()
    return genres


@app.route('/music')
def music_select():
    return 'test'


if __name__ == '__main__':
    app.run()
