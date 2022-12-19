from dataclasses import dataclass, field
from utils import get_player


class Queues:

    def __init__(self):
        self.ranked_queue = {
            "S": {
                "captain_queue": [],
                "random_queue": []
            },
            "A": {
                "captain_queue": [],
                "random_queue": []
            },
            "B": {
                "captain_queue": [],
                "random_queue": []
            },
            "C": {
                "captain_queue": [],
                "random_queue": []
            },
            "D": {
                "captain_queue": [],
                "random_queue": []
            }
        }
        self.casual_queue = []

    def is_in_queue(self, username):
        if username in self.casual_queue:
            return True
        
        if username in self.ranked_queue[self.get_player_rank(username)]["captain_queue"] or \
            username in self.ranked_queue[self.get_player_rank(username)]["random_queue"]:
                return True
        return False

    def add_to_ranked_queue(self, username, queue_type):
        if self.is_in_queue(username):
            return False
        self.ranked_queue[self.get_player_rank(username)][queue_type].append(username)
        return True

    def add_to_casual_queue(self, username):
        if self.is_in_queue(username):
            return False
        self.casual_queue.append(username)
        return True
    
    def remove_from_ranked_queue(self, username, queue_type):
        if not self.is_in_queue(username):
            return False
        self.ranked_queue[self.get_player_rank(username)][queue_type].remove(username)
        return True
    
    def remove_from_casual_queue(self, username):
        if not self.is_in_queue(username):
            return False
        self.casual_queue.remove(username)
        return True
    
    def get_player_rank(self, username):
        return get_player(username)["rank"]
    
    def get_my_queue(self, username):
        if username in self.casual_queue:
            return self.casual_queue
        if username in self.ranked_queue[self.get_player_rank(username)]["captain_queue"]:
            return self.ranked_queue[self.get_player_rank(username)]["captain_queue"]
        if username in self.ranked_queue[self.get_player_rank(username)]["random_queue"]:
            return self.ranked_queue[self.get_player_rank(username)]["random_queue"]
        return None
    
