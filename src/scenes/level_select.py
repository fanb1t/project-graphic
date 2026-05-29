import pygame

from src.core.settings import HEIGHT, WIDTH
from src.scenes.base_scene import BaseScene


class LevelSelectScene(BaseScene):
    # Level select scene maps clicked buttons to level scene classes.
    def __init__(self, app):
        super().__init__(app)
        self.background = self.assets.image("image/เมนู/l1_sky.png", (WIDTH, HEIGHT), alpha=True)
        self.map_image = self.assets.image("image/เมนู/level.png", (WIDTH, HEIGHT), alpha=True)
        self.button_image = self.assets.image("image/เมนู/button01.png", (70, 70), alpha=True)
        self.level_buttons = {
            1: self.button_image.get_rect(topleft=(575, 580)),
            2: self.button_image.get_rect(topleft=(400, 410)),
            3: self.button_image.get_rect(topleft=(635, 260)),
        }

    def handle_events(self, events):
        from src.data.level_data import LEVEL_1, LEVEL_2
        from src.scenes.level_scene import LevelScene

        for event in events:
            if event.type == pygame.QUIT:
                self.state_manager.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.level_buttons[1].collidepoint(event.pos):
                    self.app.sound.play("click")
                    self.state_manager.set_scene(LevelScene(self.app, LEVEL_1, next_level_data=LEVEL_2))
                elif self.level_buttons[2].collidepoint(event.pos):
                    self.app.sound.play("click")
                    self.state_manager.set_scene(LevelScene(self.app, LEVEL_2))
                elif self.level_buttons[3].collidepoint(event.pos):
                    self.app.sound.play("error")
                    print("Level 3 is not connected yet")

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.map_image, (0, 0))
        for rect in self.level_buttons.values():
            self.screen.blit(self.button_image, rect)
