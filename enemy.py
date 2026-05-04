from settings import *
import spritesheet

class Enemy:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.hit_radius = 0
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
    def __init__(self, pos, direction, damage, radius):
        self.pos = pygame.Vector2(pos)
        self.vel = direction.normalize() * 10
        self.radius = radius
        self.damage = damage
        self.lifetime = 120

    def update(self):
        self.pos += self.vel
        self.lifetime -= 1

    def alive(self):
        return self.lifetime > 0

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.pos.x), int(self.pos.y)), self.radius)
        pygame.draw.circle(screen, (44, 255, 5), (int(self.pos.x), int(self.pos.y)), self.radius, 2)

class SeekerEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.health = 100
        self.base_damage = 10
        self.base_speed = 3
        self.hit_radius = 30
        self.angle = 0
        self.turn_speed = 0.3

        self.sprite_sheet_image = load_image_alpha("enemies/seeker.png")
        self.sprite_sheet = spritesheet.SpriteSheet(self.sprite_sheet_image)
        self.animation_list = []
        self.animation_steps = 6
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 100
        self.frame = 0
        for x in range(self.animation_steps):
            self.animation_list.append(self.sprite_sheet.get_image(x, 0, 33, 30, 1.5))

    @property
    def max_speed(self):
        return self.base_speed * self.speed_multiplier
    @property
    def final_damage(self):
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

class EliteSeekerEnemy(SeekerEnemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.health = 175
        self.base_damage = 12
        self.base_speed = 4
        self.hit_radius = 30
        self.angle = 0
        self.turn_speed = 0.2

        self.sprite_sheet_image = load_image_alpha("enemies/elite_seeker.png")
        self.sprite_sheet = spritesheet.SpriteSheet(self.sprite_sheet_image)
        self.animation_list = []
        self.animation_steps = 4
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 100
        self.frame = 0
        for x in range(self.animation_steps):
            self.animation_list.append(self.sprite_sheet.get_image(x, 0, 41, 29, 1.5))
        
class ShooterEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.health = 75
        self.base_damage = 5
        self.base_speed = 2
        self.hit_radius = 40
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
            "shoot": 110,
        }
        self.animation_list = self.animations[self.state]
        self.animation_step = {
            "move": 6,
            "shoot": 4,
        }
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = self.animation_cooldowns[self.state]
        self.frame = 0
        for x in range(self.animation_step["move"]):
            self.animations["move"].append(self.sprite_sheet.get_image(x, 2, 25, 27, 1.5))
        for x in range(self.animation_step["shoot"]):   
            self.animations["shoot"].append(self.sprite_sheet.get_image(x, 1, 25, 27, 1.5))
        
        self.shoot_sounds = pygame.mixer.Sound("assets/audio/sfx/enemy/shooter_shoot.wav")
        

    @property
    def max_speed(self):
            return self.base_speed * self.speed_multiplier
    @property
    def final_damage(self):
            return self.base_damage * self.damage_multiplier
        
    def update(self, player_pos):
        self.current_time = pygame.time.get_ticks()
        self.animation_list = self.animations[self.state]
        self.animation_cooldown = self.animation_cooldowns[self.state]
        if self.current_time - self.last_update >= self.animation_cooldown:
            self.frame += 1
            self.last_update = self.current_time
            if self.frame >= len(self.animation_list):
                self.frame = 0
        self.state_timer += 1

        # -------------------
        # SHOOT STATE
        # -------------------
        if self.state == "shoot":
            direction = player_pos - self.pos
            direction = direction.normalize()

            forward = pygame.Vector2(math.cos(self.angle), math.sin(self.angle))

            if self.state_timer % 25 == 0:
                bullet_pos = self.pos + forward * 15
                bullet1 = Enemy_Bullet(bullet_pos, forward, self.final_damage, 6)
                self.shoot_sounds.play()
                self.bullets.append(bullet1)
                

            strafe = pygame.Vector2(-direction.y, direction.x)
            self.velocity += strafe * 0.98 

            if self.velocity.length() > self.max_speed:
                self.velocity.scale_to_length(self.max_speed)

            total_velocity = self.velocity + self.knockback
            self.pos += total_velocity
            self.knockback *= self.knockback_decay

            # transition
            if self.state_timer > 350:
                self.state = "move"
                self.state_timer = 0
                self.frame = 0
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
                self.frame = 0

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

