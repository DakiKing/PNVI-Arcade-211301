import pygame
import sys
import subprocess

# Initialize Pygame
pygame.init()

# Prozorecot za igrata
WIDTH, HEIGHT = 800, 800 
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Lobby")

# Vcituvanje na player
player_img = pygame.image.load('images/boy.png')
player_size = player_img.get_size()
player_pos = [WIDTH // 2 - player_size[0] // 2, HEIGHT // 2 - player_size[1] // 2]

# Vcituvanje na igrite
game_box_imgs = []
for i in range(1, 4):
    img = pygame.image.load(f'images/game_box_{i}.png')
    img = pygame.transform.scale(img, (150, 150))  
    game_box_imgs.append(img)

game_box_sizes = [img.get_size() for img in game_box_imgs]

game_boxes = [(50, 50), (50, 240), (50, 450)]  #pozicija na igrite


font = pygame.font.Font(None, 36)

# Vcituvanje na parite
coin_img = pygame.image.load('images/coin2.png')
coin_size = coin_img.get_size()

ticket_img = pygame.image.load('images/tickets.png')
ticket_size = ticket_img.get_size()

# Vcituvanje na prodavnicata
shop_frame_img = pygame.image.load('images/shop-frame5.png')
shop_frame_size = shop_frame_img.get_size()

# Vcituvanje na igrackite
toy_images = [
    pygame.image.load('images/teddy_bear.png'),
    pygame.image.load('images/robot.png'),
    pygame.image.load('images/burger.png'),
    pygame.image.load('images/unicorn.png'),
    pygame.image.load('images/squirrel_toy.png')
]


class Toy:
    def __init__(self, name, cost, available, image):
        self.name = name
        self.cost = cost
        self.available = available
        self.image = image

# Objekti za igrackite
toys = [
    Toy("Teddy Bear", 15, True, toy_images[0]),
    Toy("Robot", 20, True, toy_images[1]),
    Toy("Burger", 10, True, toy_images[2]),
    Toy("Unicorn", 25, True, toy_images[3]),
    Toy("Squirl", 20, True, toy_images[4])
]

# Inventory 
inventory_area = pygame.Rect(0, HEIGHT - 200, WIDTH, 200)
inventory = []

# Kupeni igracki
purchased_toys = []

def display_popup(text, image=None):
    popup_font = pygame.font.Font(None, 36)
    popup_window = True
    popup_timer = pygame.time.get_ticks()  # vrakja vreme
    while popup_window:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        WINDOW.fill((255, 255, 255))
        draw_text(text, (WIDTH // 2, HEIGHT // 3), font=popup_font)
        if image:
            image_rect = image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            WINDOW.blit(image, image_rect)
        pygame.display.update()
        if pygame.time.get_ticks() - popup_timer >= 3000:  #trae 3 sec
            popup_window = False

# Launch game
def launch_game(game_file):
    output = subprocess.check_output(['python', game_file]).decode('utf-8').strip()
    lines = output.splitlines()
    score_line = lines[-1]  
    score = score_line.split(':')[-1].strip()  
    return score

# funkcija za text prompt
def draw_text(text, position, color=(0, 0, 0), font=None):
    if font is None:
        font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    WINDOW.blit(text_surface, text_rect)

#Informacii
def info():
    info_window = True
    instructions = [
        "INSTRUCTIONS:",
        "",
        "COLLECT ALL TOYS TO WIN",
        "",
        "Use the arrow keys to move around the lobby.",
        "You can access the GAME you are in front of by clicking SPACE.",
        "You can access the SHOP when you are in front of it.",
        "If you have no coins, press 'B' and enter the code 'extra'."
        
    ]
    
    while info_window:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
        WINDOW.fill((255, 255, 255))
        draw_text("PRESS ENTER KEY TO RETURN.", (WIDTH//2, HEIGHT -20))
        y_offset = HEIGHT // 4
        for line in instructions:
            draw_text(line, (WIDTH // 2, y_offset))
            y_offset += 30 
        pygame.display.update()

# VAUCHER CODE
def create_input_window():
    input_window = True
    input_text = ""
    while input_window:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_text == "admin":
                        return 999
                    if input_text == "extra":
                        return 5
                    else:
                        return -1
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        WINDOW.fill((255, 255, 255))
        draw_text("ENTER CODE AND REDEEM COINS:", (WIDTH // 2, HEIGHT // 4))
        draw_text(input_text, (WIDTH // 2, HEIGHT // 2))
        pygame.display.update()


# Main game loop
running = True
coins = 1  #Br coins
tickets = 0  #Br tickets
in_shop_range = False
selected_toy_index = 0

# NPC 
npc_img = pygame.image.load('images/girl.png') 
npc_size = npc_img.get_size()
npc_pos = [WIDTH - npc_size[0] - 50, HEIGHT // 2 - npc_size[1] // 2 -70]
npc_speed = 2  # brzina na dvizenje
npc_target_pos = npc_pos[:]  # Cuva pozicija na player

while running:
    WINDOW.fill((255, 255, 255))
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if in_shop_range:
                    selected_toy = toys[selected_toy_index]
                    if selected_toy.available and tickets >= selected_toy.cost and selected_toy.name not in purchased_toys:
                        # Za kopuvanje
                        tickets -= selected_toy.cost
                        purchased_toys.append(selected_toy.name)
                        inventory.append((selected_toy.name, selected_toy.image))  # Add toy to inventory
                        display_popup(f"You bought a {selected_toy.name}!", selected_toy.image)
                        print(f"Bought {selected_toy.name}!")
                        # Proverka za dali se site kupeni
                        if len(purchased_toys) == len(toys):
                            display_popup("Congrats! You won.")
                            # Pobeda dokolku site se kupeni
                    elif selected_toy.available and tickets < selected_toy.cost:
                        print("Not enough tickets to buy this toy.")
                    elif not selected_toy.available:
                        print("This toy is not available.")
                else:
                    for i, box in enumerate(game_boxes):
                        box_rect = pygame.Rect(box[0], box[1], game_box_sizes[i][0], game_box_sizes[i][1])
                        player_rect = pygame.Rect(player_pos[0]+player_size[0]//2, player_pos[1], player_size[0]//2, player_size[1])
                        if player_rect.colliderect(box_rect):
                            if coins > 0:
                                coins -= 1
                                if i == 0:
                                    score = launch_game('games\WORMY.PY')
                                    tickets += int(score)
                                elif i == 1:
                                    score = launch_game('games\SQUIRLY.PY') 
                                    tickets += int(score)
                                elif i == 2:
                                    score = launch_game('games\SPACE.PY')
                                    print("hi")
                                    print(score)
                            else:
                                print("Not enough coins to play!")
            elif event.key == pygame.K_UP:
                selected_toy_index = (selected_toy_index - 1) % len(toys)
            elif event.key == pygame.K_DOWN:
                selected_toy_index = (selected_toy_index + 1) % len(toys)
            elif event.key == pygame.K_b and coins == 0:
                result = create_input_window()
                if result == 999:
                    coins = 999
                    tickets = 999
                if result == 5:
                    coins = 5
                else:
                    print("Sorry, wrong code.")
            elif event.key == pygame.K_i:
                result = info()
    # Get keyboard input
    keys = pygame.key.get_pressed()
    move_distance = 2
    next_pos = player_pos.copy()

    # Sledna pozicija na player
    if keys[pygame.K_LEFT]:
        next_pos[0] -= move_distance
    if keys[pygame.K_RIGHT]:
        next_pos[0] += move_distance
    if keys[pygame.K_UP]:
        next_pos[1] -= move_distance
    if keys[pygame.K_DOWN]:
        next_pos[1] += move_distance

        # Granici
    next_pos[0] = max(140, min(WIDTH - 140 - player_size[0], next_pos[0]))
    next_pos[1] = max(100, min(HEIGHT - 200 - player_size[1], next_pos[1]))   # Adjusts for the top with a maximum range of 100 pixels
    next_pos[1] = min(HEIGHT - 200, max(100, next_pos[1]))  # Adjusts for the bottom

    # Dali sledniot cekor e vo granicite
    if WIDTH - 140 - player_size[0] <= next_pos[0] <= WIDTH - 50 and \
            100 <= next_pos[1] <= HEIGHT - player_size[1]:
        in_shop_range = True
    else:
        in_shop_range = False

    # Update player position 
    player_pos = next_pos

    # Update NPC position
    if in_shop_range:
        # NPC kon player
        if npc_pos[1] < player_pos[1]:
            npc_pos[1] += npc_speed
        elif npc_pos[1] > player_pos[1]:
            npc_pos[1] -= npc_speed
    else:
        # NPC kon pocetna pozicija
        if npc_pos[1] < npc_target_pos[1]:
            npc_pos[1] += npc_speed
        elif npc_pos[1] > npc_target_pos[1]:
            npc_pos[1] -= npc_speed

    # NPC da bide vo ramka na postavenite granici
    npc_pos[1] = max(10, min(HEIGHT - 10 - npc_size[1], npc_pos[1]))

    # Draw player
    WINDOW.blit(player_img, player_pos)

    # Draw NPC
    WINDOW.blit(npc_img, npc_pos)

    # Draw game boxes
    for i, box in enumerate(game_boxes):
        WINDOW.blit(game_box_imgs[i], box)
        box_center = (box[0] + game_box_sizes[i][0] // 2, box[1] + game_box_sizes[i][1] // 2)
        distance_to_box = ((player_pos[0] - box_center[0]) ** 2 + (player_pos[1] - box_center[1]) ** 2) ** 0.5
        if distance_to_box < 45:
            game_name = None
            if i == 0:
                game_name = 'to play Wormy'
            elif i == 1:
                game_name = ' to play Squirls'
            elif i == 2:
                game_name = 'to play Space-Invador'
            if game_name:
                draw_text(f"Press SPACE {game_name}", (player_pos[0] + player_size[0] // 2 + 10, player_pos[1] - 30))

    # Draw shop menu
    if in_shop_range:
        shop_width = 500
        shop_height = 550
        shop_x = (100) // 2
        shop_y = (HEIGHT - shop_height-105) // 2
        pygame.draw.rect(WINDOW, (200, 200, 200), (shop_x, shop_y, shop_width, shop_height))

        draw_text("Shop Menu", (WIDTH//2 -75, shop_y + 30))

        toy_image_width = 80  
        toy_image_height = 80  
        for i, toy in enumerate(toys):
            y = shop_y + 50 + i * 100 
            toy_x = shop_x + 50
            toy_image_rect = toy.image.get_rect()
            toy_image_rect.topleft = (toy_x, y)
            WINDOW.blit(pygame.transform.scale(toy.image, (toy_image_width, toy_image_height)), toy_image_rect.topleft)
            # Draw toy name
            draw_text(toy.name, (toy_x + toy_image_width + 50, y + toy_image_height // 2), color=(0, 0, 0))
            # Draw toy price
            draw_text(f"{toy.cost} Tickets", (toy_x + toy_image_width + 300, y + toy_image_height // 2 ), color=(0, 0, 0))

            # Draw < koga e selektiran
            if selected_toy_index == i:
                draw_text(">", (toy_x - 30, y + toy_image_height // 2), color=(255, 0, 0))  # Add "<" symbol

            # crta za oddeluvanje
            pygame.draw.line(WINDOW, (0, 0, 0), (toy_x, y + 60), (toy_x + toy_image_width + 200, y + 60), 2)
            
            # Preshkrtuva dokolku e kupen
            if toy.name in purchased_toys:
                pygame.draw.line(WINDOW, (255, 0, 0), (toy_x + toy_image_width - 100, y + toy_image_height // 2), 
                                 (toy_x + toy_image_width + 50 + 310, y + toy_image_height // 2), 2)

    # Draw inventory area
    pygame.draw.rect(WINDOW, (200, 200, 200), inventory_area)

    # Draw toys in inventory
    for i, (toy_name, toy_image) in enumerate(inventory):
        toy_x = 50 + i * 120
        toy_y = HEIGHT - 150
        WINDOW.blit(toy_image, (toy_x, toy_y))

    draw_text("Click 'I' for Info",(100, 15))
    # Draw coin count
    WINDOW.blit(coin_img, (WIDTH - 75, -10))
    draw_text(f"Coins: {coins}", (WIDTH - 100, 25))
    if coins==0:
        draw_text("No more coins", (WIDTH // 2, 15))
        draw_text("Press B and ENTER code", (WIDTH // 2, 585))

    # Draw ticket count
    WINDOW.blit(ticket_img, (WIDTH - 60, 20))
    draw_text(f"Tickets: {tickets}", (WIDTH - 100, 60))

    WINDOW.blit(shop_frame_img, (WIDTH - 475, 75))
    pygame.display.update()

# Quit Pygame
pygame.quit()
sys.exit()
