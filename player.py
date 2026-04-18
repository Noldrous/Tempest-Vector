from settings import *

class Player:
    def __init__(self, image):
        self.ship_pos = pygame.Vector2(width // 2, height // 2)
        self.health = 100
        self.shield = 50
        self.velocity = pygame.Vector2(0, 0)
        self.angle = 0
        self.thrust_power = 0.20
        self.friction = 0.99
        self.max_speed = 10
        self.ship_radius = 32
        self.image = image
        self.max_fuel = 100
        self.fuel = self.max_fuel
        self.fuel_consumption_rate = 0.8
        self.fuel_regen_rate = 0.3

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
            if self.fuel > 0:
                thrust = pygame.Vector2(math.cos(angle), math.sin(angle))
                self.velocity += thrust * self.thrust_power
                self.fuel -= self.fuel_consumption_rate
                if self.fuel < 0:
                    self.fuel = 0
            else:
                self.velocity *= self.friction
        else:
            self.velocity *= self.friction
            if self.fuel < self.max_fuel:
                self.fuel += self.fuel_regen_rate
                if self.fuel > self.max_fuel:
                    self.fuel = self.max_fuel

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

class FuelBar:
    def __init__(self, x, y, w, h, max_fuel):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.max_fuel = max_fuel

    def draw(self, screen, current_fuel):
        fuel_ratio = max(0, min(current_fuel / self.max_fuel, 1))
        pygame.draw.rect(screen, (50, 50, 50), (self.x, self.y, self.w, self.h))
        pygame.draw.rect(screen, (0, 150, 255), (self.x, self.y, self.w * fuel_ratio, self.h))