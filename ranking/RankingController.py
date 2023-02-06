import json

from user.UserController import UserController


PATH = "./data/"

class RankingController:
    def get_leaderboard(self):
        with open(PATH + "ranks.json", "r") as f:
            ranks = json.load(f)
        leaderboard = []
        for _, item in ranks.items():
            leaderboard.extend(item["players"])
            if len(leaderboard) >= 10:
                break
        # return first 10 players
        leaderboard.sort(key=lambda x: UserController(x).ranking_points, reverse=True)
        return leaderboard[:10]
    
    def get_full_leaderboard(self):
        with open(PATH + "ranks.json", "r") as f:
            ranks = json.load(f)
        leaderboard = []
        for _, item in ranks.items():
            leaderboard.extend(item["players"])
        leaderboard.sort(key=lambda x: UserController(x).ranking_points, reverse=True)
        return leaderboard
    
    def get_rank(self, rank):
        with open(PATH + "ranks.json", "r") as f:
            ranks = json.load(f)
        return ranks[rank]
    
    def get_player_global_ranking(self, username):
        user = UserController(username)
        leaderboard = self.get_full_leaderboard()
        return leaderboard.index(user.username)
    
    def get_my_rank(self, username):
        user = UserController(username)
        return user.ranking
        