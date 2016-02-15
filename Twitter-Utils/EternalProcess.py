import time
import datetime
from SportsData import SportsData


class EternalProcess:
    def __init__(self):
        self.start_time = time.time()
        self.tick_time_in_seconds = 60.0
        self.time_to_check_games_for_the_day = "18:55"
        self.sports_data = SportsData()

    def start_process(self):
        # This process runs once every tick_time
        while True:
            time_now = datetime.datetime.now()
            if self.time_to_check_games_for_the_day == time_now.strftime("%H:%M"):
                # making two calls to this method, should figure out python syntax to use above call
                return self.sports_data.get_nba_games_for_today()

            time.sleep(self.tick_time_in_seconds - ((time.time() - self.start_time) % self.tick_time_in_seconds))
