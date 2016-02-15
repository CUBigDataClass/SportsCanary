import time
import datetime
import dateutil.parser
import os
import json
from SportsData import SportsData
from DataGatherer import DataGatherer
from KeywordGenerator import KeywordGenerator


class EternalProcess:
    def __init__(self):
        self.sports_data = SportsData()
        self.keyword_generator = KeywordGenerator()
        self.start_time = time.time()
        self.tick_time_in_seconds = 60.0
        self.time_to_check_games_for_the_day = "15:01"
        self.base_path = os.getcwd() + '/Twitter-Utils/data/daily-logs/'
        self.APP_KEY = os.environ['TWITTER_APP_KEY']
        self.APP_SECRET = os.environ['TWITTER_APP_SECRET']
        self.OAUTH_TOKEN = os.environ['TWITTER_OAUTH_TOKEN']
        self.OAUTH_TOKEN_SECRET = os.environ['TWITTER_OAUTH_TOKEN_SECRET']

    def start_process(self):
        """
        This process is our workhorse, it has to check if it should log games.
        It has to check if a game is starting and if that is the case, fork the process,
        And in that new process check for game data during the time period assigned to it.
        Probably don't have to fork it, just make a call to a different func
        """
        print 50 * '*' + '\n' + 10 * '*' + "  STARTING SCANNING PROCESS   " + 10 * '*' + '\n' + 50 * '*'

        # TODO - Add IOError as excpetion so our process doesn't crash
        while True:
            print "Round"
            time_now = datetime.datetime.now()
            if self.time_to_check_games_for_the_day == time_now.strftime('%H:%M'):
                write_path = self.base_path + time_now.strftime('%Y-%m-%d') + '.json'
                data_to_write = self.sports_data.get_nba_games_for_today()
                with open(write_path, 'w+') as f:
                    f.write(data_to_write)
                f.close()

            # Read in file to see if it is time to analyze twitter
            read_path = self.base_path + time_now.strftime('%Y-%m-%d') + '.json'

            try:
                with open(read_path) as f:
                    data = json.load(f)
                    current_time = datetime.datetime.now().strftime('%H:%M')
                    for idx, game in enumerate(data):
                        game_time = dateutil.parser.parse(game['start_time']).strftime('%H:%M')
                        if game_time == current_time:
                            # At this point we'd want to get the twitter data, probably by first checking
                            # to see what teams are playing, generating the right words and then setting the data
                            # gatherer to get it
                            if not game['being_streamed']:
                                self.update_is_streamed_json(index=idx)
                                print "Time to get twitter data."
                                data_gather = DataGatherer(self.APP_KEY, self.APP_SECRET,
                                                           self.OAUTH_TOKEN, self.OAUTH_TOKEN_SECRET)

                                # TODO - Refactor this
                                search_terms_home = self.keyword_generator.generate_search_terms(game['home_team_id'])
                                search_terms_away = self.keyword_generator.generate_search_terms(game['away_team_id'])
                                keyword_string_home = ', '.join(search_terms_home)
                                keyword_string_away = ', '.join(search_terms_away)

                                keyword_string = keyword_string_home + ', ' + keyword_string_away
                                game_name = datetime.datetime.now().strftime('%Y-%m-%d') + '-' + game['title'].replace(' ', '-')

                                data_gather.get_tweet_stream(keyword_string, game['uuid'], game_name)

            except IOError:
                print 'File not found'

            # restart loop after sleep, given by our tick_time
            time.sleep(self.tick_time_in_seconds - ((time.time() - self.start_time) % self.tick_time_in_seconds))

    def update_is_streamed_json(self, index):
        time_now = datetime.datetime.now()
        read_path = self.base_path + time_now.strftime('%Y-%m-%d') + '.json'
        try:
            json_file = open(read_path, "r")
            data = json.load(json_file)
            json_file.close()

            data[index]['being_streamed'] = True

            json_file = open(read_path, "w+")
            json_file.write(json.dumps(data))
            json_file.close()
            
        except IOError:
                print 'File not found'
