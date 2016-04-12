import json
import logging
import requests
from CommonUtils import CommonUtils
from pymongo import MongoClient


class ScoreUpdater:
    def __init__(self):
        self.CLIENT_ID = CommonUtils.get_environ_variable('STAT_CLIENT_ID')
        self.STAT_CLIENT_SECRET = CommonUtils.get_environ_variable('STAT_CLIENT_SECRET')
        self.STAT_ACCESS_TOKEN = CommonUtils.get_environ_variable('STAT_ACCESS_TOKEN')
        self.logger = logging.getLogger(__name__)
        self.headers = {
            'Authorization': str(self.STAT_ACCESS_TOKEN),
            'Accept': 'application/vnd.stattleship.com; version=1',
            'Content-Type': 'application/json'
        }

    @staticmethod
    def get_aws_mongo_db():
        """
        Connects to AWS hosted MongoDB
        :return: MongoDB instance with database
        """
        uri = 'mongodb://' + CommonUtils.get_environ_variable('AWS_MONGO_USER') + ':' \
              + CommonUtils.get_environ_variable('AWS_MONGO_PASS') + '@' \
              + CommonUtils.get_environ_variable('AWS_ADDRESS')
        client = MongoClient(uri)
        return client.admin

    @staticmethod
    def get_url_for_sport(sport):
        if sport == "nba":
            return 'https://www.stattleship.com/basketball/nba/'
        elif sport == "nhl":
            return 'https://www.stattleship.com/hockey/nhl/'
        elif sport == "mlb":
            return 'https://www.stattleship.com/baseball/mlb/'

    def get_slugs_of_games_that_need_updating(self):
        db = self.get_aws_mongo_db()
        cursor = db.results.find({'score_1': 0, 'score_2': 0})
        list_of_documents = []
        for document in cursor:
            print(document['stattleship_slug'])
            list_of_documents.append(document)

        return list_of_documents

    def get_scores_for_list_of_slugs(self):
        list_of_documents = self.get_slugs_of_games_that_need_updating()
        try:
            for document in list_of_documents:
                url = self.get_url_for_sport(document['stattleship_slug'][:3]) + 'game_logs?game_id=' + document['stattleship_slug']
                self.logger.info('Getting games for ' + document['stattleship_slug'])
                res = requests.get(url, headers=self.headers)
                content = json.loads(res.content)
                print(content['games'][0]['away_team_score'])
                print(content['games'][0]['home_team_score'])
                db = self.get_aws_mongo_db()
                result = db.results.update_one(
                            {'stattleship_slug': document['stattleship_slug']},
                            {
                                "$set": {
                                    'score_1': content['games'][0]['away_team_score'],
                                    'score_2': content['games'][0]['home_team_score']
                                },
                            }
                        )
                print(result)
        except KeyError:
            self.logger.error('KeyError updating scores.')
        except IndexError:
            self.logger.error('IndexError updating scores.')
