
class Games(object):
    def __init__(self, json_game_details):
        data = json_game_details
        try:
            self.name = data["event"]["name"]
        except KeyError:
            self.name = None
            print 'error getting game name'

        try:
            self.event_time = data["event"]["openDate"]
        except KeyError:
            self.event_time = None
            print 'error getting game date'

        try:
            self.event_time_zone = data["event"]["timezone"]
        except KeyError:
            self.event_time_zone = None
            print 'error getting timezone'

        try:
            self.country_code = data["event"]["countryCode"]
        except KeyError:
            self.country_code = None
            print 'error getting country code'

    def get_game_name(self):
        return self.name

    def get_game_time_zone(self):
        return self.event_time_zone

    def get_game_time(self):
        return self.event_time

    def get_game_country_code(self):
        return self.country_code

    def __str__(self):
        str_game = ""
        if self.get_game_name() is not None:
            str_game = self.name.encode('utf-8')
        if self.get_game_time() is not None:
            str_game += " " + self.event_time.encode('utf-8')
        if self.get_game_time_zone() is not None:
            str_game += " " + self.event_time_zone.encode('utf-8')
        if self.country_code is not None:
            str_game += " " + self.country_code.encode('utf-8')
        return str_game



