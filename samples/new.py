import os
import io
import json
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
import requests
from PIL import Image, ImageDraw, ImageFont

"""
Example 3. Guess a person's emotion & age
| Attribute Type List
| https://docs.microsoft.com/en-us/python/api/azure-cognitiveservices-vision-face/azure.cognitiveservices.vision.face.models.faceattributetype?view=azure-python
"""

credential = json.load(open('AzureCloudKeys.json'))
API_KEY = credential['API_KEY']
ENDPOINT = credential['ENDPOINT']
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))

img_file = open('1.jpg', 'rb')

response_detection = face_client.face.detect_with_stream(
    image=img_file,
    detection_model='detection_01',
    recognition_model='recognition_04',
    return_face_attributes=['age', 'emotion'],
)

img = Image.open(img_file)
draw = ImageDraw.Draw(img)
font = ImageFont.truetype(r'C:\Windows\Fonts\OpenSans-Bold.ttf', 35)
for face in response_detection:
    age = face.face_attributes.age
    emotion = face.face_attributes.emotion
    neutral = '{0:.0f}%'.format(emotion.neutral * 100)
    happiness = '{0:.0f}%'.format(emotion.happiness * 100)
    anger = '{0:.0f}%'.format(emotion.anger * 100)
    sandness = '{0:.0f}%'.format(emotion.sadness * 100)

    rect = face.face_rectangle
    left = rect.left
    top = rect.top
    right = rect.width + left
    bottom = rect.height + top
    draw.rectangle(((left, top), (right, bottom)), outline='green', width=5)

    draw.text((right + 4, top), 'Age: ' + str(int(age)), fill=(255, 255, 255), font=font)
    draw.text((right + 4, top+35), 'Neutral: ' + neutral, fill=(255, 255, 255), font=font)
    draw.text((right + 4, top+70), 'Happy: ' + happiness, fill=(255, 255, 255), font=font)
    draw.text((right + 4, top+105), 'Sad: ' + sandness, fill=(255, 255, 255), font=font)
    draw.text((right + 4, top+140), 'Angry: ' + anger, fill=(255, 255, 255), font=font)

img.show()
img.save('test.jpg')