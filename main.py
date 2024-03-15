import pygame
import os
import sys
import random

pygame.init()
current_path = os.path.dirname(__file__)
os.chdir(current_path)
WIDTH = 1200
HEIGHT = 600
FPS = 60
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
camera_gruop = pygame.sprite.Group()
from load import *

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
        for i in range(0, 100):
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
                edit_dir_group.add(bush_tile1)
                camera_gruop.add(bush_tile1)
            elif maps[i][j] == "6":
                bush_tile_tower = Bush(bush_tile_tower_image, pos)
                edit_dir_group.add(bush_tile_tower)
                camera_gruop.add(bush_tile_tower)
            elif maps[i][j] == "7":
                grass_tile_1 = Bush(grass_tile_1_image, pos)
                edit_dir_group.add(grass_tile_1)
                camera_gruop.add(grass_tile_1)

def restart():
    global enemy_group, bush_group, platform_group, edit_dir_group
    enemy_group = pygame.sprite.Group()
    bush_group = pygame.sprite.Group()
    platform_group = pygame.sprite.Group()
    edit_dir_group = pygame.sprite.Group()


def game_lvl():
    sc.fill('gray')
    enemy_group.update()
    enemy_group.draw(sc)
    bush_group.update()
    bush_group.draw(sc)
    platform_group.update()
    platform_group.draw(sc)
    edit_dir_group.update()
    edit_dir_group.draw(sc)
    pygame.display.update()

restart()
drawMaps('1.txt')
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    game_lvl()
    clock.tick(FPS)
