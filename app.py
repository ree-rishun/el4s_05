from flask import Flask
import firebase_admin
from firebase_admin import credentials, firestore
import directions
import requests

app = Flask(__name__)

cred = credentials.Certificate("el4s-05-firebase-adminsdk-988jv-eaa46c25d2.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


# ジャンル一覧取得
@app.route('/genre')
def genre():
    # データ取得
    genres = db.collection(u'genres').get()
    json = '{'

    # データの整形
    for doc in genres:
        # カンマ区切りの挿入
        if json != '{':
            json += ','

        # JSON形式に整形
        json += u'\"' + doc.id + '\":{\"name\": \" ' + doc.to_dict()['name'] + ' \"}'

    json += '}'

    # JSONの返却
    return json


# 音楽取得
@app.route('/music')
def music_select():
    origin = '35.8592065,139.7665079'
    destination = '35.8592065,139.7665079'
    APIKEY = directions.APIKEY()
    APILINK = 'https://maps.googleapis.com/maps/api/directions/json?' \
              + 'origin=' + origin \
              + '&destination=' + destination \
              + '&mode=walking' \
              + '&key=' + APIKEY

    print(APILINK)

    data = requests.get(APILINK)

    print(data)

    return data


if __name__ == '__main__':
    app.run()
