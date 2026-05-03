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
        self.wave_delay = 7
        self.wave_timer = 0

    def setup_wave(self):
        self.wave_complete = False
        self.upgrades_pending = False
        self.upgrade_trigger_delay = 1.0
        self.current_wave += 1
        self.enemies_spawned = 0
        self.spawn_timer = 0

        # scaling formulas
        self.enemy_count = int(self.base_count * (1.25 ** self.current_wave))
        self.spawn_interval = max(0.5, self.spawn_interval - self.current_wave * 0.003)
        self.speed_multiplier = 1.035 ** self.current_wave
        self.damage_multiplier = 1.08 ** self.current_wave

    def update(self, delta_time):
        self.spawn_timer += delta_time

        # Spawn enemies during wave
        if self.enemies_spawned < self.enemy_count:
            if self.spawn_timer >= self.spawn_interval:
                self.spawn_enemy()
                self.spawn_timer = 0
                self.enemies_spawned += 1
                return

        # next wave only when all enemies are dead
        if self.enemies_spawned >= self.enemy_count and len(self.all_enemies) == 0:
            self.wave_complete = True
            self.wave_timer += delta_time
            
            if not hasattr(self, 'upgrades_pending'):
                self.upgrades_pending = False
            self.upgrades_pending = True

            if self.wave_timer >= self.wave_delay:
                self.wave_timer = 0
                self.setup_wave()

    def spawn_enemy(self):
        spawn_locations = [
            (random.randint(0, width), - 200),
            (random.randint(0, width), height + 200),
            (-200, random.randint(0, height)),
            (width + 200, random.randint(0, height))]

        x, y = random.choice(spawn_locations)

        enemy = None
        if self.current_wave % 14 == 0:
            if self.enemies_spawned == 0:
                enemy = MotherShip()
            else:
                return
        elif self.current_wave % 7 == 0:
            if self.enemies_spawned == 0:
                enemy = ChargerBoss(x, y)
            else:
                return
        elif self.current_wave > 14 and self.current_wave % 7 == 0:
            if self.enemies_spawned == 0:
                enemy = ChargerBoss(x, y) if random.random() < 0.5 else ShooterEnemy(x, y)
            else:
                return
        elif self.current_wave > 7:
            r = random.random()

            if r < 0.1:
                enemy = EliteSeekerEnemy(x, y)
            elif r < 0.2:
                enemy = EliteShooterEnemy(x, y)
            elif r < 0.5:
                enemy = SeekerEnemy(x, y)
            elif r < 0.8:
                enemy = ShooterEnemy(x, y)
            else:
                enemy = TeleporterEnemy(x, y)
        else:
            r = random.random()

            if r < 0.3:
                enemy = SeekerEnemy(x, y)
            elif r < 0.6:
                enemy = ShooterEnemy(x, y)
            else:
                enemy = TeleporterEnemy(x, y)

        if enemy is None:
            return

        enemy.speed_multiplier = self.speed_multiplier
        enemy.damage_multiplier = self.damage_multiplier

        self.all_enemies.append(enemy)

    def remove_enemy(self, enemy):
        if enemy in self.all_enemies:
            self.all_enemies.remove(enemy)