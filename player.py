from settings import *
from particle import Particle

class Player:
    def __init__(self, image):
        self.ship_pos = pygame.Vector2(width//2, height // 2 + 500)
        self.health = 200
        self.shield = 100
        self.shield_regeneration = 0.1
        self.max_shield = 100
        self.shield_regen_delay = 240
        self.ram_damage = 2
        self.last_damage_timer = 0
        self.velocity = pygame.Vector2(0, 0)
        self.angle = 0
        self.thrust_power = 0.25
        self.friction = 0.98
        self.max_speed = 12
        self.turn_speed = 0.09  # radians per frame (adjust)
        self.angular_velocity = 0
        self.ship_radius = 16  # Adjusted for smaller ship size
        self.image = image
        self.particles = []
        self.entering = True

    @property
    def ramming_damage(self):
        return self.velocity.length() * self.ram_damage
    
    def draw(self, screen):
        resized_image = pygame.transform.scale(self.image, (128, 128))
        rotated_image = pygame.transform.rotate(resized_image, -math.degrees(self.angle) -90)
        rect = rotated_image.get_rect(center=self.ship_pos)
        for p in self.particles:
            p.draw(screen)
        screen.blit(rotated_image, rect.topleft)
    
    def move(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
    
        dx = mouse_x - self.ship_pos.x
        dy = mouse_y - self.ship_pos.y
        angle = math.atan2(dy, dx)

        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
    
        if keys[pygame.K_SPACE] or mouse_buttons[2]:
            thrust = pygame.Vector2(math.cos(angle), math.sin(angle))
            self.velocity += thrust * self.thrust_power

            # spawn particles behind ship
            for _ in range(2):
                offset = pygame.Vector2(-math.cos(self.angle), -math.sin(self.angle)) * 20
                pos = self.ship_pos + offset

                vel = pygame.Vector2(random.uniform(-1,1), random.uniform(-1,1)) - thrust * 2
                self.particles.append(Particle(pos, vel))

        else:
            self.velocity *= self.friction

        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        if self.ship_pos.x < 0:
            self.ship_pos.x = width
        elif self.ship_pos.x > width:
            self.ship_pos.x = 0 
        if self.ship_pos.y < 0:
            self.ship_pos.y = height
        elif self.ship_pos.y > height:
            self.ship_pos.y = 0

        target_angle = angle

        # shortest angular difference (-pi to pi)
        diff = (target_angle - self.angle + math.pi) % (2 * math.pi) - math.pi

        # apply turning speed limit
        self.angle += diff * self.turn_speed
        self.ship_pos += self.velocity

        for p in self.particles[:]:
            p.update()
            if p.life <= 0:
                self.particles.remove(p)
        
    def take_damage(self, amount):
        self.last_damage_timer = self.shield_regen_delay

        if self.shield > 0:
            if self.shield >= amount:
                self.shield -= amount
                return
            else:
                amount -= self.shield
                self.shield = 0

        self.health -= amount
    
    def regen_shield(self):
        if self.last_damage_timer > 0:
            self.last_damage_timer -= 1
        else:
            if self.shield < self.max_shield:
                self.shield += self.shield_regeneration
                if self.shield > self.max_shield:
                    self.shield = self.max_shield

    def apply_recoil(self, angle, strength=3):
        recoil = pygame.Vector2(
            -math.cos(angle),
            -math.sin(angle)
        )
        self.velocity += recoil * strength

    def entrance(self):
        target = pygame.Vector2(width // 2, height // 2)

        if self.entering:
            direction = target - self.ship_pos

            # rotate ship toward center
            self.angle = math.atan2(direction.y, direction.x)

            self.ship_pos += direction * 0.05

            if direction.length() < 5:
                self.entering = False

class HealthBar:
    def __init__(self, x, y, w, h, max_health):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.max_health = max_health

    def draw(self, screen, current_health):
        health_ratio = current_health / self.max_health
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.w, self.h))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.w * health_ratio, self.h))

class ShieldBar:
    def __init__(self, x, y, w, h, max_shield):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.max_shield = max_shield

    def draw(self, screen, current_shield):
        shield_ratio = current_shield / self.max_shield
        pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, self.w, self.h))
        pygame.draw.rect(screen, (0, 255, 255), (self.x, self.y, self.w * shield_ratio, self.h))