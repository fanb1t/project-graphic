import pygame
import sys
import game

# Constants
WIDTH, HEIGHT = 1200, 700
FPS = 60
WHITE = (255, 255, 255)
GROUND_HEIGHT = 50 
def buttonlevel():
    pygame.init()
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Two Player Game")
    
# Load and scale the background image
    background_image = pygame.image.load("image/เมนู/l1_sky.png").convert_alpha()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    
    valcano_image = pygame.image.load("image/เมนู/level.png").convert_alpha()
    valcano_image = pygame.transform.scale(valcano_image, (WIDTH, HEIGHT))

# Load and scale buttons
    button_level1 = pygame.image.load("image/เมนู/button01.png").convert_alpha()
    button_level1 = pygame.transform.scale(button_level1, (70, 70))  #ปุ่มด่านเลเวลที่1
    
    button_level2 = pygame.image.load("image/เมนู/button01.png").convert_alpha()
    button_level2 = pygame.transform.scale(button_level2, (70, 70))   #ปุ่มด่านเลเวลที่2

    button_level3 = pygame.image.load("image/เมนู/button01.png").convert_alpha()
    button_level3 = pygame.transform.scale(button_level3, (70, 70))  #ปุ่มด่านเลเวลที่3
    
    clock = pygame.time.Clock()


    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:  # Check if mouse button is pressed
                mouse_pos = pygame.mouse.get_pos()  # Get mouse position

                # Check for button clicks
                if button_level1_rect.collidepoint(mouse_pos):
                    game.run_game()
                    # Uncomment the line below to run main.py
                    # exec(open("main.py").read())
                elif button_level2_rect.collidepoint(mouse_pos):
                    print("Level 2 Selected")  # Replace with your function to go to another file
                    # exec(open("main.py").read())
                elif button_level3_rect.collidepoint(mouse_pos):
                    print("Level 3 Selected")  # Replace with your function to go to another file
                    # exec(open("main.py").read())

        # Draw the background
        screen.blit(background_image, (0, 0))
        
        # Draw volcano image
        screen.blit(valcano_image, (0, 0))
        
        # Draw buttons and create rects for collision detection
        button_level1_rect = screen.blit(button_level1, (575, 580))  # Level 1 button
        button_level2_rect = screen.blit(button_level2, (400, 410))  # Level 2 button
        button_level3_rect = screen.blit(button_level3, (635, 260))  # Level 3 button

        # Update the display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    buttonlevel()
