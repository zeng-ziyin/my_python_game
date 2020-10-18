import pygame


class heroPlane(object):
    """
    heroPlane类
    """

    def __init__(self, background_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load(".\\py_game_test\\madoka1.jpg").convert_alpha()
        self.image2 = pygame.image.load(".\\py_game_test\\madoka2.jpg").convert_alpha()
        self.rect = self.image1.get_rect()
        self.width, self.height = background_size
        self.rect.left, self.rect.top = 40, (self.height - self.rect.height) // 2
        self.speed = 10
        self.activate = True

    def move_up(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    def move_down(self):
        if self.rect.bottom < self.height:
            self.rect.top += self.speed
        else:
            self.rect.bottom = self.height

    def move_left(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def move_right(self):
        if self.rect.right < self.width:
            self.rect.left += self.speed
        else:
            self.rect.right = self.width

    def reset(self):
        self.activate = True
        self.rect.left, self.rect.top = 40, (self.height - self.rect.height) // 2