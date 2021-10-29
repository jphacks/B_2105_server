import firebase_admin
from firebase_admin import firestore, auth, credentials
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status


class FirebaseClient:
    cred = credentials.Certificate('firebase-credential.json')
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'techinterview-a88b9.appspot.com.appspot.com'
    })

    def upload_movie(self, uid, document_id, result_movie):
        db = firestore.client()
        doc_ref = db.collection('user').document(uid).collection('interview').document(document_id)
        doc_ref.update({
            'movie_id': result_movie
        })

    def upload_result(self, uid, document_id, result_emotion):
        db = firestore.client()
        doc_ref = db.collection('user').document(uid).collection('interview').document(document_id)
        doc_ref.update({
            'result': result_emotion,
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


# result_emotion = {"anger": 0.07870, "contempt": 0.078709, "disgust": 0.078709, "fear": 0.000000, "happiness": 99.134199,
#                   "sadness": 0.511610, "surprise": 0.118064}

# 呼び出し（引数＝ユーザーID、documentID、動画URL,分析結果の配列）
# upload_all("q0REUe0hbYbacVskUlgVQKz1pd33", "BJaroA3FiEJpO9JKjYqZ", "aaaaaa", result_emotion).upload_movie()

# upload_all("q0REUe0hbYbacVskUlgVQKz1pd33", "BJaroA3FiEJpO9JKjYqZ", "aaaaaa", result_emotion).upload_result()
