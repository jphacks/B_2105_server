# Tech.面接


![Tayzer](https://user-images.githubusercontent.com/63713624/139520215-b30afad8-357e-498e-afb4-424b8eb3651e.png)

## 製品概要
### 背景(製品開発のきっかけ、課題等）
#### 我々23卒世代が特に今年頭を抱えたリモート面接の対策に課題はありました。リモート面接の対策なんてどうしたらいいのだろうか。相手にどんなふうに表情が伝わっているのか、友達と練習するにもリモートだとなあ。。時間を撮ってもらうのも申し訳ないし。。そういった悩みを課題点として考えました。
### 製品説明（具体的な製品の説明）
#### リモート面接のアップデートを図るwebアプリケーションです。Github/Googleアカウントよりアカウントを作っていただき、「模擬面接モード」「練習モード」
### 特長
####1. FaceAPIによる感情データ分析
####2. 重回帰分析を用いた独自で開発した印象分析モデル
####3. それらの数値をGraph.jsによりグラフ化

### 今後の展望
* 学生エンジニアの7割がこのwebサービスを通して練習する
* サンプルを集めて印象データの精度を高める

### 注力したこと（こだわり等）
* AI によるデータ分析
* 

## 開発技術
### 活用した技術
#### API・データ
* Microsoft Azure Face API
* 画像に対しての印象アンケートデータ

#### フレームワーク・ライブラリ・モジュール
* FastAPI
* OpenCV

#### インフラ・開発ツール
* Google Cloud Platform (CloudRun)
* Github Actions for auto deploying to CloudRun


### 独自技術
#### 印象予測機能
* Face API を活用して画像から感情のデータを獲得した。そして、「誠実そう」、「自信ある」、「リーダーシップありそう」、「一緒に働きたい」、「緊張しているように見える」、「不安そうに見える」と言ったアンケートからの印象データを目的変数とし、重回帰分析を行うことで、感情データから印象を予測できるモデルを作成した。
* <img width="624" alt="Screen Shot 2021-10-30 at 10 16 11" src="https://user-images.githubusercontent.com/78252529/139518017-a41bea5f-1b22-47fc-a2d4-603ece78ffe6.png">



## Before you begin

- 必要なライブラリをインストール
```
pip install -r requirements.txt
```
- 認証ファイルをappの配下に入れる
## Start Docker

```
docker compose up -d --build
```

## Deploy to Google Cloud run

```
gloud deploy run
```
