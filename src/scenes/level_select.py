import pygame

from src.core.settings import HEIGHT, WIDTH
from src.scenes.base_scene import BaseScene


class LevelSelectScene(BaseScene):
    # Level select scene maps clicked buttons to level scene classes.
    def __init__(self, app):
        super().__init__(app)
        self.background = self.assets.image("image/เมนู/level_select_background.png", (WIDTH, HEIGHT), alpha=False)
        self.title_image = self.assets.image("image/เมนู/level_select_title.png", (560, 132), alpha=True)
        self.level_images = {
            1: self.assets.image("image/เมนู/level_skull_1.png", (165, 165), alpha=True),
            2: self.assets.image("image/เมนู/level_skull_2.png", (180, 180), alpha=True),
            3: self.assets.image("image/เมนู/level_skull_3.png", (165, 165), alpha=True),
        }
        self.level_buttons = {
            1: self.level_images[1].get_rect(center=(330, 450)),
            2: self.level_images[2].get_rect(center=(600, 380)),
            3: self.level_images[3].get_rect(center=(870, 450)),
        }
        self.hover_color = (255, 225, 120)

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
        mouse_pos = pygame.mouse.get_pos()
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.title_image, self.title_image.get_rect(center=(WIDTH // 2, 95)))
        for level, rect in self.level_buttons.items():
            self.screen.blit(self.level_images[level], rect)
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, self.hover_color, rect.inflate(16, 16), 4, border_radius=18)
