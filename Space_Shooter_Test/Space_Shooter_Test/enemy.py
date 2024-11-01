import pygame
from ship import Ship
from laser import Laser
from settings import SMALL_ENEMY, MEDIUM_ENEMY, LARGE_ENEMY, RED_LASER, GREEN_LASER, BLUE_LASER, BOSS_ENEMY, BOSS_LASER
class Enemy(Ship):
    COLOR_MAP = {
                "small": (SMALL_ENEMY, RED_LASER),
                "medium": (MEDIUM_ENEMY, GREEN_LASER),
                "large": (LARGE_ENEMY, BLUE_LASER),
                "boss": (BOSS_ENEMY, BOSS_LASER)
                }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
