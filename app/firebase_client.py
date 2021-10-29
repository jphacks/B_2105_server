import firebase_admin
from firebase_admin import firestore, auth, credentials
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status


class FirebaseClient:
    cred = credentials.Certificate('firebase-credential.json')
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'techinterview-a88b9.appspot.com.appspot.com'
    })

    def upload_movie(uid, document_id, result_movie):
        db = firestore.client()
        doc_ref = db.collection('user').document(uid).collection('interview').document(document_id)
        doc_ref.update({
            'movie_id': result_movie
        })

    def upload_result(uid, document_id, result_emotions,result_impressions):
        result_emotions.update(result_impressions)
        for key,value in result_emotions.items():
            if int(value) < 0:
              result_emotions[key] = 0

        db = firestore.client()
        doc_ref = db.collection('user').document(uid).collection('interview').document(document_id)
        doc_ref.update({
            'result': result_emotions,
        })

    def get_current_user(self, cred: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        try:
            decoded_token = auth.verify_id_token(cred.credentials)
        except:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid authentication credentials',
                headers={'WWW-Authenticate': 'Bearer'},
            )

        # user = decoded_token['firebase']['identities']
        uid = decoded_token['uid']

        return uid


# 呼び出し（引数＝ユーザーID、documentID、動画URL,表情の配列,印象の配列）
# result_emotions = {"anger": 12, "contempt": 22, "disgust": 33, "fear": 44, "happiness": 55,
#                   "sadness": 66, "surprise": 77}

# result_impressions = {"honest": 39.97834336927723, "confidence": 26.460891949863026, "leadership": 35.65540659219143, "anxious": 336.35048017028286, "anxious": -32.80743136616357,
#                   "nervous": -26.27180524020688}



# FirebaseClient.upload_result("xmkjt589JgTbhbOUlVCvvLh6ILO2", "X7VvOEU9JxKbU7cLDBfw", result_emotions,result_impressions)
