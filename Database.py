import sqlite3
import time
from datetime import datetime

class DatabaseManager:
    
    def __init__(self):
        self.connection = sqlite3.connect("space_force.db")
        self.cursor = self.connection.cursor()

    def insert(self, playerName, score, timer, specialSkillUsage, destroyedEnemy):
        sql = "INSERT INTO game_result" + \
              "(player_ship, score, game_date, game_time, special_skill_usage, destroyed_normal_enemy, destroyed_armed_enemy, destroyed_boss)" + \
              "VALUES" + \
              "('{}', {}, {}, {}, {}, {}, {}, {})".format(playerName, score, int(time.time()), int(timer), specialSkillUsage, destroyedEnemy[0], destroyedEnemy[1], destroyedEnemy[2])
        self.cursor.execute(sql)
        self.connection.commit()

    def getHighScoreByShip(self, ship):
        sql = "SELECT * " + \
              "FROM game_result " + \
              "WHERE score = (SELECT MAX(score) " + \
                             "FROM game_result " + \
                             "WHERE player_ship = '" + ship + "')"
        result = self.cursor.execute(sql).fetchone()
        if result == None:
            return [ship, 0, 0, 0, 0, 0, 0, 0]
        result = list(result)
        result[2] = datetime.fromtimestamp(result[2])
        return result

    def disconnect(self):
        pass