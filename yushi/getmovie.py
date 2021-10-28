
import firebase_admin
from firebase_admin import _FIREBASE_CONFIG_ENV_VAR, firestore
import firebase_admin
from firebase_admin import credentials


cred = credentials.Certificate('techinterview-a88b9-firebase-adminsdk-nd1jy-102817f0eb.json')

firebase_admin.initialize_app(cred, {
    'storageBucket': 'techinterview-a88b9.appspot.com.appspot.com'
})
# bucket = storage.bucket()
class upload_all:
    def __init__(self, uid,documentid,result):
        self.uid = uid; 
        self.documentid = documentid; 
        self.result = result; 


    def upload_movie(self):
        db = firestore.client()
        doc_ref = db.collection('user').document(self.uid).collection('result').document(self.documentid)
        return doc_ref.update({
            'movie_url': self.result
            })
            
    # def upload_result(uid,documentid,result):
    #     db = firestore.client()
    #     doc_ref = db.collection('user').document(uid).collection('result').document(documentid)
    #     doc_ref.update({
    #         'result': {kye: value},
    #         })

# upload_result("q0REUe0hbYbacVskUlgVQKz1pd33","BJaroA3FiEJpO9JKjYqZ","aa","vv")
upload_all("q0REUe0hbYbacVskUlgVQKz1pd33","BJaroA3FiEJpO9JKjYqZ","aaaaaaaa").upload_movie()


