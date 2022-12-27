import os
import json


PATH = "./data/"
PATH_PLAYER = "./data/players/"

class UserController():
    def __init__(self, username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = username
        self.filename = self.fix_username()
        player = self.get_player()
        self.in_game_username = player["in_game_username"]
        self.ranking = player["ranking"]
        self.ranking_points = player["ranking_points"]
        self.winstreak_multiplier = player["winstreak_multiplier"]
        self.current_game_id = player["current_game_id"]
        self.matches_played = player["matches_played"]
        self.matches_won = player["matches_won"]
        self.matches_lost = player["matches_lost"]
        self.matches_abandoned = player["matches_abandoned"]

    def get_player(self):
        if self.is_player_registered():
            with open(PATH_PLAYER + self.filename + ".json", "r") as f:
                return json.load(f)
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
                    "ranking": "D",
                    "ranking_points": 0,
                    "winstreak_multiplier": 1,
                    "current_game_id": "",
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
            if self.username not in ranks[rank]["players"]:
                ranks[rank]["players"].append(self.username)
        with open(PATH + "ranks.json", "w") as f:
            json.dump(ranks, f)
    
    def remove_player_from_rank(self, rank):
        with open(PATH + "ranks.json", "r") as f:
            ranks = json.load(f)
            if self.username in ranks[rank]["players"]:
                ranks[rank]["players"].remove(self.username)
        with open(PATH + "ranks.json", "w") as f:
            json.dump(ranks, f)
    
    def add_ingame_username(self, username):
        with open(PATH_PLAYER + self.filename + ".json", "r") as f:
            data = json.load(f)
            data["in_game_username"] = username
        with open(PATH_PLAYER + self.filename + ".json", "w") as f:
            json.dump(data, f)
    
    def add_current_game_id(self, game_id):
        with open(PATH_PLAYER + self.filename + ".json", "r") as f:
            data = json.load(f)
            data["current_game_id"] = game_id
        with open(PATH_PLAYER + self.filename + ".json", "w") as f:
            json.dump(data, f)

    def determine_rank(self, points):
        if points < 25:
            return "D"
        elif points < 50:
            return "C"
        elif points < 75:
            return "B"
        elif points < 100:
            return "A"
        else:
            return "S"
    
    def increase_rank_points(self, points):
        with open(PATH_PLAYER + self.filename + ".json", "r") as f:
            data = json.load(f)
            data["ranking_points"] += points * self.winstreak_multiplier
            data["winstreak_multiplier"] += 0.2
            data["current_game_id"] = ""
            data["matches_played"] += 1
            data["matches_won"] += 1
            new_rank = self.determine_rank(data["ranking_points"])
            if new_rank != data["ranking"]:
                self.add_player_to_rank(new_rank)
                self.remove_player_from_rank(data["ranking"])
            data["ranking"] = new_rank
        with open(PATH_PLAYER + self.filename + ".json", "w") as f:
            json.dump(data, f)
    
    def decrease_rank_points(self, points):
        with open(PATH_PLAYER + self.filename + ".json", "r") as f:
            data = json.load(f)
            data["ranking_points"] -= points
            data["winstreak_multiplier"] = 1
            data["current_game_id"] = ""
            data["matches_played"] += 1
            data["matches_lost"] += 1
            new_rank = self.determine_rank(data["ranking_points"])
            if new_rank != data["ranking"]:
                self.add_player_to_rank(new_rank)
                self.remove_player_from_rank(data["ranking"])
            data["ranking"] = new_rank
        with open(PATH_PLAYER + self.filename + ".json", "w") as f:
            json.dump(data, f)
    
    def abandon_match(self):
        with open(PATH_PLAYER + self.filename + ".json", "r") as f:
            data = json.load(f)
            data["matches_abandoned"] += 1
            data["current_game_id"] = ""
        with open(PATH_PLAYER + self.filename + ".json", "w") as f:
            json.dump(data, f)
