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
            print json_blob
            return json_blob

        except:
            return None
