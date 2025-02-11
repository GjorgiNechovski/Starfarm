import pygame

from models.constants import SCREEN_WIDTH, SCREEN_HEIGHT, BROWN, WHITE
import time


class SleepPopup:
    def __init__(self):
        self.show = False
        self.yes_rect = None
        self.no_rect = None

    def display(self):
        self.show = True

    def draw(self, screen):
        if self.show:
            popup_width = 300
            popup_height = 150
            popup_x = (SCREEN_WIDTH - popup_width) // 2
            popup_y = (SCREEN_HEIGHT - popup_height) // 2

            pygame.draw.rect(screen, BROWN, (popup_x, popup_y, popup_width, popup_height))
            pygame.draw.rect(screen, WHITE, (popup_x, popup_y, popup_width, popup_height), 2)

            font = pygame.font.Font(None, 36)
            message_text = font.render("Sleep for the night?", True, WHITE)
            message_x = popup_x + (popup_width - message_text.get_width()) // 2
            message_y = popup_y + 20
            screen.blit(message_text, (message_x, message_y))

            yes_button_width = 80
            yes_button_height = 40
            yes_button_x = popup_x + 50
            yes_button_y = popup_y + 80
            self.yes_rect = pygame.Rect(yes_button_x, yes_button_y, yes_button_width, yes_button_height)
            pygame.draw.rect(screen, (0, 255, 0), self.yes_rect)
            yes_text = font.render("YES", True, WHITE)
            screen.blit(yes_text, (yes_button_x + 10, yes_button_y + 10))

            no_button_width = 80
            no_button_height = 40
            no_button_x = popup_x + 170
            no_button_y = popup_y + 80
            self.no_rect = pygame.Rect(no_button_x, no_button_y, no_button_width, no_button_height)
            pygame.draw.rect(screen, (255, 0, 0), self.no_rect)
            no_text = font.render("NO", True, WHITE)
            screen.blit(no_text, (no_button_x + 10, no_button_y + 10))

    def handle_click(self, mouse_x, mouse_y):
        if self.show:
            if self.yes_rect and self.yes_rect.collidepoint(mouse_x, mouse_y):
                self.show = False
                return "yes"
            elif self.no_rect and self.no_rect.collidepoint(mouse_x, mouse_y):
                self.show = False
                return "no"
        return None
