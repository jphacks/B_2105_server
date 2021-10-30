from fastapi import FastAPI, File, UploadFile, BackgroundTasks, Form, Depends
from gcloud import storage
import os
import uvicorn
from secrets import token_hex
from firebase_client import FirebaseClient
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from emotion_api import emotion_api

os.environ["GCLOUD_PROJECT"] = "ornate-genre-330308"
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
storage_client = storage.Client.from_service_account_json('cred.json')


def upload_to_bucket(data, uid, document_id, file_name):
    """ Upload data to a bucket"""
    bucket = storage_client.get_bucket("jphacks")
    blob = bucket.blob(file_name)
    blob.upload_from_string(data=data, content_type="video/mp4")

    with open("temp.mp4", 'wb') as f:
        f.write(data)
    result_emotion, result_impression = emotion_api("temp.mp4")
    id = uid.pop()
    firebase_client.upload_movie(uid=id, document_id=document_id, result_movie=file_name)
    firebase_client.upload_result(uid=id, document_id=document_id, result_emotions=result_emotion,
                                  result_impressions=result_impression)


@app.get('/')
def health():
    return {"status": "JP HACKS!"}


@app.post('/upload_movie', status_code=201)
async def upload_movie(background_tasks: BackgroundTasks,
                       uid=Depends(firebase_client.get_current_user),
                       interview_id: str = Form(...),
                       file: UploadFile = File(...)):
    """
    Adds upload_movie task to worker queue.
    """
    if file.content_type != 'video/mp4':
        return {
            'file content error': f'please upload video/mp4 content file. your uploaded file is {file.content_type} content.'}
    data = file.file.read()
    filename = f"{uid}/{token_hex(8)}.mp4"

    background_tasks.add_task(upload_to_bucket, data, {uid}, interview_id, filename)
    return {"message": "Video uploaded"}


@app.get('/download_movie')
async def download_movie(uid=Depends(firebase_client.get_current_user), movie_id: str = Form(...)):
    filename = f"{uid}/{movie_id}.mp4"
    bucket = storage_client.get_bucket("ornate-genre-330308_cloudbuild")
    blob = bucket.blob(filename)
    with open("temp.mp4", 'wb') as f:
        blob.download_to_file(f)
    return FileResponse("temp.mp4")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    port = int(os.environ.get("PORT", 8080))
    print(f"listening on port {port}")
