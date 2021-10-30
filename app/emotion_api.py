import os

import requests
import numpy as np
import cv2
from datetime import datetime
import pandas as pd


def emotion_api(file):
    location_videofile = file

    cap = cv2.VideoCapture(location_videofile)  # 0にするとmacbookのカメラ、1にすると外付けのUSBカメラにできる
    data_name = ["anger", "contempt", "disgust", "fear", "happiness", 'sadness', 'surprise']  # 保存データの系列
    emotion_data = [0, 0, 0, 0, 0, 0, 0]  # 初期値
    cal = [0, 0, 0, 0, 0, 0, 0]
    count = 0  # 撮影回数を示すカウンタ
    percent = None

    # 顔認識の設定
    cascade_path = 'haarcascade_frontalface_alt.xml'  # 顔判定で使うxmlファイルを指定する。(opencvのpathを指定)
    cascade = cv2.CascadeClassifier(cascade_path)

    # Faceの設定
    subscription_key = os.getenv("subscription") # ここに取得したキー１を入力
    assert subscription_key
    face_api_url = os.getenv("get url") # ここに取得したエンドポイントのURLを入力
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

    new_video = []
    new_video += sample(video, 5)
    for frame in new_video:
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
                # print(df)

            count = count + 1  # 撮影回数の更新
            df_past = df  # df_pastを更新

            cal = (df.sum(axis=1, skipna=True) / df.to_numpy().sum())
            percent = cal * 100

    honest = (-3.536945) * cal['anger'] + (-0.003553) * cal['contempt'] + (3.603171) * cal[
        'disgust'] + (-9.930411) * cal['fear'] + (2.075296) * cal['happiness'] + (4.816988) * cal[
                 'sadness'] + (3.227738) * cal['surprise'] + (0.07189923925578044)
    confidence = (0.315414) * cal['anger'] + (0.430329) * cal['contempt'] + (-0.707628) * cal[
        'disgust'] + (-9.235996) * cal['fear'] + (1.136739) * cal['happiness'] + (4.790115) * cal[
                     'sadness'] + (3.570750) * cal['surprise'] + (0.07357999007209934)
    leadership = (-2.096394) * cal['anger'] + (0.054996) * cal['contempt'] + (2.265064) * cal[
        'disgust'] + (-8.790275) * cal['fear'] + (1.941947) * cal['happiness'] + (3.659011) * cal[
                     'sadness'] + (3.342414) * cal['surprise'] + (0.051826723716245596)
    niceCowoker = (-5.196182) * cal['anger'] + (-0.381129) * cal['contempt'] + (5.767330) * cal[
        'disgust'] + (-9.043258) * cal['fear'] + (2.025452) * cal['happiness'] + (3.570378) * cal[
                      'sadness'] + (3.483190) * cal['surprise'] + (0.039110747404379254)
    anxious = (2.262031) * cal['anger'] + (0.015123) * cal['contempt'] + (-2.364740) * cal[
        'disgust'] + (5.559835) * cal['fear'] + (-1.892181) * cal['happiness'] + (-2.217211) * cal[
                  'sadness'] + (-1.223585) * cal['surprise'] + (-0.08040851038993796)
    nervous = (0.540086) * cal['anger'] + (0.068549) * cal['contempt'] + (-0.405309) * cal[
        'disgust'] + (3.006133) * cal['fear'] + (-1.562904) * cal['happiness'] + (-1.568253) * cal[
                  'sadness'] + (0.345784) * cal['surprise'] + (-0.04618933147625519)
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

    return result_emotions,result_impressions
