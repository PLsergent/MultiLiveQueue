import os
import json


PATH = "./data/"
PATH_PLAYER = "./data/players/"

class UserController():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = ""
        self.filename = ""
        self.in_game_username = ""
        self.ranking = ""
        self.ranking_points = ""
        self.matches_played = ""
        self.matches_won = ""
        self.matches_lost = ""
        self.matches_abandoned = ""

    def init_user(self, username):
        self.username = username
        self.filename = self.fix_username()
        self.in_game_username = self.get_player()["in_game_username"]
        self.ranking = self.get_player()["ranking"]
        self.ranking_points = self.get_player()["ranking_points"]
        self.matches_played = self.get_player()["matches_played"]
        self.matches_won = self.get_player()["matches_won"]
        self.matches_lost = self.get_player()["matches_lost"]
        self.matches_abandoned = self.get_player()["matches_abandoned"]

    def get_player(self):
        if self.is_player_registered():
            with open(PATH_PLAYER + self.filename + ".json", "r") as f:
                return json.load(f)
        else:
            return self.register_player()

    def fix_username(self):
        username = self.username.replace(" ", "_")
        username = username.replace("/", "-")
        return username

    def is_player_registered(self):
        for path in os.listdir(PATH_PLAYER):
            if self.filename == path[:-5]:
                return True
        return False

    def register_player(self):
        if not self.is_player_registered():
            open(PATH_PLAYER + self.filename + ".json", "x")
            with open(PATH_PLAYER + self.filename + ".json", "w+") as f:
                data = {
                    "username": self.username,
                    "in_game_username": "",
                    "rank": "D",
                    "ranking_points": 0,
                    "matches_played": 0,
                    "matches_won": 0,
                    "matches_lost": 0,
                    "matches_abandoned": 0,
                }
                json.dump(data, f)
                self.add_player_to_rank("D")
            return data

    def add_player_to_rank(self, rank):
        with open(PATH + "ranks.json", "r") as f:
            ranks = json.load(f)
            if self.username not in ranks[rank]:
                ranks[rank].append(self.username)
        with open(PATH + "ranks.json", "w") as f:
            json.dump(ranks, f)
    
    def add_ingame_username(self, username):
        with open(PATH_PLAYER + self.filename + ".json", "r") as f:
            data = json.load(f)
            data["in_game_username"] = username
        with open(PATH_PLAYER + self.filename + ".json", "w") as f:
            json.dump(data, f)
