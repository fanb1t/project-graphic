from pathlib import Path

import pygame

from src.core.asset_loader import AssetLoader
from src.core.settings import FPS, HEIGHT, TITLE, WIDTH
from src.core.state_manager import StateManager
from src.scenes.start_menu import StartMenuScene


class GameApp:
    # Application root: owns pygame, the window, assets, and scene switching.
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.project_root = Path(__file__).resolve().parents[2]
        self.assets = AssetLoader(self.project_root)
        self.state_manager = StateManager()
        self.selected_character = None
        self.state_manager.set_scene(StartMenuScene(self))

    def run(self):
        while self.state_manager.running:
            events = pygame.event.get()
            self.state_manager.handle_events(events)
            self.state_manager.update()
            self.state_manager.draw()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

