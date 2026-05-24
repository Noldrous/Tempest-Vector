from settings import *
from player import *
from enemy import *
from weapons import *
from waves import *
from upgrades import *
from particle import *

class Game:
    def __init__(self):
        #setup
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        pygame.display.set_caption("Tempest Vector")
        self.clock = pygame.time.Clock()
        self.sfont = pygame.font.Font("assets/font/black-and-white.ttf", 20)
        self.mfont = pygame.font.Font("assets/font/black-and-white.ttf", 35)
        self.svcfont = pygame.font.Font("assets/font/VCR.ttf", 20)
        self.lvcfont = pygame.font.Font("assets/font/VCR.ttf", 80)
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
            "title": load_image_alpha('ui/title.png'),
            "play_button1": load_image_alpha('ui/button_play.png'),
            "play_button2": load_image_alpha('ui/hoveredButton_play.png'),
            "tutorial_button1": load_image_alpha('ui/button_tutorial.png'),
            "tutorial_button2": load_image_alpha('ui/hoveredButton_tutorial.png'),
            "tutorial_image": load_image_alpha('ui/tutorial.png'),
            "back_button": load_image_alpha('ui/back_button.png'),
            "quit_button1": load_image_alpha('ui/button_quit.png'),
            "quit_button2": load_image_alpha('ui/hoveredButton_quit.png'),
            "resume_button1": load_image_alpha('ui/resume1.png'),
            "resume_button2": load_image_alpha('ui/resume2.png'),
            "restart_button1": load_image_alpha('ui/restart1.png'),
            "restart_button2": load_image_alpha('ui/restart2.png'),
            "quit1": load_image_alpha('ui/quit1.png'),
            "quit2": load_image_alpha('ui/quit2.png'),
            "over_restart1": load_image_alpha('ui/over_restart1.png'),
            "over_restart2": load_image_alpha('ui/over_restart2.png'),
            "over_quit1": load_image_alpha('ui/over_quit1.png'),
            "over_quit2": load_image_alpha('ui/over_quit2.png'),
            "skull1": load_image_alpha('ui/skull1.png'),
            "skull2": load_image_alpha('ui/skull2.png'),
            "player_ship": load_image_alpha('player/shiper.png'),
            "cursor": load_image_alpha("ui/crosshair.png"), 
            "cursor_scaled": pygame.transform.scale(load_image_alpha("ui/crosshair.png"), (48, 48))
        }

        self.sfx = {
            "explosion": pygame.mixer.Sound("assets/audio/sfx/enemy/Explosion.wav"),
            "player_hit": pygame.mixer.Sound("assets/audio/sfx/player/Hit.wav"),
            "enemy_hit": pygame.mixer.Sound("assets/audio/sfx/enemy/enemy_hit.wav"),
            "crash": pygame.mixer.Sound("assets/audio/sfx/crash.wav"),
            "skeleton": pygame.mixer.Sound("assets/audio/sfx/skeleton.mp3"),
            "boost": pygame.mixer.Sound("assets/audio/sfx/boost.mp3"),
            "boost2": pygame.mixer.Sound("assets/audio/sfx/boost2.mp3"),
            "click": pygame.mixer.Sound("assets/audio/sfx/UI/click.wav"),
            "upgrade": pygame.mixer.Sound("assets/audio/sfx/UI/upgrade.wav"),
        }

        self.music = {
            "menu": "assets/audio/music/menu_music.mp3",
            "game": "assets/audio/music/game_music.mp3"
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

        self.score = 0

    def setbackground(self, key, speed, pos1, pos2, pos3, pos4, pos5):
        bg = self.assets[key]
        bg_width = bg.get_width()
        x = self.bg_positions[key]

        for y in (pos1, pos2, pos3, pos4, pos5):
            self.screen.blit(bg, (x, y))
            self.screen.blit(bg, (x + bg_width, y))

        x -= speed
        if x <= -5760:
            x = 0

        self.bg_positions[key] = x

    def start_menu(self):
        title = pygame.transform.scale(self.assets["title"], (self.width // 1.6, self.height // 2.5))
        play1 = pygame.transform.scale(self.assets["play_button1"], (self.width // 8, self.height // 14))
        play2 = pygame.transform.scale(self.assets["play_button2"], (self.width // 8, self.height // 14))
        tutorial1 = pygame.transform.scale(self.assets["tutorial_button1"], (self.width // 8, self.height // 14))
        tutorial2 = pygame.transform.scale(self.assets["tutorial_button2"], (self.width // 8, self.height // 14))
        tutorial_image = pygame.transform.scale(self.assets["tutorial_image"], (self.width // 1.6, self.height // 1.5))
        back = self.assets["back_button"]
        quit1 = pygame.transform.scale(self.assets["quit_button1"], (self.width // 8, self.height // 14))
        quit2 = pygame.transform.scale(self.assets["quit_button2"], (self.width // 8, self.height // 14))
        
        sprite_sheet = SpriteSheet(self.assets["player_ship"])
        menu_frames = []
        frame_width = 48
        frame_height = 48
        scale = 4  
        for i in range(12):  
            frame = sprite_sheet.get_image(i, 3, frame_width, frame_height, scale)
            frame = pygame.transform.rotate(frame, -90)
            menu_frames.append(frame)
        menu_frame_index = 0
        menu_anim_speed = 0.1

        ship = pygame.transform.scale(self.assets["player_ship"], (240, 240))
        ship = pygame.transform.rotate(ship, -90)
        
        play_rect = play1.get_rect(bottomleft=(self.width - self.width // 5, self.height - self.height // 3.5))
        tutorial_rect = tutorial1.get_rect(bottomleft=(self.width - self.width // 5, self.height - self.height // 5))
        tutorial_rect_img = tutorial_image.get_rect(center=(self.width // 2, self.height // 2))
        back_rect = back.get_rect(topright=(self.width - 40, 40))
        quit_rect = quit1.get_rect(bottomleft=(self.width - self.width // 5, self.height - self.height // 9))
        title_rect = title.get_rect(topleft=(50, 50))

        play_pressed = False
        tutorial_pressed = False

        shadow1_speed = 4
        shadow2_speed = 1
        celestials = 1.2
        star1_speed = 3
        star2_speed = 2

        ship_base_x = self.width // 3
        ship_move_x = 0
        ship_y = self.height // 1.7
        ship_particles = []

        pygame.mixer.music.load(self.music["menu"])
        pygame.mixer.music.play(-1)
        boost_played = False

        sway_time = 0

        while True:
            dt = self.clock.tick(60) / 1000.0   
            sway_time += dt
            mouse = pygame.mouse.get_pos()
            
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_buttons = pygame.mouse.get_pressed()

                    # NORMAL MENU
                    if not tutorial_pressed:

                        if play_rect.collidepoint(mouse) and mouse_buttons[0]:
                            pygame.mixer.music.stop()
                            self.sfx["click"].play()
                            play_pressed = True

                        if tutorial_rect.collidepoint(mouse) and mouse_buttons[0]:
                            self.sfx["click"].play()
                            tutorial_pressed = True

                        if quit_rect.collidepoint(mouse) and mouse_buttons[0]:
                            pygame.quit()
                            sys.exit()

                    # TUTORIAL SCREEN
                    else:
                        if back_rect.collidepoint(mouse) and mouse_buttons[0]:
                            self.sfx["click"].play()
                            tutorial_pressed = False

            
            if play_pressed:
                shadow1_speed = 8
                shadow2_speed = 8
                celestials = 10
                star1_speed = 8
                star2_speed = 6
                play_rect.x += 15
                tutorial_rect.x += 15
                quit_rect.x += 15
                title_rect.x -= 25

                ship_move_x += 30
                if not boost_played:
                    self.sfx["boost"].play()
                    boost_played = True

                if ship_base_x + ship_move_x > self.width + 500:
                    self.game()

            self.screen.blit(self.background, (0, 0))
            
            self.setbackground("shadow1", shadow1_speed, 0, 360, 720, 1080, 1440)
            self.setbackground("shadow2", shadow2_speed, 0, 360, 720, 1080, 1440)
            self.setbackground("celestial1", celestials, 300, self.height, self.height, self.height, self.height)
            self.setbackground("celestial2", celestials, 0, self.height, self.height, self.height, self.height)
            self.setbackground("celestial3", celestials, 500, self.height, self.height, self.height, self.height)
            self.setbackground("star1", star1_speed, 0, 360, 720, 1080, 1440)
            self.setbackground("star2", star2_speed, 0, 360, 720, 1080, 1440)

            if tutorial_pressed:
                # dark overlay
                overlay = pygame.Surface((self.width, self.height))
                overlay.set_alpha(180)
                overlay.fill((0, 0, 0))
                self.screen.blit(overlay, (0, 0))
                self.screen.blit(tutorial_image, tutorial_rect_img)
                self.screen.blit(back, back_rect)

            else:
                play_button = play2 if play_rect.collidepoint(mouse) else play1
                tutorial_button = tutorial2 if tutorial_rect.collidepoint(mouse) else tutorial1
                quit_button = quit2 if quit_rect.collidepoint(mouse) else quit1

                offset_x = math.sin(sway_time * 2) * 10
                offset_y = math.cos(sway_time * 1.5) * 30

                ship_rect = ship.get_rect(topleft=(ship_base_x + ship_move_x + offset_x, ship_y + offset_y))

                #particle
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
                ship_particles[:] = [p for p in ship_particles if p.life > 0]
                for particle in ship_particles:
                    particle.draw(self.screen)
                
                #animation
                menu_frame_index += menu_anim_speed
                if menu_frame_index >= len(menu_frames):
                    menu_frame_index = 0

                ship = menu_frames[int(menu_frame_index)]

                self.screen.blit(ship, ship_rect)
                
                self.screen.blit(title, title_rect)

                self.screen.blit(play_button, play_rect)
                self.screen.blit(tutorial_button, tutorial_rect)
                self.screen.blit(quit_button, quit_rect)

            pygame.display.update()
            
    def pause_menu(self, background):
        pygame.mouse.set_visible(True)
        panel_width = 300
        panel_x = self.width
        target_x = self.width - panel_width

        overlay_alpha = 0

        anim_speed = 20
        fade_speed = 15

        resume1 = pygame.transform.scale(self.assets["resume_button1"], (200, 60))
        resume2 = pygame.transform.scale(self.assets["resume_button2"], (200, 60))
        restart1 = pygame.transform.scale(self.assets["restart_button1"], (200, 60))
        restart2 = pygame.transform.scale(self.assets["restart_button2"], (200, 60))
        quit1 = pygame.transform.scale(self.assets["quit1"], (200, 60))
        quit2 = pygame.transform.scale(self.assets["quit2"], (200, 60))

        resume = False

        while True:
            mouse = pygame.mouse.get_pos()
            resume_rect = pygame.Rect(panel_x + 50, 200, 200, 60)
            restart_rect = pygame.Rect(panel_x + 50, 300, 200, 60)
            quit_rect = pygame.Rect(panel_x + 50, 400, 200, 60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if resume_rect.collidepoint(mouse):
                        pygame.mixer.music.set_volume(1.0)
                        self.sfx["click"].play()
                        resume = True
                    if restart_rect.collidepoint(mouse):
                        pygame.mixer.music.stop()
                        self.sfx["click"].play()
                        self.score = 0
                        self.game()
                    if quit_rect.collidepoint(mouse):
                        self.start_menu()

            if not resume:
                panel_x = max(target_x, panel_x - anim_speed)
                overlay_alpha = min(180, overlay_alpha + fade_speed)
            else:
                panel_x = min(self.width, panel_x + anim_speed)
                overlay_alpha = max(0, overlay_alpha - fade_speed)

                if panel_x >= self.width and overlay_alpha <= 0:
                    return

            # -------- Draw --------
            self.screen.blit(background, (0, 0))

            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, overlay_alpha))
            self.screen.blit(overlay, (0, 0))

            panel_rect = pygame.Rect(panel_x, 0, panel_width, self.height)
            pygame.draw.rect(self.screen, (20, 20, 50), panel_rect)
            
            # Grid background
            grid_size = 25
            grid_color = (35, 45, 75)

            # Vertical lines
            for x in range(int(panel_x), int(panel_x + panel_width), grid_size):
                pygame.draw.line(
                    self.screen,
                    grid_color,
                    (x, 0),
                    (x, self.height),
                    1
                )

            # Horizontal lines
            for y in range(0, self.height, grid_size):
                pygame.draw.line(
                    self.screen,
                    grid_color,
                    (panel_x, y),
                    (panel_x + panel_width, y),
                    1
                )
            
            
            pygame.draw.rect(self.screen, "darkgray", (panel_x, 0, 300, 100), 35)
            pygame.draw.rect(self.screen, "darkgray", (panel_x + 10, 0, 60, 100)) 
            pygame.draw.rect(self.screen, "darkgray", (panel_x + 230, 0, 60, 100))
            pygame.draw.rect(self.screen, (255, 255, 255), (panel_x, 0, 300, 100), 5) 
            pygame.draw.rect(self.screen, (255, 255, 255), panel_rect, 5)

            resume_button = resume2 if resume_rect.collidepoint(mouse) else resume1
            restart_button = restart2 if restart_rect.collidepoint(mouse) else restart1
            quit_button = quit2 if quit_rect.collidepoint(mouse) else quit1

            paused_text = self.mfont.render("Paused", True, "darkgray")

            self.screen.blit(paused_text, (panel_x + 70, 35))
            self.screen.blit(resume_button, resume_rect)
            self.screen.blit(restart_button, restart_rect)
            self.screen.blit(quit_button, quit_rect)

            pygame.display.update()
            self.clock.tick(60)

    def game_over(self, background):
        pygame.mouse.set_visible(True)
        panel_width = self.width
        panel_height = self.height // 4
        right_panel_x = self.width
        right_panel_targetx = 0
        left_panel_x = -self.width
        left_panel_targetx = 0

        anim_speed = 20

        restart1 = pygame.transform.scale(self.assets["over_restart1"], (200, 60))
        restart2 = pygame.transform.scale(self.assets["over_restart2"], (200, 60))
        quit1 = pygame.transform.scale(self.assets["over_quit1"], (200, 60))
        quit2 = pygame.transform.scale(self.assets["over_quit2"], (200, 60))
        skull1 = pygame.transform.scale(self.assets["skull1"], (self.width//4,self.width//4))
        skull2 = pygame.transform.scale(self.assets["skull2"], (self.width//4,self.width//4))
        game_over_text = self.lvcfont.render("[-_-] YOU ARE DEAD [-_-]", False, "white")
        score_text = self.svcfont.render(f"SCORE: {self.score}", False, "white")

        text_rect = game_over_text.get_rect(center=(self.width//2, 60))
        score_rect = score_text.get_rect(center=(self.width//2, 120))
        restart_rect = restart1.get_rect(center=(self.width//2, self.height - 180))
        quit_rect = quit1.get_rect(center=(self.width//2, self.height - 100))
        skull_rect = skull1.get_rect(center=(self.width//2, self.height//2 - 75))

        timer = 0
        skeleton_played = True

        while True:
            mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_buttons = pygame.mouse.get_pressed()
                    if restart_rect.collidepoint(mouse) and mouse_buttons[0]:
                        self.sfx["click"].play()
                        self.score = 0
                        self.game()

                    if quit_rect.collidepoint(mouse) and mouse_buttons[0]:
                        pygame.quit()
                        sys.exit()

            self.screen.blit(background, (0, 0))
                        
            right_panel_x = max(right_panel_targetx, right_panel_x - anim_speed)
            left_panel_x = min(left_panel_targetx, left_panel_x + anim_speed)

            pygame.draw.rect(self.screen, (0, 0, 0), (right_panel_x, 0, panel_width, panel_height))
            pygame.draw.rect(self.screen, (0, 0, 0), (right_panel_x, panel_height*2, panel_width, panel_height))
            pygame.draw.rect(self.screen, (0, 0, 0), (left_panel_x, panel_height, panel_width, panel_height))
            pygame.draw.rect(self.screen, (0, 0, 0), (left_panel_x, panel_height*3, panel_width, panel_height))

            restart_button = restart2 if restart_rect.collidepoint(mouse) else restart1
            quit_button = quit2 if quit_rect.collidepoint(mouse) else quit1

            timer += 1
            if timer < 90:
                skull = skull1
                skeleton_played = False
            else:
                skull = skull2
                if not skeleton_played:
                    self.sfx["skeleton"].play()
                    skeleton_played = True

            if timer > 180:
                timer=0

            self.screen.blit(game_over_text, text_rect)
            self.screen.blit(score_text, score_rect)
            self.screen.blit(restart_button, restart_rect)
            self.screen.blit(quit_button, quit_rect)
            self.screen.blit(skull, skull_rect)

            pygame.display.update()

    def game(self):
        player = Player(self.assets["player_ship"])
        player_bullets = []
        weapons = Weapons()
        player.weapon = weapons.main  # Connect player to the weapons system
        load_bullet_sheets()
        
        # HEALTH BAR
        hpBar_x = 50
        hpBar_y = self.height - 550
        health_bar = HealthBar(hpBar_x, hpBar_y, 20, 500)
        
        shield_bar_x = 75
        shield_bar_y = self.height - 550
        shield_bar = ShieldBar(shield_bar_x, shield_bar_y, 20, 500)

        # Initialize Wave Manager
        wave_manager = WaveManager()
        wave_message = ""
        wave_message_time = 0
        wave_message_duration = 2000
        last_announced_wave = 0

        #UPGRADE SYSTEM
        font_small = pygame.font.SysFont("Arial", 20)
        font_large = pygame.font.SysFont("Arial", 28)

        # GAME STATE
        show_upgrade_screen = False
        upgrade_selected = False
        upgrade_trigger_time = 0
        upgrade_fade_alpha = 0
        upgrade_cards = []
        upgrade_delay = 1.0  # 1 second delay before upgrade cards
        game_time = 0.0

        ui_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        ui_alpha = 0
        ui_fade_speed = 300

        cursor_rect = self.assets["cursor_scaled"].get_rect()

        boost_played = False
        music_started = False

        while True:
            dt = self.clock.tick(60) / 1000.0
            game_time += dt
            mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    # If the mouse is moved, set the center of the rect
                    # to the mouse pos. You can also use pygame.mouse.get_pos()
                    # if you're not in the event loop.
                    cursor_rect.center = event.pos

                if show_upgrade_screen and not upgrade_selected:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, card in enumerate(upgrade_cards):
                        if card.handle_event(event, mouse_pos):
                            upgrade_selected = True
                            self.sfx["upgrade"].play()

                            # Animate cards
                            for other_card in upgrade_cards:
                                other_card.animating_out = True

                                if other_card == card:
                                    other_card.selected = True
                                    other_card.animation_direction = -1  # goes UP
                                else:
                                    other_card.animation_direction = 1   # goes DOWN

                            selected_upgrade = card.title
                            upgrade_animation_start = pygame.time.get_ticks()
                            
                else:
                    upgrade_selected = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            player.boost_sound.stop()
                            pygame.mixer.music.set_volume(0.5)
                            self.sfx["click"].play()
                            pause_bg = self.screen.copy()
                            self.pause_menu(pause_bg)
                            

            ui_alpha = min(255, ui_alpha + ui_fade_speed * dt)
            ui_surface.fill((0, 0, 0, 0))  # clear with transparency
            

            self.screen.blit(self.background, (0, 0))
            self.setbackground("shadow1", 2, 0, 360, 720, 1080, 1440)
            self.setbackground("shadow2", 1, 0, 360, 720, 1080, 1440)
            self.setbackground("celestial1", 0.5, 300, self.height, self.height, self.height, self.height)
            self.setbackground("celestial2", 0.4, 0, self.height, self.height, self.height, self.height)
            self.setbackground("celestial3", 0.3, 500, self.height, self.height, self.height, self.height)
            self.setbackground("star1", 0.8, 0, 360, 720, 1080, 1440)
            self.setbackground("star2", 0.5, 0, 360, 720, 1080, 1440)

            #player -------------------------------------------------------------------------------------------------------------------------------------------------------
            if player.entering:
                player.entrance()
                if not boost_played:
                    self.sfx["boost2"].play()
                    boost_played = True
            else:
                player.move()

                if not music_started:
                    pygame.mixer.music.load(self.music["game"])
                    pygame.mixer.music.play(-1)
                    music_started = True

            player.regen_shield()
            player.draw(self.screen)

            if player.health <= 0:
                pygame.mixer.music.stop()
                player.boost_sound.stop()
                game_over_bg = self.screen.copy()
                self.game_over(game_over_bg)

            health_bar.draw(ui_surface, player.health, player.max_health)
            shield_bar.draw(ui_surface, player.shield, player.max_shield)

            # shoot with equipped weapon -------------------------------------------------------------------------------------------------------------------------------------------------------
            if not show_upgrade_screen:
                player.shoot(player.weapon, player_bullets, weapons)

            # weapon swap check
            if player.weapon.ammo <= 0:
                weapons.cycle_weapon()
                player.weapon = weapons.main

            for bullet in player_bullets:
                bullet.update(all_enemies)
                bullet.draw(self.screen)

            # Update waves to get all_enemies before checking bullet lifetimes
            if not show_upgrade_screen:
                wave_manager.update(dt)
            
            all_enemies = wave_manager.all_enemies
            
            # Check for exploded bullets (when lifetime expires) and create visual effect
            alive_bullets = []
            for bullet in player_bullets:
                alive = bullet.is_alive(all_enemies, player_bullets)
                # If bullet just exploded (not alive and has explosion_radius), create visual effect
                if not alive and bullet.explosion_radius > 0 and not hasattr(bullet, '_visual_created'):
                    bullet._visual_created = True
                    explosion = Explosion(int(bullet.pos.x), int(bullet.pos.y), bullet.explosion_radius)
                    explosion_group.add(explosion)
                    self.sfx["explosion"].play()
                if alive:
                    alive_bullets.append(bullet)
            
            player_bullets = alive_bullets

            weapon_name = player.weapon.name if player.weapon else "No Weapon"
            ammo_text = player.weapon.ammo if player.weapon else 0
            current_wave = wave_manager.current_wave
            status_text = self.sfont.render(f"Wave: {current_wave} | {weapon_name} Ammo: {ammo_text}", False, "white")
            score_text = self.sfont.render(f"Score: {self.score}", False, "white")
            score_rect = score_text.get_rect(topright=(self.width - 20, 20))
            ui_surface.blit(status_text, (20, 20))
            ui_surface.blit(score_text, score_rect)

            # Display "changing weapon" message if cycling
            if weapons.should_show_message():
                message_text = self.sfont.render("Swapping Weapon...", False, (255, 165, 0))
                message_rect = message_text.get_rect(center=(self.width // 2, self.height // 2))
                ui_surface.blit(message_text, message_rect)
            
            # Check for upgrade trigger with DELAY
            if hasattr(wave_manager, 'upgrades_pending') and wave_manager.upgrades_pending and not show_upgrade_screen:
                if upgrade_trigger_time == 0:
                    upgrade_trigger_time = game_time  # Start delay timer
                
                elapsed_delay = game_time - upgrade_trigger_time
                delay_progress = elapsed_delay / upgrade_delay
                if delay_progress > 1.0:
                    show_upgrade_screen = True
                    upgrade_cards = Upgrade.generate_upgrades()
                    upgrade_fade_alpha = 0  # Start fade in
                elif delay_progress > 0.3:  # Show "WAVE CLEARED!" after 30% of delay
                    # WAVE CLEARED message
                    clear_msg = self.sfont.render("WAVE CLEARED!", True, (255, 255, 0))
                    clear_msg.set_alpha(int(255 * (delay_progress - 0.5) / 0.9))
                    clear_rect = clear_msg.get_rect(center=(self.width // 2, self.height // 3))
                    self.screen.blit(clear_msg, clear_rect)

            current_wave = wave_manager.current_wave
            if current_wave != last_announced_wave:
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
                    self.score += enemy.killed_score
                    # Create explosion animation at enemy position
                    explosion = EnemyExplosion(int(enemy.pos.x), int(enemy.pos.y), enemy.hit_radius)
                    explosion_group.add(explosion)
                    self.sfx["explosion"].play()
                    wave_manager.remove_enemy(enemy)

            #collision detection -------------------------------------------------------------------------------------------------------------------------------------------------------
            # Player bullets hit enemies
            for bullet in player_bullets[:]:
                for enemy in all_enemies:
                    distance = enemy.pos.distance_to(bullet.pos)

                    if distance < enemy.hit_radius + bullet.radius:
                        self.sfx["enemy_hit"].play()
                        enemy.take_damage(bullet.damage)
                        if bullet in player_bullets:
                            if hasattr(bullet, 'explode') and bullet.explosion_radius > 0:
                                bullet.explode(all_enemies, player_bullets)
                                explosion = Explosion(int(bullet.pos.x), int(bullet.pos.y), bullet.explosion_radius)
                                explosion_group.add(explosion)
                                self.sfx["explosion"].play()
                            if bullet.piercing == False:
                                player_bullets.remove(bullet)
                            if bullet.piercing == True:
                                bullet.pierce_level -= 1
                                if bullet.pierce_level <= 0:
                                    player_bullets.remove(bullet)
                        break

            # Enemy bullets hit player
            for enemy in all_enemies:
                if hasattr(enemy, 'bullets'):
                    for bullet in enemy.bullets[:]:
                        distance = player.ship_pos.distance_to(bullet.pos)

                        if distance < player.ship_radius + bullet.radius:
                            player.take_damage(bullet.damage)
                            enemy.bullets.remove(bullet)
                            self.sfx["player_hit"].play()
                            break
                            
            # Enemy collision with player
            for enemy in all_enemies[:]:
                distance = player.ship_pos.distance_to(enemy.pos)
                
                if distance < player.ship_radius + enemy.hit_radius:

                    player.take_damage(enemy.final_damage)
                    enemy.take_damage(player.ramming_damage)
                    self.sfx["crash"].play()

                    direction = enemy.pos - player.ship_pos
                    if direction.length() != 0:
                        direction = direction.normalize()

                        enemy.knockback += direction * 10
                        player.velocity -= direction * enemy.knockback_force

            # Update and draw explosions
            explosion_group.update()
            explosion_group.draw(self.screen)
            enemy_explosion_group.update()
            enemy_explosion_group.draw(self.screen)
            
            # Finish upgrade animation before applying
            if show_upgrade_screen and 'selected_upgrade' in locals():
                if pygame.time.get_ticks() - upgrade_animation_start > 700:

                    Upgrade.apply_upgrade(player, weapons, selected_upgrade)
                    print(f"Applied upgrade: {selected_upgrade}")

                    upgrade_trigger_time = 0
                    show_upgrade_screen = False
                    upgrade_cards = []

                    wave_manager.upgrades_pending = False
                    wave_manager.setup_wave()

                    del selected_upgrade

            # UPGRADE SCREEN
            if show_upgrade_screen:
                # Fade transition
                upgrade_fade_alpha = min(255, upgrade_fade_alpha + 8)  # Fade in

                # Dark overlay with fade
                overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, int(180 * (upgrade_fade_alpha / 255))))
                self.screen.blit(overlay, (0, 0))

                # Fade title
                title_surface = self.sfont.render("CHOOSE UPGRADE", True, (255, 255, 255))
                title_surface.set_alpha(upgrade_fade_alpha)
                title_rect = title_surface.get_rect(center=(self.width//2, self.height - 25))
                self.screen.blit(title_surface, title_rect)

                # Update and draw cards (cards have their own pop-up animation)
                for card in upgrade_cards:
                    card.update()
                    card_surf = card.draw(ui_surface, font_large, font_small)  # Get surface for alpha
                    if hasattr(card_surf, 'set_alpha'):
                        card_surf.set_alpha(upgrade_fade_alpha)
            if wave_message and (pygame.time.get_ticks() - wave_message_time) < wave_message_duration:
                wave_msg_surface = self.sfont.render(wave_message, True, (255, 255, 0))
                wave_msg_rect = wave_msg_surface.get_rect(center=(self.width // 2, 120))
                self.screen.blit(wave_msg_surface, wave_msg_rect)
            
            pygame.mouse.set_visible(False)
            self.screen.blit(ui_surface, (0, 0))
            self.screen.blit(self.assets["cursor_scaled"], cursor_rect)
            ui_surface.set_alpha(ui_alpha)
            pygame.display.update()

if __name__ == "__main__":
    Game().start_menu()