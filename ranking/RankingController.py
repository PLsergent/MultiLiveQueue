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
        return leaderboard[:11]
    
    def get_rank(self, rank):
        with open(PATH + "ranks.json", "r") as f:
            ranks = json.load(f)
        return ranks[rank]
    
    def get_my_rank(self, username):
        user = UserController(username)
        return user.ranking
        