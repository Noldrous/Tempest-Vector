from settings import *
from player import Player

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

            play_button = pygame.Rect(300, 300, 140, 50)
            quit_button = pygame.Rect(300, 380, 140, 50)

            pygame.draw.rect(self.screen, "skyblue" if play_button.collidepoint(mouse) else "darkgray", play_button)
            pygame.draw.rect(self.screen, "skyblue" if quit_button.collidepoint(mouse) else "darkgray", quit_button)

            play_text = self.font.render("Play", True, "white")
            quit_text = self.font.render("Quit", True, "white")

            self.screen.blit(play_text, (335, 305))
            self.screen.blit(quit_text, (335, 385))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if play_button.collidepoint(mouse):
                        self.game()

                    if quit_button.collidepoint(mouse):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

    def game(self):
        player = Player()
        
        while True:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((40, 40, 40))
            player.move()
            player.draw(self.screen)
            pygame.display.update()
            fps = self.clock.tick(60)

if __name__ == "__main__":
    Game().start_menu()