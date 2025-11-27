import pygame
from pygame.sprite import Sprite
import os
import sys

def resource_path(relative_path):
    """获取资源文件的绝对路径,支持 PyInstaller 打包"""
    try:
        # PyInstaller 创建临时文件夹,将路径存储在 _MEIPASS 中
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Ship(Sprite):
    '''管理飞船的类'''
    def __init__(self, ai_game):
        '''初始化飞船并设置其初始位置'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #加载飞船图像并获取其外接矩形
        self.image = pygame.image.load(resource_path('images/ship.bmp'))
        self.rect = self.image.get_rect()
        self.center_ship()
        #移动标志
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        '''根据移动标志调整飞船位置'''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x

    def blitme(self):
        '''在指定位置绘制飞船'''
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        """将飞船放在屏幕正中央"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)