# Constants
WIDTH = 1200
HEIGHT = 700
FPS = 60
GAME_OVER_TEXT_COLOR = (255, 0, 0)


# Level 1 setup
level1_set_up = {
    # Player and object positions
    "PLAYER1_START_POS": (100, HEIGHT - 100),
    "PLAYER2_START_POS": (150, HEIGHT - 100),
    "KEY_POS": (350, HEIGHT - 150),
    "DOOR_POS": (-50, HEIGHT - 650),
    
    # ขนาดกล่องแต่ละอัน (width, height)
    "BOX_SIZES": [
        (50, 50), (50, 50), (50, 50), (50, 50),
        (80, 80), (80, 80), (80, 80), (80, 80), (80, 80), (80, 80),
        (50, 50), (50, 50), (50, 50), (50, 50), (50, 50),
        (50, 50), (50, 50), (50, 50), (50, 50),
        (50, 50), (50, 50), (50, 50),
    ],
    
    # ตำแหน่งของกล่อง
    "BOX_POSITIONS": [
        (0, HEIGHT - 50), (50, HEIGHT - 50), (100, HEIGHT - 50), (150, HEIGHT - 50), 
        (400, HEIGHT - 80), (480, HEIGHT - 80), (560, HEIGHT - 80), (640, HEIGHT - 80), (720, HEIGHT - 80), (800, HEIGHT - 80),
        (650, HEIGHT - 400), (700, HEIGHT - 400), (750, HEIGHT - 400), (800, HEIGHT - 400), (850, HEIGHT - 400),
        (0, HEIGHT - 500), (50, HEIGHT - 500), (100, HEIGHT - 500), (150, HEIGHT - 500),
        (200, HEIGHT - 450), (250, HEIGHT - 450), (300, HEIGHT - 450),
    ],
    
    # ขนาดเเซอเฟซลาวา
    "LAVA_SIZES": [
        (100, 70), (100, 70), (100, 70), (100, 70)
    ],
    
    # ตำแหน่งลาวา
    "LAVA_POSITIONS": [
        (900, HEIGHT - 70), (1000, HEIGHT - 70), (1100, HEIGHT - 70), (880, HEIGHT - 70)
    ],
    
    # ขนาดเเซอเฟซลิฟต์
    "ELEVATOR_SIZES": [
        (100, 20), (100, 20)
    ],

    # ตำแหน่งลิฟต์
    "ELEVATOR_POSITIONS": [
        (940, HEIGHT - 20), (1040, HEIGHT - 20),
        (400, HEIGHT - 20), (480, HEIGHT - 20), (560, HEIGHT - 20)
    ]
}

level2_set_up = {
     # Player and object positions
    "PLAYER1_START_POS": (500, HEIGHT - 200),
    "PLAYER2_START_POS": (700, HEIGHT - 200),
    "KEY_POS": (350, HEIGHT - 150),
    "DOOR_POS": (-50, HEIGHT - 650),
    
      # ขนาดกล่องแต่ละอัน (width, height)
   # Box sizes (width, height)
    "BOX_SIZES" : [
        (750, 50),(250, 50),(400, 50),(300, 50),  # Box 2 sizew
    ],
    
   # Box positions
    "BOX_POSITIONS" : [(500, HEIGHT - 50),(600, HEIGHT - 200),(0, HEIGHT - 50),(600, HEIGHT // 2 - 50)  # Box 4 position
    ],
    
    "WATER_SIZES" : [
        (40, 50), (40, 50), (40, 50), (40, 50),
    ],
    "WATER_POSIIONS" : [
        (200,HEIGHT - 50),(250,HEIGHT - 50),(300,HEIGHT - 50),(200,HEIGHT - 50),
    ]
       
}
def screen_load_level1():
    {}
    
level3_set_up = {
    "PLAYER1_START_POS": (500, HEIGHT - 200),
    "PLAYER2_START_POS": (700, HEIGHT - 200),
      # ขนาดกล่องแต่ละอัน (width, height)
   # Box sizes (width, height)
    "BOX_SIZES" : [
        (50, 50),(50, 50),(50, 50),(50, 50),(50, 50),(50, 50),  # Box 2 sizew
    ],
    
   # Box positions
    "BOX_POSITIONS" : [(1000, HEIGHT - 50),(1050, HEIGHT - 50),(1100, HEIGHT - 50),(1150, HEIGHT - 50),(1200, HEIGHT - 50),(1250, HEIGHT // 2 - 50)  # Box 4 position
    ],
}