from fastapi import FastAPI, File, UploadFile, BackgroundTasks, Form, Depends
from fastapi.openapi.utils import get_openapi
from gcloud import storage
from secrets import token_hex
from firebase_client import FirebaseClient
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from emotion_api import emotion_api
from schemas import User, ReviewInterview, InterviewRequests, Interview
from typing import Optional, List

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

firebase_client = FirebaseClient()
storage_client = storage.Client.from_service_account_json('secret/cred.json', "jp-hacks-332107")


def upload_to_bucket(data, uid, document_id):
    """ Upload data to a bucket"""
    filename = token_hex(8)
    bucket = storage_client.get_bucket("interview-logs")
    blob = bucket.blob(f"{uid}/{filename}.mp4")
    blob.upload_from_string(data=data, content_type="video/mp4")

    firebase_client.upload_movie_id(document_id=document_id, result_movie=filename)

    """ Start analysis"""
    # with open("temp.mp4", 'wb') as f:
    #     f.write(data)
    # result_emotion, result_impression = emotion_api("temp.mp4")
    #
    # firebase_client.upload_result(document_id=document_id, result_emotions=result_emotion,
    #                               result_impressions=result_impression)


@app.get('/')
def health():
    return {"status": "JP HACKS!"}


@app.post('/create_interview', status_code=201, response_model=Interview, summary="面接sessionを作成してidを返す")
async def create_interview(background_tasks: BackgroundTasks,
                           uid=Depends(firebase_client.get_current_user),
                           file: UploadFile = File(...)):
    """
    Adds upload_movie task to worker queue.
    """
    if file.content_type != 'video/mp4':
        return {
            'file content error': f'please upload video/mp4 content file. your uploaded file is {file.content_type} content.'}
    data = file.file.read()
    interview_id = firebase_client.create_document(uid)
    background_tasks.add_task(upload_to_bucket, data, {uid}, interview_id)
    return Interview(interview_id=interview_id)


@app.get('/download_video', summary="動画をダウンロード")
async def download_video(video_id=str):
    uid = "test"
    filename = f"{uid}/{video_id}.mp4"
    bucket = storage_client.get_bucket("interview-logs")
    # print(filename)
    blob = bucket.blob(filename)
    blob.download_to_filename(f"temp/{video_id}.mp4")
    return FileResponse(f"temp/{video_id}.mp4")


@app.get('/get_mentors', response_model=List[User], summary="面接官リスト")
def get_mentors():
    mentor = User(id="test",
                  name="test",
                  email="test",
                  affiliation="test",
                  age=22,
                  introduction="自己紹介入ります",
                  skills=["Javascript"]
                  )
    return [mentor]


@app.get('/search_mentors', response_model=List[User], summary="面接官を検索")
def search_mentor(name: Optional[str] = "Sample user", affiliation: Optional[str] = "Tech uni"):
    mentor = User(id="test",
                  name=name,
                  email="test",
                  affiliation=affiliation,
                  age=22,
                  introduction="自己紹介入ります",
                  skills=["Javascript"]
                  )
    return [mentor]


@app.post('/create_user', summary="ユーザーアカウント作成時に一応ユーザープロフィールを送信しておく")
def create_user(user: User):
    return {'result': f"User is created with name {user.name}"}


@app.get('/user_info', response_model=User,
         summary="ユーザー情報取得",
         description="面接官アカウントの場合は自分にレビュー依頼する一般ユーザーのみ情報を取得できる\n一般アカウントの場合は面接官アカウントの情報しか取得できない")
def get_user_info(user_id: str):
    return {}


@app.get('/my_info', response_model=User, summary="自分のプロフィール情報を取得")
def get_my_info():
    return {}


@app.put('/my_info', response_model=User, summary="自分のプロフィール情報を修正")
def edit_my_info():
    return {}


@app.post('/request_review', summary="指定した面接官にコメントを依頼する")
def request_interview(mentor_id: str, interview_id: str):
    # Create review in firestore
    return {'result': 'Wait for review'}


@app.get('/interviews_requests', response_model=List[InterviewRequests], summary="自分宛の面接コメント依頼一覧")
def get_interviews_requests():
    interview_request = InterviewRequests(interview_id="abc", user_id="abc")
    return [interview_request]


@app.post('/review', summary="面接にコメントをつける（面接官アカウント用)")
def post_interview_review(review_item: ReviewInterview):
    return {'result': 'Comment saved'}


@app.get('/reviewed_interviews', response_model=List[ReviewInterview], summary="過去に自分がコメントつけた面接一覧（面接官アカウント用)")
def get_reviewed_interviews():
    review_interview = ReviewInterview(interview_id="abc", comment="test")
    return [review_interview]
