import os

import pygame

from models.constants import TILE_SIZE


class Plant:
    def __init__(self, plant_type, base_path, num_phases, position, days_to_grow=1):
        self.plant_type = plant_type
        self.base_path = base_path
        self.num_phases = num_phases
        self.current_phase = 1
        self.position = position
        self.images = []
        self.days_to_grow = days_to_grow
        self.days_in_current_phase = 0

        grown_image_path = os.path.join(base_path, f"{plant_type}{num_phases}.png")
        self.grown_image = pygame.image.load(grown_image_path).convert_alpha()
        self.grown_image = pygame.transform.scale(self.grown_image, (TILE_SIZE[0], TILE_SIZE[1]))

        for i in range(1, num_phases + 1):
            image_path = os.path.join(base_path, f"{plant_type}{i}.png")
            image = pygame.image.load(image_path).convert_alpha()

            if i == num_phases:
                scaled_image = self.grown_image
            else:
                scaled_image = pygame.transform.scale(image, (TILE_SIZE[0] // 2, TILE_SIZE[1] // 2))

            self.images.append(scaled_image)

    def grow(self):
        if self.current_phase < self.num_phases:
            self.days_in_current_phase += 1
            if self.days_in_current_phase >= self.days_to_grow:
                self.current_phase += 1
                self.days_in_current_phase = 0

    def draw(self, screen):
        x, y = self.position
        if self.current_phase == self.num_phases:
            plant_image = self.grown_image
        else:
            plant_image = self.images[self.current_phase - 1]

        plant_x = x * TILE_SIZE[0] + (TILE_SIZE[0] - plant_image.get_width()) // 2
        plant_y = y * TILE_SIZE[1] + (TILE_SIZE[1] - plant_image.get_height()) // 2

        screen.blit(plant_image, (plant_x, plant_y))

    def is_grown(self):
        return self.current_phase == self.num_phases
