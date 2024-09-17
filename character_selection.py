import pygame
import sys
import subprocess

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Character Selection")

# Load character images
character1_image = pygame.image.load("image/น้ำแข็ง.png").convert_alpha()
character2_image = pygame.image.load("image/ลาวา.png").convert_alpha()

# Scale images
character1_image = pygame.transform.scale(character1_image, (150, 150))
character2_image = pygame.transform.scale(character2_image, (150, 150))

# Draw character buttons
def draw_buttons():
    screen.fill(WHITE)
    screen.blit(character1_image, (150, 200))
    screen.blit(character2_image, (500, 200))
    pygame.display.flip()

def main():
    draw_buttons()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 150 <= mouse_x <= 300 and 200 <= mouse_y <= 350:
                    selected_character = "ice"
                elif 500 <= mouse_x <= 650 and 200 <= mouse_y <= 350:
                    selected_character = "lava"
                else:
                    selected_character = None

                if selected_character:
                    # ปิดหน้าต่างเลือกตัวละคร
                    pygame.quit()

                    # เรียกใช้เกมหลัก
                    subprocess.run(["python", "game.py", selected_character])
                    return

if __name__ == "__main__":
    main()
