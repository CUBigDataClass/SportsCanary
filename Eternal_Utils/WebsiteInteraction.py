import requests
import datetime
import json


class WebsiteInteraction:
    def __init__(self):
        self.id = 0

    def post_request_to_sports_canary(self, event_name, score_1, score_2, score_applicable):
        data = {'event_name': event_name, 'score_1': score_1,
                'score_2': score_2, 'event_date': datetime.datetime.now(),
                'score_applicable': score_applicable}
        r = requests.post('http://sportscanary.com/api/results', data=data)
        json_response = r.text
        json_response = json.loads(json_response)
        self.id = json_response['_id']
        return r.status_code

    def delete_request_to_sports_canary(self):
        r = requests.delete('http://sportscanary.com/api/results/' + str(self.id) + '/edit')
        return r.status_code
#
# web = WebsiteInteraction()
# web.post_request_to_sports_canary('Cavaliers vs Rockets', 92, 100, score_applicable=True)
# web.delete_request_to_sports_canary()
