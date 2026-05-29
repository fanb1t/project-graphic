import pygame

from src.entities import Door, Elevator, ElevatorButton, Key, Platform, Player


PLAYER_IMAGE_BY_CHARACTER = {
    "ice": "image/ตัวละคร/น้ำแข็ง.1.png",
    "lava": "image/ตัวละคร/ลาวา.1.png",
}


class LevelFactory:
    # Factory Pattern: build level objects from plain level data.
    def __init__(self, asset_loader):
        self.assets = asset_loader

    def create(self, level_data, selected_players=None):
        selected_players = selected_players or {}
        platform_image = self.assets.image(level_data["platform_image"], alpha=True)
        hazard_image = None
        if level_data.get("hazard_image"):
            hazard_image = self.assets.image(level_data["hazard_image"], alpha=True)

        player1 = self._create_player(level_data["player1"], {
            "left": pygame.K_a,
            "right": pygame.K_d,
            "jump": pygame.K_w,
        }, selected_players.get(1))
        player2 = self._create_player(level_data["player2"], {
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT,
            "jump": pygame.K_UP,
        }, selected_players.get(2))

        key_data = level_data["key"]
        key = Key(*key_data["pos"], self.assets.image(key_data["image"], (50, 50), alpha=True))

        door_data = level_data["door"]
        door = Door(*door_data["pos"], self.assets.image(door_data["image"], (200, 200), alpha=True))

        platforms = pygame.sprite.Group(
            *[Platform(x, y, width, height, platform_image)
              for (x, y), (width, height) in level_data["platforms"]]
        )
        hazards = pygame.sprite.Group()
        if hazard_image:
            hazards.add(*[
                Platform(x, y, width, height, hazard_image)
                for (x, y), (width, height) in level_data["hazards"]
            ])

        elevators = pygame.sprite.Group(*[
            Elevator(*item["pos"], *item["size"], platform_image, item["target_y"])
            for item in level_data["elevators"]
        ])
        buttons = pygame.sprite.Group(*[
            ElevatorButton(*item["pos"], *item["size"], platform_image)
            for item in level_data["buttons"]
        ])

        return {
            "players": [player1, player2],
            "key": key,
            "door": door,
            "platforms": platforms,
            "hazards": hazards,
            "elevators": elevators,
            "buttons": buttons,
        }

    def _create_player(self, player_data, controls, selected_character=None):
        image_path = PLAYER_IMAGE_BY_CHARACTER.get(selected_character, player_data["image"])
        image = self.assets.image(image_path, (50, 50), alpha=True)
        return Player(*player_data["pos"], image, controls)
