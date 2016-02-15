import time
import datetime
import os
from SportsData import SportsData


class EternalProcess:
    def __init__(self):
        self.start_time = time.time()
        self.tick_time_in_seconds = 60.0
        self.time_to_check_games_for_the_day = "20:10"
        self.sports_data = SportsData()
        self.base_path = str(os.getcwd()) + '/Twitter-Utils/data/daily-logs/'

    def start_process(self):
        while True:
            time_now = datetime.datetime.now()
            if self.time_to_check_games_for_the_day == time_now.strftime("%H:%M"):
                write_path = self.base_path + time_now.strftime("%Y-%m-%d-%H:%M") + '.txt'
                data_to_write = self.sports_data.get_nba_games_for_today()
                with open(write_path, 'w+') as f:
                    f.write(data_to_write)
                f.close()

            time.sleep(self.tick_time_in_seconds - ((time.time() - self.start_time) % self.tick_time_in_seconds))
