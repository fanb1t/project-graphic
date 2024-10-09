import pygame
import sys
import random
import math
from pygame.locals import QUIT
from game import Box
from set_up import level3_set_up

# Initialize constants
WIDTH, HEIGHT = 1200, 700
FPS = 60
SPRING_HEIGHT = 30
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
COIN_SIZE = 30
KEY_SIZE = 40
DOOR_WIDTH, DOOR_HEIGHT = 100, 200
SPRING_POSITIONS = [(100, 600), (300, 500), (500, 500), (700, 500),
                    (200, 400), (400, 400), (600, 400), (300, 300), (500, 300)]
TRAP_SPRINGS = [1, 4, 7]  # Index of trap springs
NUM_COINS = 5
BOX_SIZES = level3_set_up["BOX_SIZES"]
BOX_POSITIONS = level3_set_up["BOX_POSITIONS"]


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, controls):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5
        self.gravity = 0.4
        self.jump_velocity = -10
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_jumping = False
        self.controls = controls
        self.has_key = False
        self.alive = True

    def update(self, springs,boxes):
        keys = pygame.key.get_pressed()
        if keys[self.controls['left']]:
            self.rect.x -= self.speed
        if keys[self.controls['right']]:
            self.rect.x += self.speed
        if keys[self.controls['jump']] and not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = self.jump_velocity
        
        self.velocity_y += self.gravity
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        
        # ตรวจสอบการชนกับขอบจอ
        if self.rect.left < 0:
            self.rect.left = 0
            self.velocity_x = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.velocity_x = 0
        # ตรวจสอบการตกจากขอบจอ
        if self.rect.top > HEIGHT:
            self.alive = False
            return
        
        self.handle_spring_collision(springs)
        self.handle_box_collision(boxes)
        
    def handle_box_collision(self, boxes):
        for box in boxes:
            if self.rect.colliderect(box.rect):
                # ถ้าผู้เล่นอยู่เหนือกล่อง
                if self.rect.bottom <= box.rect.top + self.velocity_y:
                    self.rect.bottom = box.rect.top
                    self.is_jumping = False
                    self.velocity_y = 0
                # ถ้าผู้เล่นชนด้านข้างของกล่อง
                elif self.rect.right > box.rect.left and self.rect.left < box.rect.right:
                    if self.velocity_x > 0:
                        self.rect.right = box.rect.left
                    elif self.velocity_x < 0:
                        self.rect.left = box.rect.right
                    self.velocity_x = 0

    def handle_spring_collision(self, springs):
        for spring in springs:
            if self.rect.colliderect(spring.rect) and self.velocity_y > 0:
                if spring.is_trap:
                    self.alive = False
                else:
                    # Calculate the angle based on where the player landed on the spring
                    relative_x = self.rect.centerx - spring.rect.left
                    spring_width = spring.rect.width
                    angle = 180 * (relative_x / spring_width)
                    
                    # แปลงมุมเป็นเรเดียน
                    angle_rad = math.radians(angle)
                    
                    # คำนวณความเร็วใหม่
                    speed = 15  # ปรับค่านี้เพื่อเปลี่ยนความแรงของการกระโดด
                    if angle < 90:
                        self.velocity_x = speed * math.sin(angle_rad)
                    else:
                        self.velocity_x = -speed * math.sin(math.radians(180 - angle))
                    self.velocity_y = -speed * math.cos(angle_rad)
                    
                    self.is_jumping = True
                    # ย้ายผู้เล่นขึ้นเล็กน้อยเพื่อป้องกันการติดสปริง
                    self.rect.bottom = spring.rect.top

class Spring(pygame.sprite.Sprite):
    def __init__(self, x, y, is_trap, normal_image_path, trap_image_path):
        super().__init__()
        self.normal_image = pygame.image.load(normal_image_path).convert_alpha()
        self.trap_image = pygame.image.load(trap_image_path).convert_alpha()
        self.image = self.trap_image if is_trap else self.normal_image
        self.image = pygame.transform.scale(self.image, (100, SPRING_HEIGHT))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_trap = is_trap


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (COIN_SIZE, COIN_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))

class Key(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (KEY_SIZE, KEY_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (DOOR_WIDTH, DOOR_HEIGHT))
        self.rect = self.image.get_rect(topleft=(x, y))

class Timer:
    def __init__(self, start_time):
        self.time_left = start_time

    def update(self):
        self.time_left -= 1

    def is_time_up(self):
        return self.time_left <= 0

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Two Player Game with Springs")
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load("image/ด่านที่2/Background.png").convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.reset_game()

    def reset_game(self):
        self.player1 = Player(1100, 600, "image/ตัวละคร/น้ำแข็ง.1.png", {'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w})
        self.player2 = Player(1200, 600, "image/ตัวละคร/ลาวา.1.png", {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'jump': pygame.K_UP})
        self.springs = pygame.sprite.Group(*[Spring(x, y, i in TRAP_SPRINGS, "image/เมนู/spring.png", "image/เมนู/trap.png") 
                                             for i, (x, y) in enumerate(SPRING_POSITIONS)])
        self.coins = pygame.sprite.Group(*[Coin(random.randint(100, 700), random.randint(100, 300), "image/เมนู/coin.png") 
                                           for _ in range(NUM_COINS)])
        self.key = Key(400, 100, "image/ด่านที่1/Image (2).png")
        self.door = Door(700, 400, "image/ด่านที่1/door.png")
        box_image = pygame.image.load("image/ด่านที่1/tile2.1.png").convert_alpha()
        self.boxes = pygame.sprite.Group(*[Box(x, y, width, height, box_image) for (x, y), (width, height) in zip(BOX_POSITIONS, BOX_SIZES)])
        self.timer = Timer(50 * FPS)  # 50 seconds

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        self.player1.update(self.springs)
        self.player2.update(self.springs)
        self.check_game_over()
        self.check_coin_collection()
        self.check_key_pickup()
        self.check_win_condition()
        self.timer.update()
        self.check_time_up()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.springs.draw(self.screen)
        self.coins.draw(self.screen)
        self.screen.blit(self.player1.image, self.player1.rect)
        self.screen.blit(self.player2.image, self.player2.rect)
        self.screen.blit(self.key.image, self.key.rect)
        self.screen.blit(self.door.image, self.door.rect)
        self.boxes.draw(self.screen)
        pygame.display.flip()

    def check_game_over(self):
        if not self.player1.alive or not self.player2.alive:
            self.show_message("Game Over", (255, 0, 0))
            self.reset_game()

    def check_coin_collection(self):
        pygame.sprite.spritecollide(self.player1, self.coins, True)
        pygame.sprite.spritecollide(self.player2, self.coins, True)

    def check_key_pickup(self):
        if not self.coins:
            if self.player1.rect.colliderect(self.key.rect):
                self.player1.has_key = True
                self.key.kill()
            if self.player2.rect.colliderect(self.key.rect):
                self.player2.has_key = True
                self.key.kill()

    def check_win_condition(self):
        if (self.player1.has_key and self.player1.rect.colliderect(self.door.rect)) or \
           (self.player2.has_key and self.player2.rect.colliderect(self.door.rect)):
            self.show_message("Winner!", (0, 255, 0))
            self.reset_game()

    def check_time_up(self):
        if self.timer.is_time_up():
            self.show_message("Time's Up!", (255, 0, 0))
            self.reset_game()

    def show_message(self, message, color):
        font = pygame.font.Font(None, 74)
        text = font.render(message, True, color)
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)

if __name__ == "__main__":
    game = Game()
    game.run()
