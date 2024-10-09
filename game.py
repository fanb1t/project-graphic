import pygame
import sys
from set_up import level1_set_up, WIDTH, HEIGHT, FPS, GAME_OVER_TEXT_COLOR
import game_2

# นำค่าจาก level1_set_up มาใช้ในเกม
PLAYER1_START_POS = level1_set_up["PLAYER1_START_POS"]
PLAYER2_START_POS = level1_set_up["PLAYER2_START_POS"]
KEY_POS = level1_set_up["KEY_POS"]
DOOR_POS = level1_set_up["DOOR_POS"]
BOX_SIZES = level1_set_up["BOX_SIZES"]
BOX_POSITIONS = level1_set_up["BOX_POSITIONS"]
LAVA_SIZES = level1_set_up["LAVA_SIZES"]
LAVA_POSITIONS = level1_set_up["LAVA_POSITIONS"]

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
        
    def update(self, boxes, elevators):
        keys = pygame.key.get_pressed()
        if keys[self.controls['left']]:
            self.rect.x -= self.speed
            self.handle_collision(boxes, elevators, 'horizontal')
        if keys[self.controls['right']]:
            self.rect.x += self.speed
            self.handle_collision(boxes, elevators, 'horizontal')
        if keys[self.controls['jump']] and not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = self.jump_velocity
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.is_jumping = False
            self.velocity_y = 0
        self.handle_collision(boxes, elevators, 'vertical')

    def handle_collision(self, boxes, elevators, direction):
        all_objects = list(boxes) + list(elevators)
        if direction == 'horizontal':
            for obj in all_objects:
                if pygame.sprite.collide_rect(self, obj):
                    if self.rect.right > obj.rect.left and self.rect.centerx < obj.rect.centerx:
                        self.rect.right = obj.rect.left
                    elif self.rect.left < obj.rect.right and self.rect.centerx > obj.rect.centerx:
                        self.rect.left = obj.rect.right
        if direction == 'vertical':
            for obj in all_objects:
                if pygame.sprite.collide_rect(self, obj):
                    if self.velocity_y > 0 and self.rect.bottom <= obj.rect.top + 10:
                        self.rect.bottom = obj.rect.top
                        self.is_jumping = False
                        self.velocity_y = 0
                    elif self.velocity_y < 0 and self.rect.top >= obj.rect.bottom - 10:
                        self.rect.top = obj.rect.bottom
                        self.velocity_y = 0

    def pick_up_key(self, key):
        if pygame.sprite.collide_rect(self, key):
            self.has_key = True
            key.following_player = self

