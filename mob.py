from character import Character
from pathfinding import Path
from sprites import IMAGE_FOR_TYPE

import random
random.seed()

ENEMY_NAMES = [('Gunther', 'he'),
        ('Woman From Baltimore, MD', 'she'),
        ('Ozymandias', 'he'),
        ('Grammy Award Winning Artist Beck', 'he'),
        ('Literally Queen Elizabeth', 'she')]

class Mob(Character):
    def __init__(self, mob_type, name, **kwargs):
        super(Mob, self).__init__(mob_type, name, **kwargs)
        self.health = 7
        self.status = "alive"
        self.path = Path()
        self.side = "evil"
        self.face = mob_type
        self.state = None

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.status = "dead"

    def move_step(self, atlas):
        self.update_status()
        if self.state == 'idle':
            direction = self.directions.get_random_direction(self.x, self.y, atlas=atlas)
        else:
            direction = self.path.get_next_step()
            if not direction:
                direction = self.directions.get_random_direction(self.x, self.y, atlas=atlas)

        self.move(atlas, direction=direction)

    def update_status(self):
        if self.path.is_far():
            self.state = "idle"
        else:
            self.state = "alert"


class Enemies(object):
    def __init__(self, x, y, atlas):
        enemies = []
        for i in range(50):
            new_enemy = Mob(IMAGE_FOR_TYPE.keys()[random.randint(0, 37)],
                    ENEMY_NAMES[i%5][0],
                    x=random.randint(0, x),
                    y=random.randint(0, y),
                    pronoun=ENEMY_NAMES[i%5][1])
            while not atlas.is_empty(new_enemy.x, new_enemy.y):
                new_enemy.x = random.randint(0, x)
                new_enemy.y = random.randint(0, y)

            atlas.place_on_tile(new_enemy, new_enemy.x, new_enemy.y)

        self.enemies = enemies

    def remove_dead_enemies(self, atlas):
        for enemy in self.enemies:
            if enemy.status == "dead":
                atlas.remove_from_tile(enemy, enemy.x, enemy.y)
                self.enemies.remove(enemy)

    def move(self, atlas, hero):
        for enemy in self.enemies:
            if not direction:
                direction = enemy.directions.get_random_direction(enemy.x, enemy.y, atlas)
            enemy.move(atlas, direction=direction)

    def __iter__(self):
        return iter(self.enemies)
