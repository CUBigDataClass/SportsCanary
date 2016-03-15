import json
import datetime
import requests
from pymongo import MongoClient
from Eternal_Utils.CommonUtils import CommonUtils


class MarchMadness:
    def __init__(self):
        pass

    @staticmethod
    def get_march_madness_games_for_the_day():
        r = requests.get('http://sportscanary.com/api/march_madness/games?date=today')
        json_response = json.loads(r.text)
        print json_response
        return json_response

    def write_days_games_data(self):  # pragma: no cover
        """
        Writes API response containing info for days games
        """
        uri = 'mongodb://' + CommonUtils.get_environ_variable('AWS_MONGO_USER') + ':' \
              + CommonUtils.get_environ_variable('AWS_MONGO_PASS') + '@' \
              + CommonUtils.get_environ_variable('AWS_ADDRESS')
        client = MongoClient(uri)
        db = client.eventsDB
        data_to_write = self.get_march_madness_games_for_the_day()
        db.mm_games.insert(data_to_write)

    @staticmethod
    def return_games_for_the_day():
        uri = 'mongodb://' + CommonUtils.get_environ_variable('AWS_MONGO_USER') + ':' \
              + CommonUtils.get_environ_variable('AWS_MONGO_PASS') + '@' \
              + CommonUtils.get_environ_variable('AWS_ADDRESS')
        client = MongoClient(uri)
        db = client.eventsDB
        data = []
        for post in db.mm_games.find():
            if post['normalized_date'] == datetime.datetime.now().strftime('%Y-%m-%d'):
                data.append(post)
        return data

    @staticmethod
    def update_is_streamed_json(game):
        """
        Replaces json file to reflect that game is being streamed
        :param game:
        """
        game_id = game["_id"]
        uri = 'mongodb://' + CommonUtils.get_environ_variable('AWS_MONGO_USER') + ':' \
              + CommonUtils.get_environ_variable('AWS_MONGO_PASS') + '@' \
              + CommonUtils.get_environ_variable('AWS_ADDRESS')
        client = MongoClient(uri)
        db = client.eventsDB
        if game["being_streamed"]:
            db.mm_games.update({'_id': game_id}, {"$set": {"being_streamed": False}}, upsert=False)
        else:
            db.mm_games.update({'_id': game_id}, {"$set": {"being_streamed": False}}, upsert=False)
