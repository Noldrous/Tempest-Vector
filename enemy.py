from settings import *

class Enemy:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.size = 20
        self.hit_radius = self.size
        self.velocity = pygame.Vector2(0, 0)
        
    def take_damage(self, damage):
        self.health -= damage

class Enemy_Bullet:
    def __init__(self, pos, direction):
        self.pos = pygame.Vector2(pos)
        self.vel = direction.normalize() * 10
        self.radius = 2
        self.damage = 3

    def update(self):
        self.pos += self.vel

    def draw(self, screen):
        pygame.draw.circle(screen, (255,200,50),
                           (int(self.pos.x), int(self.pos.y)),
                           self.radius)

class SeekerEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.health = 20
        self.contact_damage = 0.5
        self.max_speed = 5

    def update(self, player_pos):
        dx = player_pos.x - self.pos.x
        dy = player_pos.y - self.pos.y
        angle = math.atan2(dy, dx)

        thrust = pygame.Vector2(math.cos(angle), math.sin(angle))
        self.velocity += thrust 
        self.pos += self.velocity

        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

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
        self.health = 100
        self.contact_damage = 1
        self.max_speed = 5
        self.safe_distance = 200

        self.state = "move"
        self.state_timer = 0

        self.target_pos = pygame.Vector2(
            random.randint(100, width-100),
            random.randint(100, height-100)
        )

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
            if self.state_timer % 5 == 0:
                bullet = Enemy_Bullet(self.pos, direction)
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
            self.velocity *= 0.98
            dx = self.target_pos.x - self.pos.x
            dy = self.target_pos.y - self.pos.y
            angle = math.atan2(dy, dx)

            thrust = pygame.Vector2(math.cos(angle), math.sin(angle))
            self.velocity += thrust

            if self.velocity.length() > self.max_speed:
                self.velocity.scale_to_length(self.max_speed)

            self.pos += self.velocity

            distance = self.pos.distance_to(self.target_pos)

            if distance < 10:
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