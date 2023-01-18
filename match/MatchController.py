import uuid
import os
import random
import json
from user.UserController import UserController


PATH_MATCH = "./data/matches/"

class MatchController:
    def __init__(self, uuid: str, queue_type=None, players=None):
        if not queue_type and not players:
            # Match already exists
            match = self.get_match(uuid)
            self.id = match["id"]
            self.players = match["players"]
            self.available_players = self.players
            self.queue_type = match["queue_type"]
            self.status = match["status"]
            self.team1 = match["team1"]
            self.team2 = match["team2"]
        else:
            # New match
            self.id = uuid
            self.queue_type = queue_type
            self.available_players = players
            self.players = players
            self.status = "Init"
            self.team1 = []
            self.team2 = []
            self.register_match()
    
    def get_match(self, uuid: str):
        if self.is_match_registered():
            with open(PATH_MATCH + uuid + ".json", "r") as f:
                return json.load(f)
        return None

    def is_match_registered(self):
        for path in os.listdir(PATH_MATCH):
            if self.id == path[:-5]:
                return True
        return False
    
    def register_match(self):
        if not self.is_match_registered():
            open(PATH_MATCH + self.id + ".json", "x")
            with open(PATH_MATCH + self.id + ".json", "w+") as f:
                data = {
                    "id": self.id,
                    "queue_type": self.queue_type,
                    "players": self.players,
                    "available_players": self.available_players,
                    "status": "Waiting",
                    "team1": [],
                    "team2": [],
                }
                json.dump(data, f)
            return data
    
    def create_teams(self):
        random.shuffle(self.available_players)
        if self.queue_type == "random_queue" or self.queue_type == "casual":
            self.create_random_teams()
        elif self.queue_type == "captain_queue":
            self.create_captain_teams()
        self.status = "Ready"
        self.write_match()
    
    def create_random_teams(self):
        self.team1 = self.available_players[:2]
        self.team2 = self.available_players[2:]
        self.available_players = []
        self.write_match()
    
    def create_captain_teams(self):
        self.team1 = [self.available_players[0]]
        self.available_players = self.available_players[1:]
        self.write_match()
    
    def pick_mate(self, username):
        if self.queue_type == "captain_queue":
            self.team1.append(username)
            self.available_players.remove(username)
            self.team2 = self.available_players
            self.available_players = []
            self.status = "Ready"
            self.write_match()
    
    def get_teams(self):
        return (self.team1, self.team2)
    
    def report_winner(self, username, knockouts_winner, knockouts_loser):
        diff = knockouts_winner - knockouts_loser
        if username in self.team1:
            self.increase_rank_points(self.team1, diff)
            self.decrease_rank_points(self.team2, diff)
        elif username in self.team2:
            self.increase_rank_points(self.team2, diff)
            self.decrease_rank_points(self.team1, diff)
        self.status = "Finished"
        self.write_match()
    
    def report_loser(self, username, knockouts_winner, knockouts_loser):
        diff = knockouts_winner - knockouts_loser
        if username in self.team1:
            self.decrease_rank_points(self.team1, diff)
            self.increase_rank_points(self.team2, diff)
        elif username in self.team2:
            self.decrease_rank_points(self.team2, diff)
            self.increase_rank_points(self.team1, diff)
        self.status = "Finished"
        self.write_match()
    
    def increase_rank_points(self, team, diff):
        for player in team:
            user = UserController(player)
            user.increase_rank_points(diff)
    
    def decrease_rank_points(self, team, diff):
        for player in team:
            user = UserController(player)
            user.decrease_rank_points(diff)

    def write_match(self):
        with open(PATH_MATCH + self.id + ".json", "w+") as f:
            data = {
                "id": self.id,
                "queue_type": self.queue_type,
                "players": self.players,
                "available_players": self.available_players,
                "status": self.status,
                "team1": self.team1,
                "team2": self.team2,
            }
            json.dump(data, f)
        return data
    
    def delete_match(self):
        if self.is_match_registered():
            os.remove(PATH_MATCH + self.id + ".json")
