class Settings:
    '''存储游戏中的类'''
    def __init__(self):
        '''初始化游戏设置'''
        #屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)

        #飞船设置
        self.ship_speed = 3.0
        self.ship_limit = 3

        #子弹设置
        self.bullet_speed = 2.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullet_allowed = 10

        #外星人设置
        self.alien_speed = 1.0
        self.fleet_drop_speed = 30
        self.fleet_direction = 1