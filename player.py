from settings import *

class Player:
    def __init__(self, image):
        self.ship_pos = pygame.Vector2(width // 2, height // 2)
        self.health = 200
        self.shield = 100
        self.velocity = pygame.Vector2(0, 0)
        self.angle = 0
        self.thrust_power = 0.20
        self.friction = 0.99
        self.max_speed = 12
        self.ship_radius = 16  # Adjusted for smaller ship size
        self.image = image

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, -math.degrees(self.angle) - 90)
        rect = rotated_image.get_rect(center=self.ship_pos)
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

        self.angle = angle
        self.ship_pos += self.velocity
        
    def take_damage(self, amount):
        if self.shield > 0 and self.shield >= amount:
            self.shield -= amount
        elif self.shield < amount:
            amount -= self.shield
            self.shield = 0
            self.health -= (amount - self.shield)
        else:
            self.health -= amount


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