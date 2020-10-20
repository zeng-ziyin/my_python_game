import pygame
import random


class heroBullet(object):
    """
    bullet类
    传入参数：画布，bullet的坐标（x，y），bullet图片路径
    实现函数：1、display：在画布上显示bullet，并删除越界的bullet
            2、move：移动bullet
            3、is_prime_move：判断是否越界
    """

    def __init__(self, rect, background_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(".\\py_game_test\\magic_bullet.png")
        self.rect = self.image.get_rect()
        self.width, self.height = background_size
        self.rect.left, self.rect.top = rect.right, rect.top + (rect.height - self.rect.height) // 2
        # self.num_y = random.uniform(-1, 1)  # 创建随机y轴偏移
        self.speed = 25
        self.activate = True

    def move(self):
        if self.rect.left < self.width:
            self.rect.left += self.speed
        else:
            self.activate = False