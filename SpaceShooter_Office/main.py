import pygame
import random
import time
from player import Player
from enemy import Enemy
from laser import Laser
from ship import Ship
from collide import collide
from boss import Boss
from settings import BOSS_ENEMY, HEALTH_IMAGE
from health import Health
pygame.font.init()
pygame.mixer.init()
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bắn súng không gian")

#Cài background
BG = pygame.transform.scale(pygame.image.load("E:/C++/SpaceShooter_Office/assets/space_background.jpg"), (WIDTH, HEIGHT))

# Tải âm thanh bắn và nhạc nền
shoot_sound = pygame.mixer.Sound("E:/C++/SpaceShooter_Office/assets/shoot_sound.mp3")  
pygame.mixer.music.load("E:/C++/SpaceShooter_Office/assets/game_sound.mp3")

def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("Tahoma", 30)
    lost_font = pygame.font.SysFont("Tahoma", 40)
    win_font = pygame.font.SysFont("Tahoma", 50)

    enemies, health_packs = [], []
    wave_length = 5
    enemy_vel = 1
    health_vel = 1

    player_vel = 5
    laser_vel = 5

    player = Player(300, 630)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0
    won = False
    win_count = 0

    global boss
    boss = None

    pygame.mixer.music.play(-1)

    def redraw_window():
        global boss
        WIN.blit(BG, (0,0))
        # draw text
        lives_label = main_font.render(f"Số mạng: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Cấp độ: {level}", 1, (255,255,255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)
        
        for health in health_packs:
            health.draw(WIN)
        
        if boss:
            boss.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("Bạn đã thua!", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))
        if won:  
            win_label = win_font.render("Bạn đã thắng!", 1, (255, 255, 255))
            WIN.blit(win_label, (WIDTH / 2 - win_label.get_width() / 2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if boss and boss.y + boss.get_height() >= HEIGHT:
            lost = True
            run = False
            continue

        if lives <= 0 or player.health <= 0:
            lost = True
        
        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                lost_count +=1
                continue
            
        if len(enemies) == 0:
            if level < 3:
                level += 1
                wave_length += 5
                for i in range(wave_length):
                    enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["small", "large", "medium"]))
                    enemies.append(enemy)
            elif level == 3:  # Chỉ tạo boss nếu chưa có boss
                if boss is None and not won:  # Điều kiện để chỉ tạo boss nếu chưa có
                    boss = Boss(WIDTH // 2 - BOSS_ENEMY.get_width() // 2, -200, health=100)
                    enemies.append(boss)

        if boss and boss.health <= 0:
            if boss in enemies:
                enemies.remove(boss)
            boss = None
            won = True
        
        if len(health_packs) < 1 and random.random()<0.01:
            health_pack = Health(random.randrange(50, WIDTH-50), random.randrange(-1000, -100), HEALTH_IMAGE)
            health_packs.append(health_pack)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player.x - player_vel > 0: # left
            player.x -= player_vel
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player.x + player_vel + player.get_width() < WIDTH: # right
            player.x += player_vel
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and player.y - player_vel > 0: # up
            player.y -= player_vel
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and player.y + player_vel + player.get_height() + 15 < HEIGHT: # down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()
            shoot_sound.play()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                if enemy == boss:
                    player.health = 0
                else:
                    enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        for health_pack in health_packs[:]:
            health_pack.move(health_vel)
            if collide(health_pack, player):
                player.health = min(player.health + 20, player.max_health)
                health_packs.remove(health_pack)
            elif health_pack.y> HEIGHT:
                health_packs.remove(health_pack)

        player.move_lasers(-laser_vel, enemies)

        if won:
            win_count += 1
            if win_count > FPS * 3:  # Chờ 3 giây trước khi kết thúc
                run = False

def main_menu():
    instruction_font = pygame.font.SysFont("Tahoma", 20)
    run = True
    show_instructions = True  # Biến để kiểm soát hiển thị bảng hướng dẫn
    instruction_start_time = pygame.time.get_ticks()  # Lưu thời điểm bắt đầu hiển thị hướng dẫn
    while run:
        WIN.blit(BG, (0,0))

        # Hiển thị hướng dẫn trong 3 giây đầu
        if show_instructions:
            # Khung bao quanh bảng hướng dẫn
            rect_x, rect_y = WIDTH / 2 - 250, 130
            rect_width, rect_height = 500, 300
            pygame.draw.rect(WIN, (255, 255, 255), (rect_x, rect_y, rect_width, rect_height), 2)  # Khung viền trắng

            instructions = [
                 "Hướng dẫn chơi:",
                "- Di chuyển bằng các phím W, A, S, D hoặc \u2191 \u2193 \u2190 \u2192",
                "- Nhấn SPACE để bắn laser",
                "- Tránh va chạm với kẻ địch và đạn",
                "- Thu thập các gói hồi máu để tăng máu cho bản thân",
                "- Đánh bại boss để hoàn thành trò chơi!",
                "",
                "Nhấn chuột vào màn hình để bắt đầu!"
            ]

            start_y = rect_y + 20
            line_spacing = 30

            for i, line in enumerate(instructions):
                if i < len(instructions) - 1:  # Đổi màu cho các dòng hướng dẫn (trừ dòng cuối)
                    instruction_label = instruction_font.render(line, 1, (255, 255, 255))  # Màu trắng cho các dòng hướng dẫn
                else:
                    instruction_label = instruction_font.render(line, 1, (255, 255, 0))  # Màu vàng cho dòng "Nhấn chuột..."
                
                WIN.blit(instruction_label, (WIDTH / 2 - instruction_label.get_width() / 2, start_y + i * line_spacing))

            # Kiểm tra nếu đã quá 3 giây thì ẩn hướng dẫn
            if pygame.time.get_ticks() - instruction_start_time > 3000:
                show_instructions = False  # Tắt hướng dẫn sau 3 giây
            
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()


main_menu()
