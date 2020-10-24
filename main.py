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
bgm_music_path = ".\\py_game_test\\connect.wav"  # bgm音乐路径
boss_in_sound_path = ".\\py_game_test\\greatwall.wav"  # boss出场音效
smallEnemy_down_sound_path = ".\\sound\\enemy1_down.wav"  # small_enemy毁灭音效
pussed_nor_image_path = ".\\images\\pause_nor.png"  # 暂停图标路径
pussed_press_image_path = ".\\images\\pause_pressed.png"
resume_nor_image_path = ".\\images\\resume_nor.png"  #开始图标路径
resume_press_image_path = ".\\images\\resume_pressed.png"
font_path = ".\\font\\font.ttf"  # font字体路径
game_title = "zzy game demo 0.6"  # 游戏标题

# 全局变量:初始化各参数值
background_size = (940, 540)  # 背景图片大小
delay = 300  # 设置切换图片的延迟系数值
bon_num = 3  # 设置全屏炸弹次数
score = 0
wudi = [False]
pussed = [False]
boss_in_sound = pygame.mixer.Sound(boss_in_sound_path)  # 加载boss出场音效
boss_in_sound.set_volume(0.2)  # boss出场音效音量大小
smallEnemy_down_sound = pygame.mixer.Sound(smallEnemy_down_sound_path)  # 加载small_enemy毁灭音效
smallEnemy_down_sound.set_volume(0.1)  # small_enemy毁灭音效音量大小
WHITE = (255, 255, 255)


# def keyboard_control(hero, enemys, pussed_rect):
#     """
#     键盘检测函数
#     作用:1、点击QUIT退出
#         2、点击u开启无敌
#         3、点击tab清屏
#         4、单机空格发射子弹
#         5、长按空格持续射出子弹
#         6、方向键和wasd控制移动
#     :param  hero: hero对象
#     :param  bon_num: 全屏炸弹次数
#     :param  enemys: enemys数组
#     :return NULL
#     """
#
#     global bon_num  # 创建全屏炸弹次数bon_num,调整的话再全局变量里面调
#
#     for event in pygame.event.get():  # 检测不常用按钮是否被点击
#         if event.type == QUIT:
#             pygame.quit()
#             sys.exit()
#         elif event.type == KEYDOWN:
#             if event.key == K_u:
#                 wudi[0] = not wudi[0]
#             if event.key == K_SPACE:
#                 hero.use_bullet()
#             if event.key == K_TAB:
#                 if bon_num > 0:
#                     bon_num -= 1
#                     for enemy in enemys:
#                         if enemy.activate and enemy.rect.left < 1040:
#                             enemy.activate = False
#         elif event.type == MOUSEBUTTONDOWN:
#             if event.button ==1 and pussed_rect.collidepoint(event.pos):
#                 pussed[0] = not pussed[0]
#         # elif event.type == MOUSEMOTION:
#         #     if pussed_rect.collidepoint(event.pos):
#         #         if pussed:
#         #
#         #         else:
#         #
#         #     else:
#         #         if pussed:
#         #
#         #         else:
#
#     key_pressed = pygame.key.get_pressed()  # 检测常用按钮是否被持续按下
#     if key_pressed[K_w] or key_pressed[K_UP]:
#         hero.move_up()
#     if key_pressed[K_s] or key_pressed[K_DOWN]:
#         hero.move_down()
#     if key_pressed[K_a] or key_pressed[K_LEFT]:
#         hero.move_left()
#     if key_pressed[K_d] or key_pressed[K_RIGHT]:
#         hero.move_right()
#     if key_pressed[K_SPACE]:
#         if not (delay % 30):
#             hero.use_bullet()


