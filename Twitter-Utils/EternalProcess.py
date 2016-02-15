import time
import datetime
import dateutil.parser
import os
import json
from SportsData import SportsData


class EternalProcess:
    def __init__(self):
        self.start_time = time.time()
        self.tick_time_in_seconds = 60.0
        self.time_to_check_games_for_the_day = "22:48"
        self.sports_data = SportsData()
        self.base_path = str(os.getcwd()) + '/Twitter-Utils/data/daily-logs/'

    def start_process(self):
        """
        This process is our workhorse, it has to check if it should log games.
        It has to check if a game is starting and if that is the case, fork the process,
        And in that new process check for game data during the time period assigned to it.
        Probably don't have to fork it, just make a call to a different func
        """
        print 50 * '*'
        print 10 * '*' + "  STARTING SCANNING PROCESS   " + 10 * '*'
        print 50 * '*'

        while True:
            time_now = datetime.datetime.now()
            if self.time_to_check_games_for_the_day == time_now.strftime("%H:%M"):
                write_path = self.base_path + time_now.strftime("%Y-%m-%d") + '.json'
                data_to_write = self.sports_data.get_nba_games_for_today()
                with open(write_path, 'w+') as f:
                    f.write(data_to_write)
                f.close()

            # Read in file to see if it is time to analyze twitter
            read_path = self.base_path + time_now.strftime("%Y-%m-%d") + '.json'

            try:
                with open(read_path) as f:
                    data = json.load(f)
                    current_time = datetime.datetime.now().strftime("%H:%M")
                    for team in data:
                        game_time = dateutil.parser.parse(team['start_time']).strftime("%H:%M")
                        if game_time == current_time:
                            # At this point we'd want to get the twitter data, probably by first checking
                            # to see what teams are playing, generating the right words and then setting the data
                            # gatherer to get it
                            print "Time to get twitter data."

            except IOError:
                print "File not found"
            # restart loop after sleep, given by our tick_time
            time.sleep(self.tick_time_in_seconds - ((time.time() - self.start_time) % self.tick_time_in_seconds))
