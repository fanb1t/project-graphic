import pygame
import start_game


class maingame :
    def __init__(self) :
       pygame.init()
       self.screen = pygame.display.set_mode(1200,700)
       pygame.display.set_caption("Poonny Moony") 
       self.clock = pygame.time.clock()
       self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.screen.fill((0,0,0))
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        
if __name__ == "__main__":
    start_game.start_game()
    game = maingame()
    game.run()