import pygame
import sys
import level

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1200, 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
FONT_SIZE = 36
BUTTON_INACTIVE_COLOR = (177, 227, 250)
BUTTON_ACTIVE_COLOR = (106, 203, 247)

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Panny&Moony Game")

# Load images for the start menu
background_image = pygame.image.load("image/เมนู/bg22.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

logo_image = pygame.image.load("image/เมนู/logo.png")
logo_width, logo_height = 600, 300
logo_image = pygame.transform.scale(logo_image, (logo_width, logo_height))

# Positioning for logo and button
logo_x = (WIDTH - logo_width) // 2 + 8
logo_y = (HEIGHT - logo_height) // 2 - 100

button_width, button_height = 170, 50  # Adjust button size
button_x = (WIDTH - button_width) // 2 - 5
button_y = HEIGHT // 2 + 55  # Position below the logo

# Instruction button position
instruction_button_y = button_y + 70  # Position below the "Play Game" button

# Load character images
character1_image = pygame.image.load("image/ตัวละคร/น้ำแข็ง.png").convert_alpha()
character2_image = pygame.image.load("image/ตัวละคร/ลาวา.png").convert_alpha()

# Scale character images
character1_image = pygame.transform.scale(character1_image, (400, 400))
character2_image = pygame.transform.scale(character2_image, (400, 400))

# Load and scale background image for character selection
character_background_image = pygame.image.load("image/เมนู/bg4.png").convert()
character_background_image = pygame.transform.scale(character_background_image, (WIDTH, HEIGHT))

# Font for text
font = pygame.font.Font(None, FONT_SIZE)



# Function for drawing buttons
def draw_button(screen, text, x, y, width, height, inactive_color, active_color, font, border_width=3):
    """Draw a button with a border and detect clicks."""
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Check if the mouse is over the button
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        pygame.draw.rect(screen, BLACK, (x, y, width, height), border_width)
        if click[0] == 1:  # Left-click
            return True  # Return True if the button is clicked
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))
        pygame.draw.rect(screen, BLACK, (x, y, width, height), border_width)

    # Draw the text on the button
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

    return False



# ปุ่มกดเริ่มเกม
def start_game():
    """Function to show the start menu."""
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(background_image, (0, 0))
        screen.blit(logo_image, (logo_x, logo_y))

        # Draw the "Play Game" button
        if draw_button(screen, "Play Game", button_x, button_y, button_width, button_height,
                       BUTTON_INACTIVE_COLOR, BUTTON_ACTIVE_COLOR, font):
            # Start character selection when the button is clicked
            draw_character_selection()

        # Draw the "Instruction" button
        if draw_button(screen, "Instruction", button_x, instruction_button_y, button_width, button_height,
                       BUTTON_INACTIVE_COLOR, BUTTON_ACTIVE_COLOR, font):
            # Show instructions when the button is clicked
            show_instruction()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()



