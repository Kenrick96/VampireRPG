import random
player_stats = {}

class Vampire:
    def __init__(self, name, strength, speed, health, defense):
      #insert here
        self.name = name
        self.strength = strength
        self.speed = speed
        self.health = health
        self.defense = defense

    def attack(self, player_id, target):
      #get function query takes param in to select $(param) from db
        self_id = player_id
        self_stats = player_stats.get(self_id)
        self_name = self_stats['name']
        self_attack = self_stats['strength']
        target_id = target.id
        target_stats = player_stats.get(target_id)
        target_name = target_stats['name']
        target_speed = target_stats['speed']
        target_defense = target_stats['defense']
        damage = (random.randint(self_attack, 100)) - (
            (target_defense) * random.randint(1, 10))
        if (target_speed * random.randint(1, 10) > damage):
            damage = 0
        target_stats['health'] -= damage
        if damage == 0:
            return f"{self_name} attack miss!"
        else:
            return f"{self_name} attacks {target_name} and deals {damage} damage!"

    def is_alive(self, target_id):
        target_stats = player_stats.get(target_id)
        target_health = target_stats['health']
        return target_health > 0

    def exist(self, player_id):

        if player_id in player_stats:
            # Player exists
            return True
        else:
            # Player does not exist
            # Rest of the code for when the player does not exist
            return False