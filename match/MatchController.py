import uuid
import os
import random
import json
from user.UserController import UserController


PATH_MATCH = "./data/matches/"

class MatchController:
    def __init__(self, uuid, queue_type=None, players=None):
        if not queue_type and not players:
            self.id = self.get_match(uuid)["id"]
            self.players = self.get_match(uuid)["players"]
            self.queue_type = self.get_match(uuid)["queue_type"]
            self.status = self.get_match(uuid)["status"]
            self.team1 = self.get_match(uuid)["team1"]
            self.team2 = self.get_match(uuid)["team2"]
        else:
            self.id = uuid
            self.queue_type = queue_type
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
                    "status": "Waiting",
                    "team1": [],
                    "team2": [],
                }
                json.dump(data, f)
            return data
    
    def create_teams(self):
        random.shuffle(self.players)
        if self.queue_type == "random":
            self.create_random_teams()
        elif self.queue_type == "captain":
            self.create_captain_teams()
        self.status = "Ready"
    
    def create_random_teams(self):
        self.team1 = self.players[:2]
        self.team2 = self.players[2:]
        self.players = []
    
    def create_captain_teams(self):
        self.team1 = [self.players[0]]
        self.players = self.players[1:]
    
    def pick_mate(self, username):
        if self.queue_type == "captain":
            self.team1.append(username)
            self.players.remove(username)
            self.team2 = self.players
            self.players = []
    
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
    
    def report_loser(self, username, knockouts_winner, knockouts_loser):
        diff = knockouts_winner - knockouts_loser
        if username in self.team1:
            self.decrease_rank_points(self.team1, diff)
            self.increase_rank_points(self.team2, diff)
        elif username in self.team2:
            self.decrease_rank_points(self.team2, diff)
            self.increase_rank_points(self.team1, diff)
        self.status = "Finished"
    
    def increase_rank_points(self, team, diff):
        for player in team:
            user = UserController()
            user.init_user(player)
            user.increase_rank_points(diff)
    
    def decrease_rank_points(self, team, diff):
        for player in team:
            user = UserController()
            user.init_user(player)
            user.decrease_rank_points(diff)


