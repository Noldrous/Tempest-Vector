from settings import *

class Player:
    def __init__(self):
        self.ship_pos = pygame.Vector2(width // 2, height // 2)
        self.velocity = pygame.Vector2(0, 0)
        self.angle = 0
        self.thrust_power = 0.8
        self.friction = 0.95
        self.max_speed = 8
        self.ship_size = 20
        self.ship_radius = self.ship_size 

    def draw(self, screen):
        tip = (self.ship_pos.x + math.cos(self.angle)*self.ship_size,
          self.ship_pos.y + math.sin(self.angle)*self.ship_size)

        left = (self.ship_pos.x + math.cos(self.angle+2.5)*self.ship_size,
                self.ship_pos.y + math.sin(self.angle+2.5)*self.ship_size)
    
        right = (self.ship_pos.x + math.cos(self.angle-2.5)*self.ship_size,
                 self.ship_pos.y + math.sin(self.angle-2.5)*self.ship_size)

        pygame.draw.polygon(screen, (200,200,255), [tip, left, right])
    
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
        