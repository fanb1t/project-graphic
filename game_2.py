import pygame
import sys
from set_up import level2_set_up, WIDTH, HEIGHT, FPS
from game import Key, Box, Door

# นำค่าจาก level2_set_up มาใช้ในเกม
PLAYER1_START_POS = level2_set_up["PLAYER1_START_POS"]
PLAYER2_START_POS = level2_set_up["PLAYER2_START_POS"]
KEY_POS = level2_set_up["KEY_POS"]
DOOR_POS = level2_set_up["DOOR_POS"]
BOX_SIZES = level2_set_up["BOX_SIZES"]
BOX_POSITIONS = level2_set_up["BOX_POSITIONS"]
WATER_SIZES = level2_set_up["WATER_SIZES"]
WATER_POSIIONS = level2_set_up["WATER_POSIIONS"]

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image, controls):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5
        self.gravity = 0.4
        self.jump_velocity = -10
        self.velocity_y = 0
        self.is_jumping = False
        self.has_key = False
        self.controls = controls
        
    def update(self, boxes):
        keys = pygame.key.get_pressed()
        if keys[self.controls['left']]:
            self.rect.x -= self.speed
            self.handle_horizontal(boxes)
        if keys[self.controls['right']]:
            self.rect.x += self.speed
            self.handle_horizontal(boxes)
        if keys[self.controls['jump']] and not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = self.jump_velocity
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.is_jumping = False
            self.velocity_y = 0
        self.handle_vertical(boxes)
    
    def pick_up_key(self, key):
        if self.rect.colliderect(key.rect):
            self.has_key = True  # Set the has_key attribute to True
            key.kill()

    def handle_horizontal(self, boxes):
        all_objects = list(boxes) 
        for obj in all_objects:
            if pygame.sprite.collide_rect(self, obj):
                if self.rect.right > obj.rect.left and self.rect.centerx < obj.rect.centerx:
                    self.rect.right = obj.rect.left
                elif self.rect.left < obj.rect.right and self.rect.centerx > obj.rect.centerx:
                    self.rect.left = obj.rect.right

    def handle_vertical(self, boxes):
        all_objects = list(boxes) 
        for obj in all_objects:
            if pygame.sprite.collide_rect(self, obj):
                if self.velocity_y > 0 and self.rect.bottom <= obj.rect.top + 10:
                    self.rect.bottom = obj.rect.top
                    self.is_jumping = False
                    self.velocity_y = 0
                elif self.velocity_y < 0 and self.rect.top >= obj.rect.bottom - 10:
                    self.rect.top = obj.rect.bottom
                    self.velocity_y = 0

def screen_load_level2():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Two Player Game")

    # Load images
    background_image = pygame.image.load("image/ด่านที่2/Background.png").convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    player1_image_ice = pygame.image.load("image/ตัวละคร/น้ำแข็ง.1.png").convert_alpha()
    player2_image_lava = pygame.image.load("image/ตัวละคร/ลาวา.1.png").convert_alpha()
    player1_image_ice = pygame.transform.scale(player1_image_ice, (50, 50))
    player2_image_lava = pygame.transform.scale(player2_image_lava, (50, 50))

    key_image = pygame.image.load("image/ด่านที่1/Image (2).png").convert_alpha()
    key_image = pygame.transform.scale(key_image, (50, 50))

    door_image = pygame.image.load("image/ด่านที่1/door.png").convert_alpha()
    door_image = pygame.transform.scale(door_image, (200, 200))

    box_image = pygame.image.load("image/ด่านที่2/Tile_01.png").convert_alpha()

    # Create game objects
    player1 = Player(*PLAYER1_START_POS, player1_image_ice, {'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w})
    player2 = Player(*PLAYER2_START_POS, player2_image_lava, {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'jump': pygame.K_UP})
    
    key = Key(*KEY_POS, key_image)
    door = Door(*DOOR_POS, door_image)
    
    boxes = pygame.sprite.Group(*[Box(x, y, width, height, box_image) for (x, y), (width, height) in zip(BOX_POSITIONS, BOX_SIZES)])
        
    clock = pygame.time.Clock()
    
    return screen, background_image, player1, player2, key, door, boxes, clock
    
def run_game2():
    screen, background_image, player1, player2, key, door, boxes, clock = screen_load_level2()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        # Check for key pickup
        if not player1.has_key:
            player1.pick_up_key(key)
        if not player2.has_key:
            player2.pick_up_key(key)
                
        # Update players
        player1.update(boxes)
        player2.update(boxes)
        key.update()

        screen.blit(background_image, (0, 0))
        boxes.draw(screen)
        key.draw(screen)
        door.draw(screen)
        screen.blit(player1.image, player1.rect)
        screen.blit(player2.image, player2.rect)
        
        pygame.display.flip()
        clock.tick(FPS)

# Call the function to run the game

