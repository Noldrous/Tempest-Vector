from settings import *

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
            pygame.draw.rect(screen, (255, 150, 50), (int(self.pos.x)+2, int(self.pos.y)+2, 4, 4))