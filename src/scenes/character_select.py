import pygame

from src.core.settings import BLACK, HEIGHT, WHITE, WIDTH
from src.scenes.base_scene import BaseScene
from src.systems.ui import TextButton


class CharacterSelectScene(BaseScene):
    # Character selection currently records the choice and moves to level select.
    def __init__(self, app):
        super().__init__(app)
        self.background = self.assets.image("image/เมนู/bg4.png", (WIDTH, HEIGHT), alpha=False)
        self.ice_image = self.assets.image("image/ตัวละคร/น้ำแข็ง.png", (400, 400), alpha=True)
        self.lava_image = self.assets.image("image/ตัวละคร/ลาวา.png", (400, 400), alpha=True)
        self.font = pygame.font.Font(None, 36)
        self.back_button = TextButton((50, 50, 100, 50), "Back", self.font, (255, 0, 0), (0, 255, 0), WHITE)
        self.ice_rect = self.ice_image.get_rect(topleft=(150, 200))
        self.lava_rect = self.lava_image.get_rect(topleft=(650, 200))

    def handle_events(self, events):
        from src.scenes.level_select import LevelSelectScene
        from src.scenes.start_menu import StartMenuScene

        for event in events:
            if event.type == pygame.QUIT:
                self.state_manager.quit()
            elif self.back_button.is_clicked(event):
                self.state_manager.set_scene(StartMenuScene(self.app))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.ice_rect.collidepoint(event.pos):
                    self.app.selected_character = "ice"
                    self.state_manager.set_scene(LevelSelectScene(self.app))
                elif self.lava_rect.collidepoint(event.pos):
                    self.app.selected_character = "lava"
                    self.state_manager.set_scene(LevelSelectScene(self.app))

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self._draw_hover_glow()
        self.screen.blit(self.ice_image, self.ice_rect)
        self.screen.blit(self.lava_image, self.lava_rect)
        self.screen.blit(self.font.render("Ice", True, BLACK), (195, 360))
        self.screen.blit(self.font.render("Lava", True, BLACK), (695, 360))
        self.back_button.draw(self.screen)

    def _draw_hover_glow(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.ice_rect.collidepoint(mouse_pos):
            self._draw_glow(self.ice_rect.center, (0, 255, 255))
        elif self.lava_rect.collidepoint(mouse_pos):
            self._draw_glow(self.lava_rect.center, (255, 165, 0))

    def _draw_glow(self, center, color):
        for radius in range(10, 140, 8):
            pygame.draw.circle(self.screen, color, (center[0] - 4, center[1] + 20), radius, width=2)

