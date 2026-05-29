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


class StartMenuScene(BaseScene):
    # Main menu scene; it only decides which scene comes next.
    def __init__(self, app):
        super().__init__(app)
        self.background = self.assets.image("image/เมนู/bg22.png", (WIDTH, HEIGHT), alpha=False)
        self.logo = self.assets.image("image/เมนู/logo.png", (600, 300), alpha=True)
        self.font = pygame.font.Font(None, 36)
        self.play_button = TextButton(
            ((WIDTH - 170) // 2, HEIGHT // 2 + 55, 170, 50),
            "Play Game",
            self.font,
            BUTTON_INACTIVE_COLOR,
            BUTTON_ACTIVE_COLOR,
        )
        self.instruction_button = TextButton(
            ((WIDTH - 170) // 2, HEIGHT // 2 + 125, 170, 50),
            "Instruction",
            self.font,
            BUTTON_INACTIVE_COLOR,
            BUTTON_ACTIVE_COLOR,
        )

    def handle_events(self, events):
        from src.scenes.character_select import CharacterSelectScene
        from src.scenes.instruction import InstructionScene

        for event in events:
            if event.type == pygame.QUIT:
                self.state_manager.quit()
            elif self.play_button.is_clicked(event):
                self.app.sound.play("click")
                self.state_manager.set_scene(CharacterSelectScene(self.app))
            elif self.instruction_button.is_clicked(event):
                self.app.sound.play("click")
                self.state_manager.set_scene(InstructionScene(self.app))

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.logo, ((WIDTH - 600) // 2 + 8, (HEIGHT - 300) // 2 - 100))
        self.play_button.draw(self.screen)
        self.instruction_button.draw(self.screen)
