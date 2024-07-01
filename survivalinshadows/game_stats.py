
class GameStats:
    def __init__(self):
        self.pathfinding = ''
        self.time_played = 0
        self.died = False
        self.won = False
        self.amount_paused = 0
        self.wall_bumps = 0
        self.encounters = 0
        self.chases_escaped = 0
        self.chase_times = 0

    def reset(self):
        self.pathfinding = ''
        self.time_played = 0
        self.died = False
        self.won = False
        self.amount_paused = 0
        self.wall_bumps = 0
        self.encounters = 0
        self.chases_escaped = 0
        self.chase_times = 0