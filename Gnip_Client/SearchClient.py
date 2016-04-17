import os
import json
import requests
from requests.auth import HTTPBasicAuth


class GnipSearchClient:
    def __init__(self):
        self.username = os.environ['GNIP_USERNAME']
        self.password = os.environ['GNIP_PASSWORD']
        self.url = os.environ['GNIP_URL']

    # Date is done by UTC, which is a five hour difference to EST.
    # Kobe's last game was 10:30 EST, so 2:30 AM UTC on the 14
    def initial_search(self, query, max_results, from_date, to_date):
        from_date = '201604140230'
        to_date = '201604140530'
        max_results = 10
        next = ''
        for i in range(2):
            query = '?query=' + str(query) + '&maxResults=' + str(max_results)
            date = '&fromDate=' + str(from_date) + '&toDate=' + str(to_date)
            if next == '':
                url = self.url + query + date
            else:
                url = self.url + query + date + next

            r = requests.get(url, auth=HTTPBasicAuth(self.username, self.password))
            content = json.loads(r.content)
            next = content['next']
            print(content['next'])

