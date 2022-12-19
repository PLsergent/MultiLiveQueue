import json
import os

PATH = "./data/"
PATH_PLAYER = "./data/players/"

def is_player_registered(username):
    username = fix_username(username)
    for path in os.listdir(PATH_PLAYER):
        if username == path[:-5]:
            return True
    return False

def register_player(username):
    filename = fix_username(username)
    if not is_player_registered(username):
        open(PATH_PLAYER + filename + ".json", "x")
        with open(PATH_PLAYER + filename + ".json", "w+") as f:
            data = {
                "username": username,
                "rank": "D",
                "ranking_points": 0,
                "matches_played": 0,
                "matches_won": 0,
                "matches_lost": 0,
                "matches_abandoned": 0
            }
            json.dump(data ,f)
            add_player_to_rank(username, "D")
        return data

def add_player_to_rank(username, rank):
    with open(PATH + "ranks.json", "r") as f:
        ranks = json.load(f)
        ranks[rank].append(username)
    with open(PATH + "ranks.json", "w") as f:
        json.dump(ranks ,f)

def get_player(username):
    filename = fix_username(username)
    if is_player_registered(username):
        with open(PATH_PLAYER + filename + ".json", "r") as f:
            return json.load(f)
    else:
        return register_player(username)

def fix_username(username):
    username = username.replace(" ", "_")
    username = username.replace("/", "-")
    return username