from datetime import datetime

import firebase_admin
from firebase_admin import firestore, auth, credentials
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status


class FirebaseClient:
    def __init__(self):
        self.cred = credentials.Certificate('secret/firebase-credential.json')
        self.app = firebase_admin.initialize_app(self.cred, {
            'storageBucket': 'techinterview-a88b9.appspot.com.appspot.com'
        })

    def create_document(self, uid):
        db = firestore.client(self.app)
        document_ref = db.collection(u'interview').document()
        document_ref.set({
            "finish_analysis": False,
            "user_id": uid,
            "movie_id": '',
            "result_emotions": {
                "anger": 0,
                "contempt": 0,
                "disgust": 0,
                "fear": 0,
                "happiness": 0,
                "sadness": 0,
                "surprise": 0,
            },
            "result_impressions": {
                "anxious": 0,
                "confidence": 0,
                "honest": 0,
                "leadership": 0,
                "nervous": 0,
                "niceCoworker": 0,
            },
            "created": datetime.now()
        })
        document_ref.collection(u'reviews')
        return document_ref.id

    def upload_movie_id(self, document_id, result_movie):
        db = firestore.client(self.app)
        doc_ref = db.collection('interview').document(document_id)
        doc_ref.update({
            'movie_id': result_movie
        })

    def upload_result(self, document_id, result_emotions, result_impressions):
        db = firestore.client(self.app)
        doc_ref = db.collection('interview').document(document_id)
        doc_ref.update({
            'result_emotions': result_emotions,
            'result_impressions': result_impressions
        })

    def get_current_user(self, cred: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        try:
            decoded_token = auth.verify_id_token(cred.credentials, self.app)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid authentication credentials',
                headers={'WWW-Authenticate': 'Bearer'},
            )

        uid = decoded_token['uid']

        return uid
