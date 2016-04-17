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
    def get_aws_mongo_db_admin():
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
    def get_aws_mongo_db_events():
        """
        Connects to AWS hosted MongoDB
        :return: MongoDB instance with database
        """
        uri = 'mongodb://' + CommonUtils.get_environ_variable('AWS_MONGO_USER') + ':' \
              + CommonUtils.get_environ_variable('AWS_MONGO_PASS') + '@' \
              + CommonUtils.get_environ_variable('AWS_ADDRESS')
        client = MongoClient(uri)
        return client.eventsDB

    @staticmethod
    def get_url_for_sport(sport):
        if sport == "nba":
            return 'https://www.stattleship.com/basketball/nba/'
        elif sport == "nhl":
            return 'https://www.stattleship.com/hockey/nhl/'
        elif sport == "mlb":
            return 'https://www.stattleship.com/baseball/mlb/'

    def get_slugs_of_games_that_need_updating(self):
        db = self.get_aws_mongo_db_admin()
        cursor = db.results.find({'score_1': 0, 'score_2': 0})
        list_of_documents = []
        for document in cursor:
            print(document['stattleship_slug'])
            list_of_documents.append(document)

        return list_of_documents

    def get_score_and_update_mongo(self):
        list_of_documents = self.get_slugs_of_games_that_need_updating()
        for document in list_of_documents:
            try:
                url = self.get_url_for_sport(document['stattleship_slug'][:3]) + 'game_logs?game_id=' + document['stattleship_slug']
                self.logger.info('Getting games for ' + document['stattleship_slug'])
                res = requests.get(url, headers=self.headers)
                content = json.loads(res.content)
                print(content['games'][0]['away_team_score'])
                print(content['games'][0]['home_team_score'])
                db = self.get_aws_mongo_db_admin()
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

    def retroactive_team_name_updater(self):  # pragma: no cover
        list_of_documents = self.get_documents_that_are_missing_team_names()
        for document in list_of_documents:
            try:
                game_name = document['event_name']
                print(game_name)
                teams_tuple = self.get_teams_in_game_tuple(game_name)
                db = self.get_aws_mongo_db_admin()
                result = db.results.update_one(
                    {'event_name': document['event_name']},
                    {
                        "$set": {
                            'team_1_name': teams_tuple[0],
                            'team_2_name': teams_tuple[1]
                        }
                    }
                )
                print(result)

            except KeyError:
                self.logger.error('KeyError updating team names.')
            except IndexError:
                self.logger.error('IndexError updating team names.')

    def get_documents_that_are_missing_team_names(self):
        db = self.get_aws_mongo_db_admin()
        cursor = db.results.find({'team_1_name': {'$exists': False}, 'team_2_name': {'$exists': False}})
        list_of_documents = []
        for document in cursor:
            # print(document)
            list_of_documents.append(document)

        return list_of_documents

    @staticmethod
    def get_teams_in_game_tuple(game_name):
        """
        Given a Team_1 vs Team_2 returns a tuple of Team_1, Team_2
        :param game_name: Game name in Team_1 vs Team_2
        :return: tuple of team names in string format
        """
        try:
            split_str = game_name.split(' ')
            vs_index = split_str.index('vs')
            team1_name, team2_name = split_str[vs_index - 1], split_str[vs_index + 1]
            return str(team1_name), str(team2_name)
        except ValueError:
            print('ValueError getting team names.')
        except IndexError:
            print('IndexError getting team names.')

    def get_all_documents(self):
        db = self.get_aws_mongo_db_admin()
        cursor = db.results.find()
        list_of_documents = []
        for document in cursor:
            list_of_documents.append(document)

        return list_of_documents

    def count_number_of_right_and_wrong_predictions(self):
        correct_count = 0
        wrong_count = 0
        list_of_documents = self.get_all_documents()
        for document in list_of_documents:
            # if document['score_1'] != 0 and document['score_2'] != 0:
            if document['score_1'] > document['score_2']:
                if document['team_1_percentage_win'] > document['team_2_percentage_win']:
                    correct_count += 1
                elif document['team_1_percentage_win'] < document['team_2_percentage_win']:
                    wrong_count += 1
            elif document['score_1'] < document['score_2']:
                if document['team_1_percentage_win'] < document['team_2_percentage_win']:
                    wrong_count += 1
                elif document['team_1_percentage_win'] > document['team_2_percentage_win']:
                    correct_count += 1

        print(self.get_success_percentage(correct_count, wrong_count))
        return self.get_success_percentage(correct_count, wrong_count)

    @staticmethod
    def get_success_percentage(correct, wrong):
        return (float(correct) / float(correct + wrong)) * 100

    def get_results_for_date(self, date):
        list_of_documents = self.get_all_documents()
        result_list = []
        for document in list_of_documents:
            if str(document['event_date'])[:10] == date:
                result_list.append(document['event_name'])
                print document['event_name']

        return result_list

    def get_team_ids_for_game(self, slug, sport):
        """
        Gets tuple of home and away teams for game
        :param slug: Stattleship slug
        :param sport: Sport being played, currently nba, nhl and mlb
        :return: Tuple of ID's
        """
        db = self.get_aws_mongo_db_events()
        if sport == 'nba':
            cursor = db.nba_logs.find({'slug': slug})
            for document in cursor:
                return document['home_team_id'], document['away_team_id']

        elif sport == 'nhl':
            cursor = db.nhl_logs.find({'slug': slug})
            for document in cursor:
                return document['home_team_id'], document['away_team_id']

        elif sport == 'mlb':
            cursor = db.mlb_logs.find({'slug': slug})
            for document in cursor:
                return document['home_team_id'], document['away_team_id']
