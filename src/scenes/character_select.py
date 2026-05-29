import pygame

from src.core.settings import (
    BLACK,
    BUTTON_ACTIVE_COLOR,
    BUTTON_INACTIVE_COLOR,
    HEIGHT,
    WHITE,
    WIDTH,
)
from src.scenes.base_scene import BaseScene
from src.systems.ui import TextButton


class CharacterSelectScene(BaseScene):
    # Lets each player choose a character, then confirms before level select.
    def __init__(self, app):
        super().__init__(app)
        self.background = self.assets.image("image/เมนู/bg4.png", (WIDTH, HEIGHT), alpha=False)
        self.character_images = {
            "ice": self.assets.image("image/ตัวละคร/น้ำแข็ง.png", (170, 170), alpha=True),
            "lava": self.assets.image("image/ตัวละคร/ลาวา.png", (170, 170), alpha=True),
        }
        self.title_font = pygame.font.Font(None, 56)
        self.font = pygame.font.Font(None, 34)
        self.small_font = pygame.font.Font(None, 28)
        self.back_button = TextButton((50, 50, 100, 46), "Back", self.font, (255, 0, 0), (0, 210, 80), WHITE)
        self.confirm_button = TextButton(
            ((WIDTH - 170) // 2, HEIGHT - 95, 170, 50),
            "Confirm",
            self.font,
            BUTTON_INACTIVE_COLOR,
            BUTTON_ACTIVE_COLOR,
        )
        self.player_panels = {
            1: pygame.Rect(110, 150, 440, 450),
            2: pygame.Rect(650, 150, 440, 450),
        }
        self.choice_rects = self._build_choice_rects()
        self.clear_buttons = {
            player_number: TextButton(
                (panel.centerx - 55, panel.y + 405, 110, 38),
                "Clear",
                self.small_font,
                (230, 220, 210),
                (245, 190, 170),
            )
            for player_number, panel in self.player_panels.items()
        }
        self.selections = dict(self.app.selected_players)

    def handle_events(self, events):
        from src.scenes.level_select import LevelSelectScene
        from src.scenes.start_menu import StartMenuScene

        for event in events:
            if event.type == pygame.QUIT:
                self.state_manager.quit()
            elif self.back_button.is_clicked(event):
                self.app.sound.play("click")
                self.state_manager.set_scene(StartMenuScene(self.app))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self._handle_clear_click(event):
                    continue
                self._handle_character_click(event.pos)
                if self.confirm_button.is_clicked(event):
                    if self._can_confirm():
                        self.app.sound.play("confirm")
                        self.app.selected_players = dict(self.selections)
                        self.app.selected_character = self.selections[1]
                        self.state_manager.set_scene(LevelSelectScene(self.app))
                    else:
                        self.app.sound.play("error")

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        title = self.title_font.render("Choose Characters", True, BLACK)
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 85)))

        for player_number, panel in self.player_panels.items():
            self._draw_player_panel(player_number, panel)

        self.back_button.draw(self.screen)
        self._draw_confirm_button()

    def _build_choice_rects(self):
        rects = {}
        for player_number, panel in self.player_panels.items():
            rects[(player_number, "ice")] = pygame.Rect(panel.x + 42, panel.y + 165, 170, 170)
            rects[(player_number, "lava")] = pygame.Rect(panel.x + 228, panel.y + 165, 170, 170)
        return rects

    def _handle_character_click(self, mouse_pos):
        for (player_number, character), rect in self.choice_rects.items():
            if rect.collidepoint(mouse_pos):
                if self.selections.get(player_number) == character:
                    self.selections[player_number] = None
                    self.app.sound.play("click")
                    return

                other_player = 1 if player_number == 2 else 2
                if self.selections.get(other_player) == character:
                    self.app.sound.play("error")
                    return

                self.selections[player_number] = character
                self.app.sound.play("select")

    def _handle_clear_click(self, event):
        for player_number, button in self.clear_buttons.items():
            if button.is_clicked(event):
                self.selections[player_number] = None
                self.app.sound.play("click")
                return True
        return False

    def _draw_player_panel(self, player_number, panel):
        pygame.draw.rect(self.screen, (235, 246, 250), panel, border_radius=8)
        pygame.draw.rect(self.screen, BLACK, panel, 3, border_radius=8)

        heading = self.font.render(f"Player {player_number}", True, BLACK)
        self.screen.blit(heading, heading.get_rect(center=(panel.centerx, panel.y + 38)))

        controls = "Controls: A / W / D" if player_number == 1 else "Controls: Arrow Keys"
        controls_text = self.small_font.render(controls, True, BLACK)
        self.screen.blit(controls_text, controls_text.get_rect(center=(panel.centerx, panel.y + 78)))

        prompt = self.small_font.render("Select one character", True, BLACK)
        self.screen.blit(prompt, prompt.get_rect(center=(panel.centerx, panel.y + 113)))

        for character in ("ice", "lava"):
            self._draw_character_choice(player_number, character)

        selected = self.selections.get(player_number)
        selected_label = f"Selected: {selected.title()}" if selected else "Selected: -"
        selected_text = self.small_font.render(selected_label, True, BLACK)
        self.screen.blit(selected_text, selected_text.get_rect(center=(panel.centerx, panel.y + 385)))
        self.clear_buttons[player_number].draw(self.screen)

    def _draw_character_choice(self, player_number, character):
        rect = self.choice_rects[(player_number, character)]
        selected = self.selections.get(player_number) == character
        unavailable = self._is_taken_by_other_player(player_number, character)

        if selected:
            border_color = (0, 170, 90)
            fill_color = (220, 255, 235)
        elif unavailable:
            border_color = (150, 150, 150)
            fill_color = (225, 225, 225)
        else:
            border_color = BLACK
            fill_color = (255, 255, 255)

        pygame.draw.rect(self.screen, fill_color, rect.inflate(18, 18), border_radius=8)
        pygame.draw.rect(self.screen, border_color, rect.inflate(18, 18), 4, border_radius=8)
        self.screen.blit(self.character_images[character], rect)

        label_color = (80, 80, 80) if unavailable and not selected else BLACK
        label = self.small_font.render(character.title(), True, label_color)
        self.screen.blit(label, label.get_rect(center=(rect.centerx, rect.bottom + 28)))

    def _draw_confirm_button(self):
        if self._can_confirm():
            self.confirm_button.draw(self.screen)
            return

        pygame.draw.rect(self.screen, (190, 190, 190), self.confirm_button.rect)
        pygame.draw.rect(self.screen, BLACK, self.confirm_button.rect, 3)
        label = self.font.render("Confirm", True, (90, 90, 90))
        self.screen.blit(label, label.get_rect(center=self.confirm_button.rect.center))

    def _can_confirm(self):
        return bool(self.selections.get(1) and self.selections.get(2))

    def _is_taken_by_other_player(self, player_number, character):
        other_player = 1 if player_number == 2 else 2
        return self.selections.get(other_player) == character
