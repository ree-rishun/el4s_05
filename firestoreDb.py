import firebase_admin
from firebase_admin import credentials, firestore


def db():
    cred = credentials.Certificate("el4s-05-firebase-adminsdk-988jv-eaa46c25d2.json")
    firebase_admin.initialize_app(cred)
    return firestore.client()
