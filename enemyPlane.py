import pygame
from random import *

"""
之后用继承方法重构代码，现在先就这样
"""


class smallEnemy(pygame.sprite.Sprite):
    def __init__(self, background_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(".\\images\\enemy1.png").convert_alpha()
        self.destory_image = []
        self.destory_image.extend([pygame.image.load(".\\images\\enemy1_down1.png").convert_alpha(),
                                   pygame.image.load(".\\images\\enemy1_down2.png").convert_alpha(),
                                   pygame.image.load(".\\images\\enemy1_down3.png").convert_alpha(),
                                   pygame.image.load(".\\images\\enemy1_down4.png").convert_alpha(), ])
        self.rect = self.image.get_rect()
        self.width, self.height = background_size
        self.speed = 3
        self.hp = 1
        self.activate = True
        self.isCollide = True
        self.rect.left, self.rect.top = randint((self.width + self.rect.width), (5 * self.width)), \
                                        randint(30, self.height - self.rect.height - 30)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.right > 0:
            self.rect.left -= self.speed
        else:
            self.reset()

    def reset(self):
        self.activate = True
        self.rect.left, self.rect.top = randint((self.width + self.rect.width), 5 * self.width), \
                                        randint(30, self.height - self.rect.height - 30)


class midEnemy(pygame.sprite.Sprite):
    def __init__(self, background_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(".\\images\\enemy2.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = background_size
        self.speed = 2
        self.hp = 3
        self.activate = True
        self.isCollide = True
        self.rect.left, self.rect.top = randint(2 * (self.width + self.rect.width), 10 * self.width), \
                                        randint(0, self.height - self.rect.height)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.right > 0:
            self.rect.left -= self.speed
        else:
            self.reset()

    def reset(self):
        self.activate = True
        self.rect.left, self.rect.top = randint(2 * (self.width + self.rect.width), 10 * self.width), \
                                        randint(30, self.height - self.rect.height - 30)


class bigEnemy(pygame.sprite.Sprite):
    def __init__(self, background_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(".\\images\\enemy3_n1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = background_size
        self.speed = 1.5
        self.hp = 7
        self.activate = True
        self.isCollide = True
        self.rect.left, self.rect.top = randint(3 * (self.width + self.rect.width), 15 * self.width), \
                                        randint(30, self.height - self.rect.height - 30)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.right > 0:
            self.rect.left -= self.speed
        else:
            self.reset()

    def reset(self):
        self.activate = True
        self.rect.left, self.rect.top = randint(3 * (self.width + self.rect.width), 15 * self.width), \
                                        randint(30, self.height - self.rect.height - 30)


class boss(pygame.sprite.Sprite):
    def __init__(self, background_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load(".\\py_game_test\\madoka1.png").convert_alpha()
        self.image2 = pygame.image.load(".\\py_game_test\\madoka2.png").convert_alpha()
        self.rect = self.image1.get_rect()
        self.width, self.height = background_size
        self.speed = 0.5
        self.hp = 20
        self.activate = True
        self.isCollide = True
        self.in_sound_key = True
        self.rect.left, self.rect.top = randint(5 * (self.width + self.rect.width), 20 * self.width), \
                                        randint(30, self.height - self.rect.height - 30)
        self.mask = pygame.mask.from_surface(self.image1)

    def move(self):
        if self.rect.right > 0:
            self.rect.left -= self.speed
        else:
            self.reset()

    def reset(self):
        self.activate = True
        self.rect.left, self.rect.top = randint(5 * (self.width + self.rect.width), 20 * self.width), \
                                        randint(30, self.height - self.rect.height - 30)


def add_small_enemy(group1, group2, num, background_size):
    for i in range(num):
        enemy = smallEnemy(background_size)
        group1.add(enemy)
        group2.add(enemy)


def add_mid_enemy(group1, group2, num, background_size):
    for i in range(num):
        enemy = midEnemy(background_size)
        group1.add(enemy)
        group2.add(enemy)


def add_big_enemy(group1, group2, num, background_size):
    for i in range(num):
        enemy = bigEnemy(background_size)
        group1.add(enemy)
        group2.add(enemy)


def add_boss(group1, group2, num, background_size):
    for i in range(num):
        enemy = boss(background_size)
        group1.add(enemy)
        group2.add(enemy)
