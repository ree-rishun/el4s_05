from flask import Flask, send_from_directory
import firebase_admin
from firebase_admin import credentials, firestore
import directions
import requests
import json

app = Flask(__name__)

cred = credentials.Certificate("el4s-05-firebase-adminsdk-988jv-eaa46c25d2.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

PUBLIC_IMAGES = "public/images"
@app.route('/' + PUBLIC_IMAGES + '/<filename>')
def public_images(filename):
    return send_from_directory(PUBLIC_IMAGES, filename)

PUBLIC_MUSICS = "public/musics"
@app.route('/' + PUBLIC_MUSICS + '/<filename>')
def public_musics(filename):
    return send_from_directory(PUBLIC_MUSICS, filename)

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
        json += u'\"' + doc.id + '\":{\"name\": \"' + doc.to_dict()['name'] + '\"}'

    json += '}'

    # JSONの返却
    return json


# 座標登録
@app.route('/location')
def location_post():
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


# 音楽取得
@app.route('/music')
def music_select(id=None):
    # params.id取得
    # userのbpm求める
    # bpmに一番近い曲を取得
    # 曲のファイルのURLを送信
    return json.dumps({
        "url": "http://www.hmix.net/music/n/n67.mp3"
    })


if __name__ == '__main__':
    app.run()
