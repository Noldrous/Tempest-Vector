from settings import *
from spritesheet import *

class Particle:
    def __init__(self, pos, velocity):
        self.pos = pygame.Vector2(pos)
        self.velocity = velocity
        self.life = 50

    def update(self):
        self.pos += self.velocity
        self.life -= 1

    def draw(self, screen):
        if self.life > 0:
            pygame.draw.rect(screen, (255, 0, 0), (int(self.pos.x), int(self.pos.y), 8 , 8))
            pygame.draw.rect(screen, (44, 255, 5), (int(self.pos.x)+2, int(self.pos.y)+2, 4, 4))

class EnemyExplosion(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        pygame.sprite.Sprite.__init__(self)
        
        size = int(radius * 4)
        self.frame_width = None   # will be set after loading
        self.frame_height = None

        # load spritesheet once and slice into frames
        sheet_surface = pygame.image.load("assets/img/enemies/enemy_explosion1.png").convert_alpha()
        sheet = SpriteSheet(sheet_surface)
        
        self.frame_width = sheet_surface.get_width() // 30   # 10 frames
        self.frame_height = sheet_surface.get_height()

        self.images = []
        for i in range(4, 30):
            image = sheet.get_image(i, 0, self.frame_width, self.frame_height, 1)
            image = pygame.transform.scale(image, (size, size))
            self.images.append(image)

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.counter = 0

    def update(self):
        explosion_speed = 2
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        pygame.sprite.Sprite.__init__(self)
        self.images = []

        size = int(radius * 2)  # convert radius → diameter

        for i in range(1, 8):
            image = pygame.image.load(f"assets/img/bullets/explosion/explosion-f{i}.png").convert_alpha()
            image = pygame.transform.scale(image, (size, size))
            self.images.append(image)

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.counter = 0

    def update(self):
        explosion_speed = 4
        #update explosion animation
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        
        # if animation is complete, reset animation index
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()
    
explosion_group = pygame.sprite.Group()
enemy_explosion_group = pygame.sprite.Group()