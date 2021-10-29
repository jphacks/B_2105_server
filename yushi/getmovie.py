
import firebase_admin
from firebase_admin import _FIREBASE_CONFIG_ENV_VAR, firestore
import firebase_admin
from firebase_admin import credentials


cred = credentials.Certificate('techinterview-a88b9-firebase-adminsdk-nd1jy-102817f0eb.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'techinterview-a88b9.appspot.com.appspot.com'
})

class upload_all:
    def __init__(self, uid,documentid,result_movie,result_emotion):
        self.uid = uid; 
        self.documentid = documentid; 
        self.result_movie = result_movie; 
        self.result_emotion = result_emotion; 


    def upload_movie(self):
        db = firestore.client()
        doc_ref = db.collection('user').document(self.uid).collection('result').document(self.documentid)
        return doc_ref.update({
            'movie_url': self.result_movie
            })
            
    def upload_result(self):
        db = firestore.client()
        doc_ref = db.collection('user').document(self.uid).collection('result').document(self.documentid)
        doc_ref.update({
            'result': result_emotion,
            })

result_emotion={"anger":0.07870,"contempt":0.078709,"disgust":0.078709,"fear":0.000000,"happiness":99.134199,"sadness":0.511610,"surprise":0.118064}

# 呼び出し（引数＝ユーザーID、documentID、動画URL,分析結果の配列）
upload_all("q0REUe0hbYbacVskUlgVQKz1pd33","BJaroA3FiEJpO9JKjYqZ","aaaaaa",result_emotion).upload_movie()

upload_all("q0REUe0hbYbacVskUlgVQKz1pd33","BJaroA3FiEJpO9JKjYqZ","aaaaaa",result_emotion).upload_result()