# ปุ่มเงื่อนไข
def show_instruction():
    """Function to show the instructions."""
    running = True

    # โหลดรูปภาพพื้นหลังและปรับขนาดให้พอดีกับหน้าจอ
    instruction_background_image = pygame.image.load("image/เมนู/castle bridge.png")
    instruction_background_image = pygame.transform.scale(instruction_background_image, (WIDTH, HEIGHT))

    # สร้างฟอนต์ขนาดเล็กสำหรับ instruction text
    small_font = pygame.font.Font(None, 38)  # เปลี่ยนขนาดฟอนต์เป็น 30 

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # แสดงรูปภาพพื้นหลังบนหน้าจอ
        screen.blit(instruction_background_image, (0, 0))

        # Instruction text
        instruction_text = [
            " Instructions : ",
            "- Use A,W,D to move character 1",
            "- Use the arrow keys to move character 2",
            "- In levels get to the next doors as possible ",
            "grabbing the golden keys"
        ]

        # Render and display the instruction text
        y_offset = 290
        for line in instruction_text:
            text_surface = small_font.render(line, True, WHITE)  # ใช้ฟอนต์ขนาดเล็ก
            text_rect = text_surface.get_rect(center=(WIDTH // 2, y_offset))  # ปรับให้ข้อความอยู่ตรงกลางแนวนอน
            screen.blit(text_surface, text_rect)
            y_offset += 55  # ลดระยะห่างระหว่างบรรทัดลงให้เข้ากับฟอนต์ขนาดเล็ก

        # ปรับขนาดของปุ่ม "OK"
        back_button_width = 60  # ความกว้างของปุ่ม
        back_button_height = 40  # ความสูงของปุ่ม

        # คำนวณตำแหน่งสำหรับปุ่ม "OK" ให้อยู่ตรงกลาง
        button_x = (WIDTH - back_button_width) // 2  # คำนวณตำแหน่ง x
        button_y = HEIGHT - 130  # ตำแหน่ง y (ปรับค่าได้ตามต้องการ)

        # วาดปุ่ม "OK" เพื่อกลับไปยังเมนูหลัก
        if draw_button(screen, "OK", button_x, button_y, back_button_width, back_button_height,
                       BUTTON_INACTIVE_COLOR, BUTTON_ACTIVE_COLOR, font):
            # Return to the main menu when "OK" is clicked
            return

        pygame.display.flip()

def draw_character_selection(selected_character=None):
    """Draw the character selection screen."""
    glow_radius = 140  # กำหนดรัศมีของการเรืองแสง

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # วาดพื้นหลัง
            screen.blit(character_background_image, (0, 0))

            # ตรวจจับตำแหน่งเมาส์
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # เช็คว่าเมาส์อยู่ที่ตัวละคร Ice หรือ Lava หรือไม่
            character1_rect = character1_image.get_rect(topleft=(150, 200))
            character2_rect = character2_image.get_rect(topleft=(650, 200))

            # ถ้าเมาส์อยู่ที่ตัวละคร Ice
            if character1_rect.collidepoint(mouse_x, mouse_y):
                glow_color = (0, 255, 255)  # สีฟ้าเรืองแสง
                character_center = character1_rect.center
                draw_glow_effect(character_center[0]-4, character_center[1]+20, glow_radius, glow_color)
                selected_character = "ice"
            # ถ้าเมาส์อยู่ที่ตัวละคร Lava
            elif character2_rect.collidepoint(mouse_x, mouse_y):
                glow_color = (255, 165, 0)  # สีส้มเรืองแสง
                character_center = character2_rect.center
                draw_glow_effect(character_center[0]-4, character_center[1]+20, glow_radius, glow_color)
                selected_character = "lava"
            else:
                selected_character = None

            # วาดรูปตัวละคร (หลังการเรืองแสง)
            screen.blit(character1_image, (150, 200))  # ice
            screen.blit(character2_image, (650, 200))  # lava

            # วาดชื่อของตัวละคร
            ice_text = font.render("Ice", True, BLACK)
            lava_text = font.render("Lava", True, BLACK)
            screen.blit(ice_text, (195, 360))  # ป้ายชื่อ "Ice"
            screen.blit(lava_text, (695, 360))  # ป้ายชื่อ "Lava"

            # วาดปุ่มย้อนกลับ
            back_button_rect = pygame.Rect(50, 50, 100, 50)  # กำหนดพื้นที่ของปุ่ม

            # ตรวจสอบว่ามีการเอาเมาส์ไปวางที่ปุ่ม Back หรือไม่
            if back_button_rect.collidepoint(mouse_x, mouse_y):
                back_button_color = (0, 255, 0)  # เปลี่ยนเป็นสีเขียวเมื่อเมาส์อยู่บนปุ่ม
            else:
                back_button_color = (255, 0, 0)  # สีแดงเมื่อเมาส์ไม่ได้แตะปุ่ม

            pygame.draw.rect(screen, back_button_color, back_button_rect)  # วาดปุ่มย้อนกลับ
            back_text = font.render("Back", True, WHITE)  # ข้อความบนปุ่ม
            screen.blit(back_text, (back_button_rect.x + 10, back_button_rect.y + 10))  # วางข้อความในปุ่ม

            pygame.display.flip()

            # ตรวจจับการคลิกเมาส์
            if event.type == pygame.MOUSEBUTTONDOWN:
                # ตรวจสอบการเลือกตัวละคร
                if character1_rect.collidepoint(mouse_x, mouse_y):
                    selected_character = "ice"
                elif character2_rect.collidepoint(mouse_x, mouse_y):
                    selected_character = "lava"
                elif back_button_rect.collidepoint(mouse_x, mouse_y):
                    # เมื่อคลิกที่ปุ่มย้อนกลับ
                    return  # กลับไปยังหน้าจอเดิม

                if selected_character:
                    # ปิดหน้าจอการเลือกตัวละคร
                    pygame.quit()

                    # รันหน้าจอเกมหลักพร้อมตัวละครที่เลือก
                    level.buttonlevel()
                    return

                
def draw_glow_effect(x, y, radius, color):
    """ฟังก์ชันวาดการเรืองแสงรอบ ๆ ตัวละคร"""
    for i in range(10, radius, 2):
        pygame.draw.circle(screen, color + (50,), (x, y), i, width=2)

if __name__ == "__main__":
    start_game()
