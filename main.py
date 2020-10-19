import pygame
import sys
import traceback
from pygame.locals import *
from random import *
import time
import heroPlane
import enemyPlane

pygame.init()
# 全局变量:各资源文件的路径
background_image_path = ".\\py_game_test\\toho_bg.jpg"  # 背景图片路径
hero_image_path = ".\\py_game_test\\madoka.jpg"  # heroPlane图片路径
bullet_image_path = ".\\py_game_test\\magic_bullet.jpg"  # bullet图片路径
bgm_music_path = ".\\py_game_test\\connect.mp3"  # bgm音乐路径
boss_in_sound_path = ".\\py_game_test\\greatwall.wav"  # boss出场音效
smallEnemy_down_sound_path = ".\\sound\\enemy1_down.wav"  # small_enemy毁灭音效
game_title = "zzy game"  # 游戏标题

# 全局变量:初始化各参数值
background_size = (940, 540)  # 背景图片大小
delays = 200  # 设置切换图片的延迟系数值
boss_in_sound = pygame.mixer.Sound(boss_in_sound_path)  # 加载boss出场音效
boss_in_sound.set_volume(0.2)  # boss出场音效音量大小
smallEnemy_down_sound = pygame.mixer.Sound(smallEnemy_down_sound_path)  # 加载small_enemy毁灭音效
smallEnemy_down_sound.set_volume(0.1)  # small_enemy毁灭音效音量大小


def set_music(music_path):
    """
    set_music函数
    作用:1、加载背景音乐
        2、调节音量大小
        3、设置音乐循环次数
    """
    pygame.mixer.init()
    pygame.mixer.music.load(music_path)  # 加载背景音乐
    pygame.mixer.music.set_volume(0.4)  # 音量大小
    pygame.mixer.music.play(-1)  # 循环次数，-1为无限循环


def main():
    # 初始化部分参数
    set_music(bgm_music_path)  # 调用set_music,设置音乐
    background = pygame.image.load(background_image_path)  # 加载背景图片
    pygame.display.set_caption(game_title)  # 设置标题
    screen = pygame.display.set_mode(background_size)  # 这里后期要调全屏还有硬件加速，在这里修改
    running = True  # 运行关键词，False则中断运行
    wudi = False
    clock = pygame.time.Clock()
    delay = delays  # 创建切换图片的延迟系数delay,调整的话在全局变量里面调

    # 创建对象
    hero = heroPlane.heroPlane(background_size)  # 创建hero对象

    enemys = pygame.sprite.Group()
    small_enemys = pygame.sprite.Group()  # 创建small_enemy对象
    mid_enemys = pygame.sprite.Group()  # 创建mid_enemy对象
    big_enemys = pygame.sprite.Group()  # 创建big_enemy对象
    bosses = pygame.sprite.Group()
    enemyPlane.add_small_enemy(enemys, small_enemys, 15, background_size)
    enemyPlane.add_mid_enemy(enemys, mid_enemys, 5, background_size)
    enemyPlane.add_big_enemy(enemys, big_enemys, 2, background_size)
    enemyPlane.add_boss(enemys, bosses, 1, background_size)

    # 索引值
    hero_destory_index = 0
    small_enemy_destory_index = 0
    mid_enemy_destory_index = 0
    big_enemy_destory_index = 0
    boss_destory_index = 0

    # group = pygame.sprite.Group()
    # pygame.sprite.spritecollide()

    # 当运行关键词为True时，持续循环，False时终止循环
    while running:

        for event in pygame.event.get():  # 检测不常用按钮是否被点击
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_u:
                    wudi = not wudi
                if event.key == K_SPACE:
                    hero.use_bullet()

        key_pressed = pygame.key.get_pressed()  # 检测常用按钮是否被持续按下
        if key_pressed[K_w] or key_pressed[K_UP]:
            hero.move_up()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            hero.move_down()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            hero.move_left()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            hero.move_right()

        # 每次循环，延迟系数-1，归零时重置
        delay -= 1
        if delay == -delays:
            delay = delays

        # 碰撞检测---hero与enemy是否碰撞
        hero_collide = pygame.sprite.spritecollide(hero, enemys, False, pygame.sprite.collide_mask)
        if hero_collide:
            if not wudi:
                hero.activate = False
            for enemy in hero_collide:
                enemy.hp -= 1
                if enemy.hp <= 0:
                    enemy.activate = False

        # 碰撞检测---bullet与enemy是否碰撞
        for bullet in hero.hero_bullet_list:
            bullet_collide = pygame.sprite.spritecollide(bullet, enemys, False)
            if bullet_collide:
                bullet.activate = False
                for enemy in bullet_collide:
                    enemy.hp -= 1
                    if enemy.hp <= 0:
                        enemy.activate = False

        # 生成并更新画面
        screen.blit(background, (0, 0))

        # 生成并切换heroPlane图片
        if hero.activate:
            if delay < 0:
                screen.blit(hero.image2, hero.rect)
            else:
                screen.blit(hero.image1, hero.rect)
        else:
            print("GAME OVER")
            hero.reset()
            running = False

        for bullet in hero.hero_bullet_list:
            if bullet.activate:
                screen.blit(bullet.image, bullet.rect)
                bullet.move()
            else:
                hero.remove_bullet(bullet)

        # 生成并切换boss图片
        for boss in bosses:
            if boss.activate:
                boss.move()
                if delay < 0:
                    screen.blit(boss.image2, boss.rect)
                else:
                    screen.blit(boss.image1, boss.rect)
                if boss.rect.left < 1040 and boss.in_sound_key == True:
                    boss_in_sound.play()
                    boss.in_sound_key = False
            else:  # 绘制destory图像
                boss.reset()
        # 生成big_enemy
        for big_enemy in big_enemys:
            if big_enemy.activate:
                big_enemy.move()
                screen.blit(big_enemy.image, big_enemy.rect)
            else:
                big_enemy.reset()
        # 生成mid_enemy
        for mid_enemy in mid_enemys:
            if mid_enemy.activate:
                mid_enemy.move()
                screen.blit(mid_enemy.image, mid_enemy.rect)
            else:
                mid_enemy.reset()
        # 生成small_enemy
        for small_enemy in small_enemys:
            if small_enemy.activate:
                small_enemy.move()
                screen.blit(small_enemy.image, small_enemy.rect)
            else:
                if not (delay % 2):  # 每三帧切换一次毁灭图片
                    if small_enemy_destory_index == 0:
                        smallEnemy_down_sound.play()
                    screen.blit(small_enemy.destory_image[small_enemy_destory_index], small_enemy.rect)
                    small_enemy_destory_index = (small_enemy_destory_index + 1) % 4
                    if small_enemy_destory_index == 0:
                        small_enemy.reset()

        clock.tick(60)  # 界面设置为60帧
        pygame.display.update()


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        with open(".//except.txt", 'a') as txt:
            txt.write(time.asctime(time.localtime(time.time())) + '\n' + traceback.format_exc() + '\n')
        pygame.quit()
        print("出现bug，按下任意键退出。" + "\n" + "请打开游戏文件夹下面的except.txt文件，并将其发送给游戏制作者。")
        # input()