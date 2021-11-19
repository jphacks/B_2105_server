import time

import requests
import numpy as np
import cv2
from datetime import datetime
import pandas as pd


def emotion_api(video_file):
    cap = cv2.VideoCapture(video_file)  # 0にするとmacbookのカメラ、1にすると外付けのUSBカメラにできる
    cap.get(2)
    data_name = ["anger", "contempt", "disgust", "fear", "happiness", 'sadness', 'surprise']  # 保存データの系列
    emotion_data = [0] * 7  # 初期値
    cal = [0] * 7
    count = 0  # 撮影回数を示すカウンタ
    percent = None

    # 顔認識の設定
    cascade_path = 'dataset/haarcascade_frontalface_alt.xml'  # 顔判定で使うxmlファイルを指定する。(opencvのpathを指定)
    cascade = cv2.CascadeClassifier(cascade_path)

    # Faceの設定
    subscription_key = "ea98d7f8c3054d4b8f5b6034f2a611dd"  # ここに取得したキー１を入力
    assert subscription_key
    face_api_url = "https://jphacks-emotion.cognitiveservices.azure.com/face/v1.0/detect" # ここに取得したエンドポイントのURLを入力

    from random import sample

    video = list()
    ## 実行
    while True:
        r, img = cap.read()
        if r:
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # グレースケールに変換
            faces = cascade.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=1, minSize=(
                100, 100))  # 顔判定 minSizeで顔判定する際の最小の四角の大きさを指定できる。(小さい値を指定し過ぎると顔っぽい小さなシミのような部分も判定されてしまう。)

            if len(faces) > 0:
                video.append(img)
        else:
            cap.release()
            break

    new_video = video
    # new_video += sample(video, 5)
    for frame in new_video:
        time.sleep(3)
        now = datetime.now()  # 撮影時間
        image_data = cv2.imencode('.jpg', frame)[1].tobytes()
        # image_data = open(filename, "rb").read()  # 処理をする画像を選択
        headers = {'Ocp-Apim-Subscription-Key': subscription_key,
                   'Content-Type': 'application/octet-stream'}
        params = {
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'emotion',
            'recognitionModel': 'recognition_01'
        }
        response = requests.post(face_api_url, headers=headers,
                                 params=params, data=image_data)
        response.raise_for_status()
        analysis = response.json()  # json出力
        print(analysis)

        if analysis:
            result = [analysis[0]['faceAttributes']['emotion']['anger'],
                      analysis[0]['faceAttributes']['emotion']['contempt'],
                      analysis[0]['faceAttributes']['emotion']['disgust'],
                      analysis[0]['faceAttributes']['emotion']['fear'],
                      analysis[0]['faceAttributes']['emotion']['happiness'],
                      analysis[0]['faceAttributes']['emotion']['sadness'],
                      analysis[0]['faceAttributes']['emotion']['surprise']]
            emotion_data = np.array(result) + np.array(emotion_data)

            df = pd.DataFrame({now: emotion_data}, index=data_name)  # 取得データをDataFrame1に変換しdfとして定
            if count != 0:
                df = pd.concat([df_past, df], axis=1, sort=False)  # dfを更新
                print(df)

            count = count + 1  # 撮影回数の更新
            df_past = df  # df_pastを更新

            cal = (df.sum(axis=1, skipna=True) / df.to_numpy().sum())
            percent = cal * 100

    honest = (52280.606593) * percent['anger'] + (52280.615729) * percent['contempt'] + (52279.892070) * percent[
        'disgust'] + (52280.245897) * percent['fear'] + (52280.648301) * percent['happiness'] + (52280.639561) * percent[
                 'sadness'] + (52280.638808) * percent['surprise'] + (-5228060.324772324)
    confidence = (45948.874900) * percent['anger'] + ( 45948.901872) * percent['contempt'] + (45948.562104) * percent[
        'disgust'] + (45948.671443) * percent['fear'] + (45948.945392) * percent['happiness'] + (45948.932109) * percent[
                     'sadness'] + (45948.923942) * percent['surprise'] + (-4594889.890189231)
    leadership = (-56125.315486) * percent['anger'] + (56125.291467) * percent['contempt'] + (56124.734395) * percent[
        'disgust'] + (56125.074472) * percent['fear'] + ( 56125.324700) * percent['happiness'] + (56125.313211) * percent[
                     'sadness'] + (56125.302735) * percent['surprise'] + (0-5612528.268499151)
    niceCowoker = (65148.270992) * percent['anger'] + (65148.327761) * percent['contempt'] + ( 65147.862069) * percent[
        'disgust'] + (-65148.065374) * percent['fear'] + (65148.362371) * percent['happiness'] + (65148.353771) * percent[
                      'sadness'] + (65148.348149) * percent['surprise'] + (-6514832.054117618)
    anxious = (-4042.326116) * percent['anger'] + (-4042.233209) * percent['contempt'] + (-4042.249229) * percent[
        'disgust'] + (-4042.504887) * percent['fear'] + (-4042.254423) * percent['happiness'] + (-4042.239087) * percent[
                  'sadness'] + (-4042.235853) * percent['surprise'] + (404227.11271251354)
    nervous = (-44771.912270) * percent['anger'] + (-44771.819912) * percent['contempt'] + ( -44771.836730) * percent[
        'disgust'] + (-44772.024092) * percent['fear'] + (-44771.841884) * percent['happiness'] + ( -44771.832570) * percent[
                  'sadness'] + (-44771.824220) * percent['surprise'] + (4477185.820396536)
    honest = (honest / 6) * 100
    confidence = (confidence / 6) * 100
    leadership = (leadership / 6) * 100
    niceCowoker = (niceCowoker / 6) * 100
    anxious = (anxious / 6) * 100
    nervous = (nervous / 6) * 100

    result_emotions = {"anger": percent[0],
                       "contempt": percent[1],
                       "disgust": percent[2],
                       "fear": percent[3],
                       "happiness": percent[4],
                       'sadness': percent[5],
                       'surprise': percent[6]
                       }

    result_impressions = {"honest": honest, "confidence": confidence,
                          "leadership": leadership, "anxious": anxious, "niceCoworker": niceCowoker,
                          "nervous": nervous}

    print(result_emotions)


if __name__ == "__main__":
    emotion_api("../samples/sample.mp4")
