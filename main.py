import pygame
import os
import random
import threading

pygame.font.init()

WIDTH, HEIGHT = 950, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LAST ARCHER")

ENEMY = pygame.image.load(os.path.join("images", "Enemy.png"))

ARCHER = pygame.image.load(os.path.join("images", "Archer.png"))

ARROW_ARCHER = pygame.image.load(os.path.join("images", "Arrow_archer.png"))

BG = pygame.transform.scale(pygame.image.load(os.path.join("images", "Battle.png")), (WIDTH, HEIGHT))


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
            arrow = Arrow(self.x, self.y, self.arrow_img)
            self.arrows.append(arrow)
            self.cool_down_counter = 1

    def get_width(self):
        return self.object_img.get_width()

    def get_height(self):
        return self.object_img.get_height()
import threading

class MiHilo(threading.Thread):

    def __init__(self,x):
        self.__x = x
        threading.Thread.__init__(self)

    def run (self):  
          print(str(self.__x))

for i in range(10):
    MiHilo(i).start()
class Player(Objects):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.object_img = ARCHER
        self.arrow_img = ARROW_ARCHER
        self.mask = pygame.mask.from_surface(self.object_img)

    def move_arrows(self, vel, objs):
        self.cooldown()
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

class Arrow:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


class Enemy(Objects):
    COLOR_MAP = {
        "red": (ENEMY)
    }

    def __init__(self, x, y, color):
        super().__init__(x, y)
        self.object_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.object_img)

    def move(self, vel):
        self.y += vel


def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("arial", 50)
    lost_font = pygame.font.SysFont("arial", 60)

    enemies = []
    wave_length = 5
    enemy_vel = 2

    archer_vel = 5
    arrow_vel = 10

    archer = Player(300, 630)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG, (0, 0))
        lives_label = pygame.font.SysFont("arial", 30).render(f"Lives: {lives}", 1, (0, 255, 0))
        level_label = pygame.font.SysFont("arial", 30).render(f"Level: {level}", 1, (0, 0, 255))

        WIN.blit(lives_label, (10, 60))
        WIN.blit(level_label, (10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        archer.draw(WIN)

        if lost:
            lost_label = lost_font.render("GAME OVER", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["red"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and archer.x - archer_vel > 0:  # left
            archer.x -= archer_vel
        if keys[pygame.K_RIGHT] and archer.x + archer_vel + archer.get_width() < WIDTH:  # right
            archer.x += archer_vel
        if keys[pygame.K_SPACE]:
            archer.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)

            if collide(enemy, archer):
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        archer.move_arrows(-arrow_vel, enemies)


def titleScreen():
    title_font = pygame.font.SysFont("arial", 70)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render("LAST ARCHER", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()


titleScreen()