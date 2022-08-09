import pygame

pygame.init()
#创建主窗口 480*700
screen=pygame.display.set_mode((480,700))
#绘制背景图像
bg=pygame.image.load("./images/background.png")
screen.blit(bg,(0,0))
pygame.display.update()

while True:
    pass
pygame.quit()