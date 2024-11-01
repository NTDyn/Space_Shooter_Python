import pygame
from laser import Laser
from ship import Ship
from settings import PLAYER_SHIP, YELLOW_LASER
from boss import Boss

WIDTH, HEIGHT = 750, 750
class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = PLAYER_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers[:]:  # Duyệt qua từng laser
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs[:]:  # Duyệt qua từng đối tượng để kiểm tra va chạm
                    if laser.collision(obj):
                    # Nếu đối tượng là boss
                        if isinstance(obj, Boss):
                            obj.health -= 10  # Trừ máu boss mỗi lần trúng laser
                            if obj.health <= 0:  # Nếu boss hết máu
                                objs.remove(obj)  # Xóa boss khỏi danh sách
                        else:
                            objs.remove(obj)  # Xóa đối tượng khác (kẻ địch thông thường)

                        if laser in self.lasers:
                            self.lasers.remove(laser)  # Xóa laser sau khi va chạm

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))
