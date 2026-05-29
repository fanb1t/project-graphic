import pygame

from src.core.settings import (
    BUTTON_ACTIVE_COLOR,
    BUTTON_INACTIVE_COLOR,
    HEIGHT,
    WHITE,
    WIDTH,
)
from src.scenes.base_scene import BaseScene
from src.systems.ui import TextButton


class InstructionScene(BaseScene):
    # Simple instructions scene before returning to the start menu.
    def __init__(self, app):
        super().__init__(app)
        self.background = self.assets.image("image/เมนู/castle bridge.png", (WIDTH, HEIGHT), alpha=False)
        self.font = pygame.font.Font(None, 38)
        self.button_font = pygame.font.Font(None, 36)
        self.ok_button = TextButton(
            ((WIDTH - 70) // 2, HEIGHT - 130, 70, 40),
            "OK",
            self.button_font,
            BUTTON_INACTIVE_COLOR,
            BUTTON_ACTIVE_COLOR,
        )
        self.lines = [
            "Instructions:",
            "- Use A, W, D to move character 1",
            "- Use arrow keys to move character 2",
            "- Grab the golden key",
            "- Enter the door to clear the level",
        ]

    def handle_events(self, events):
        from src.scenes.start_menu import StartMenuScene

        for event in events:
            if event.type == pygame.QUIT:
                self.state_manager.quit()
            elif self.ok_button.is_clicked(event):
                self.app.sound.play("click")
                self.state_manager.set_scene(StartMenuScene(self.app))

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        y = 250
        for line in self.lines:
            text = self.font.render(line, True, WHITE)
            self.screen.blit(text, text.get_rect(center=(WIDTH // 2, y)))
            y += 55
        self.ok_button.draw(self.screen)
