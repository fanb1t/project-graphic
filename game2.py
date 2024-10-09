import pygame
import sys
from set_up import level2_set_up, WIDTH, HEIGHT, FPS, GAME_OVER_TEXT_COLOR

def setup(HEIGHT,level1_set_up):
   # นำค่าจาก level1_set_up มาใช้ในเกม
    PLAYER1_START_POS = level1_set_up["PLAYER1_START_POS"]
    PLAYER2_START_POS = level1_set_up["PLAYER2_START_POS"]
    KEY_POS = level1_set_up["KEY_POS"]
    DOOR_POS = level1_set_up["DOOR_POS"]
    BOX_SIZES = level1_set_up["BOX_SIZES"]
    BOX_POSITIONS = level1_set_up["BOX_POSITIONS"]
    WATER_SIZES = level1_set_up["WATER_SIZES"]
    WATER_POSIIONS = level1_set_up["WATER_POSIIONS"]

    # Box sizes (width, height)
    BOX_SIZES = [
        (750, 50),  # Box 1 size
        (250, 50),  # Box 3 size
        (400, 50),  # Box 4 size
        (300, 50),  # Box 2 sizew
    ]

    # Box positions
    BOX_POSITIONS = [
        (500, HEIGHT - 50),  # Box 1 position
        (600, HEIGHT - 200),  # Box 2 position
        (0, HEIGHT - 50),     # Box 3 position
        (600, HEIGHT // 2 - 50)  # Box 4 position
    ]

def run2_game():
    """Main game function"""
    # Initialize Pygame
    pygame.init()

    # Create the game window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Two Player Game")

    # Load background image and scale it to fit the screen
    background_image = pygame.image.load("image/ด่านที่2/Background.png").convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    # Load player images
    player1_image_ice = pygame.image.load("image/ตัวละคร/น้ำแข็ง.png").convert_alpha()
    player2_image_lava = pygame.image.load("image/ตัวละคร/ลาวา.png").convert_alpha()

    # Scale player images
    player1_image_ice = pygame.transform.scale(player1_image_ice, (100, 100))
    player2_image_lava = pygame.transform.scale(player2_image_lava, (100, 100))

    # Load key image
    key_image = pygame.image.load("image/ด่านที่1/key.png").convert_alpha()
    key_image = pygame.transform.scale(key_image, (50, 50))

    # Load door image
    door_image = pygame.image.load("image/ด่านที่1/door.png").convert_alpha()
    door_image = pygame.transform.scale(door_image, (200, 200))

    # Load box image
    box_image = pygame.image.load("image/ด่านที่2/Tile_01.png").convert_alpha()

    # Define the Player class
    class Player(pygame.sprite.Sprite):
        def __init__(self, x, y, image, controls):
            super().__init__()
            self.image = image
            self.rect = self.image.get_rect(topleft=(x, y))
            self.mask = pygame.mask.from_surface(self.image)  # Create mask
            self.speed = 5
            self.gravity = 0.5
            self.jump_velocity = -10
            self.velocity_y = 0
            self.is_jumping = False
            self.has_key = False
            self.controls = controls
            self.on_ground = False  # Track if the player is on the ground

        def update(self, boxes):
            keys = pygame.key.get_pressed()
            if keys[self.controls['left']]:
                self.rect.x -= self.speed
                self.handle_collision(boxes, 'horizontal')
            if keys[self.controls['right']]:
                self.rect.x += self.speed
                self.handle_collision(boxes, 'horizontal')

            # Only jump if the jump key is pressed and the player is on the ground
            if keys[self.controls['jump']] and not self.is_jumping and self.on_ground:
                self.is_jumping = True
                self.velocity_y = self.jump_velocity
                self.on_ground = False  # Set on_ground to False when jumping

            # Apply gravity
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y
            
            # Check if the player is on the ground
            if self.rect.bottom >= HEIGHT:
                self.rect.bottom = HEIGHT
                self.is_jumping = False
                self.velocity_y = 0
                self.on_ground = True  # Player is on the ground
                
            self.handle_collision(boxes, 'vertical')

        def handle_collision(self, boxes, direction):
            if direction == 'horizontal':
                for box in boxes:
                    if pygame.sprite.collide_mask(self, box):  # Use mask collision
                        # Remove the stopping mechanism
                        if self.rect.right > box.rect.left and self.rect.centerx < box.rect.centerx:
                            self.rect.right = box.rect.left
                        elif self.rect.left < box.rect.right and self.rect.centerx > box.rect.centerx:
                            self.rect.left = box.rect.right

            if direction == 'vertical':
                for box in boxes:
                    if pygame.sprite.collide_mask(self, box):  # Use mask collision
                        if self.velocity_y > 0 and self.rect.bottom <= box.rect.bottom + 10:
                            self.rect.bottom = box.rect.top
                            self.is_jumping = False
                            self.velocity_y = 0
                            self.on_ground = True  # Player is on a box
                        elif self.velocity_y < 0 and self.rect.top >= box.rect.top - 10:
                            self.rect.top = box.rect.bottom
                            self.velocity_y = 0
                            self.on_ground = False  # Player is not on a box when jumping

        def pick_up_key(self, key):
            if pygame.sprite.collide_mask(self, key):  # Use mask collision
                self.has_key = True
                key.following_player = self

    class Key(pygame.sprite.Sprite):
        def __init__(self, x, y, image):
            super().__init__()
            self.image = image
            self.rect = self.image.get_rect(topleft=(x, y))
            self.mask = pygame.mask.from_surface(self.image)  # Create mask
            self.following_player = None

        def update(self):
            if self.following_player:
                self.rect.center = self.following_player.rect.center

        def draw(self, screen):
            screen.blit(self.image, self.rect)

    class Box(pygame.sprite.Sprite):
        def __init__(self, x, y, width, height, image):
            super().__init__()
            self.image = pygame.transform.scale(image, (width, height))
            self.rect = self.image.get_rect(topleft=(x, y))
            self.mask = pygame.mask.from_surface(self.image)  # Create mask

        def draw(self, screen):
            screen.blit(self.image, self.rect)

    class Door(pygame.sprite.Sprite):
        def __init__(self, x, y, image):
            super().__init__()
            self.image = image
            self.rect = self.image.get_rect(topleft=(x, y))
            self.mask = pygame.mask.from_surface(self.image)  # Create mask

        def draw(self, screen):
            screen.blit(self.image, self.rect)

        def check_entry(self, player):
            if pygame.sprite.collide_mask(self, player) and player.has_key:  # Use mask collision
                print("Player wins!")
                
def set_up_game2(Box,box_image,BOX_POSITIONS,BOX_SIZES,Player,PLAYER1_START_POS,PLAYER2_START_POS,
         player1_image_ice,player2_image_lava,Key,KEY_POS,key_image,Door,DOOR_POS,screen,background_image):
    # Create the boxes with specified sizes
    boxes = pygame.sprite.Group(*[Box(x, y, width, height, box_image) for (x, y), (width, height) in zip(BOX_POSITIONS, BOX_SIZES)])

    # Initialize players with different controls
    player1_controls = {'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w}
    player2_controls = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'jump': pygame.K_SPACE}

    player1 = Player(*PLAYER1_START_POS, player1_image_ice, player1_controls)
    player2 = Player(*PLAYER2_START_POS, player2_image_lava, player2_controls)

    key = Key(*KEY_POS, key_image)
    door = Door(*DOOR_POS, DOOR_POS)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_x, mouse_y = event.pos
                    print(f"Mouse clicked at: ({mouse_x}, {mouse_y})")  # Output the coordinates

        players = pygame.sprite.Group(player1, player2)
        players.update(boxes)
        key.update()
        player1.pick_up_key(key)
        player2.pick_up_key(key)

        # Check if either player enters the door with the key
        door.check_entry(player1)
        door.check_entry(player2)

        # Draw everything
        screen.blit(background_image, (0, 0))
        boxes.draw(screen)
        players.draw(screen)
        key.draw(screen)
        door.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    
    run_game2()
