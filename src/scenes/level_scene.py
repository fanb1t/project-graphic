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
        self.ui_font = pygame.font.Font(None, 42)
        self._load_level()

    def _load_level(self):
        objects = self.factory.create(self.level_data, self.app.selected_players)
        self.players = objects["players"]
        self.key = objects["key"]
        self.door = objects["door"]
        self.platforms = objects["platforms"]
        self.hazards = objects["hazards"]
        self.elevators = objects["elevators"]
        self.buttons = objects["buttons"]
        self.coins = objects["coins"]
        self.springs = objects["springs"]
        self.total_coins = len(self.coins)
        self.collected_coins = 0
        self.key_visible = self.total_coins == 0
        self.time_limit = self.level_data.get("time_limit")
        self.started_at = pygame.time.get_ticks()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.state_manager.quit()

    def update(self):
        self._update_buttons_and_elevators()
        for player in self.players:
            other_players = [other for other in self.players if other is not player]
            player.update(self.platforms, self.elevators, other_players)
            self._check_springs(player)
            self._collect_coins(player)
            if self.key_visible and not player.has_key:
                had_key = player.has_key
                player.pick_up_key(self.key)
                if not had_key and player.has_key:
                    self.app.sound.play("key")

        if self.key_visible:
            self.key.update()
        self._check_timer()
        self._check_hazards()
        self._check_door()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.platforms.draw(self.screen)
        self.hazards.draw(self.screen)
        self.elevators.draw(self.screen)
        self.buttons.draw(self.screen)
        self.springs.draw(self.screen)
        self.coins.draw(self.screen)
        if self.key_visible:
            self.screen.blit(self.key.image, self.key.rect)
        self.screen.blit(self.door.image, self.door.rect)
        for player in self.players:
            self.screen.blit(player.image, player.rect)
        self._draw_hud()

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
                self.app.sound.play("error")
                self._show_message("Game Over", GAME_OVER_TEXT_COLOR)
                self._load_level()
                return

    def _check_springs(self, player):
        for spring in self.springs:
            if spring.bounce(player):
                self.app.sound.play("select")
                return

    def _collect_coins(self, player):
        collected = pygame.sprite.spritecollide(player, self.coins, dokill=True)
        if not collected:
            return

        self.collected_coins += len(collected)
        self.app.sound.play("select")
        if self.collected_coins >= self.total_coins:
            self.key_visible = True
            self.app.sound.play("key")

    def _check_timer(self):
        if self.time_limit is None:
            return

        if self._remaining_time() <= 0:
            self.app.sound.play("error")
            self._show_message("Game Over", GAME_OVER_TEXT_COLOR)
            self._load_level()

    def _check_door(self):
        if self.door.can_clear_level(self.players):
            if self.next_level_data:
                self.app.sound.play("confirm")
                self.state_manager.set_scene(LevelScene(self.app, self.next_level_data))
            else:
                self.app.sound.play("win")
                self._show_message("Winner!", WIN_TEXT_COLOR)
                self._load_level()

    def _show_message(self, message, color):
        text = self.font.render(message, True, color)
        self.screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        pygame.display.flip()
        pygame.time.delay(1200)

    def _remaining_time(self):
        elapsed = (pygame.time.get_ticks() - self.started_at) / 1000
        return max(0, int(self.time_limit - elapsed + 0.999))

    def _draw_hud(self):
        if self.total_coins:
            coin_text = self.ui_font.render(
                f"Coins {self.collected_coins}/{self.total_coins}", True, WHITE
            )
            self.screen.blit(coin_text, (24, 20))

        if self.time_limit is not None:
            timer_text = self.ui_font.render(f"Time {self._remaining_time()}", True, WHITE)
            self.screen.blit(timer_text, timer_text.get_rect(topright=(WIDTH - 24, 20)))
