from settings import *
from player import Player
from enemy import *
from weapons import *

class Game:
    def __init__(self):
        #setup
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((self.width - 10, self.height - 50), pygame.FULLSCREEN)
        pygame.display.set_caption("Tempest Vector")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 40)
        self.running = True
    
    def start_menu(self):
        while True:

            self.screen.fill((40, 40, 40))
            mouse = pygame.mouse.get_pos()

            play_button = pygame.Rect(width - 200, height -200, 140, 50)
            quit_button = pygame.Rect(width - 200, height -125, 140, 50)

            pygame.draw.rect(self.screen, "skyblue" if play_button.collidepoint(mouse) else "darkgray", play_button)
            pygame.draw.rect(self.screen, "skyblue" if quit_button.collidepoint(mouse) else "darkgray", quit_button)

            play_text = self.font.render("Play", True, "white")
            quit_text = self.font.render("Quit", True, "white")

            self.screen.blit(play_text, (width - 200 + 40, height - 200))
            self.screen.blit(quit_text, (width - 200 + 40, height - 125))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_buttons = pygame.mouse.get_pressed()
                    if play_button.collidepoint(mouse) and mouse_buttons[0]:
                        self.game()

                    if quit_button.collidepoint(mouse) and mouse_buttons[0]:
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

    def pause_menu(self):
        while True:

            self.screen.fill((40, 40, 40))
            mouse = pygame.mouse.get_pos()

            resume_button = pygame.Rect(width//2 - 70, height - 500, 140, 50)
            quit_button = pygame.Rect(width //2 - 70, height - 400, 140, 50)

            pygame.draw.rect(self.screen, "skyblue" if resume_button.collidepoint(mouse) else "darkgray", resume_button)
            pygame.draw.rect(self.screen, "skyblue" if quit_button.collidepoint(mouse) else "darkgray", quit_button)

            play_text = self.font.render("Play", True, "white")
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

    def game(self):
        player = Player()
        bullets = []
        weapons = Weapons()
        player.weapon = weapons.main  # Connect player to the weapons system

        seekers = [
                SeekerEnemy(100,100),
                SeekerEnemy(700,500)
            ]

        shooters = [
            ShooterEnemy(600,100)
        ]

        while True:
            self.screen.fill((40, 40, 40))

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

                # if event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_1 and len(player.weapons) > 0:
                #         player.weapon_index = 0
                #         player.weapon = player.weapons[player.weapon_index]
                #     elif event.key == pygame.K_2 and len(player.weapons) > 1:
                #         player.weapon_index = 1
                #         player.weapon = player.weapons[player.weapon_index]
                #     elif event.key == pygame.K_q and len(player.weapons) > 0:
                #         player.weapon_index = (player.weapon_index - 1) % len(player.weapons)
                #         player.weapon = player.weapons[player.weapon_index]
                #     elif event.key == pygame.K_e and len(player.weapons) > 0:
                #         player.weapon_index = (player.weapon_index + 1) % len(player.weapons)
                #         player.weapon = player.weapons[player.weapon_index]

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        weapons.swap_weapon()
                        player.weapon = weapons.main  # Update player's weapon after swapping

            #player -------------------------------------------------------------------------------------------------------------------------------------------------------
            player.move()
            player.draw(self.screen)

            # shoot with equipped weapon -------------------------------------------------------------------------------------------------------------------------------------------------------
            if player.weapon is not None and pygame.mouse.get_pressed()[0]:
                bullets.extend(player.weapon.shoot(player.ship_pos.x, player.ship_pos.y, player.angle))
                
                # Check if weapon is depleted and cycle to next
                if player.weapon.ammo <= 0:
                    weapons.cycle_weapon()
                    player.weapon = weapons.main  # Update player's weapon after cycling

            for bullet in bullets:
                bullet.update()
                bullet.draw(self.screen)

            bullets = [bullet for bullet in bullets if bullet.is_alive()]

            weapon_name = player.weapon.name if player.weapon else "No Weapon"
            ammo_text = player.weapon.ammo if player.weapon else 0
            status_text = self.font.render(f"{weapon_name} Ammo: {ammo_text}", True, "white")
            self.screen.blit(status_text, (20, 20))


            #enemies -------------------------------------------------------------------------------------------------------------------------------------------------------
            for enemy in seekers:
                enemy.update(player.ship_pos)
                enemy.draw(self.screen)

            for enemy in shooters:
                enemy.update(player.ship_pos)
                enemy.draw(self.screen)

                for bullet in enemy.bullets[:]:
                    distance = player.ship_pos.distance_to(bullet.pos)

                    if distance < player.ship_radius + bullet.radius:
                        print("Player hit by bullet!")
                        enemy.bullets.remove(bullet)

            for seeker in seekers:
                distance = player.ship_pos.distance_to(seeker.pos)
                if distance < player.ship_radius + seeker.hit_radius:
                    print("Player hit by seeker!")

            pygame.display.update()
            fps = self.clock.tick(60)

if __name__ == "__main__":
    Game().start_menu()