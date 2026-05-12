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
        self.spawn_interval = 1.75
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
        self.wave_timer = 0

        self.is_boss_wave = (self.current_wave % 10 == 0)

        if self.is_boss_wave:
            self.enemy_count = 1  
        else:
            self.enemy_count = min(int(self.base_count * (1.225 ** self.current_wave)), 67)

        self.spawn_interval = max(0.25, self.spawn_interval - self.current_wave * 0.01)
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
            (random.randint(0, width), -200),
            (random.randint(0, width), height + 200),
            (-200, random.randint(0, height)),
            (width + 200, random.randint(0, height))
        ]

        x, y = random.choice(spawn_locations)

        if self.is_boss_wave:
            if self.current_wave < 11: 
                enemy = ChargerBoss(x, y) 
            elif self.current_wave < 21: 
                enemy = MotherShip() 
            else: 
                boss_roll = random.random() 
                if boss_roll < 0.5: 
                    enemy = ChargerBoss(x, y) 
                else: 
                    enemy = MotherShip()

            enemy.speed_multiplier = self.speed_multiplier
            enemy.damage_multiplier = self.damage_multiplier
            health_multiplier = 1.4 ** (self.current_wave // 10 - 1)
            enemy.max_health *= health_multiplier
            enemy.health = enemy.max_health

            self.all_enemies.append(enemy)
            return

        enemy_type_roll = random.random()

        elite_chance = 0
        if self.current_wave >= 11:
            elite_chance = min(0.5, (self.current_wave - 10) * 0.05)  

        is_elite = random.random() < elite_chance

        if enemy_type_roll < 0.4:
            enemy = EliteSeekerEnemy(x, y) if is_elite else SeekerEnemy(x, y)

        elif enemy_type_roll < 0.8:
            enemy = EliteShooterEnemy(x, y) if is_elite else ShooterEnemy(x, y)

        else:
            enemy = TeleporterEnemy(x, y)

        enemy.speed_multiplier = self.speed_multiplier
        enemy.damage_multiplier = self.damage_multiplier
        health_multiplier = 1.25 ** (self.current_wave // 5)
        enemy.max_health *= health_multiplier
        enemy.health = enemy.max_health

        self.all_enemies.append(enemy)

    def remove_enemy(self, enemy):
        if enemy in self.all_enemies:
            self.all_enemies.remove(enemy)