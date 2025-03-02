import pygame
import random
import sys

def run_game():
    # Initialize Pygame
    pygame.init()

    # Set up the screen
    WIDTH, HEIGHT = 800, 650
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Invaders")

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    # Player
    player_img = pygame.image.load('images/player.png')
    player_img = pygame.transform.scale(player_img, (100, 100))
    player_rect = player_img.get_rect()
    player_rect.centerx = WIDTH // 2
    player_rect.bottom = HEIGHT - 50
    player_speed = 15

    # Bullets
    bullet_img = pygame.image.load('images/bullet.png')
    bullet_img = pygame.transform.scale(bullet_img, (20, 40))
    bullets = []
    bullet_speed = 10

    # Enemies
    enemy_types = [
        {'img': pygame.image.load('images/enemy1.png'), 'speed': 3},
        {'img': pygame.image.load('images/enemy2.png'), 'speed': 4},
        {'img': pygame.image.load('images/enemy3.png'), 'speed': 5}
    ]
    enemy_spawn_counts = [10, 15, 20]  # Number of enemies to kill before spawning the next type for each level
    enemy_kill_count = 0
    current_enemy_type = 0
    enemies = []

    # Boss images
    boss_vulnerable_img = pygame.image.load('images/boss.png')
    boss_vulnerable_img = pygame.transform.scale(boss_vulnerable_img, (200, 200))
    boss_invincible_img = pygame.image.load('images/boss-2.png')
    boss_invincible_img = pygame.transform.scale(boss_invincible_img, (200, 200))
    boss_img = boss_vulnerable_img  # Initial boss image
    boss_rect = boss_img.get_rect()
    boss_rect.centerx = WIDTH // 2
    boss_rect.top = 10
    boss_speed = 3
    boss_hp = 100
    boss_bullets = []
    boss_bullet_speed = 5
    boss_hit_count = 0  # Counter to track hits on boss
    boss_invincible = False  # Flag to indicate if boss is invincible
    boss_spawn_time = None  # Variable to track the time when boss spawns ships

    # Game variables
    level = 1
    player_hp = 100
    font = pygame.font.Font(None, 36)
    game_over = False
    you_won = False

    # Health bar parameters
    BAR_LENGTH = 200
    BAR_HEIGHT = 20
    BAR_BORDER_WIDTH = 2
    BAR_COLOR = (0, 255, 0)
    BAR_BORDER_COLOR = (255, 255, 255)

    # Function to draw health bar
    def draw_health_bar(surface, x, y, health, color):
        # Calculate health bar width based on health
        bar_width = int(BAR_LENGTH * health / 100)

        # Draw the background bar
        pygame.draw.rect(surface, BAR_BORDER_COLOR, (x, y, BAR_LENGTH, BAR_HEIGHT))

        # Draw the health bar
        if health > 0:
            pygame.draw.rect(surface, color, (x + BAR_BORDER_WIDTH, y + BAR_BORDER_WIDTH, bar_width, BAR_HEIGHT - 2 * BAR_BORDER_WIDTH))

        # Draw the border
        pygame.draw.rect(surface, BAR_BORDER_COLOR, (x, y, BAR_LENGTH, BAR_HEIGHT), BAR_BORDER_WIDTH)

    # Function to spawn enemies
    def spawn_enemies(current_enemy_type):
        for _ in range(5):
            enemy = enemy_types[current_enemy_type]
            enemy_img = pygame.transform.scale(enemy['img'], (100, 100))
            enemy_rect = enemy_img.get_rect()
            enemy_rect.x = random.randint(0, WIDTH - enemy_rect.width)
            enemy_rect.y = random.randint(-HEIGHT, -100)
            enemies.append({'img': enemy_img, 'rect': enemy_rect, 'speed': enemy['speed']})

    # Function to spawn boss bullets
    def spawn_boss_bullets():
        bullet_rect = bullet_img.get_rect()
        bullet_rect.centerx = boss_rect.centerx
        bullet_rect.centery = boss_rect.bottom
        boss_bullets.append(bullet_rect)

    def terminate():
        pygame.quit()
        sys.exit()

    # Main loop
    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
                return 0
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                    return 0
                if event.key == pygame.K_SPACE:
                    bullet_rect = bullet_img.get_rect()
                    bullet_rect.centerx = player_rect.centerx
                    bullet_rect.bottom = player_rect.top
                    bullets.append(bullet_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
            player_rect.x += player_speed

        for bullet in bullets:
            bullet.y -= bullet_speed
            if bullet.y < 0:
                bullets.remove(bullet)
            else:
                screen.blit(bullet_img, bullet)

        screen.blit(player_img, player_rect)

        # Spawn enemies
        if len(enemies) == 0 and level < 4:
            spawn_enemies(current_enemy_type)

        for enemy in enemies:
            enemy['rect'].y += enemy['speed']
            screen.blit(enemy['img'], enemy['rect'])
            if enemy['rect'].top > HEIGHT:
                enemies.remove(enemy)
                player_hp -= 10  # Decrement HP when an enemy ship passes the player

        # Spawn boss and handle boss logic for level 4
        if level == 4:
            screen.blit(boss_img, boss_rect)
            boss_rect.x += boss_speed
            if boss_rect.left <= 0 or boss_rect.right >= WIDTH:
                boss_speed = -boss_speed  # Reverse direction if boss hits screen edge

            # Boss shooting logic
            if random.randint(1, 60) == 1:  # Adjust this number for frequency of boss shooting
                spawn_boss_bullets()

            # Move and draw boss bullets
            for bullet in boss_bullets:
                bullet.y += boss_bullet_speed
                if bullet.colliderect(player_rect):
                    boss_bullets.remove(bullet)
                    player_hp -= 5  # Decrement HP when hit by boss bullet
                elif bullet.y > HEIGHT:
                    boss_bullets.remove(bullet)
                else:
                    screen.blit(bullet_img, bullet)

            # Draw boss HP and health bar above the boss
            boss_hp_text = font.render(f"Boss HP: {boss_hp}", True, RED)
            screen.blit(boss_hp_text, (10, 10))
            draw_health_bar(screen, boss_rect.centerx - BAR_LENGTH // 2, boss_rect.bottom + 10, boss_hp, RED)

            # Check collision between player's bullets and boss
            for bullet in bullets:
                if bullet.colliderect(boss_rect) and not boss_invincible:
                    bullets.remove(bullet)
                    boss_hp -= 50  # Decrease boss HP when hit by player's bullet
                    boss_hit_count += 1
                    if boss_hit_count >= 3:  # If boss is hit 3 times
                        # Spawn 4 level 3 enemy ships
                        for _ in range(4):
                            enemy_img = pygame.transform.scale(enemy_types[2]['img'], (100, 100))
                            enemy_rect = enemy_img.get_rect()
                            enemy_rect.x = random.randint(0, WIDTH - enemy_rect.width)
                            enemy_rect.y = random.randint(-HEIGHT, -100)
                            enemies.append({'img': enemy_img, 'rect': enemy_rect, 'speed': enemy_types[2]['speed']})
                        boss_invincible = True
                        boss_spawn_time = pygame.time.get_ticks()  # Record boss spawn time
                if boss_invincible:  # Boss is invincible, don't check collision
                    break

            if boss_hp <= 0:
                game_over = True  # Boss defeated, set game over flag
                you_won = True  # Player won the game

        # Check bullet-enemy collisions
        for bullet in bullets:
            for enemy in enemies:
                if bullet.colliderect(enemy['rect']):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    enemy_kill_count += 1

        # Check enemy spawn conditions
        if level <= len(enemy_spawn_counts) and enemy_kill_count >= enemy_spawn_counts[level - 1]:
            enemy_kill_count = 0
            current_enemy_type = min(current_enemy_type + 1, len(enemy_types) - 1)
            level += 1
            player_hp = 100  # Reset player HP when entering a new level

        # Check if boss invincibility time has elapsed
        if boss_invincible and pygame.time.get_ticks() - boss_spawn_time > 3000:  # 3000 milliseconds = 3 seconds
            boss_invincible = False
            boss_hit_count = 0  # Reset boss hit count

        # Check if boss is currently invincible
        if boss_invincible:
            boss_img = boss_invincible_img
        else:
            boss_img = boss_vulnerable_img

        # Draw player HP and health bar at bottom left corner
        player_hp_text = font.render(f"Player HP: {player_hp}", True, WHITE)
        screen.blit(player_hp_text, (10, HEIGHT - 30))
        draw_health_bar(screen, 150, HEIGHT - 30, player_hp, BAR_COLOR)

        if player_hp <= 0 or game_over:
            if player_hp <= 0:
                game_over_text = font.render("GAME OVER", True, RED)
                screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))
                pygame.display.flip()
                pygame.time.wait(3000) 
                terminate()
                return "win"
            elif boss_hp <= 0:
                game_over_text = font.render("BOSS DEFEATED!", True, RED)
                screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))
                pygame.display.flip()
                pygame.time.wait(3000) 
                terminate()
                return "lost"
             # Wait for 4 seconds
            

        pygame.display.flip()
        clock.tick(60)
  # Player lost, terminate game with exit code 1
        
        pygame.display.flip()
        clock.tick(60)

    

# Run the game
run_game()
