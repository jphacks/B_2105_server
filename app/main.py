from typing import List
from fastapi import FastAPI, File, UploadFile, BackgroundTasks, WebSocket, Form
from gcloud import storage
from os import environ
import uvicorn

# from typing import Optional
# from pydantic import BaseModel
# from fastapi.responses import HTMLResponse

app = FastAPI()


def upload_to_bucket(data, file_name):
    """ Upload data to a bucket"""
    storage_client = storage.Client.from_service_account_json('cred.json')

    bucket = storage_client.get_bucket("ornate-genre-330308_cloudbuild")
    blob = bucket.blob(file_name)
    blob.upload_from_string(data=data, content_type="video/mp4")

    return blob.public_url


@app.get('/')
def health():
    return {"status": "JP HACKS!"}


@app.post('/upload_movie', status_code=201)
async def upload_movie(background_tasks: BackgroundTasks,
                       user_id: str = Form(...),
                       question_id: str = Form(...),
                       file: UploadFile = File(...)):
    """
    Adds upload_movie task to worker queue.
    """
    if file.content_type != 'video/mp4':
        return {
            'file content error': f'please upload video/mp4 content file. your uploaded file is {file.content_type} content.'}
    data = file.file.read()
    filename = f"{user_id}/{file.filename}"
    print(question_id)

    background_tasks.add_task(upload_to_bucket, data, filename)
    return {"message": "Video uploaded"}


class ConnectionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    async def broadcast(self, data: str):
        for connection in self.connections:
            await connection.send_text(data)


manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    while True:
        data = await websocket.receive_text()
        await manager.broadcast(f"Client {client_id}: {data}")


if __name__ == "__main__":
    port = int(environ.get('PORT', 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
    print(f"listening on port {port}")