def collide_test(hero, enemys):
    """
    碰撞检测函数
    作用:1、检测hero与enemy是否碰撞
        2、检测bullet与enemy是否碰撞

    :param  hero: hero对象
    :param  enemys: enemys数组
    :return NULL
    """
    # 碰撞检测---hero与enemy是否碰撞
    hero_collide = pygame.sprite.spritecollide(hero, enemys, False, pygame.sprite.collide_mask)
    if hero_collide:
        if not wudi[0]:
            hero.hp -= 1
            hero.reset()
            if hero.hp <= 0:
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


def set_music(music_path):
    """
    set_music函数
    作用:1、加载背景音乐
        2、调节音量大小
        3、设置音乐循环次数
    """
    pygame.mixer.init()
    music = pygame.mixer.Sound(music_path)  # 加载背景音乐
    music.set_volume(0.4)  # 音量大小
    music.play(-1)  # 循环次数，-1为无限循环


def main():
    # 初始化部分参数
    set_music(bgm_music_path)  # 调用set_music,设置音乐
    font = pygame.font.Font(font_path, 36)  # 设置字体及大小
    background = pygame.image.load(background_image_path)  # 加载背景图片
    pygame.display.set_caption(game_title)  # 设置标题
    screen = pygame.display.set_mode(background_size)  # 这里后期要调全屏还有硬件加速，在这里修改
    pussed_nor_image = pygame.image.load(pussed_nor_image_path)  # 加载暂停图标图片
    pussed_press_image = pygame.image.load(pussed_press_image_path)  # 加载暂停图标图片
    resume_nor_image = pygame.image.load(resume_nor_image_path)  # 加载开始图标图片
    resume_press_image = pygame.image.load(resume_press_image_path)  # 加载开始图标图片
    running = True  # 创建运行标志，False则中断运行
    clock = pygame.time.Clock()
    global delay  # 创建切换图片的延迟系数delay,调整的话在全局变量里面调
    global bon_num  # 创建全屏炸弹次数bon_num,调整的话再全局变量里面调
    temp_delay = delay
    global wudi  # 创建无敌标志
    global score # 初始化得分
    global pussed  # 创建暂停标志
    level = 1  # 设置等级

    # 创建对象
    hero = heroPlane.heroPlane(background_size)  # 创建hero对象
    enemys = pygame.sprite.Group()
    small_enemys = pygame.sprite.Group()  # 创建small_enemy对象
    mid_enemys = pygame.sprite.Group()  # 创建mid_enemy对象
    big_enemys = pygame.sprite.Group()  # 创建big_enemy对象
    bosses = pygame.sprite.Group()
    enemyPlane.add_small_enemy(enemys, small_enemys, 10, background_size)
    enemyPlane.add_mid_enemy(enemys, mid_enemys, 5, background_size)
    enemyPlane.add_big_enemy(enemys, big_enemys, 2, background_size)
    enemyPlane.add_boss(enemys, bosses, 1, background_size)

    # 创建索引值
    hero_destory_index = 0
    small_enemy_destory_index = 0
    mid_enemy_destory_index = 0
    big_enemy_destory_index = 0
    boss_destory_index = 0

    # 图标修正
    pussed_rect = pussed_press_image.get_rect()
    pussed_rect.left, pussed_rect.top = 940 - 100, 0
    pussed_image = pussed_nor_image

    # 当运行关键词为True时，持续循环，False时终止循环
    while running:
        for event in pygame.event.get():  # 检测不常用按钮是否被点击
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_u:
                    wudi[0] = not wudi[0]
                if event.key == K_SPACE:
                    hero.use_bullet()
                if event.key == K_TAB:
                    if bon_num > 0:
                        bon_num -= 1
                        for enemy in enemys:
                            if enemy.activate and enemy.rect.left < 1040:
                                enemy.activate = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and pussed_rect.collidepoint(event.pos):
                    pussed[0] = not pussed[0]
            elif event.type == MOUSEMOTION:
                if pussed_rect.collidepoint(event.pos):
                    if pussed:
                        pussed_image = resume_press_image
                    else:
                        pussed_image = pussed_press_image
                else:
                    if pussed:
                        pussed_image = resume_nor_image
                    else:
                        pussed_image = pussed_nor_image

        key_pressed = pygame.key.get_pressed()  # 检测常用按钮是否被持续按下
        if key_pressed[K_w] or key_pressed[K_UP]:
            hero.move_up()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            hero.move_down()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            hero.move_left()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            hero.move_right()
        if key_pressed[K_SPACE]:
            if not (delay % 30):
                hero.use_bullet()

        # keyboard_control(hero, enemys, pussed_rect)  # 调用键盘控制函数

        collide_test(hero, enemys)  # 调用碰撞检测函数

        # 每次循环，延迟系数-1，相反时重置
        delay -= 1
        if delay == -temp_delay:
            delay = temp_delay

        screen.blit(pussed_image, (100,100))
        # 生成背景
        screen.blit(background, (0, 0))

        # 设置等级
        lv_temp = level
        level = level + (score // (level * level * 20000))
        level_text = font.render("level : " + str(level), True, WHITE)
        screen.blit(level_text, (10, 50))
        if lv_temp != level:
            enemyPlane.add_small_enemy(enemys, small_enemys, 5, background_size)
            if not (level%3):
                enemyPlane.add_mid_enemy(enemys, mid_enemys, 2, background_size)
            if not (level%5):
                enemyPlane.add_big_enemy(enemys, big_enemys, 1, background_size)
            if not (level%7):
                for enemy in small_enemys:
                    enemy.speed += 0.5
            if not (level%10):
                for enemy in mid_enemys:
                    enemy.speed += 0.3

        # 生成分数
        score_text = font.render("score : " + str(score), True, WHITE)
        screen.blit(score_text, (10, 0))

        # 设置hp
        hp_text = font.render("hp : " + str(hero.hp), True, WHITE)
        screen.blit(hp_text, (800, 0))

        # 设置bone
        bomb_text = font.render("bomb : " + str(bon_num), True, WHITE)
        screen.blit(bomb_text, (800, 50))

        # 生成并切换heroPlane
        if hero.activate:
            if delay < 0:
                screen.blit(hero.image2, hero.rect)
            else:
                screen.blit(hero.image1, hero.rect)
        else:
            hero.reset()
            running = False

        if not (delay % 15):
            hero.use_bullet()

        # 生成bullet
        for bullet in hero.hero_bullet_list:
            if bullet.activate:
                screen.blit(bullet.image, bullet.rect)
                bullet.move()
            else:
                hero.remove_bullet(bullet)

        # 生成并切换boss
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
                boss_in_sound.stop()
                boss.reset()

        # 生成big_enemy
        for big_enemy in big_enemys:
            if big_enemy.activate:
                big_enemy.move()
                screen.blit(big_enemy.image, big_enemy.rect)
            else:
                if big_enemy_destory_index == 0:
                    smallEnemy_down_sound.play()
                big_enemy.reset()
                score += 20000

        # 生成mid_enemy
        for mid_enemy in mid_enemys:
            if mid_enemy.activate:
                mid_enemy.move()
                screen.blit(mid_enemy.image, mid_enemy.rect)
            else:
                if mid_enemy_destory_index == 0:
                    smallEnemy_down_sound.play()
                mid_enemy.reset()
                score += 5000

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
                        score += 1000

        clock.tick(60)  # 界面设置为60帧
        pygame.display.update()


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        with open(".//score.txt", 'a') as txt:
            txt.write(time.asctime(time.localtime(time.time())) + '\n' + "score : " + str(score) + '\n')
    except:
        traceback.print_exc()
        with open(".//except.txt", 'a') as txt:
            txt.write(time.asctime(time.localtime(time.time())) + '\n' + traceback.format_exc() + '\n')
        pygame.quit()
        print("出现bug，按下任意键退出。" + "\n" + "请打开游戏文件夹下面的except.txt文件，并将其发送给游戏制作者。")
        input()
