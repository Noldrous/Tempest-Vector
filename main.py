from settings import *
from player import Player
from enemy import *

class Game:
    def __init__(self):
        pygame.init()
        
        #setup
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((self.width, self.height))
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

    def game(self):
        player = Player()
        seekers = [
                SeekerEnemy(100,100),
                SeekerEnemy(700,500)
            ]

        shooters = [
            ShooterEnemy(600,100)
        ]
        
        while True:
            self.screen.fill((40, 40, 40))

            #pause_button
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
                        self.start_menu()

            #player
            player.move()
            player.draw(self.screen)

            #enemies
            for enemy in seekers:
                enemy.update(player.ship_pos)
                enemy.draw(self.screen)

            for enemy in shooters:
                enemy.update(player.ship_pos)
                enemy.draw(self.screen)

            for seeker in seekers:
                distance = player.ship_pos.distance_to(seeker.pos)
                if distance < player.ship_radius + Enemy.radius:
                    print("Player hit by seeker!")

            pygame.display.update()
            fps = self.clock.tick(60)

if __name__ == "__main__":
    Game().start_menu()