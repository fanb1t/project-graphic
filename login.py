import pygame
import sys

pygame.init()

# กำหนดขนาดหน้าจอ
screen_width, screen_height = 1200, 700
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption('My Game with Image Button')

# โหลดรูปภาพพื้นหลังและปรับขนาด 
background_image = pygame.image.load('image/back.jpg')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# โหลดรูปภาพโลโก้และปรับขนาด
logo_image = pygame.image.load('image/Boader.png')
logo_width, logo_height = 600, 300
logo_image = pygame.transform.scale(logo_image, (logo_width, logo_height))

# ตำแหน่งโลโก้ให้อยู่ตรงกลางและขยับขึ้น
logo_x = (screen_width - logo_width) // 2
logo_y = (screen_height - logo_height) // 2 - 50

# โหลดรูปภาพปุ่มเริ่มเกมและปรับขนาด
start_button_image = pygame.image.load('image/start.png')
button_width, button_height = 120, 100
start_button_image = pygame.transform.scale(start_button_image, (button_width, button_height))

# คำนวณตำแหน่งปุ่มให้อยู่ใต้โลโก้
button_x = (screen_width - button_width) // 2 - 10
button_y = screen_height // 2 + 55  # ปุ่มอยู่ด้านล่างโลโก้

# กำหนดตัวแปรสำหรับการควบคุมเกม
running = True
clock = pygame.time.Clock()

def start_game():
    """ฟังก์ชันจำลองสำหรับการเริ่มเกม"""
    print("เริ่มเกมแล้ว!")  # ใช้แทนการเรียกฟังก์ชันจาก level.py
    # เพิ่มโค้ดที่ต้องการเมื่อเริ่มเกม เช่น สลับไปยังหน้าจอใหม่หรือเข้าสู่เกม

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # ตรวจสอบว่าคลิกในตำแหน่งของปุ่มหรือไม่
            if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
                start_game()  # เรียกใช้ฟังก์ชันเริ่มเกม

    # แสดงภาพพื้นหลัง, โลโก้ และปุ่มเริ่มเกม
    screen.blit(background_image, (0, 0))
    screen.blit(logo_image, (logo_x, logo_y))
    screen.blit(start_button_image, (button_x, button_y))

    # อัปเดตหน้าจอ
    pygame.display.flip()
    clock.tick(60)

# ปิดโปรแกรม
pygame.quit()
sys.exit()
