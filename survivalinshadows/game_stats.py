class GameStats:
    def __init__(self):
        #player stats
        self.time_played = 0
        self.died = False
        self.won = False
        self.amount_paused = 0
        self.encounters = 0
        self.chases_escaped = 0
        self.avg_heartbeat = 0
        self.most_often_mood = 'null'
        self.rarest_mood = 'null'
        self.total_distance_travelled = 0 
        self.stamina_used = 0 
        self.player_distance_sprinted = 0 
        #enemy stats
        self.pathfinding = '' 
        self.chase_times = 0
        self.pathfinding_length = 0
        self.total_enemy_distance_travelled_sprint = 0
        #
        self.nodes_explored = 0