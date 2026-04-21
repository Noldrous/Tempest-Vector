from settings import *
from player import *
from enemy import *
from weapons import *
from waves import *

class Game:
    def __init__(self):
        #setup
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        pygame.display.set_caption("Tempest Vector")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 40)
        self.running = True
        
        self.assets = {
            "background": load_image_alpha('background/background.png'),
            "shadow1": load_image_alpha('background/shadow1.png'),
            "shadow2": load_image_alpha('background/shadow2.png'),
            "star1": load_image_alpha('background/star1.png'),
            "star2": load_image_alpha('background/star2.png'),
            "celestial1": load_image_alpha('background/celestial1.png'),
            "celestial2": load_image_alpha('background/celestial2.png'),
            "celestial3": load_image_alpha('background/celestial3.png'),
            "title": load_image_alpha('ui/Title.png'),
            "play_button1": load_image_alpha('ui/button_play.png'),
            "play_button2": load_image_alpha('ui/hoveredButton_play.png'),
            "credits_button1": load_image_alpha('ui/button_credits.png'),
            "credits_button2": load_image_alpha('ui/hoveredButton_credits.png'),
            "quit_button1": load_image_alpha('ui/exit_button.png'),
            "quit_button2": load_image_alpha('ui/sad.png'),
            "player_ship": load_image_alpha('player/player.png'),
            "seeker": load_image_alpha('enemies/seeker.png'),
        }

        self.bg_positions = {
            "shadow1": 0,
            "shadow2": 0,
            "star1": 0,
            "star2": 0,
            "celestial1": 0,
            "celestial2": 0,
            "celestial3": 0,
        }
        self.background = pygame.transform.scale(self.assets["background"], (self.width, self.height))
        self.sway_time = 0

    def setbackground(self, key, speed, pos1, pos2, pos3):
        bg = self.assets[key]
        bg_width = bg.get_width()
        x = self.bg_positions[key]

        for y in (pos1, pos2, pos3):
            self.screen.blit(bg, (x, y))
            self.screen.blit(bg, (x + bg_width, y))

        x -= speed
        if x <= -5760:
            x = 0

        self.bg_positions[key] = x

    def start_menu(self):
        title = pygame.transform.scale(self.assets["title"], (self.width / 2.4, self.height / 2.9))
        play1 = pygame.transform.scale(self.assets["play_button1"], (self.width // 8, self.height // 14))
        play2 = pygame.transform.scale(self.assets["play_button2"], (self.width // 8, self.height // 14))
        credits1 = pygame.transform.scale(self.assets["credits_button1"], (self.width // 8, self.height // 14))
        credits2 = pygame.transform.scale(self.assets["credits_button2"], (self.width // 8, self.height // 14))
        quit1 = self.assets["quit_button1"]
        quit2 = self.assets["quit_button2"]
        ship = pygame.transform.scale(self.assets["player_ship"], (240, 240))
        ship = pygame.transform.rotate(ship, -90)
        
        play_rect = play1.get_rect(bottomleft=(self.width - self.width // 5, self.height - self.height // 5))
        credit_rect = credits1.get_rect(bottomleft=(self.width - self.width // 5, self.height - self.height // 9))
        quit_rect = quit1.get_rect(topright=(self.width - 50, 50))
        title_rect = title.get_rect(topleft=(75, 75))

        play_pressed = False

        shadow1_speed = 4
        shadow2_speed = 1
        celestials = 1.2
        star1_speed = 3
        star2_speed = 2

        ship_base_x = self.width // 3
        ship_move_x = 0
        ship_y = self.height // 1.9
        ship_particles = []

        while True:
            dt = self.clock.tick(60) / 1000.0   
            mouse = pygame.mouse.get_pos()
            
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_buttons = pygame.mouse.get_pressed()
                    if play_rect.collidepoint(mouse) and mouse_buttons[0]:
                        play_pressed = True
                            
                    if quit_rect.collidepoint(mouse) and mouse_buttons[0]:
                        pygame.quit()
                        sys.exit()
            
            if play_pressed:
                shadow1_speed = 8
                shadow2_speed = 8
                celestials = 10
                star1_speed = 8
                star2_speed = 6
                play_rect.x += 15
                credit_rect.x += 15
                quit_rect.x += 15
                title_rect.x -= 25

                ship_move_x += 30

                if ship_base_x + ship_move_x > self.width + 500:
                    self.game()

            self.screen.blit(self.background, (0, 0))

            play_button = play2 if play_rect.collidepoint(mouse) else play1
            credits_button = credits2 if credit_rect.collidepoint(mouse) else credits1
            quit_button = quit2 if quit_rect.collidepoint(mouse) else quit1
            
            self.setbackground("shadow1", shadow1_speed, 0, 360, 720)
            self.setbackground("shadow2", shadow2_speed, 0, 360, 720)
            self.setbackground("celestial1", celestials, 300, self.height, self.height)
            self.setbackground("celestial2", celestials, 0, self.height, self.height)
            self.setbackground("celestial3", celestials, 500, self.height, self.height)
            self.setbackground("star1", star1_speed, 0, 360, 720)
            self.setbackground("star2", star2_speed, 0, 360, 720)
            
            self.sway_time += dt

            offset_x = math.sin(self.sway_time * 2) * 10
            offset_y = math.cos(self.sway_time * 1.5) * 30

            ship_rect = ship.get_rect(topleft=(ship_base_x + ship_move_x + offset_x, ship_y + offset_y))

            if ship_move_x < width//2:  
                pos = pygame.Vector2(
                    ship_rect.left + 75,
                    ship_rect.centery - 3
                )

                vel = pygame.Vector2(
                    random.uniform(-3, -1),
                    random.uniform(-1, 1)
                )

                ship_particles.append(Particle(pos, vel))
            for particle in ship_particles:
                particle.update()
            ship_particles = [p for p in ship_particles if p.life > 0]
            for particle in ship_particles:
                particle.draw(self.screen)
            

            self.screen.blit(ship, ship_rect)
            
            self.screen.blit(title, title_rect)

            self.screen.blit(play_button, play_rect)
            self.screen.blit(credits_button, credit_rect)
            self.screen.blit(quit_button, quit_rect)

            pygame.display.update()
            
    def pause_menu(self):
        while True:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_buttons = pygame.mouse.get_pressed()
                    if resume_button.collidepoint(mouse) and mouse_buttons[0]:
                        return

                    if quit_button.collidepoint(mouse) and mouse_buttons[0]:
                        pygame.quit()
                        sys.exit()

            resume_button = pygame.Rect(width//2 - 70, height - 500, 140, 50)
            quit_button = pygame.Rect(width //2 - 70, height - 400, 140, 50)

            pygame.draw.rect(self.screen, "skyblue" if resume_button.collidepoint(mouse) else "darkgray", resume_button)
            pygame.draw.rect(self.screen, "skyblue" if quit_button.collidepoint(mouse) else "darkgray", quit_button)

            play_text = self.font.render("Resume", True, "white")
            quit_text = self.font.render("Quit", True, "white")

            self.screen.blit(play_text, (width//2 - 50, height - 500))
            self.screen.blit(quit_text, (width//2 - 50, height - 400))

            pygame.display.update()

    def game_over(self):
        while True:
            mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_buttons = pygame.mouse.get_pressed()
                    if try_again_button.collidepoint(mouse) and mouse_buttons[0]:
                        self.game()

                    if quit_button.collidepoint(mouse) and mouse_buttons[0]:
                        pygame.quit()
                        sys.exit()

            try_again_button = pygame.Rect(width//2 - 70, height - 500, 140, 50)
            quit_button = pygame.Rect(width //2 - 70, height - 400, 140, 50)

            pygame.draw.rect(self.screen, "skyblue" if try_again_button.collidepoint(mouse) else "darkgray", try_again_button)
            pygame.draw.rect(self.screen, "skyblue" if quit_button.collidepoint(mouse) else "darkgray", quit_button)

            try_again_text = self.font.render("Try Again", True, "white")
            quit_text = self.font.render("Quit", True, "white")

            self.screen.blit(try_again_text, (width//2 - 50, height - 500))
            self.screen.blit(quit_text, (width//2 - 50, height - 400))

            pygame.display.update()

    def game(self):
        player = Player(self.assets["player_ship"])
        player_bullets = []
        weapons = Weapons()
        player.weapon = weapons.main  # Connect player to the weapons system

        # HEALTH BAR
        hpBar_x = self.width // 2 - 400
        hpBar_y = self.height - 40
        health_bar = HealthBar(hpBar_x, hpBar_y, 800, 20, player.health)
        
        shield_bar_x = self.width // 2 - 400
        shield_bar_y = self.height - 70
        shield_bar = ShieldBar(shield_bar_x, shield_bar_y, 800, 20, player.shield)

        # Initialize Wave Manager
        wave_manager = WaveManager()
        wave_message = ""
        wave_message_time = 0
        wave_message_duration = 2000
        last_announced_wave = 0

        while True:
            dt = self.clock.tick(60) / 1000.0  # Delta time in seconds - Change 60 to 30 or 45 to slow down
            mouse = pygame.mouse.get_pos()

            self.screen.blit(self.background, (0, 0))
            self.setbackground("shadow1", 2, 0, 360, 720)
            self.setbackground("shadow2", 1, 0, 360, 720)
            self.setbackground("celestial1", 0.5, 300, self.height, self.height)
            self.setbackground("celestial2", 0.4, 0, self.height, self.height)
            self.setbackground("celestial3", 0.3, 500, self.height, self.height)
            self.setbackground("star1", 0.8, 0, 360, 720)
            self.setbackground("star2", 0.5, 0, 360, 720)
            
            #pause_button -------------------------------------------------------------------------------------------------------------------------------------------------------
            pause_button = pygame.Rect(width - 50, 25, 25, 50)
            pygame.draw.rect(self.screen, "skyblue" if pause_button.collidepoint(mouse) else "darkgray", pause_button)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_buttons = pygame.mouse.get_pressed()
                    if pause_button.collidepoint(mouse) and mouse_buttons[0]:
                        self.pause_menu()

            #player -------------------------------------------------------------------------------------------------------------------------------------------------------
            if player.entering:
                player.entrance()
            else:
                player.move()
            player.regen_shield()
            player.draw(self.screen)

            if player.health <= 0:
                self.game_over()

            health_bar.draw(self.screen, player.health)
            shield_bar.draw(self.screen, player.shield)
            
            # Wave info display
            wave_text = self.font.render(f"Wave: {wave_manager.get_current_wave_number()}", True, "white")
            self.screen.blit(wave_text, (20, 60))
            
            enemy_count_text = self.font.render(f"Enemies: {len(wave_manager.get_all_enemies())}", True, "white")
            self.screen.blit(enemy_count_text, (20, 100))

            # shoot with equipped weapon -------------------------------------------------------------------------------------------------------------------------------------------------------
            if player.weapon is not None and pygame.mouse.get_pressed()[0] and not weapons.should_show_message():
                bullets = player.weapon.shoot(
                    player.ship_pos.x,
                    player.ship_pos.y,
                    player.angle
                )

                if bullets:
                    player_bullets.extend(bullets)

                    # recoil ONLY when actual shot happens
                    recoil_strength = {
                        "Machine Gun": 1,
                        "Shotgun": 5,
                        "Rail Gun": 6,
                        "Rockets": 8
                    }

                    player.apply_recoil(
                        player.angle,
                        recoil_strength[player.weapon.name]
                    )

                # weapon swap check
                if player.weapon.ammo <= 0:
                    weapons.cycle_weapon()
                    player.weapon = weapons.main

            for bullet in player_bullets:
                bullet.update()
                bullet.draw(self.screen)

            player_bullets = [bullet for bullet in player_bullets if bullet.is_alive()]
            weapon_name = player.weapon.name if player.weapon else "No Weapon"
            ammo_text = player.weapon.ammo if player.weapon else 0
            status_text = self.font.render(f"{weapon_name} Ammo: {ammo_text}", True, "white")
            self.screen.blit(status_text, (20, 20))

            # Display "changing weapon" message if cycling
            if weapons.should_show_message():
                message_text = self.font.render("Swapping Weapon...", True, (255, 165, 0))
                message_rect = message_text.get_rect(center=(self.width // 2, self.height // 2))
                self.screen.blit(message_text, message_rect)

            #wave management -------------------------------------------------------------------------------------------------------------------------------------------------------
            wave_manager.update(dt)
            all_enemies = wave_manager.get_all_enemies()

            current_wave = wave_manager.get_current_wave_number()
            if not wave_manager.is_wave_complete() and current_wave != last_announced_wave:
                wave_message = f"Wave {current_wave}"
                wave_message_time = pygame.time.get_ticks()
                last_announced_wave = current_wave

            #enemies -------------------------------------------------------------------------------------------------------------------------------------------------------
            for enemy in all_enemies:
                enemy.update(player.ship_pos)
                enemy.draw(self.screen)

            # Remove dead enemies
            for enemy in all_enemies[:]:
                if enemy.health <= 0:
                    wave_manager.remove_enemy(enemy)

            #collision detection -------------------------------------------------------------------------------------------------------------------------------------------------------
            # Player bullets hit enemies
            for bullet in player_bullets[:]:
                for enemy in all_enemies:
                    distance = enemy.pos.distance_to(bullet.pos)

                    if distance < enemy.size + bullet.radius:
                        enemy.take_damage(bullet.damage)
                        if bullet in player_bullets:
                            player_bullets.remove(bullet)
                        break
            
            # Enemy collision with player
            for enemy in all_enemies:
                if enemy.__class__.__name__ == "SeekerEnemy":
                    distance = player.ship_pos.distance_to(enemy.pos)
                    if distance < player.ship_radius + enemy.hit_radius:
                        player.take_damage(enemy.contact_damage)
                        break
            
            for enemy in all_enemies:
                if enemy.__class__.__name__ == "ShooterEnemy":
                    distance = player.ship_pos.distance_to(enemy.pos)
                    if distance < player.ship_radius + enemy.hit_radius:
                        player.take_damage(enemy.contact_damage)
                        break
            
            # Enemy bullets hit player
            for enemy in all_enemies:
                if hasattr(enemy, 'bullets'):
                    for bullet in enemy.bullets[:]:
                        distance = player.ship_pos.distance_to(bullet.pos)

                        if distance < player.ship_radius + bullet.radius:
                            player.take_damage(bullet.damage)
                            enemy.bullets.remove(bullet)
                            break
            
            # Wave start message
            if wave_message and (pygame.time.get_ticks() - wave_message_time) < wave_message_duration:
                wave_msg_surface = self.font.render(wave_message, True, (255, 255, 0))
                wave_msg_rect = wave_msg_surface.get_rect(center=(self.width // 2, 120))
                self.screen.blit(wave_msg_surface, wave_msg_rect)

            # Victory condition
            if wave_manager.is_wave_complete():
                victory_text = self.font.render("ALL WAVES COMPLETE! VICTORY!", True, (0, 255, 0))
                victory_rect = victory_text.get_rect(center=(self.width // 2, self.height // 2))
                self.screen.blit(victory_text, victory_rect)
                pygame.display.update()
                pygame.time.wait(3000)
                self.start_menu()

            pygame.display.update()

if __name__ == "__main__":
    Game().start_menu()