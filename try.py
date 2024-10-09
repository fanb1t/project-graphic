import pygame
import sys

# เริ่มต้น Pygame
pygame.init()

# ขนาดหน้าจอ
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Rect Collision Example')

# ตัวแปรพื้นฐาน
clock = pygame.time.Clock()
gravity = 1
player_speed = 5
player_jump = 15
on_ground = False

# โหลดรูปภาพสำหรับตัวละคร
player_image = pygame.image.load('image/ตัวละคร/ลาวา.png')  # เปลี่ยนเป็นเส้นทางของภาพตัวละคร
player_image = pygame.transform.scale(player_image, (50, 50))  # ปรับขนาดภาพ

# สร้างกล่อง (ใช้ rect)
box_image = pygame.Surface((100, 50))
box_image.fill((255, 0, 0))  # สีแดง
box_rect = box_image.get_rect(topleft=(300, 450))

# ตำแหน่งเริ่มต้น
player_rect = player_image.get_rect(topleft=(300, 400))  # ปรับตำแหน่งให้สูงขึ้น
player_y_velocity = 0

# กำหนดตำแหน่งพื้นดิน
ground_rect = pygame.Rect(0, 550, screen_width, 50)  # พื้นดิน

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    
    # การเคลื่อนไหว
    if keys[pygame.K_LEFT]:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_rect.x += player_speed
    if keys[pygame.K_SPACE] and on_ground:
        player_y_velocity = -player_jump

    # การจัดการแรงโน้มถ่วง
    player_y_velocity += gravity
    player_rect.y += player_y_velocity

    # ตรวจสอบการชนกับพื้น
    if player_rect.y + player_rect.height >= 550:
        player_rect.y = 550 - player_rect.height
        player_y_velocity = 0
        on_ground = True
    else:
        on_ground = False

    # ตรวจสอบการชนกับกล่องโดยใช้ Rect
    if player_rect.colliderect(box_rect):
        # วางตัวละครบนกล่อง
        if player_y_velocity > 0:  # ถ้ากำลังตก
            player_rect.y = box_rect.top - player_rect.height
            player_y_velocity = 0
            on_ground = True
        else:
            # ปรับตำแหน่งของตัวละครเมื่อเคลื่อนที่ไปทางกล่อง
            if player_rect.x < box_rect.x:  # ซ้ายของกล่อง
                player_rect.x = box_rect.left - player_rect.width
            elif player_rect.x > box_rect.x + box_rect.width:  # ขวาของกล่อง
                player_rect.x = box_rect.right

    # ล้างหน้าจอ
    screen.fill((255, 255, 255))
    
    # วาดวัตถุ
    screen.blit(player_image, player_rect)  # ตัวละคร
    screen.blit(box_image, box_rect)        # กล่อง

    # วาดกรอบรอบตัวละคร
    pygame.draw.rect(screen, (0, 255, 0), player_rect, 2)  # กรอบสีเขียวสำหรับตัวละคร
    # วาดกรอบรอบกล่อง
    pygame.draw.rect(screen, (255, 0, 0), box_rect, 2)    # กรอบสีแดงสำหรับกล่อง
    # วาดกรอบรอบพื้น
    pygame.draw.rect(screen, (0, 0, 255), ground_rect, 2) # กรอบสีน้ำเงินสำหรับพื้นดิน

    # อัปเดตหน้าจอ
    pygame.display.flip()
    clock.tick(60)
