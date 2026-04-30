from settings import *
import random


class Bullet:
    def __init__(self, x, y, angle, speed=20, size=0, lifetime=150, damage=10, max_distance=None, bullet_piercing=False, explosion_radius=0, is_homing=False, seek_range=1000):
        self.pos = pygame.Vector2(x, y)
        self.start_pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(math.cos(angle) * speed, math.sin(angle) * speed)
        self.radius = size
        self.lifetime = lifetime
        self.damage = damage
        self.piercing = bullet_piercing
        self.max_distance = max_distance
        self.explosion_radius = explosion_radius
        self.is_homing = is_homing
        self.seek_range = seek_range
        self.exploded = False
        self.color = (255, 255, 0)

    def explode(self, all_enemies, player_bullets):
        if self.exploded or self.explosion_radius == 0:
            return
            
        # Damage all enemies in explosion radius
        for enemy in all_enemies[:]:
            distance = enemy.pos.distance_to(self.pos)
            if distance < self.explosion_radius:
                enemy.take_damage(self.damage // 2)
        
        # Visual explosion effect
        for _ in range(20):
            angle = random.uniform(0, 2*math.pi)
            speed = random.uniform(2, 6)
            offset_pos = self.pos + pygame.Vector2(math.cos(angle), math.sin(angle)) * self.explosion_radius * 0.5
        
        self.exploded = True
        self.lifetime = 0  # Remove after explosion

    def update(self, all_enemies=None):
        if self.is_homing and all_enemies:
            alive_enemies = [e for e in all_enemies if hasattr(e, 'health') and e.health > 0]
            if alive_enemies:
                nearest = min(alive_enemies, key=lambda e: e.pos.distance_to(self.pos))
                dist = nearest.pos.distance_to(self.pos)
                if dist < self.seek_range:
                    target_dir = (nearest.pos - self.pos).normalize()
                    self.velocity = self.velocity.lerp(target_dir * self.velocity.length(), 0.12)
        
        self.pos += self.velocity
        self.lifetime -= 1

    def draw(self, screen):
        pygame.draw.circle(screen, (255,255,255), (int(self.pos.x), int(self.pos.y)), self.radius)
        pygame.draw.circle(screen, (100,100,100), (int(self.pos.x), int(self.pos.y)), self.radius, 2)

    def is_alive(self):
        if self.lifetime <= 0:
            return False
        if self.max_distance is not None:
            distance = self.pos.distance_to(self.start_pos)
            if distance > self.max_distance:
                return False
        return True
    
class Weapon:
    def __init__(self, name, bullet_speed, ammo, rate, damage, bullet_size, spread, bullet_count, bullet_lifetime, bullet_range=None, bullet_piercing=False):
        self.name = name
        self.bullet_speed =  bullet_speed
        self.ammo = ammo
        self.rate = rate
        self.damage = damage
        self.bullet_size = bullet_size
        self.spread = spread
        self.bullet_count = bullet_count
        self.bullet_lifetime = bullet_lifetime
        self.bullet_range = bullet_range if bullet_range is not None else bullet_speed * bullet_lifetime
        self.bullet_piercing = bullet_piercing
        self.last_shot = 0

    def can_shoot(self):
        current_time = pygame.time.get_ticks()
        return self.ammo > 0 and (current_time - self.last_shot) >= self.rate
    
    def shoot(self, x, y, angle ):
        if not self.can_shoot():
            return []
        
        self.last_shot = pygame.time.get_ticks()
        self.ammo -= 1
        return self._create_bullets(x,y,angle)
    
    def _create_bullets(self, x, y, angle):
        bullets = []
        for _ in range(self.bullet_count):
            spread_angle = angle + math.radians(random.uniform(-self.spread / 2, self.spread / 2))
            bullets.append(Bullet(
                x,
                y,
                spread_angle,
                self.bullet_speed,
                self.bullet_size,
                self.bullet_lifetime,
                self.damage,
                max_distance=self.bullet_range,
                bullet_piercing = self.bullet_piercing,
                explosion_radius=60 if self.name == "Rockets" else 0,
                is_homing=(self.name == "Rockets")
            ))
        return bullets
    
class MachineGun(Weapon):
    def __init__(self):
        super().__init__(
            name='Machine Gun',
            bullet_speed=30,
            ammo=20,
            rate=100,
            damage=10,
            bullet_size=4,
            spread=7,
            bullet_count=3,
            bullet_lifetime=90,
            bullet_piercing=False
        )
    
class Shotgun(Weapon):
    def __init__(self):
        super().__init__(
            name='Shotgun',
            bullet_speed=30,
            ammo=10,
            rate=800,
            damage=30,
            bullet_size=6,
            spread=50,
            bullet_count=8,
            bullet_lifetime=17,
            bullet_piercing=False
        )

class RailGun(Weapon):
    def __init__(self):
        super().__init__(
            name='Rail Gun',
            bullet_speed=100,
            ammo=5,
            rate=700,
            damage=50,
            bullet_size=8,
            spread=0,
            bullet_count=1,
            bullet_lifetime=100,
            bullet_piercing=False
        )

class Rockets(Weapon):
    def __init__(self):
        super().__init__(
            name='Rockets',
            bullet_speed=50,
            ammo=3,
            rate=1000,
            damage=200,
            bullet_size=11,
            spread=25,
            bullet_count=1,
            bullet_lifetime=100,
            bullet_piercing=False
        )

class Weapons:
    def __init__(self, cycle_delay=2000):
        self.queue = [MachineGun(), Shotgun(), RailGun(), Rockets()]
        self.main = random.choice(self.queue)
        self.cycle_delay = cycle_delay  # Delay in milliseconds
        self.last_cycle_time = pygame.time.get_ticks()
        self.message_time = 0  # Time when message should be displayed
        self.message_duration = 800  # How long to show message in milliseconds
        self.max_ammo_bonus = 0
        
        # Store original ammo for each weapon type
        self.original_ammo = {
            'Machine Gun': 20,
            'Shotgun': 10,
            'Rail Gun': 5,
            'Rockets': 3
        }

    def can_cycle_weapon(self):
        """Check if enough time has passed to cycle to the next weapon"""
        current_time = pygame.time.get_ticks()
        return (current_time - self.last_cycle_time) >= self.cycle_delay

    def should_show_message(self):
        """Check if the changing weapon message should be displayed"""
        current_time = pygame.time.get_ticks()
        return current_time < self.message_time

    def cycle_weapon(self):
        # Check if the cycle delay has passed
        if not self.can_cycle_weapon():
            return
        
        # Update the cycle time
        self.last_cycle_time = pygame.time.get_ticks()
        self.message_time = self.last_cycle_time + self.message_duration  # Show message for duration
        
        # Get the old weapon
        old_weapon = self.main
        
        # Reload the old weapon to full ammo
        old_weapon.ammo = self.original_ammo[old_weapon.name] + self.max_ammo_bonus
        
        # Add reloaded weapon back to the end of the queue
        self.queue.append(old_weapon)

        # Pull the next weapon from the front of the queue
        self.main = self.queue.pop(0)