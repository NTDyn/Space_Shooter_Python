import pygame
from collide import collide
class Health:
    def __init__(self, x, y, health_img):
        self.x = x
        self.y = y
        self.img = health_img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return self.y > height

    def collide(self, obj):
        return collide(self, obj)