class EliteShooterEnemy(ShooterEnemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.health = 150
        self.base_damage = 4
        self.base_speed = 2
        self.hit_radius = 40
        self.angle = 0
        self.turn_speed = 0.09

        self.state = "move"
        self.state_timer = 0

        self.target_pos = pygame.Vector2(
            random.randint(100, width-100),
            random.randint(100, height-100)
        )
        self.bullets = []

        self.sprite_sheet_image = load_image_alpha("enemies/elite_shooter.png")
        self.sprite_sheet = spritesheet.SpriteSheet(self.sprite_sheet_image)
        self.animations = {
            "move":  [],
            "shoot": []
        }
        self.animation_cooldowns = {
            "move": 150,
            "shoot": 40,
        }
        self.animation_list = self.animations[self.state]
        self.animation_steps = 5
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = self.animation_cooldowns[self.state]
        self.frame = 0
        for x in range(self.animation_steps):
            self.animations["move"].append(self.sprite_sheet.get_image(x, 2, 47, 36, 1.5))
            self.animations["shoot"].append(self.sprite_sheet.get_image(x, 1, 47, 36, 1.5))
        
    def update(self, player_pos):
        self.current_time = pygame.time.get_ticks()
        self.animation_list = self.animations[self.state]
        self.animation_cooldown = self.animation_cooldowns[self.state]
        if self.current_time - self.last_update >= self.animation_cooldown:
            self.frame += 1
            self.last_update = self.current_time
            if self.frame >= len(self.animation_list):
                self.frame = 0
        self.state_timer += 1

        # -------------------
        # SHOOT STATE
        # -------------------
        if self.state == "shoot":
            direction = player_pos - self.pos
            direction = direction.normalize()

            forward = pygame.Vector2(math.cos(self.angle), math.sin(self.angle))
            side = pygame.Vector2(-forward.y, forward.x)

            if self.state_timer % 10 == 0:
                offset = 8
                bullet_pos = self.pos + forward * 15
                if (self.state_timer // 20) % 2 == 0:
                    bullet = Enemy_Bullet(bullet_pos + side * offset, forward, self.final_damage, 4)
                    self.shoot_sounds.play()
                else:
                    bullet = Enemy_Bullet(bullet_pos - side * offset, forward, self.final_damage, 4)
                    self.shoot_sounds.play()

                self.bullets.append(bullet)

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

class TeleporterEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.health = 125
        self.base_damage = 6
        self.base_speed = 100
        self.hit_radius = 30
        self.angle = 0

        self.state = "teleport"
        self.state_timer = 0

        self.target_pos = pygame.Vector2(
            random.randint(100, width-100),
            random.randint(100, height-100)
        )
        self.bullets = []
        self.sprite_sheet_image = load_image_alpha("enemies/teleporter.png")
        self.sprite_sheet = spritesheet.SpriteSheet(self.sprite_sheet_image)
        self.animations = {
            "teleport":  [],
            "shoot": []
        }
        self.animation_cooldowns = {
            "teleport": 150,
            "shoot": 100,
        }

        self.animation_list = self.animations[self.state]
        self.animation_cooldown = self.animation_cooldowns[self.state]

        self.last_update = pygame.time.get_ticks()
        self.frame = 0
        for x in range(4):
            self.animations["teleport"].append(self.sprite_sheet.get_image(x, 0, 66, 66, 0.8))
        for x in range(8):
            self.animations["shoot"].append(self.sprite_sheet.get_image(x, 0, 66, 66, 0.8))

        self.shoot_sounds = pygame.mixer.Sound("assets/audio/sfx/enemy/teleporter_shoot.wav")
        self.teleport_sounds = pygame.mixer.Sound("assets/audio/sfx/enemy/teleporter_teleport.wav")
        self.teleport_played = False

    @property
    def max_speed(self):
            return self.base_speed * self.speed_multiplier
    @property
    def final_damage(self):
            return self.base_damage * self.damage_multiplier
        
    def update(self, player_pos):
        self.current_time = pygame.time.get_ticks()
        self.animation_list = self.animations[self.state]
        self.animation_cooldown = self.animation_cooldowns[self.state]
        if self.current_time - self.last_update >= self.animation_cooldown:
            self.frame += 1
            self.last_update = self.current_time
            if self.frame >= len(self.animation_list):
                self.frame = 0
        self.state_timer += 1

        

        # -------------------
        # SHOOT STATE
        # -------------------
        if self.state == "shoot":
            if self.state_timer % 45 == 0:
                bullet_count = 8
                angle_step = 360 / bullet_count

                forward = pygame.Vector2(math.cos(self.angle), math.sin(self.angle))
                self.shoot_sounds.play()
                for i in range(bullet_count):
                    direction = forward.rotate(i * angle_step)

                    self.bullets.append(
                    Enemy_Bullet(self.pos, direction, self.final_damage, 7))
                    
            drift = pygame.Vector2(
                random.uniform(-0.05,0.05),
                random.uniform(-0.05,0.05)
            )

            self.velocity += drift
            self.velocity *= 0.99

            # limit speed
            if self.velocity.length() > self.max_speed:
                self.velocity.scale_to_length(self.max_speed)

            total_velocity = self.velocity + self.knockback
            self.pos += total_velocity
            self.knockback *= self.knockback_decay
            

            # transition
            if self.state_timer > 500:
                self.state = "teleport"
                self.state_timer = 0
                self.frame = 0
                self.teleport_played = False
                self.target_pos = pygame.Vector2(
                    random.randint(100, width - 100),
                    random.randint(100, height - 100)
                )

        # -------------------
        # TELEPORT STATE
        # -------------------
        elif self.state == "teleport":
            direction = self.target_pos - self.pos
            distance = direction.length()

            blink_speed = 40

            if distance > blink_speed:
                direction = direction.normalize()
                self.pos += direction * blink_speed
                if not self.teleport_played:
                    self.teleport_sounds.play()
                    self.teleport_played = True        
            else:
                if self.state_timer > 50:
                    self.state = "shoot"
                    self.state_timer = 0
                    self.frame = 0

        # update bullets
        self.bullets = [b for b in self.bullets if b.alive()]
        for bullet in self.bullets:
            bullet.update()

    def draw(self, screen):
        image = self.animation_list[self.frame]
        rect = image.get_rect(center=self.pos)
        screen.blit(image, rect.topleft)

        # draw bullets
        for bullet in self.bullets:
            bullet.draw(screen)

class ChargerBoss(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.health = 5000
        self.base_damage = 1.5
        self.base_speed = 3
        self.hit_radius = 90

        self.angle = 0
        self.turn_speed = 0.05

        self.state = "enter"
        self.enter_target = pygame.Vector2(width // 2, height // 2)
        self.state_timer = 0
        self.bullets = []

        self.velocity = pygame.Vector2(0,0)

        self.charge_speed = 35
        self.recovery_time = 175

        self.sprite_sheet_image = load_image_alpha("enemies/charger.png")
        self.sprite_sheet = spritesheet.SpriteSheet(self.sprite_sheet_image)
        self.animations = {
            "enter": [],
            "aim":  [],
            "charge": [],
            "recover": [],
        }
        self.animation_cooldowns = {
            "enter": 20,
            "aim": 320,
            "charge": 150,
            "recover": 90,
        }

        self.animation_list = self.animations[self.state]
        self.animation_cooldown = self.animation_cooldowns[self.state]

        self.last_update = pygame.time.get_ticks()
        self.frame = 0
        for x in range(34):
            self.animations["enter"].append(self.sprite_sheet.get_image(x, 0, 128, 128, 1.5))
        for x in range(34):
            self.animations["aim"].append(self.sprite_sheet.get_image(x, 0, 128, 128, 1.5))
        for x in range(34):
            self.animations["charge"].append(self.sprite_sheet.get_image(x, 0, 128, 128, 1.5))
        for x in range(34):
            self.animations["recover"].append(self.sprite_sheet.get_image(x, 0, 128, 128, 1.5))

    @property
    def max_speed(self):
            return self.base_speed * self.speed_multiplier
    @property
    def final_damage(self):
            return self.base_damage * self.damage_multiplier
    
    def update(self, player_pos):
        self.current_time = pygame.time.get_ticks()
        self.animation_list = self.animations[self.state]
        self.animation_cooldown = self.animation_cooldowns[self.state]
        if self.current_time - self.last_update >= self.animation_cooldown:
            self.frame += 1
            self.last_update = self.current_time
            if self.frame >= len(self.animation_list):
                self.frame = 0
        self.state_timer += 1

        # -------------------
        # ENTER STATE
        # -------------------
        if self.state == "enter":
            direction = self.enter_target - self.pos
            distance = direction.length()

            if distance > 5:
                direction = direction.normalize()
                self.pos += direction * 4  # entry speed (adjust feel here)
            else:
                self.state = "aim"
                self.state_timer = 0
                self.frame = 0

            # optional: still rotate toward target for drama
            dx = player_pos.x - self.pos.x
            dy = player_pos.y - self.pos.y
            target_angle = math.atan2(dy, dx)

            diff = (target_angle - self.angle + math.pi) % (2 * math.pi) - math.pi

            self.angle += max(-self.turn_speed, min(self.turn_speed, diff))

            return
        # -------------------
        # AIM STATE
        # -------------------
        elif self.state == "aim":

            dx = player_pos.x - self.pos.x
            dy = player_pos.y - self.pos.y
            target_angle = math.atan2(dy, dx)

            diff = (target_angle - self.angle + math.pi) % (2 * math.pi) - math.pi

            if diff > self.turn_speed:
                diff = self.turn_speed
            elif diff < -self.turn_speed:
                diff = -self.turn_speed

            self.angle += diff

            if self.state_timer > 120:
                self.state = "charge"
                self.state_timer = 0
                self.frame = 0

                self.velocity = pygame.Vector2(
                    math.cos(self.angle),
                    math.sin(self.angle)
                ) * self.charge_speed

        # -------------------
        # CHARGE STATE
        # -------------------
        elif self.state == "charge":
            self.velocity *= 0.99
            self.pos += self.velocity
            if self.state_timer > 60:
                self.state = "recover"
                self.state_timer = 0
                self.frame = 0
        
        # -------------------
        # RECOVERY STATE
        # -------------------
        elif self.state == "recover":
            self.velocity *= 0.95
            self.pos += self.velocity

            if self.state_timer % 45 == 0:
                bullet_count = 32
                angle_step = 360 / bullet_count

                forward = pygame.Vector2(math.cos(self.angle), math.sin(self.angle))

                for i in range(bullet_count):
                    direction = forward.rotate(i * angle_step)

                    self.bullets.append(Enemy_Bullet(self.pos, direction, 5, 7))

            if self.state_timer > self.recovery_time:
                self.state = "aim"
                self.state_timer = 0
                self.frame = 0

        if self.pos.x < 0:
            self.pos.x = width
        elif self.pos.x > width:
            self.pos.x = 0 
        if self.pos.y < 0:
            self.pos.y = height
        elif self.pos.y > height:
            self.pos.y = 0

        self.bullets = [b for b in self.bullets if b.alive()]
        for bullet in self.bullets:
            bullet.update()

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.animation_list[self.frame], -math.degrees(self.angle) - 90)
        rect = rotated_image.get_rect(center=self.pos)
        screen.blit(rotated_image, rect.topleft)

        for bullet in self.bullets:
            bullet.draw(screen)

class MotherShip(Enemy):
    def __init__(self):
        super().__init__(width // 2, height // 2)

        self.health = 8000
        self.base_damage = 10
        self.base_speed = 0
        self.hit_radius = 90

        self.angle = 0
        self.angle1 = 0
        self.angle2 = 0
        self.rotation_speed = 2  # degrees per frame
        self.state_timer = 0

        self.bullets = []
        self.shoot_timer = 0
        self.shoot_timer1 = 0
        self.shoot_timer2 = 0

        self.float_timer = 0
        self.float_amplitude = 25
        self.float_speed = 0.05

        self.spawn_timer = 0
        self.alpha = 0
        self.active = False
        self.intro_duration = 180  # ~3 seconds at 60 FPS

        self.sprite_sheet_image = load_image_alpha("enemies/mothership.png")
        self.sprite_sheet = spritesheet.SpriteSheet(self.sprite_sheet_image)

        self.animation_list = []
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 20

        # simple animation (adjust if you have more frames)
        for x in range(76):
            self.animation_list.append(self.sprite_sheet.get_image(x, 0, 256, 256, 0.8))

        self.shoot_sound = pygame.mixer.Sound("assets/audio/sfx/enemy/mothership_shoot.wav")

    @property
    def max_speed(self):
            return self.base_speed * self.speed_multiplier
    @property
    def final_damage(self):
            return self.base_damage * self.damage_multiplier

    def update(self, player_pos):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.frame += 1
            self.last_update = current_time
            if self.frame >= len(self.animation_list):
                self.frame = 0

        #fade in
        if not self.active:
            self.spawn_timer += 1

            if self.alpha < 255:
                self.alpha = min(255, self.spawn_timer * 2)

            if self.spawn_timer < self.intro_duration:
                return
            
            self.active = True

        self.float_timer += 1
        self.state_timer += 1

        if self.state_timer >= 1000:
            self.state_timer = 0

        if self.state_timer < 300:
            self.angle += 1
            self.shoot_timer += 1

            if self.shoot_timer % 5 == 0: 
                bullet_count = 8
                angle_step = 360 / bullet_count
                self.shoot_sound.play()

                for i in range(bullet_count):
                    direction = pygame.Vector2(1, 0).rotate(self.angle + i * angle_step)
                    self.bullets.append(Enemy_Bullet(self.pos, direction, self.final_damage, 6))

        elif self.state_timer < 600:
            self.angle -= 1
            self.shoot_timer += 1

            if self.shoot_timer % 5 == 0:
                bullet_count = 8
                angle_step = 360 / bullet_count
                self.shoot_sound.play()

                for i in range(bullet_count):
                    direction = pygame.Vector2(1, 0).rotate(self.angle + i * angle_step)
                    self.bullets.append(Enemy_Bullet(self.pos, direction, self.final_damage, 6))

        elif self.state_timer < 750:
            self.angle1 += 1
            self.shoot_timer1 += 1

            if self.shoot_timer1 % 20 == 0: 
                bullet_count = 4
                angle_step = 360 / bullet_count
                self.shoot_sound.play()

                for i in range(bullet_count):
                    direction = pygame.Vector2(1, 0).rotate(self.angle1 + i * angle_step)
                    self.bullets.append(Enemy_Bullet(self.pos, direction, self.final_damage, 6))

            self.angle2 -= 1
            self.shoot_timer2 += 1

            if self.shoot_timer2 % 10 == 0:
                bullet_count = 4
                angle_step = 360 / bullet_count
                self.shoot_sound.play()

                for i in range(bullet_count):
                    direction = pygame.Vector2(1, 0).rotate(self.angle2 + i * angle_step)
                    self.bullets.append(Enemy_Bullet(self.pos, direction, self.final_damage, 6))

        self.bullets = [b for b in self.bullets if b.alive()]
        for bullet in self.bullets:
            bullet.update()

    def draw(self, screen):
        float_offset = math.sin(self.float_timer * self.float_speed) * self.float_amplitude
        image = self.animation_list[self.frame].copy()
        image.set_alpha(self.alpha)
        rect = image.get_rect(center=(self.pos.x, self.pos.y + float_offset))
        screen.blit(image, rect.topleft)

        for bullet in self.bullets:
            bullet.draw(screen)