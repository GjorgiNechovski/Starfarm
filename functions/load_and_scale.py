import pygame


def load_and_scale_image(file_path, size=None):
    image = pygame.image.load(file_path).convert_alpha()

    if size:
        image = pygame.transform.scale(image, size)

    return image
