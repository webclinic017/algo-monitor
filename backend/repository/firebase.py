import firebase_admin
from firebase_admin import credentials

def init():
    _cred = credentials.Certificate("./serviceKey.json")
    firebase_admin.initialize_app(_cred, {
        'storageBucket': 'algo-monitor.appspot.com'
    })