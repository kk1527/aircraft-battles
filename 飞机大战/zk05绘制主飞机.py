import pygame

pygame.init()
#创建主窗口 480*700
screen=pygame.display.set_mode((480,700))
#绘制背景图像
bg=pygame.image.load("./images/background.png")
screen.blit(bg,(0,0))
#pygame.display.update()
#绘制主飞机
hero=pygame.image.load("./images/me1.png")
screen.blit(hero,(200,400))
pygame.display.update()
#创建时钟对象
clock=pygame.time.Clock()

i=0
while True:
    clock.tick(60)
    i=i+1

pygame.quit()