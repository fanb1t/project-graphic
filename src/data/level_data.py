from src.core.settings import HEIGHT

LEVEL_1 = {
    "name": "Level 1",
    "background": "image/ด่านที่1/Background.png",
    "player1": {
        "pos": (100, HEIGHT - 100),
        "image": "image/ตัวละคร/น้ำแข็ง.1.png",
    },
    "player2": {
        "pos": (150, HEIGHT - 100),
        "image": "image/ตัวละคร/ลาวา.1.png",
    },
    "key": {
        "pos": (350, HEIGHT - 150),
        "image": "image/ด่านที่1/Image (2).png",
    },
    "door": {
        "pos": (-50, HEIGHT - 650),
        "image": "image/ด่านที่1/door.png",
    },
    "platform_image": "image/ด่านที่1/tile2.1.png",
    "hazard_image": "image/ด่านที่1/lava_tile6.png",
    "platforms": [
        ((0, HEIGHT - 50), (50, 50)), ((50, HEIGHT - 50), (50, 50)),
        ((100, HEIGHT - 50), (50, 50)), ((150, HEIGHT - 50), (50, 50)),
        ((400, HEIGHT - 80), (80, 80)), ((480, HEIGHT - 80), (80, 80)),
        ((560, HEIGHT - 80), (80, 80)), ((640, HEIGHT - 80), (80, 80)),
        ((720, HEIGHT - 80), (80, 80)), ((800, HEIGHT - 80), (80, 80)),
        ((650, HEIGHT - 400), (50, 50)), ((700, HEIGHT - 400), (50, 50)),
        ((750, HEIGHT - 400), (50, 50)), ((800, HEIGHT - 400), (50, 50)),
        ((850, HEIGHT - 400), (50, 50)), ((0, HEIGHT - 500), (50, 50)),
        ((50, HEIGHT - 500), (50, 50)), ((100, HEIGHT - 500), (50, 50)),
        ((150, HEIGHT - 500), (50, 50)), ((200, HEIGHT - 450), (50, 50)),
        ((250, HEIGHT - 450), (50, 50)), ((300, HEIGHT - 450), (50, 50)),
    ],
    "hazards": [
        ((900, HEIGHT - 70), (100, 70)), ((1000, HEIGHT - 70), (100, 70)),
        ((1100, HEIGHT - 70), (100, 70)), ((880, HEIGHT - 70), (100, 70)),
    ],
    "elevators": [
        {"pos": (900, HEIGHT - 100), "size": (100, 20), "target_y": 200},
        {"pos": (400, 200), "size": (100, 20), "target_y": HEIGHT - 100},
    ],
    "buttons": [
        {"pos": (560, HEIGHT - 100), "size": (50, 20)},
        {"pos": (700, HEIGHT - 420), "size": (50, 20)},
    ],
}

LEVEL_2 = {
    "name": "Level 2",
    "background": "image/ด่านที่2/Background.png",
    "player1": {
        "pos": (720, HEIGHT - 100),
        "image": "image/ตัวละคร/น้ำแข็ง.1.png",
    },
    "player2": {
        "pos": (800, HEIGHT - 100),
        "image": "image/ตัวละคร/ลาวา.1.png",
    },
    "key": {
        "pos": (640, HEIGHT - 105),
        "image": "image/ด่านที่1/Image (2).png",
    },
    "door": {
        "pos": (-50, HEIGHT - 650),
        "image": "image/ด่านที่1/door.png",
    },
    "platform_image": "image/ด่านที่2/Tile_01.png",
    "hazard_image": None,
    "platforms": [
        ((0, HEIGHT - 50), (1200, 50)),
        ((780, HEIGHT - 165), (300, 35)),
        ((430, HEIGHT - 280), (300, 35)),
        ((780, HEIGHT - 395), (300, 35)),
        ((350, HEIGHT - 430), (360, 35)),
        ((0, HEIGHT - 430), (330, 35)),
    ],
    "hazards": [],
    "elevators": [],
    "buttons": [],
}

LEVEL_3 = {
    "name": "Level 3",
    "background": "image/ด่านที่3/1.png",
    "player1": {
        "pos": (120, HEIGHT - 100),
        "image": "image/ตัวละคร/น้ำแข็ง.1.png",
    },
    "player2": {
        "pos": (200, HEIGHT - 100),
        "image": "image/ตัวละคร/ลาวา.1.png",
    },
    "key": {
        "pos": (600, HEIGHT - 105),
        "image": "image/ด่านที่3/000_0045_coin.png",
    },
    "door": {
        "pos": (950, HEIGHT - 250),
        "image": "image/ด่านที่1/door.png",
    },
    "platform_image": "image/ด่านที่3/Tile_01.png",
    "hazard_image": None,
    "platforms": [
        ((0, HEIGHT - 50), (1200, 50)),
        ((420, HEIGHT - 150), (250, 35)),
        ((760, HEIGHT - 250), (330, 35)),
    ],
    "hazards": [],
    "elevators": [],
    "buttons": [],
}
