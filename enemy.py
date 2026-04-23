from settings import *
import spritesheet

class Enemy:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.size = 20
        self.hit_radius = self.size
        self.velocity = pygame.Vector2(0, 0)
        self.health = 1
        self.base_damage = 1
        self.base_speed = 1
        self.damage_multiplier = 1
        self.speed_multiplier = 1
        self.knockback = pygame.Vector2(0, 0)
        self.knockback_decay = 0.85
        
    def take_damage(self, damage):
        self.health -= damage

class Enemy_Bullet:
    def __init__(self, pos, direction, damage):
        self.pos = pygame.Vector2(pos)
        self.vel = direction.normalize() * 10
        self.radius = 2
        self.damage = damage
        self.lifetime = 120

    def update(self):
        self.pos += self.vel
        self.lifetime -= 1

    def alive(self):
        return self.lifetime > 0

    def draw(self, screen):
        pygame.draw.circle(screen, (255,200,50),
                           (int(self.pos.x), int(self.pos.y)),
                           self.radius)

class SeekerEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.health = 20
        self.base_damage = 3
        self.base_speed = 3
        self.angle = 0
        self.turn_speed = 0.3
        self.sprite_sheet_image = load_image_alpha("enemies/seeker.png")
        self.sprite_sheet = spritesheet.SpriteSheet(self.sprite_sheet_image)
        self.animation_list = []
        self.animation_steps = 4
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 100
        self.frame = 0
        for x in range(self.animation_steps):
            self.animation_list.append(self.sprite_sheet.get_image(x, 0, 33, 30, 1.5))

    @property
    def max_speed(self):
        return self.base_speed * self.speed_multiplier
    @property
    def max_damage(self):
        return self.base_damage * self.damage_multiplier

    def update(self, player_pos):
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.last_update >= self.animation_cooldown:
            self.frame += 1
            self.last_update = self.current_time
            if self.frame >= len(self.animation_list):
                self.frame = 0

        dx = player_pos.x - self.pos.x
        dy = player_pos.y - self.pos.y
        angle = math.atan2(dy, dx)
        
        thrust = pygame.Vector2(math.cos(self.angle), math.sin(self.angle))
        self.velocity += thrust 
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)
        
        total_velocity = self.velocity + self.knockback
        self.pos += total_velocity
        self.knockback *= self.knockback_decay
        target_angle = angle

        diff = (target_angle - self.angle + math.pi) % (2 * math.pi) - math.pi

        if diff > self.turn_speed:
            diff = self.turn_speed
        elif diff < -self.turn_speed:
            diff = -self.turn_speed

        self.angle += diff

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.animation_list[self.frame], -math.degrees(self.angle) - 90)
        rect = rotated_image.get_rect(center=self.pos)
        screen.blit(rotated_image, rect.topleft)

class ShooterEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.health = 100
        self.base_damage = 1
        self.base_speed = 2
        self.angle = 0
        self.turn_speed = 0.09

        self.state = "move"
        self.state_timer = 0

        self.target_pos = pygame.Vector2(
            random.randint(100, width-100),
            random.randint(100, height-100)
        )
        self.bullets = []

        self.sprite_sheet_image = load_image_alpha("enemies/shooter.png")
        self.sprite_sheet = spritesheet.SpriteSheet(self.sprite_sheet_image)
        self.animations = {
            "move":  [],
            "shoot": []
        }
        self.animation_cooldowns = {
            "move": 150,
            "shoot": 25,
        }
        self.animation_list = self.animations[self.state]
        self.animation_steps = 5
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = self.animation_cooldowns[self.state]
        self.frame = 0
        for x in range(self.animation_steps):
            self.animations["move"].append(self.sprite_sheet.get_image(x, 2, 47, 36, 1.5))
            self.animations["shoot"].append(self.sprite_sheet.get_image(x, 1, 47, 36, 1.5))

    @property
    def max_speed(self):
            return self.base_speed * self.speed_multiplier
    @property
    def max_damage(self):
            return self.base_damage * self.damage_multiplier
        
    def update(self, player_pos):
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.last_update >= self.animation_cooldown:
            self.frame += 1
            self.last_update = self.current_time
            if self.frame >= len(self.animation_list):
                self.frame = 0
        self.state_timer += 1

        self.animation_list = self.animations[self.state]
        self.animation_cooldown = self.animation_cooldowns[self.state]

        # -------------------
        # SHOOT STATE
        # -------------------
        if self.state == "shoot":
            direction = player_pos - self.pos
            direction = direction.normalize()

            forward = pygame.Vector2(math.cos(self.angle), math.sin(self.angle))
            side = pygame.Vector2(-forward.y, forward.x)

            if self.state_timer % 5 == 0:
                offset = 8
                bullet_pos = self.pos + forward * 15
                bullet1 = Enemy_Bullet(bullet_pos + side * offset, forward, self.max_damage)
                bullet2 = Enemy_Bullet(bullet_pos - side * offset, forward, self.max_damage)
                

                self.bullets.append(bullet1)
                self.bullets.append(bullet2)

            strafe = pygame.Vector2(-direction.y, direction.x)
            self.velocity += strafe * 0.98 

            if self.velocity.length() > self.max_speed:
                self.velocity.scale_to_length(self.max_speed)

            total_velocity = self.velocity + self.knockback
            self.pos += total_velocity
            self.knockback *= self.knockback_decay

            # transition
            if self.state_timer > 200:
                self.state = "move"
                self.state_timer = 0
                self.target_pos = pygame.Vector2(
                    random.randint(100, width - 100),
                    random.randint(100, height - 100)
                )

            target_angle = math.atan2(player_pos.y - self.pos.y, player_pos.x - self.pos.x)
            self.target_angle = target_angle

            diff = (target_angle - self.angle + math.pi) % (2 * math.pi) - math.pi

            if diff > self.turn_speed:
                diff = self.turn_speed
            elif diff < -self.turn_speed:
                diff = -self.turn_speed

            self.angle += diff

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

            total_velocity = self.velocity + self.knockback
            self.pos += total_velocity
            self.knockback *= self.knockback_decay

            distance = self.pos.distance_to(self.target_pos)

            if distance < 10:
                self.state = "shoot"
                self.state_timer = 0

            target_angle = angle

            diff = (target_angle - self.angle + math.pi) % (2 * math.pi) - math.pi

            if diff > self.turn_speed:
                diff = self.turn_speed
            elif diff < -self.turn_speed:
                diff = -self.turn_speed

            self.angle += diff

        # update bullets
        self.bullets = [b for b in self.bullets if b.alive()]
        for bullet in self.bullets:
            bullet.update()

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.animation_list[self.frame], -math.degrees(self.angle) - 90)
        rect = rotated_image.get_rect(center=self.pos)
        screen.blit(rotated_image, rect.topleft)

        for bullet in self.bullets:
            bullet.draw(screen)