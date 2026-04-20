from settings import *
from player import *
from enemy import *
from weapons import *

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
        self.screen.fill("DARKBLUE")
        background = pygame.transform.scale(self.assets["background"], (self.width, self.height))
        title = pygame.transform.scale(self.assets["title"], (self.width / 2.4, self.height / 2.9))
        play1 = pygame.transform.scale(self.assets["play_button1"], (self.width // 8, self.height // 14))
        play2 = pygame.transform.scale(self.assets["play_button2"], (self.width // 8, self.height // 14))
        credits1 = pygame.transform.scale(self.assets["credits_button1"], (self.width // 8, self.height // 14))
        credits2 = pygame.transform.scale(self.assets["credits_button2"], (self.width // 8, self.height // 14))
        quit1 = self.assets["quit_button1"]
        quit2 = self.assets["quit_button2"]
        
        play_rect = play1.get_rect(bottomleft=(self.width - self.width // 5, self.height - self.height // 5))
        credit_rect = credits1.get_rect(bottomleft=(self.width - self.width // 5, self.height - self.height // 9))
        quit_rect = self.assets["quit_button1"].get_rect(topright=(self.width - 50, 50))

        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_buttons = pygame.mouse.get_pressed()
                    if play_rect.collidepoint(mouse) and mouse_buttons[0]:
                        self.game()

                    if quit_rect.collidepoint(mouse) and mouse_buttons[0]:
                        pygame.quit()
                        sys.exit()
        
            self.screen.blit(background, (0, 0))
            mouse = pygame.mouse.get_pos()

            play_button = play2 if pygame.Rect(play_rect.x, play_rect.y, play_rect.width, play_rect.height).collidepoint(mouse) else play1
            credits_button = credits2 if pygame.Rect(credit_rect.x, credit_rect.y, credit_rect.width, credit_rect.height).collidepoint(mouse) else credits1
            quit_button = quit2 if pygame.Rect(quit_rect.x, quit_rect.y, quit_rect.width, quit_rect.height).collidepoint(mouse) else quit1

            pos = random.randint(0, self.height - 360)
            self.setbackground("celestial1", 1, 300, self.height, self.height)
            self.setbackground("celestial2", 1, 0, self.height, self.height)
            self.setbackground("celestial3", 1, 500, self.height, self.height)
            self.setbackground("star1", 0.5, 0, 360, 720)
            self.setbackground("star2", 0.5, 0, 360, 720)
            self.setbackground("shadow1", 0.8, 0, 360, 720)
            
            self.screen.blit(title, (75,75))

            self.screen.blit(play_button, play_rect)
            self.screen.blit(credits_button, credit_rect)
            self.screen.blit(quit_button, quit_rect)

            pygame.display.update()
            self.clock.tick(60)
            
    def pause_menu(self):
        while True:

            self.screen.fill((40, 40, 40))
            mouse = pygame.mouse.get_pos()

            resume_button = pygame.Rect(width//2 - 70, height - 500, 140, 50)
            quit_button = pygame.Rect(width //2 - 70, height - 400, 140, 50)

            pygame.draw.rect(self.screen, "skyblue" if resume_button.collidepoint(mouse) else "darkgray", resume_button)
            pygame.draw.rect(self.screen, "skyblue" if quit_button.collidepoint(mouse) else "darkgray", quit_button)

            play_text = self.font.render("Resume", True, "white")
            quit_text = self.font.render("Quit", True, "white")

            self.screen.blit(play_text, (width//2 - 50, height - 500))
            self.screen.blit(quit_text, (width//2 - 50, height - 400))

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

            pygame.display.update()

    def game_over(self):
        while True:

            self.screen.fill((40, 40, 40))
            mouse = pygame.mouse.get_pos()

            try_again_button = pygame.Rect(width//2 - 70, height - 500, 140, 50)
            quit_button = pygame.Rect(width //2 - 70, height - 400, 140, 50)

            pygame.draw.rect(self.screen, "skyblue" if try_again_button.collidepoint(mouse) else "darkgray", try_again_button)
            pygame.draw.rect(self.screen, "skyblue" if quit_button.collidepoint(mouse) else "darkgray", quit_button)

            try_again_text = self.font.render("Try Again", True, "white")
            quit_text = self.font.render("Quit", True, "white")

            self.screen.blit(try_again_text, (width//2 - 50, height - 500))
            self.screen.blit(quit_text, (width//2 - 50, height - 400))

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

            pygame.display.update()

    def game(self):
        bg = pygame.transform.scale(self.assets["background"], (self.width, self.height))
        bg_x = 0
        speed = 1
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
            self.screen.fill((40, 40, 40))
            self.screen.blit(bg, (bg_x, 0))
            self.screen.blit(bg, (bg_x + width, 0))
            bg_x -= speed
            if bg_x <= -width:
                bg_x = 0

            #pause_button -------------------------------------------------------------------------------------------------------------------------------------------------------
            mouse = pygame.mouse.get_pos()
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
            player.move()
            player.draw(self.screen)

            if player.health <= 0:
                self.game_over()

            health_bar.draw(self.screen, player.health)
            fuel_bar.draw(self.screen, player.fuel)

            # shoot with equipped weapon -------------------------------------------------------------------------------------------------------------------------------------------------------
            if player.weapon is not None and pygame.mouse.get_pressed()[0] and not weapons.should_show_message():
                player_bullets.extend(player.weapon.shoot(player.ship_pos.x, player.ship_pos.y, player.angle))
                
                # Check if weapon is depleted and cycle to next
                if player.weapon.ammo <= 0:
                    weapons.cycle_weapon()
                    player.weapon = weapons.main  # Update player's weapon after cycling

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

            #enemies -------------------------------------------------------------------------------------------------------------------------------------------------------
            for enemy in seekers:
                enemy.update(player.ship_pos)
                enemy.draw(self.screen)

            for enemy in shooters:
                enemy.update(player.ship_pos)
                enemy.draw(self.screen)

            for enemy in seekers + shooters:
                if enemy.health <= 0:
                    if enemy in seekers:
                        seekers.remove(enemy)
                    else:
                        shooters.remove(enemy)

            #collision detection -------------------------------------------------------------------------------------------------------------------------------------------------------
            for bullet in player_bullets[:]:
                for enemy in seekers + shooters:
                    distance = enemy.pos.distance_to(bullet.pos)

                    if distance < enemy.size + bullet.radius:
                        print(f"{enemy.__class__.__name__} hit by bullet!")
                        enemy.take_damage(bullet.damage)
                        player_bullets.remove(bullet)
                        break
            
            for seeker in seekers:
                distance = player.ship_pos.distance_to(seeker.pos)
                if distance < player.ship_radius + seeker.hit_radius:
                    print("Player hit by seeker!")
                    player.take_damage(seeker.contact_damage)
                    break
            
            for shooter in shooters:
                distance = player.ship_pos.distance_to(shooter.pos)
                if distance < player.ship_radius + shooter.hit_radius:
                    print("Player hit by shooter!")
                    player.take_damage(shooter.contact_damage)
                    break
            
            for enemy in shooters:
                for bullet in enemy.bullets[:]:
                    distance = player.ship_pos.distance_to(bullet.pos)

                    if distance < player.ship_radius + bullet.radius:
                        print("Player hit by bullet!")
                        player.take_damage(bullet.damage)
                        enemy.bullets.remove(bullet)
                        break

            

            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    Game().start_menu()