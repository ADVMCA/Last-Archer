import Objects
import pygame
import os

class Player(Objects.Objects):
    def __init__(self, x, y):
        super().__init__(x, y)
        ARCHER = pygame.image.load(os.path.join("images", "Archer.png"))
        ARROW_ARCHER = pygame.image.load(os.path.join("images", "Arrow_archer.png"))
        self.object_img = ARCHER
        self.arrow_img = ARROW_ARCHER
        self.mask = pygame.mask.from_surface(self.object_img)

    def move_arrows(self, vel, objs):
        self.cooldown()
        HEIGHT = 750
        for arrow in self.arrows:
            arrow.move(vel)
            if arrow.off_screen(HEIGHT):
                self.arrows.remove(arrow)
            else:
                for obj in objs:
                    if arrow.collision(obj):
                        objs.remove(obj)
                        if arrow in self.arrows:
                            self.arrows.remove(arrow)

    def draw(self, window):
        super().draw(window)

