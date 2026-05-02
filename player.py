from settings import *
from particle import Particle
from spritesheet import *
import time

class Player:
    def __init__(self, image):
        self.ship_pos = pygame.Vector2(width//2, height // 2 + 500)
        self.ship_radius = 16

        self.health = 200
        self.max_health = 300

        self.shield = 100
        self.shield_regeneration = 1
        self.max_shield = 100
        self.shield_regen_delay = 240
        self.last_damage_timer = 0

        self.ram_damage = 2
        self.thrust_power = 0.25
        self.max_speed = 12

        self.velocity = pygame.Vector2(0, 0)
        self.friction = 0.98
        self.angle = 0
        self.turn_speed = 0.09 
        self.angular_velocity = 0

        self.entering = True

        self.particles = []

        self.image = image
        self.sprite_sheet = SpriteSheet(image)
        self.state_lock_timer = 0
        self.shooting_anim = False
        self.shoot_timer = 0
        self.shoot_anim_duration = 24  
        self.boosting = False
        self.current_frame = 0
        self.frames = []
        self.frame_width = 48
        self.frame_height = 48
        self.scale = 1.5
        self.frame_count = 12

        for row in range(12):  # your full table
            row_frames = []
            for i in range(self.frame_count):
                row_frames.append(self.sprite_sheet.get_image(i, row,self.frame_width, self.frame_height, self.scale))
            self.frames.append(row_frames)

    @property
    def ramming_damage(self):
        return self.velocity.length() * self.ram_damage
    
    def get_damage_state(self):
        if self.health > 120:
            return 0  # no damage
        elif self.health > 50:
            return 1  # light damage
        else:
            return 2  # heavy damage
    
    def get_anim_speed(self):
        if self.boosting:
            return 0.5  # faster animation
        return 0.2
        
    def get_anim_row(self):
        shield = 1 if self.shield > 0 else 0
        dmg = self.get_damage_state()
        shooting = 1 if self.shooting_anim else 0

        if shooting == 0 and shield == 1 and dmg == 0:
            return 0
        if shooting == 0 and shield == 1 and dmg == 1:
            return 1
        if shooting == 0 and shield == 1 and dmg == 2:
            return 2

        if shooting == 0 and shield == 0 and dmg == 0:
            return 3
        if shooting == 0 and shield == 0 and dmg == 1:
            return 4
        if shooting == 0 and shield == 0 and dmg == 2:
            return 5

        if shooting == 1 and shield == 1 and dmg == 0:
            return 6
        if shooting == 1 and shield == 1 and dmg == 1:
            return 7
        if shooting == 1 and shield == 1 and dmg == 2:
            return 8

        if shooting == 1 and shield == 0 and dmg == 0:
            return 9
        if shooting == 1 and shield == 0 and dmg == 1:
            return 10
        if shooting == 1 and shield == 0 and dmg == 2:
            return 11
    
    def draw(self, screen):
        row = self.get_anim_row()
        frames = self.frames[row]

        frame = frames[int(self.current_frame)]

        self.current_frame += self.get_anim_speed()

        if self.current_frame >= len(frames):
            self.current_frame = 0

        rotated = pygame.transform.rotate(frame, -math.degrees(self.angle) - 90)

        rect = rotated.get_rect(center=self.ship_pos)

        for p in self.particles:
            p.draw(screen)

        # Draw glow effect behind the player
        #self.draw_glow(screen)

        screen.blit(rotated, rect.topleft)
    
    def draw_glow(self, screen):
        """Draw a pulsing glow indicator around the player"""
        # Create pulsing animation using current time
        pulse = (math.sin(time.time() * 3) + 1) / 2  # Oscillates between 0 and 1
        
        # Outer glow ring - larger, more transparent
        glow_radius = int(self.ship_radius * 2.5 + pulse * 8)
        glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        
        # Draw outer glow with gradient effect
        for i in range(3):
            alpha = int(30 + pulse * 20)
            radius = glow_radius - i * 5
            if radius > 0:
                pygame.draw.circle(glow_surface, (0, 200, 255, alpha), (glow_radius, glow_radius), radius, 2)
        
        # Inner glow - brighter, follows shield state
        if self.shield > 0:
            inner_color = (0, 255, 255, 150 + int(pulse * 50))  # Cyan for shield
        else:
            inner_color = (255, 100, 50, 100 + int(pulse * 50))  # Orange when no shield
        
        # Draw inner glow circle
        inner_radius = int(self.ship_radius * 1.5 + pulse * 4)
        pygame.draw.circle(glow_surface, inner_color, (glow_radius, glow_radius), inner_radius, 2)
        
        # Position the glow surface centered on player
        glow_rect = glow_surface.get_rect(center=(int(self.ship_pos.x), int(self.ship_pos.y)))
        
        # Blit with blend for additive glow effect
        screen.blit(glow_surface, glow_rect.topleft, special_flags=pygame.BLEND_ADD)
        
        # Draw direction indicator (line pointing where player is facing)
        indicator_length = int(self.ship_radius * 2 + pulse * 3)
        end_pos = (
            self.ship_pos.x + math.cos(self.angle) * indicator_length,
            self.ship_pos.y + math.sin(self.angle) * indicator_length
        )
        
        if self.shield > 0:
            indicator_color = (0, 255, 255)
        else:
            indicator_color = (255, 150, 50)
        
        # Main direction line
        pygame.draw.line(screen, indicator_color, self.ship_pos, end_pos, 2)
    
    def move(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
    
        dx = mouse_x - self.ship_pos.x
        dy = mouse_y - self.ship_pos.y
        angle = math.atan2(dy, dx)

        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
    
        if keys[pygame.K_SPACE] or mouse_buttons[2]:
            self.boosting = True
            thrust = pygame.Vector2(math.cos(angle), math.sin(angle))
            self.velocity += thrust * self.thrust_power

            # spawn particles behind ship
            for _ in range(2):
                offset = pygame.Vector2(-math.cos(self.angle), -math.sin(self.angle)) * 20
                pos = self.ship_pos + offset

                vel = pygame.Vector2(random.uniform(-1,1), random.uniform(-1,1)) - thrust * 2
                self.particles.append(Particle(pos, vel))

        else:
            self.boosting = False
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

        if self.shoot_timer > 0:
            self.shoot_timer -= 1
        else:
            self.shooting_anim = False
        
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

    def shoot(self, weapon, player_bullets, weapons, firing):
        if weapon is None or self.entering:
            return

        if firing and not weapons.should_show_message():
            bullets = weapon.shoot(self.ship_pos.x, self.ship_pos.y, self.angle)

            if bullets:
                player_bullets.extend(bullets)

                self.shooting_anim = True
                self.shoot_timer = self.shoot_anim_duration

                recoil_strength = {
                    "Machine Gun": 1,
                    "Shotgun": 4,
                    "Rail Gun": 5,
                    "Rockets": 6
                }

                self.apply_recoil(self.angle, recoil_strength.get(weapon.name, 3))

    def entrance(self):
        target = pygame.Vector2(width // 2, height // 2)

        if self.entering:
            direction = target - self.ship_pos

            # rotate ship toward center
            self.angle = math.atan2(direction.y, direction.x)

            self.ship_pos += direction * 0.09

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
        current_height = self.h * health_ratio
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.w, self.h))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y + (self.h - current_height), self.w, current_height))
        pygame.draw.rect(screen, (120, 0, 0), (self.x, self.y, self.w, self.h), 4)

class ShieldBar:
    def __init__(self, x, y, w, h, max_shield):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.max_shield = max_shield

    def draw(self, screen, current_shield):
        shield_ratio = current_shield / self.max_shield
        current_height = self.h * shield_ratio
        pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, self.w, self.h))
        pygame.draw.rect(screen, (0, 255, 255), (self.x, self.y + (self.h - current_height), self.w, current_height))
        pygame.draw.rect(screen, (0, 0, 130), (self.x, self.y, self.w, self.h), 4)
