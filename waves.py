from settings import *
from enemy import *
import random

class WaveManager:
    def __init__(self):
        self.current_wave = 0
        self.spawn_timer = 0
        self.enemies_spawned = 0
        self.all_enemies = []

        self.base_count = 3
        self.spawn_interval = 1.5
        self.setup_wave()
        
        self.wave_complete = False
        self.wave_delay = 3
        self.wave_timer = 0

    def setup_wave(self):
        self.wave_complete = False
        self.current_wave += 1
        self.enemies_spawned = 0
        self.spawn_timer = 0

        # scaling formulas
        self.enemy_count = int(self.base_count * (1.25 ** self.current_wave))
        self.spawn_interval = max(0.25, self.spawn_interval - self.current_wave * 0.005)
        self.speed_multiplier = 1.05 ** self.current_wave
        self.damage_multiplier = 1.08 ** self.current_wave

    def update(self, delta_time):
        self.spawn_timer += delta_time

        # spawn enemies over time
        if self.enemies_spawned < self.enemy_count:
            if self.spawn_timer >= self.spawn_interval:
                self.spawn_enemy()
                self.spawn_timer = 0
                
                self.enemies_spawned += 1

        # next wave only when all enemies are dead
        if self.enemies_spawned >= self.enemy_count and len(self.all_enemies) == 0:
            self.wave_complete = True
            self.wave_timer += delta_time

            if self.wave_timer >= self.wave_delay:
                self.wave_timer = 0
                self.setup_wave()

    def spawn_enemy(self):
        spawn_locations = [
            (random.randint(0, width), -100),
            (random.randint(0, width), height + 100),
            (-100, random.randint(0, height)),
            (width + 100, random.randint(0, height))
        ]

        x, y = random.choice(spawn_locations)

        # scale difficulty per wave
        enemy_type_roll = random.random()

        if enemy_type_roll < 0.3:
            enemy = SeekerEnemy(x, y)
        if enemy_type_roll < 0.6:
            enemy = ShooterEnemy(x, y)
        else:
            enemy = TeleporterEnemy(x, y)

        enemy.speed_multiplier = self.speed_multiplier
        enemy.damage_multiplier = self.damage_multiplier
        self.all_enemies.append(enemy)

    def remove_enemy(self, enemy):
        if enemy in self.all_enemies:
            self.all_enemies.remove(enemy)