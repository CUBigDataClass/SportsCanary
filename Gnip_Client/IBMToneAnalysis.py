import os
import requests
import json
from requests.auth import HTTPBasicAuth


class ToneAnalyzer:
    def __init__(self):
        self.username = os.environ['IBM_USERNAME']
        self.password = os.environ['IBM_PASSWORD']

    def query_ibm_for_tone(self, tweet):
        try:
            payload = {"text": str(tweet)}
            header = {'Content-Type': 'application/json'}
            r = requests.post('https://gateway.watsonplatform.net/tone-analyzer-beta/api/v3/tone?version=2016-02-11',
                              auth=HTTPBasicAuth(self.username, self.password),
                              json=payload, headers=header)
            json_blob = json.loads(r.content)
            emotion_tones = json_blob['document_tone']['tone_categories'][0]['tones']
            anger = 0.0
            disgust = 0.0
            fear = 0.0
            joy = 0.0
            sadness = 0.0
            for index, tone in enumerate(emotion_tones):
                if index == 0:
                    anger = str(tone['score'])
                if index == 1:
                    disgust = str(tone['score'])
                if index == 2:
                    fear = str(tone['score'])
                if index == 3:
                    joy = str(tone['score'])
                if index == 4:
                    sadness = str(tone['score'])

            print anger, disgust, fear, joy, sadness
            return anger, disgust, fear, joy, sadness

        except:
            return None
