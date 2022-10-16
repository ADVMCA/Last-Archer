import pygame
import os
import Objects

class Enemy(Objects.Objects):
    ENEMY = pygame.image.load(os.path.join("images", "Enemy.png"))
    COLOR_MAP = {
        "red": (ENEMY)
    }

    def __init__(self, x, y, color):
        super().__init__(x, y)
        self.object_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.object_img)

    def move(self, vel):
        self.y += vel
