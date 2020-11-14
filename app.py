from flask import Flask, send_from_directory, request
import firebase_admin
from firebase_admin import credentials, firestore
import directions
import urllib.request
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
    doc_ref = db.collection(u'users').document(u'DuYXB5RPULTtum9Rgbmi')

    origin = '35.8592065,139.7665079'
    destination = '35.8592065,139.7665079'
    APIKEY = directions.APIKEY()
    APILINK = 'https://maps.googleapis.com/maps/api/directions/json?' \
              + 'origin=' + origin \
              + '&destination=' + destination \
              + '&mode=walking' \
              + '&key=' + APIKEY

    jsonData = {}

    # POST
    req = urllib.request.Request(APILINK)
    with urllib.request.urlopen(req) as res:
        body = res.read()
        print(body)
        jsonData = json.loads(body)

    # 距離を取得
    distance = jsonData['routes'][0]['legs'][0]['distance']['value']



    return 'ok'


# 音楽取得
@app.route('/music')
def music_select():
    # params.id取得
    id = request.args.get('id')
    # userのbpm求める
    bpm = 100
    # bpmに一番近い曲を取得 取り柄あえずlimit100...
    musicsDoc = db.collection('musics').order_by('bpm').limit(100).get()

    musicUrl = ""
    prevBpm = None
    prevMusicUrl = ""
    isContinue = False
    for musicDoc in musicsDoc:
        music = musicDoc.to_dict()
        # 初めて上回った時
        if bpm < music["bpm"]: 
            if abs(bpm - music["bpm"]) < abs(bpm - prevBpm):
                musicUrl = music["path"]
                break
            musicUrl = prevMusicUrl
            break
        prevBpm = music["bpm"]
        prevMusicUrl = music["path"]
    
    # 曲のファイルのURL
    return json.dumps({
        "url": musicUrl
    })


if __name__ == '__main__':
    app.run()
