from settings import *
from enemy import *

class WaveManager:
    def __init__(self):
        self.waves = []
        self.current_wave = 0
        self.spawn_timer = 0
        self.enemies_spawned = 0
        self.all_enemies = []
        self.wave_complete = False
        self.setup_waves()

    def setup_waves(self):
        """Define wave patterns with (enemy_type, count, spawn_interval_in_seconds)"""
        self.waves = [
            ("seeker", 3, 1.0),      # Wave 1: 3 seekers, spawn 1 every second
            ("seeker", 5, 0.8),      # Wave 2: 5 seekers, spawn 1 every 0.8 seconds
            ("shooter", 2, 2.0),     # Wave 3: 2 shooters, spawn 1 every 2 seconds
            ("mixed", 4, 1.0),       # Wave 4: Mix of 2 seekers + 2 shooters
            ("shooter", 3, 1.5),     # Wave 5: 3 shooters
            ("seeker", 6, 0.6),      # Wave 6: 6 seekers (harder wave)
        ]

    def update(self, delta_time):
        """Update wave spawning based on delta time"""
        if self.current_wave < len(self.waves):
            self.spawn_timer += delta_time

            enemy_type, count, spawn_interval = self.waves[self.current_wave]

            # Spawn enemies at intervals until this wave has spawned its full count
            if self.spawn_timer >= spawn_interval and self.enemies_spawned < count:
                self.spawn_enemy(enemy_type)
                self.spawn_timer = 0
                self.enemies_spawned += 1

            # Only advance to the next wave when all enemies in the current wave are dead
            if self.enemies_spawned >= count and len(self.all_enemies) == 0:
                self.current_wave += 1
                self.enemies_spawned = 0
                self.spawn_timer = 0

        # Mark completion only when no more waves remain and no active enemies are left
        if self.current_wave >= len(self.waves) and len(self.all_enemies) == 0:
            self.wave_complete = True

    def spawn_enemy(self, enemy_type):
        """Spawn an enemy of the specified type at a random location"""
        # Spawn enemies at edges of screen
        spawn_locations = [
            (random.randint(0, width), -100),           # Top
            (random.randint(0, width), height + 100),  # Bottom
            (-100, random.randint(0, height)),          # Left
            (width + 100, random.randint(0, height))    # Right
        ]
        
        x, y = random.choice(spawn_locations)

        if enemy_type == "seeker":
            self.all_enemies.append(SeekerEnemy(x, y))
        elif enemy_type == "shooter":
            self.all_enemies.append(ShooterEnemy(x, y))
        elif enemy_type == "mixed":
            # For mixed waves, alternate between seeker and shooter
            if self.enemies_spawned % 2 == 0:
                self.all_enemies.append(SeekerEnemy(x, y))
            else:
                self.all_enemies.append(ShooterEnemy(x, y))

    def get_all_enemies(self):
        """Return all active enemies"""
        return self.all_enemies

    def remove_enemy(self, enemy):
        """Remove a dead enemy"""
        if enemy in self.all_enemies:
            self.all_enemies.remove(enemy)

    def get_current_wave_number(self):
        """Return current wave number (1-indexed)"""
        if self.current_wave < len(self.waves):
            return self.current_wave + 1
        return len(self.waves)

    def is_wave_complete(self):
        """Check if all waves are complete"""
        return self.wave_complete and len(self.all_enemies) == 0