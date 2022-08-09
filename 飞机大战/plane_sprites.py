import random
import pygame

#屏幕大小常量
SCREEN_RECT=pygame.Rect(0,0,480,700)
#刷新帧率
FRAME_PER_SEC =60
#创建敌机的定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
#英雄发射子弹事件
HERO_FIRE_EVENT=pygame.USEREVENT+1

class GameSprite(pygame.sprite.Sprite):
    """飞机大战游戏精灵"""
    def __init__(self,image_name,speed=1):
        super().__init__()
        self.image=pygame.image.load(image_name)
        self.rect=self.image.get_rect()
        self.speed=speed
    def update(self):
        self.rect.y+=self.speed
    @staticmethod
    def image_names(prefix, count):
        names = []
        for i in range(1, count + 1):
            names.append("./images/" + prefix + str(i) + ".png")

        return names

class Background(GameSprite):
    """"游戏背景精灵"""
    def __init__(self,is_alt=False):
        #1.调用父类初始化方法
        super().__init__("./images/background.png")
        #判断是否是第二张图
        if is_alt:
            self.rect.y=-self.rect.height

    def update(self):
        #1.调用父类方法实现
        super().update()
        #2.移出屏幕，往上
        if self.rect.y>=SCREEN_RECT.height:
            self.rect.y=-self.rect.height

class PlaneSprite(GameSprite):
    """飞机精灵，包括敌机和英雄"""

    def __init__(self, image_names, destroy_names, life, speed):

        image_name = image_names[0]
        super().__init__(image_name, speed)

        # 生命值
        self.life = life

        # 正常图像列表
        self.__life_images = []
        for file_name in image_names:
            image = pygame.image.load(file_name)
            self.__life_images.append(image)

        # 被摧毁图像列表
        self.__destroy_images = []
        for file_name in destroy_names:
            image = pygame.image.load(file_name)
            self.__destroy_images.append(image)

        # 默认播放生存图片
        self.images = self.__life_images
        # 显示图像索引
        self.show_image_index = 0
        # 是否循环播放
        self.is_loop_show = True
        # 是否可以被删除
        self.can_destroied = False

    def update(self):
        self.update_images()
        super().update()

    def update_images(self):
        """更新图像"""

        pre_index = int(self.show_image_index)
        self.show_image_index += 0.05
        count = len(self.images)

        # 判断是否循环播放
        if self.is_loop_show:
            self.show_image_index %= len(self.images)
        elif self.show_image_index > count - 1:
            self.show_image_index = count - 1
            self.can_destroied = True

        current_index = int(self.show_image_index)

        if pre_index != current_index:
            self.image = self.images[current_index]

    def destroied(self):
        """飞机被摧毁"""

        # 默认播放生存图片
        self.images = self.__destroy_images
        # 显示图像索引
        self.show_image_index = 0
        # 是否循环播放
        self.is_loop_show = False

class Enemy(PlaneSprite):
    """敌机精灵"""
    def __init__(self):
        #1.调用父类方法，创建敌机和图片
        image_names = ["./images/enemy1.png"]
        destroy_names = GameSprite.image_names("enemy1_down", 4)
        # 2.指定敌机的初始随机速度1-3
        self.speed = random.randint(1, 3)
        super().__init__(image_names, destroy_names, 2, self.speed)
        #3.指定敌机的初始随机位置
        self.rect.bottom=0
        max_x=SCREEN_RECT.width-self.rect.width
        self.rect.x=random.randint(0,max_x)

    def update(self):
        super().update()

        #2.判断是否飞出屏幕
        if self.rect.y>=SCREEN_RECT.height:
        #kill方法可以将精灵从所有精灵组中移出，精灵自动销毁
            self.kill()
        if self.can_destroied:
            self.kill()
    #del方法会被kill方法调用
    def __del__(self):
        #print("敌机消失%s " %self.rect)
        pass

class Hero(PlaneSprite):
    """英雄精灵"""
    def __init__(self):
        yes=1
        image_names = GameSprite.image_names("me",2)
        destroy_names = GameSprite.image_names("me_destroy_",4)

        super().__init__(image_names, destroy_names,0,0)
        #2.英雄初始位置
        self.rect.centerx=SCREEN_RECT.centerx
        self.rect.bottom=SCREEN_RECT.bottom-120
        #speedx= self.speedx
        #speedy= self.speedy
        #3.创建子弹的精灵组
        self.bullets=pygame.sprite.Group()

    def update(self):
        self.update_images()

        #英雄移动
        #if(self.speed==2 or self.speed==-2):
        self.rect.x+=self.speedx
        #else:
        self.rect.y+=self.speedy
        #英雄不能离开屏幕
        if self.rect.x<0:
            self.rect.x=0
        elif self.rect.right>SCREEN_RECT.right:
            self.rect.right=SCREEN_RECT.right
        if self.rect.y<0:
            self.rect.y=0
        if self.rect.bottom>SCREEN_RECT.bottom:
            self.rect.bottom=SCREEN_RECT.bottom
        if self.can_destroied:
            self.kill()
    def fire(self,yes=0):
        #print("发射")

        for i in (0,1):
            #1.创建子弹精灵
            bullet=Bullet()
            #2.设置精灵的位置
            bullet.rect.bottom=self.rect.y-i*20
            bullet.rect.centerx=self.rect.centerx
            #3.讲精灵添加到精灵组
            if yes==1:
                self.bullets.add(bullet)


class Bullet(GameSprite):
    """创建子弹精灵"""
    def __init__(self):
        super().__init__("./images/bullet1.png",-2)

    def update(self):
        super().update()
        if self.rect.y<0:
            self.kill()

    def __del__(self):
        pass
