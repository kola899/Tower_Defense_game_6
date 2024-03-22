import pygame
import os
import sys
import random

pygame.init()
current_path = os.path.dirname(__file__)
os.chdir(current_path)
WIDTH = 1280
HEIGHT = 800
FPS = 60
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
camera_gruop = pygame.sprite.Group()
from load import *

def restart():
    global enemy_group, bush_group, platform_group, edit_dir_group, bullet_group
    enemy_group = pygame.sprite.Group()
    bush_group = pygame.sprite.Group()
    platform_group = pygame.sprite.Group()
    edit_dir_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    enemy = Enemy(enemy_image, (0,575))
    enemy_group.add(enemy)


def game_lvl():
    sc.fill('gray')

    bush_group.update()
    bush_group.draw(sc)
    platform_group.update()
    platform_group.draw(sc)
    edit_dir_group.update()
    edit_dir_group.draw(sc)
    enemy_group.update()
    enemy_group.draw(sc)
    sc.blit(panel_image, (0, 700))
    pygame.display.update()

class Bush(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.dir = 'right'
        self.speedx = 2
        self.speedy = 0



    def update(self):
        self.rect.x +=self.speedx
        self.rect.y +=self.speedy
        if self.dir == 'right':
            self.speedx = 2
            self.speedy = 0
            self.image = pygame.transform.rotate(enemy_image, 0)
        elif self.dir == 'left':
            self.speedx = -2
            self.speedy = 0
            self.image = pygame.transform.rotate(enemy_image, 0)
        elif self.dir == 'top':
            self.speedx = 0
            self.speedy = -2
            self.image = pygame.transform.rotate(enemy_image, 80)
        elif self.dir == 'bottom':
            self.speedx = 0
            self.speedy = 2
            self.image = pygame.transform.rotate(enemy_image, -80)
        if pygame.sprite.spritecollide(self, edit_dir_group, False):
            tile = pygame.sprite.spritecollide(self, edit_dir_group, False)[0]
            if abs(self.rect.centerx - tile.rect.centerx) <= 5 and abs(self.rect.centery - tile.rect.centery) <= 5:
                self.dir = tile.dir
class Platform(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

class Edit_dir(pygame.sprite.Sprite):
    def __init__(self, image, pos, dir):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.dir = dir





def drawMaps(nameFile):
    maps = []
    source = '' + str(nameFile)
    with open(source, 'r') as file:
        for i in range(0, 10):
            maps.append(file.readline().replace('\n', '').split(',')[0:-1])
    pos = [0,0]
    for i in range(0, len(maps)):
        pos[1] = i * 80
        for j in range(0, len(maps[0])):
            pos[0] = 80 * j
            if maps[i][j] == "1":
                bottom = Edit_dir(bottom_image, pos, 'bottom')
                edit_dir_group.add(bottom)
                camera_gruop.add(bottom)
            elif maps[i][j] == "2":
                left = Edit_dir(left_image, pos, 'left')
                edit_dir_group.add(left)
                camera_gruop.add(left)
            elif maps[i][j] == "3":
                right = Edit_dir(right_image, pos, 'right')
                edit_dir_group.add(right)
                camera_gruop.add(right)
            elif maps[i][j] == "4":
                top = Edit_dir(top_image, pos, 'top')
                edit_dir_group.add(top)
                camera_gruop.add(top)
            elif maps[i][j] == "5":
                bush_tile1 = Bush(bush_tile1_image, pos)
                bush_group.add(bush_tile1)
                camera_gruop.add(bush_tile1)
            elif maps[i][j] == "6":
                bush_tile_tower = Bush(bush_tile_tower_image, pos)
                bush_group.add(bush_tile_tower)
                camera_gruop.add(bush_tile_tower)
            elif maps[i][j] == "7":
                grass_tile_1 = Bush(grass_tile_1_image, pos)
                bush_group.add(grass_tile_1)
                camera_gruop.add(grass_tile_1)

class Tower_on_panel(pygame.sprite.Sprite):
    def __init__(self, image, pos, ):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.buy = False
        self.timer_click = 0
        money = 1000
        purchase = 100
        self.upgrate = True
    #def update(self):
    #    if money < purchase:
    #        self.image = of_image

class Tower(pygame.sprite.Sprite):
    def __init__(self, image, pos, ):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.lvl = 1
        self.damage = 30
        self.enemy = None
        self.timer_shot = 0
        self.update = False
    def update(self):
        if self.enemy is None:
            for enemy in enemy_group:
                if ((self.rect.centerx - enemy.rect.centerx) ** 2 + (
                         self.rect.centerx - enemy.rect.center) ** 2) ** 0.5 < 200:
                    self.enemy = enemy
                    break
        if self.enemy not in enemy_group:
            self.enemy = None

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, pos, damage ):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.speed = 5
        self.damage = damage
        self.start_pos =  pygame.math.Vector2(pos[0], pos[1]) #векор начальный
        self.end_pos = pygame.math.Vector2(pos[2], pos[3]) #вектор конечный
        self.velocity = (self.end_pos - self.start_pos).normalize() * self.speed #вектор смещения
        self.rect.center = self.start_pos #стартовоя позиция
        self.timer_shot += 1
        if self.enemy != None and self.timer_shot / FPS > 1:
            x_1 = self.rect.centerx
            y_1 = self.rect.top
            x_2 = self.enemy.rect.centerx
            y_2 = self.enemy.rect.centery
            bullet = Bullet(self.curren_bullet_image, (x_1, y_1, x_2, y_2 ), self.damage)
            bullet_group.add(bullet)

restart()
drawMaps('1.txt')
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    game_lvl()
    clock.tick(FPS)
