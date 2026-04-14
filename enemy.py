from settings import *

class Enemy:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.speed = 2
        self.size = 20

        self.hit_radius = self.size

class Bullet:
    def __init__(self, pos, direction):
        self.pos = pygame.Vector2(pos)
        self.vel = direction.normalize() * 6
        self.radius = 4

    def update(self):
        self.pos += self.vel

    def draw(self, screen):
        pygame.draw.circle(screen, (255,200,50),
                           (int(self.pos.x), int(self.pos.y)),
                           self.radius)

class SeekerEnemy(Enemy):

    def update(self, player_pos):
        direction = player_pos - self.pos

        if direction.length() != 0:
            direction = direction.normalize()

        self.pos += direction * self.speed

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            (255, 80, 80),
            (int(self.pos.x), int(self.pos.y)),
            self.size, 2
        )

class ShooterEnemy(Enemy):

    def __init__(self, x, y):
        super().__init__(x, y)

        self.speed = 3
        self.safe_distance = 200

        self.state = "shoot"   # shoot or move
        self.state_timer = 0

        self.target_pos = pygame.Vector2(x, y)

        self.bullets = []

    def update(self, player_pos):

        self.state_timer += 1

        # -------------------
        # SHOOT STATE
        # -------------------
        if self.state == "shoot":

            direction = player_pos - self.pos

            if direction.length() != 0:
                direction = direction.normalize()

            # fire barrage
            if self.state_timer % 10 == 0:
                bullet = Bullet(self.pos, direction)
                self.bullets.append(bullet)

            # after barrage, move somewhere else
            if self.state_timer > 120:
                self.state = "move"
                self.state_timer = 0

                self.target_pos = pygame.Vector2(
                    random.randint(100, width-100),
                    random.randint(100, height-100)
                )

        # -------------------
        # MOVE STATE
        # -------------------
        elif self.state == "move":

            direction = self.target_pos - self.pos

            if direction.length() > 5:
                direction = direction.normalize()
                self.pos += direction * self.speed
            else:
                # reached destination
                self.state = "shoot"
                self.state_timer = 0

        # update bullets
        for bullet in self.bullets:
            bullet.update()

    def draw(self, screen):

        rect = pygame.Rect(
            self.pos.x - self.size,
            self.pos.y - self.size,
            self.size * 2,
            self.size * 2
        )

        pygame.draw.rect(screen, (80,120,255), rect, 3)

        for bullet in self.bullets:
            bullet.draw(screen)