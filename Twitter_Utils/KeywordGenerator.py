import os
import simplejson as json


class KeywordGenerator:
    def __init__(self):
        self.team_data_path = os.getcwd() + '/Twitter_Utils/data/teams-data.json'

    def generate_search_terms(self, team_id):
        """
        Creates list of key words to search for.
        :param team_id: id of team, given by Stattleship API
        :return: returns list of key words
        """
        # TODO - Add exception handler
        with open(self.team_data_path, 'r') as f:
            data = json.loads(f.read())
        f.close()

        search_terms_list = []
        team_data = data['teams']
        for team in team_data:
            if team['id'] == team_id:
                if team['hashtag']:
                    search_terms_list.append(team['hashtag'])

                for hashtag in team['hashtags']:
                    search_terms_list.append(hashtag)

                if team['nickname']:
                    search_terms_list.append(team['nickname'])
                if team['name']:
                    search_terms_list.append(team['name'])

        search_terms_list = self.append_word_with_go_to_list(search_terms_list)
        return search_terms_list

    @staticmethod
    def append_word_with_go_to_list(word_list):
        # TODO - Refactor this
        search_terms_list_with_go = []
        for word in word_list:
            search_terms_list_with_go.append('go' + word)

        word_list += search_terms_list_with_go
        return word_list
