import sys
from time import sleep
import pygame
from src.settings import Settings
from src.bullet import Bullet
from src.ship import Ship
from src.alien import Alien
from src.game_stats import GameStats

class Alien_Invasion:
    '''管理游戏和资源的类'''
    def __init__(self):
        '''初始化游戏并创建游戏资源'''
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Alien Invasion')
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        #设置背景颜色
        self.bg_color = (230,230,230)
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.game_active = True

        self._create_fleet()

    def run_game(self):
        '''开始游戏主循环'''
        while True:
            self._check_events()
            if self.game_active:

                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        '''响应按键和鼠标事件'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self,event):
        '''响应按下'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        '''响应释放'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_bullets(self):
        """更新子弹位置并删除已经消失的子弹"""
        #更新子弹位置
        self.bullets.update()

        #删除已经消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        '''检查是否有子弹击中外星人'''
        #两个True表示删除子弹和外星人
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
        if not self.aliens:
            #删除现有子弹并创建新的外星舰队
            self.bullets.empty()
            self._create_fleet()

    def _update_screen(self):
        '''更新屏幕上的图像，并切换到新屏幕'''
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        pygame.display.flip()

    def _fire_bullet(self):
        """创建一颗子弹,并切换到新屏幕"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """创建一个外形舰队"""
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size
        #外星人的间距为外星人的宽度
        current_x,current_y = alien_width,alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x,current_y)
                self.aliens.add(alien)
                current_x += 2 * alien_width
            current_y += 2 * alien_height
            current_x = alien_width

    def _create_alien(self,x_position,y_position):
        """创建一个外星人并将其放在当前行中"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)  

    def _update_aliens(self):
        """更新外形舰队中所有外星人的位置"""
        self.aliens.update()
        self._check_fleet_edges()

        #检测外星人与飞船的碰撞
        #接受一个精灵和一个编组，遍历直到有成员与精灵发生碰撞
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()

        #检查是否有外星人到达屏幕的下边缘
        self._check_aliens_bottom()
    
    def _check_aliens_bottom(self):
        """检查是否有外星人到达屏幕下边缘"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                #想飞船被撞到一样处理
                self._ship_hit()
                break

    def _check_fleet_edges(self):
        """在有外星人到达边缘时采取相应措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整个舰队向下移动,并改变他们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """响应飞船与外星人的碰撞"""
        print("ship hit!")
        #将生命值减一
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            #清空外星人和子弹
            self.bullets.empty()
            self.aliens.empty()
            #创建新的外星舰队并重置飞船
            self._create_fleet()
            self.ship.center_ship()
            #暂停
            sleep(1)
        else:
            self.game_active = False

if __name__ == '__main__':
    #创建游戏实例并运行游戏
    ai = Alien_Invasion()
    ai.run_game()