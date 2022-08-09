import pygame
from plane_sprites import *

pygame.init()
# 创建主窗口 480*700
screen = pygame.display.set_mode((480, 700))
# 绘制背景图像
bg = pygame.image.load("./images/background.png")
screen.blit(bg, (0, 0))
# pygame.display.update()
# 绘制主飞机
hero = pygame.image.load("./images/me1.png")
screen.blit(hero, (200, 400))
pygame.display.update()
# 创建时钟对象
clock = pygame.time.Clock()

#1.rect记录飞机初始位置
hero_rect=pygame.Rect(200,400,102,126)
#创建敌机精灵
enemy=GameSprite("./images/enemy1.png")
enemy1=GameSprite("./images/enemy1.png",2)
#创建敌机精灵组
enemy_group=pygame.sprite.Group(enemy,enemy1)

while True:
    clock.tick(60)
    #捕获事件
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            print("游戏结束。。。")
            pygame.quit()
            exit()
    #修改飞机位置
    hero_rect.y -=1
    if hero_rect.y<=0:
        hero_rect.y=0
    screen.blit(bg,(0,0))
    screen.blit(hero,hero_rect)
    #让精灵组调用两个方法
    #update
    enemy_group.update()
    #draw
    enemy_group.draw(screen)
    pygame.display.update()

pygame.quit()