import pygame
from plane_sprites import *

class PlaneGame(object):
    """飞机大战主程序"""
    def __init__(self):
        print("游戏初始化。。。")
        #1.创建窗口
        self.screen=pygame.display.set_mode(SCREEN_RECT.size)
        #2.创建时钟
        self.clock=pygame.time.Clock()
        #3.调用私有方法
        self.__create_sprites()
        #4. 设置定时器事件，创建敌机
        pygame.time.set_timer(CREATE_ENEMY_EVENT,1000)
        pygame.time.set_timer(HERO_FIRE_EVENT,500)
        #5.游戏得分
        self.score = 0
        self.hero1=1

    def __create_sprites(self):
        #创建背景精灵和精灵组
        bg1=Background()
        bg2=Background(True)
        self.back_group=pygame.sprite.Group(bg1,bg2)
        self.enemy=Enemy()
        self.enemy_group=pygame.sprite.Group(self.enemy)
        #创建主飞机的精灵和精灵组
        self.hero=Hero()
        self.hero_group=pygame.sprite.Group(self.hero)
        self.destroy_group = pygame.sprite.Group()

    def start_game(self):
        print("游戏开始。。。")
        while True:
            #1.设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)
            #2.事件监听
            self.__event_handler()
            #3.碰撞检测
            self.__check_collide()
            #4.更新绘制精灵组
            self.__update_sprites()
            #5.更新显示
            pygame.display.update()
    def __event_handler(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                PlaneGame.__game_over()
            elif event.type==CREATE_ENEMY_EVENT:
                #print("敌机出场。。。")
                #创建敌机精灵
                enemy=Enemy()
                self.enemy_group.add(enemy)
            #elif event.type==pygame.KEYDOWN and event.key==pygame.K_RIGHT:
             #   print("向右")
            elif event.type==HERO_FIRE_EVENT and self.hero1!=0:
                self.hero.fire(1)
        #使用pygame模块
        keys_pressed=pygame.key.get_pressed()
        #判断元祖中对应的按键索引值
        if keys_pressed[pygame.K_RIGHT]:
            self.hero.speedx=2
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.speedx=-2
        elif keys_pressed[pygame.K_UP]:
            self.hero.speedy=-2
        elif keys_pressed[pygame.K_DOWN]:
            self.hero.speedy=2
        else:
            self.hero.speedx=0
            self.hero.speedy=0
        if keys_pressed[pygame.K_DOWN] and keys_pressed[pygame.K_RIGHT]:
            self.hero.speedx = 2
            self.hero.speedy = 2
        elif keys_pressed[pygame.K_DOWN] and keys_pressed[pygame.K_LEFT]:
            self.hero.speedx = -2
            self.hero.speedy = 2
        elif keys_pressed[pygame.K_UP] and keys_pressed[pygame.K_RIGHT]:
            self.hero.speedx = 2
            self.hero.speedy = -2
        elif keys_pressed[pygame.K_UP] and keys_pressed[pygame.K_LEFT]:
            self.hero.speedx = -2
            self.hero.speedy = -2

    def __check_collide(self):
        #1.子弹摧毁敌机
        enemies=pygame.sprite.groupcollide(self.enemy_group,
                                             self.hero.bullets,
                                             False,
                                             True).keys()
        for enemy in enemies:
            enemy.life -= 1
            if enemy.life <= 0:
                self.score+=1
                enemy.add(self.destroy_group)
                enemy.remove(self.enemy_group)
                enemy.destroied()
        #2.敌机撞毁英雄
        for hero in pygame.sprite.spritecollide(self.hero,
                                                self.enemy_group,
                                                True):
            self.hero1=0
            print("英雄牺牲了...")
            self.hero.destroied()
            #self.hero.fire(0)
        #3.判断列表
        """if len(enemies)>0:
            #英雄死亡
            self.hero.kill()
            #self.bullet.remove(self.bullet_group)"""

    def __update_sprites(self):
        self.back_group.update()
        self.back_group.draw(self.screen)
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
        self.hero_group.update()
        self.hero_group.draw(self.screen)
        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)
        self.destroy_group.update()
        self.destroy_group.draw(self.screen)
        self.drawText("score:" + str(self.score), SCREEN_RECT.width - 50, 30,25)
        if self.hero1==0:
            self.drawText("game over!!",SCREEN_RECT.centerx-0,SCREEN_RECT.centery-0,50)
            self.drawText("score:"+str(self.score),SCREEN_RECT.centerx+7,SCREEN_RECT.centery+30,40)
    #静态方法
    @staticmethod
    def __game_over():
        print("游戏结束。。。")
        pygame.quit()
        exit()
    def drawText(self,text,posx,posy,textHeight,fontColor=(1,1,1),backgroundColor=(255,255,255)):
        #font_list = pygame.font.get_fonts()
        pygame.init()
        fontObj = pygame.font.SysFont('宋体',textHeight)

        textSurfaceObj = fontObj.render(text,13,fontColor,backgroundColor)

        textRectObj = textSurfaceObj.get_rect()

        textRectObj.center = (posx,posy)
        #绘制得分图像
        self.screen.blit(textSurfaceObj,textRectObj)

if __name__ == '__main__':
    game = PlaneGame()
    game.start_game()