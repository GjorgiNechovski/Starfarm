import time

import pygame

from models.constants import SCREEN_HEIGHT, INVENTORY_HEIGHT, SCREEN_WIDTH, BROWN, WHITE


class AchievementPopup:
    def __init__(self):
        self.message = ""
        self.show = False
        self.timer = 0
        self.y = SCREEN_HEIGHT + 50
        self.speed = 1
        self.popup_height = 80

    def display(self, message):
        self.message = message
        self.show = True
        self.timer = time.time()
        self.y = SCREEN_HEIGHT + 50

    def update(self):
        if self.show:
            target_y = SCREEN_HEIGHT - INVENTORY_HEIGHT - self.popup_height + 150

            if time.time() - self.timer < 5:
                if self.y > target_y:
                    self.y -= self.speed
                elif self.y < target_y:
                    self.y = target_y
            else:
                if self.y < SCREEN_HEIGHT + self.popup_height + 50:
                    self.y += self.speed
                else:
                    self.show = False

    def draw(self, screen):
        if self.show:
            popup_width = 300
            popup_x = SCREEN_WIDTH - popup_width - 20
            popup_y = self.y - self.popup_height - 20

            pygame.draw.rect(screen, BROWN, (popup_x, popup_y, popup_width, self.popup_height))
            pygame.draw.rect(screen, WHITE, (popup_x, popup_y, popup_width, self.popup_height), 2)

            font = pygame.font.Font(None, 24)
            text = font.render(self.message, True, WHITE)
            text_x = popup_x + (popup_width - text.get_width()) // 2
            text_y = popup_y + (self.popup_height - text.get_height()) // 2
            screen.blit(text, (text_x, text_y))