class Key(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
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

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_entry(self, player):
        if pygame.sprite.collide_rect(self, player) and player.has_key:
            return True
        return False

class Elevator(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image,target_y):
        super().__init__()
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.original_y = y
        self.target_y = target_y  # ตำแหน่ง y ที่ลิฟต์จะขึ้นไป
        self.speed = 5

    def update(self, button_pressed):
        if button_pressed:
            # ลิฟต์กำลังเคลื่อนที่
            if self.rect.y > self.target_y:
                self.rect.y -= self.speed  # ลิฟต์เคลื่อนขึ้น
            elif self.rect.y < self.target_y:
                self.rect.y += self.speed  # ลิฟต์เคลื่อนลง
        else:
            # ลิฟต์กลับไปตำแหน่งเดิม
            if self.rect.y < self.original_y:
                self.rect.y += self.speed  # ลิฟต์กลับลง
            elif self.rect.y > self.original_y:
                self.rect.y -= self.speed  # ลิฟต์กลับขึ้น

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class ElevatorButton(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_pressed = False

    def update(self, player1, player2):
        self.is_pressed = pygame.sprite.collide_rect(self, player1) or pygame.sprite.collide_rect(self, player2)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
def check_door_entry(door, player1, player2):
    """Check if either player can enter the door and trigger the next game level."""
    if door.check_entry(player1) or door.check_entry(player2):
        if player1.has_key or player2.has_key:
            game_2.run_game2()
        
def show_game_over(screen):
    font = pygame.font.SysFont(None, 74)
    game_over_surface = font.render('Game Over', True, GAME_OVER_TEXT_COLOR)
    screen.blit(game_over_surface, (WIDTH // 2 - game_over_surface.get_width() // 2, HEIGHT // 2 - game_over_surface.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(2000)  #หน่วงเวลา 2 วินาทีแล้วค่อยปิดเกม
    pygame.quit()
    sys.exit()

def run_game():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Two Player Game")

    # Load images
    background_image = pygame.image.load("image/ด่านที่1/Background.png").convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    player1_image_ice = pygame.image.load("image/ตัวละคร/น้ำแข็ง.1.png").convert_alpha()
    player2_image_lava = pygame.image.load("image/ตัวละคร/ลาวา.1.png").convert_alpha()
    player1_image_ice = pygame.transform.scale(player1_image_ice, (50, 50))
    player2_image_lava = pygame.transform.scale(player2_image_lava, (50, 50))

    key_image = pygame.image.load("image/ด่านที่1/Image (2).png").convert_alpha()
    key_image = pygame.transform.scale(key_image, (50, 50))

    door_image = pygame.image.load("image/ด่านที่1/door.png").convert_alpha()
    door_image = pygame.transform.scale(door_image, (200, 200))

    box_image = pygame.image.load("image/ด่านที่1/tile2.1.png").convert_alpha()
    lava_image = pygame.image.load("image/ด่านที่1/lava_tile6.png").convert_alpha()
    elevator_image = pygame.image.load("image/ด่านที่1/tile2.1.png").convert_alpha()
    button_image = pygame.image.load("image/ด่านที่1/tile2.1.png").convert_alpha()

    # Create game objects
    player1 = Player(*PLAYER1_START_POS, player1_image_ice, {'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w})
    player2 = Player(*PLAYER2_START_POS, player2_image_lava, {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'jump': pygame.K_UP})
    
    key = Key(*KEY_POS, key_image)
    door = Door(*DOOR_POS, door_image)
    
    boxes = pygame.sprite.Group(*[Box(x, y, width, height, box_image) for (x, y), (width, height) in zip(BOX_POSITIONS, BOX_SIZES)])
    lava = pygame.sprite.Group(*[Box(x, y, width, height, lava_image) for (x, y), (width, height) in zip(LAVA_POSITIONS, LAVA_SIZES)])
    
    elevators = pygame.sprite.Group(
        Elevator(900, HEIGHT - 100, 100, 20, elevator_image, target_y= 200),  # ตัวแรก
        Elevator(400, 200, 100, 20, elevator_image, target_y = HEIGHT - 100)   # ตัวที่สอง
    )
    
    elevator_button = ElevatorButton(560, HEIGHT - 100, 50, 20, button_image)
    elevator_button_2 = ElevatorButton(700, HEIGHT - 420, 50, 20, button_image)  # ปุ่มใหม่
    
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(background_image, (0, 0))
        
        # ตรวจจับการชนระหว่างผู้เล่นและลาวา
        if pygame.sprite.spritecollideany(player1, lava) or pygame.sprite.spritecollideany(player2, lava):
            show_game_over(screen)  # เรียกใช้ฟังก์ชันแสดง Game Over
        
        # Update elevator button and elevators (for both elevators)
        elevator_button.update(player1, player2)
        elevator_button_2.update(player1, player2)  # อัปเดตปุ่มลิฟต์ตัวที่สอง

        elevators.sprites()[0].update(elevator_button.is_pressed)  # ลิฟต์ตัวแรก
        elevators.sprites()[1].update(elevator_button_2.is_pressed)  # ลิฟต์ตัวที่สอง

        # Update players
        player1.update(boxes, elevators)
        player2.update(boxes, elevators)
        key.update()

    # Check if players are on the elevator and move them with it
        for elevator in elevators:
            if elevator.rect.colliderect(player1.rect) and player1.rect.bottom <= elevator.rect.top + 10:
                player1.rect.bottom = elevator.rect.top
                player1.rect.y += elevator.speed if elevator.rect.y != elevator.original_y else 0  # เคลื่อนที่ไปกับลิฟต์
            if elevator.rect.colliderect(player2.rect) and player2.rect.bottom <= elevator.rect.top + 10:
                player2.rect.bottom = elevator.rect.top
                player2.rect.y += elevator.speed if elevator.rect.y != elevator.original_y else 0  # เคลื่อนที่ไปกับลิฟต์
                

    # Check for key pickup
        if not player1.has_key:
            player1.pick_up_key(key)
        if not player2.has_key:
            player2.pick_up_key(key)

        # Check for door entry
        check_door_entry(door, player1, player2)
        

        # Draw game objects
        boxes.draw(screen)
        lava.draw(screen)
        elevators.draw(screen)
        elevator_button.draw(screen)
        elevator_button_2.draw(screen)
        key.draw(screen)
        door.draw(screen)
        screen.blit(player1.image, player1.rect)
        screen.blit(player2.image, player2.rect)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    run_game()
