import pygame

from src.core.settings import (
    FPS,
    GAME_OVER_TEXT_COLOR,
    HEIGHT,
    WHITE,
    WIDTH,
    WIN_TEXT_COLOR,
)
from src.scenes.base_scene import BaseScene
from src.systems.level_factory import LevelFactory


class LevelScene(BaseScene):
    # Template Method style scene: each level follows the same update/draw steps.
    def __init__(self, app, level_data, next_level_data=None):
        super().__init__(app)
        self.level_data = level_data
        self.next_level_data = next_level_data
        self.factory = LevelFactory(self.assets)
        self.background = self.assets.image(level_data["background"], (WIDTH, HEIGHT), alpha=False)
        self.font = pygame.font.Font(None, 74)
        self._load_level()

    def _load_level(self):
        objects = self.factory.create(self.level_data)
        self.players = objects["players"]
        self.key = objects["key"]
        self.door = objects["door"]
        self.platforms = objects["platforms"]
        self.hazards = objects["hazards"]
        self.elevators = objects["elevators"]
        self.buttons = objects["buttons"]

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.state_manager.quit()

    def update(self):
        self._update_buttons_and_elevators()
        for player in self.players:
            player.update(self.platforms, self.elevators)
            if not player.has_key:
                player.pick_up_key(self.key)

        self.key.update()
        self._check_hazards()
        self._check_door()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.platforms.draw(self.screen)
        self.hazards.draw(self.screen)
        self.elevators.draw(self.screen)
        self.buttons.draw(self.screen)
        self.screen.blit(self.key.image, self.key.rect)
        self.screen.blit(self.door.image, self.door.rect)
        for player in self.players:
            self.screen.blit(player.image, player.rect)

    def _update_buttons_and_elevators(self):
        buttons = self.buttons.sprites()
        elevators = self.elevators.sprites()
        for index, elevator in enumerate(elevators):
            if index < len(buttons):
                buttons[index].update(self.players)
                elevator.update(buttons[index].is_pressed)

    def _check_hazards(self):
        for player in self.players:
            if pygame.sprite.spritecollideany(player, self.hazards):
                self._show_message("Game Over", GAME_OVER_TEXT_COLOR)
                self._load_level()
                return

    def _check_door(self):
        for player in self.players:
            if self.door.can_enter(player):
                if self.next_level_data:
                    self.state_manager.set_scene(LevelScene(self.app, self.next_level_data))
                else:
                    self._show_message("Winner!", WIN_TEXT_COLOR)
                    self._load_level()
                return

    def _show_message(self, message, color):
        text = self.font.render(message, True, color)
        self.screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        pygame.display.flip()
        pygame.time.delay(1200)

