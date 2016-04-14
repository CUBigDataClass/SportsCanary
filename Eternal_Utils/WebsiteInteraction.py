import requests
import datetime
import json
from Eternal_Utils.Encryption import Encryption


class WebsiteInteraction:
    def __init__(self):
        self.id = 0
        self.encryption = Encryption()

    def post_request_to_sports_canary(self, event_name, score_1, score_2, score_applicable, stattleship_slug,
                                      sport_type, team_1_percentage_win, team_2_percentage_win, team_1_name, team_2_name):
        enc = self.encryption.encrypt_node('API-Passkey')
        data = {'event_name': event_name, 'score_1': score_1,
                'score_2': score_2, 'stattleship_slug': stattleship_slug, 'event_date': datetime.datetime.now(),
                'score_applicable': score_applicable, 'sport_type': sport_type,
                'team_1_percentage_win': team_1_percentage_win, 'team_2_percentage_win': team_2_percentage_win,
                'team_1_name': team_1_name, 'team_2_name': team_2_name,
                'encrypted': str(enc),
                }

        r = requests.post('http://sportscanary.com/api/results', data=data)
        json_response = r.text
        json_response = json.loads(json_response)
        self.id = json_response['_id']
        return r.status_code

    def delete_request_to_sports_canary(self):
        r = requests.delete('http://sportscanary.com/api/results/' + str(self.id) + '/edit')
        return r.status_code
