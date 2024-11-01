# boss.py
import pygame
from enemy import Enemy
from laser import Laser
from settings import BOSS_ENEMY, BOSS_LASER  # Thêm hình ảnh boss và laser boss trong file settings

class Boss(Enemy):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, "boss", health)
        self.ship_img = BOSS_ENEMY
        self.laser_img = BOSS_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            # Boss có thể bắn nhiều tia laser cùng lúc
            laser1 = Laser(self.x - 20, self.y, self.laser_img)
            laser2 = Laser(self.x + 20, self.y, self.laser_img)
            self.lasers.append(laser1)
            self.lasers.append(laser2)
            self.cool_down_counter = 1
    
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))
