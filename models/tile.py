import pygame

from models.constants import TILE_SIZE, BROWN, SELL_TILE_COLOR, WHITE


class Tile:
    def __init__(self, tile_type, image, position):
        self.tile_type = tile_type
        self.image = image
        self.position = position
        self.watered = False
        self.is_river = False
        self.is_walkable = False
        if tile_type == "farmland":
            self.watered_image = self.create_darker_image(image)
        else:
            self.watered_image = None

    def create_darker_image(self, image):
        darkened_image = image.copy()
        darkened_image.fill((50, 50, 50, 0), special_flags=pygame.BLEND_RGBA_SUB)
        return darkened_image

    def draw(self, screen):
        x, y = self.position
        tile_rect = pygame.Rect(x * TILE_SIZE[0], y * TILE_SIZE[1], TILE_SIZE[0], TILE_SIZE[1])

        if self.tile_type == "farmland" and self.watered:
            screen.blit(self.watered_image, tile_rect.topleft)
        else:
            screen.blit(self.image, tile_rect.topleft)

        if self.tile_type == 'farmland':
            pygame.draw.rect(screen, BROWN, tile_rect, 1)
        elif self.tile_type == 'sell':
            pygame.draw.rect(screen, SELL_TILE_COLOR, tile_rect)
            font = pygame.font.Font(None, 24)
            sell_text = font.render("Sell", True, WHITE)
            text_x = x * TILE_SIZE[0] + (TILE_SIZE[0] - sell_text.get_width()) // 2
            text_y = y * TILE_SIZE[1] + (TILE_SIZE[1] - sell_text.get_height()) // 2
            screen.blit(sell_text, (text_x, text_y))
        elif self.tile_type == 'buy':
            pygame.draw.rect(screen, (0, 100, 0), tile_rect)
            font = pygame.font.Font(None, 24)
            buy_text = font.render("Buy", True, WHITE)
            text_x = x * TILE_SIZE[0] + (TILE_SIZE[0] - buy_text.get_width()) // 2
            text_y = y * TILE_SIZE[1] + (TILE_SIZE[1] - buy_text.get_height()) // 2
            screen.blit(buy_text, (text_x, text_y))
