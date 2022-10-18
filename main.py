import pygame
import os
import random
import threading
import Player
import Enemy
from network import Network

host = "192.168.20.100"
port = 8080

pygame.font.init()

WIDTH, HEIGHT = 950, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LAST ARCHER")

BG = pygame.transform.scale(pygame.image.load(os.path.join("images", "Battle.png")), (WIDTH, HEIGHT))

class MiHilo(threading.Thread):

    def __init__(self,x):
        self.__x = x
        threading.Thread.__init__(self)

    def run (self):  
          print(str(self.__x))

for i in range(10):
    MiHilo(i).start()

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    lost_font = pygame.font.SysFont("arial", 60)

    enemies = []
    wave_length = 5
    enemy_vel = 2

    archer_vel = 5
    arrow_vel = 10

    archer = Player.Player(300, 630)
    archer2 = Player.Player(390, 630)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    net = Network()

    def send_data():
        data = str(net.id) + ":" + str(archer.x)
        reply = net.send(data)
        return reply
    
    def parse_data(data):
        try:
            d = data.split(":")
            return int(d[0])
        except:
            return 0,0

    def redraw_window():
        WIN.blit(BG, (0, 0))
        lives_label = pygame.font.SysFont("arial", 30).render(f"Lives: {lives}", 1, (0, 255, 0))
        level_label = pygame.font.SysFont("arial", 30).render(f"Level: {level}", 1, (0, 0, 255))

        WIN.blit(lives_label, (10, 60))
        WIN.blit(level_label, (10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        archer.draw(WIN)
        archer2.draw(WIN)

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
                enemy = Enemy.Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["red"]))
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

        archer2.x = parse_data(send_data())

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