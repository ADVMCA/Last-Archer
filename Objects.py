import Arrow

class Objects:
    COOLDOWN = 30

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.object_img = None
        self.arrow_img = None
        self.arrows = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.object_img, (self.x, self.y))
        for arrow in self.arrows:
            arrow.draw(window)

    def move_arrows(self, vel, obj):
        self.cooldown()
        HEIGHT = 750
        for arrow in self.arrows:
            arrow.move(vel)
            if arrow.off_screen(HEIGHT):
                self.arrows.remove(arrow)
            elif arrow.collision(obj):
                self.arrows.remove(arrow)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 9

    def shoot(self):
        if self.cool_down_counter == 0:
            arrow = Arrow.Arrow(self.x, self.y, self.arrow_img)
            self.arrows.append(arrow)
            self.cool_down_counter = 1

    def get_width(self):
        return self.object_img.get_width()

    def get_height(self):
        return self.object_img.get_height()