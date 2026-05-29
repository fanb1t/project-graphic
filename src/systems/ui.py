import pygame

from src.core.settings import BLACK


class TextButton:
    # Small UI helper for menu buttons and scene navigation.
    def __init__(self, rect, text, font, inactive_color, active_color, text_color=BLACK):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.text_color = text_color

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

    def draw(self, screen):
        color = self.active_color if self.rect.collidepoint(pygame.mouse.get_pos()) else self.inactive_color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 3)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

