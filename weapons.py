from settings import *
import random


class Bullet:
    def __init__(self, x, y, angle, speed=20, size='sm', lifetime=150, damage=10, max_distance=None):
        self.pos = pygame.Vector2(x, y)
        self.start_pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(math.cos(angle) * speed, math.sin(angle) * speed)
        self.radius = 4 if size == 'sm' else 8 if size == 'md' else 11
        self.lifetime = lifetime
        self.damage = damage
        self.max_distance = max_distance
        self.color = (255, 255, 0) if size == 'sm' else (255, 0, 255) if size == 'md' else (255, 0, 0)

    def update(self):
        self.pos += self.velocity
        self.lifetime -= 1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)

    def is_alive(self):
        if self.lifetime <= 0:
            return False
        if self.max_distance is not None:
            distance = self.pos.distance_to(self.start_pos)
            if distance > self.max_distance:
                return False
        return True
    
class Weapon:
    def __init__(self, name, bullet_speed, ammo, rate, damage, bullet_size, spread, bullet_count, bullet_lifetime, bullet_range=None):
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
                max_distance=self.bullet_range
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
            bullet_size='md',
            spread=7,
            bullet_count=3,
            bullet_lifetime=90
        )
    

class Shotgun(Weapon):
    def __init__(self):
        super().__init__(
            name='Shotgun',
            bullet_speed=30,
            ammo=10,
            rate=800,
            damage=15,
            bullet_size='sm',
            spread=50,
            bullet_count=12,
            bullet_lifetime=17
        )

class RailGun(Weapon):
    def __init__(self):
        super().__init__(
            name='Rail Gun',
            bullet_speed=50,
            ammo=5,
            rate=700,
            damage=50,
            bullet_size='md',
            spread=25,
            bullet_count=1,
            bullet_lifetime=100
        )

class Rockets(Weapon):
    def __init__(self):
        super().__init__(
            name='Rockets',
            bullet_speed=50,
            ammo=3,
            rate=1000,
            damage=200,
            bullet_size='lg',
            spread=25,
            bullet_count=1,
            bullet_lifetime=100
        )

class Weapons:
    def __init__(self):
        self.queue = [MachineGun(), Shotgun(), RailGun(), Rockets()]
        self.main = self.queue[0]
        self.off = self.queue[1]
        
        # Store original ammo for each weapon type
        self.original_ammo = {
            'Machine Gun': 20,
            'Shotgun': 10,
            'Rail Gun': 5,
            'Rockets': 3
        }

    def swap_weapon(self):
        if self.queue:
            self.main, self.off = self.off, self.main

    def cycle_weapon(self):
        # Get the old weapon
        old_weapon = self.main
        
        # Reload the old weapon to full ammo
        old_weapon.ammo = self.original_ammo[old_weapon.name]
        
        # Add reloaded weapon back to the end of the queue
        self.queue.append(old_weapon)

        # Pull the next weapon from the front of the queue
        self.main = self.queue.pop(0)