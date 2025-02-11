import pygame

class Game:
    SCREEN_WIDTH = 960
    SCREEN_HEIGHT = 720
    START_SCREEN_COLOR = (255, 0, 0)

    def __init__(self, screen):
        self.screen = screen
        self.tilemap = self.generate_map()
        self.bush_positions = self.generate_bushes()
        self.character = Character(MAP_WIDTH // 2, MAP_HEIGHT // 2)
        self.inventory = Inventory()
        self.plants = []
        self.achievement_popup = AchievementPopup()

    def generate_map(self):
        # Map generation logic
        pass

    def generate_bushes(self):
        # Bush generation logic
        pass

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            self.screen.fill(WHITE)
            self.update_day_night_cycle()
            self.draw_map()
            self.handle_mouse_input()
            self.draw_plants()
            self.handle_input()
            self.character.update_animation()
            self.character.draw(self.screen)
            self.draw_day_night_overlay()
            self.inventory.draw(self.screen)
            self.draw_coin_balance()
            self.handle_sell_interaction()
            self.handle_buy_interaction()
            self.draw_buy_grid()
            self.draw_energy_bar()
            self.draw_water_bar()
            self.sleep_popup.draw(self.screen)
            self.handle_drag_and_drop()

            grown_crops = self.check_grown_crops()
            if all(grown_crops.values()) and not achievements["one_of_each"]["completed"]:
                achievements["one_of_each"]["completed"] = True
                self.achievement_popup.display(f"Achievement Unlocked: {achievements['one_of_each']['name']}")

            if self.COIN_BALANCE >= 30000 and not achievements["rich_farmer"]["completed"]:
                achievements["rich_farmer"]["completed"] = True
                self.achievement_popup.display(f"Achievement Unlocked: {achievements['rich_farmer']['name']}")

            self.achievement_popup.update()
            self.achievement_popup.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i:
                        self.show_achievements_menu = not self.show_achievements_menu
                elif event.type == pygame.MOUSEBUTTONDOWN and self.show_achievements_menu:
                    mouse_pos = pygame.mouse.get_pos()
                    close_button_rect = self.draw_achievements_menu(self.screen)
                    if close_button_rect.collidepoint(mouse_pos):
                        self.show_achievements_menu = False

            if self.show_achievements_menu:
                close_button_rect = self.draw_achievements_menu(self.screen)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()