import pygame
import sys
import subprocess

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 36

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Menu")


# Load character images
character1_image = pygame.image.load("image/น้ำแข็ง.png").convert_alpha()
character2_image = pygame.image.load("image/ลาวา.png").convert_alpha()

# Scale images
character1_image = pygame.transform.scale(character1_image, (150, 150))
character2_image = pygame.transform.scale(character2_image, (150, 150))

# Font
font = pygame.font.Font(None, FONT_SIZE)

def draw_start_menu():
    screen.fill(WHITE)
    start_text = font.render("Start Game", True, BLACK)
    start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(start_text, start_rect)
    pygame.display.flip()

def draw_character_selection():
    screen.fill(WHITE)
    screen.blit(character1_image, (150, 200))
    screen.blit(character2_image, (500, 200))
    pygame.display.flip()

def main():
    # Display the start menu
    draw_start_menu()

    selecting_character = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if not selecting_character:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    # Check if "Start Game" is clicked
                    start_text_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 20, 200, 40)
                    if start_text_rect.collidepoint(mouse_x, mouse_y):
                        selecting_character = True
                        draw_character_selection()
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if 150 <= mouse_x <= 300 and 200 <= mouse_y <= 350:
                        selected_character = "ice"
                    elif 500 <= mouse_x <= 650 and 200 <= mouse_y <= 350:
                        selected_character = "lava"
                    else:
                        selected_character = None

                    if selected_character:
                        # Close the character selection window
                        pygame.quit()

                        # Run the main game
                        subprocess.run(["python", "game.py", selected_character])
                        return

if __name__ == "__main__":
    main()
