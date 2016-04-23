class Game(object):  # pragma: no cover
    def __init__(self, json_game_type):
        self.data = json_game_type
        self.games = []
        try:
            self.name = self.data["eventType"]["name"]
        except KeyError:
            self.name = None
            print 'error getting game name'

        try:
            self.id = self.data["eventType"]["id"]
        except KeyError:
            self.id = None
            print 'error getting game id'

        try:
            self.market_count = self.data["marketCount"]
        except KeyError:
            self.market_count = None
            print 'error getting game market count'

    def add_games(self, games):
        self.games.append(games)

    def clear_game(self):
        self.games = []

    def __str__(self):

        str_game = ""
        if self.name is not None:
            str_game += self.name.encode('utf-8') + ": "
        for g in self.games:
            str_game += str(g) + ", "

        return str_game
