# Some part of the code was inspired by code with russ
import pygame
import os
import sys
import constants as con
from enemy import *
from tower import *
from map import *
from buttons import *
from settings import *


if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS  
else:
    base_path = os.path.abspath(".")

assets_path = os.path.join(base_path, "assets")
# Initialize Pygame
pygame.init()

# Create clock
clock = pygame.time.Clock()

##########################################################################################

# Calulates screen size based on the level layout and tile size
def calculate_screen_size(level_layout, tile_size):
    rows = len(level_layout)
    cols = len(level_layout[0])
    screen_width = cols * tile_size
    screen_height = rows * tile_size
    return screen_width, screen_height

# Layout for level
level_layout = [
    [0, 0, 4, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 4, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 4, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 4, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 4, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 4, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 4, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 4, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 4, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 4, 3, 0, 0, 0, 0, 0, 0, 0],
]

# Dynamically set screen size
tile_size = con.TILE_SIZE
screen_width, screen_height = calculate_screen_size(level_layout, tile_size)
screen = pygame.display.set_mode((screen_width + con.SIDE_PANEL, screen_height))
pygame.display.set_caption("The Defender")

# Load tile images
grass_tile_1 = pygame.image.load("assets/tiles/towerDefense_tile119.png").convert_alpha()
grass_tile_2 = pygame.image.load("assets/tiles/towerDefense_tile092.png").convert_alpha()
path_tile_1 = pygame.image.load("assets/tiles/towerDefense_tile158.png").convert_alpha()
start_tile = pygame.image.load("assets/tiles/towerDefense_tile061.png").convert_alpha()
end_tile = pygame.image.load("assets/tiles/towerDefense_tile067.png").convert_alpha()

# Define tile image 
tile_image_level_1 = {
    0: grass_tile_1,
    1: path_tile_1,
    2: start_tile,
    3: end_tile,
    4: grass_tile_2,
}


# Initialize level
current_level = Level(level_layout, tile_size, tile_image_level_1)
current_level.generate_waypoints()
current_level.process_enemies()


#################################################################################

# Variables
is_game_over = False
game_outcome = 0 # -1 is lost or 1 is won
is_level_started = False
is_last_enemy_spawn = pygame.time.get_ticks()
is_placeing_tower = False
is_selected_tower = None
is_game_paused = False
main_menu_status = "main"


############################################################################################

# Load tower spritesheets safely
tower_spritesheets = []
for x in range(1, con.TOWER_LEVELS + 1):
    image_path = f"assets/towers/Weapons_r/turret_animation_{x}.png"
    try:
        tower_animation_image = pygame.image.load(image_path).convert_alpha()
        tower_spritesheets.append(tower_animation_image)
    except FileNotFoundError:
        print(f"Warning: {image_path} not found.")

# Loads cursor image
cursor_tower = pygame.image.load("assets/towers/Weapons_r/turret_r_cursor.png").convert_alpha()

# Enemy image
enemy_type_image = {
    "slime": pygame.image.load("assets/enemys/slime/slime_1.png").convert_alpha(),
    "soldier": pygame.image.load("assets/enemys/soider/soider_1.png").convert_alpha(),
    "tank": pygame.image.load("assets/enemys/tanks/tank_green.png").convert_alpha()
}

# Creats sprite group 
enemy_group = pygame.sprite.Group()
tower_group = pygame.sprite.Group()


###############################################################################################

#GUI images and audio
money_image = pygame.image.load("assets/GUI/money.png").convert_alpha()
HP_image = pygame.image.load("assets/GUI/heart.png").convert_alpha()

# Load sound effects
round_start_sound = pygame.mixer.Sound("assets/sound_effects/game-start-6104.mp3")
round_complete_sound = pygame.mixer.Sound("assets/sound_effects/level_complete.wav")

########################################################################################################

# Text
available_fonts = ["arial", "halvetica", "timesnewroman", "comicsansms", "verdana"]
settings_menu = Settings(screen, available_fonts, initial_font_size = 24)

# Function to Draw Text-Based Buttons 
def draw_text_button(text, pos, font, active_color="grey", inactive_color="white"):
    button_rect = pygame.Rect(pos[0], pos[1], 160, 50)
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, active_color, button_rect)
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, inactive_color, button_rect)

    text_surface = font.render(text, True, "black")
    screen.blit(text_surface, (pos[0] + 10, pos[1] + 10))
    return False


#########################################################################################
# Button Positions
button_positions = {
    "Start": (screen_width + 30, 300),
    "Fast Forward": (screen_width + 30, 300),
    "Upgrade": (screen_width + 30, 180),
    "Cancel": (screen_width + 30, 180),
    "Buy": (screen_width + 30, 120),
    "Tutorial": (screen_width + 30, 380),
    
    "Resume": (297, 125),
    "Options": (297, 250),
    "Quit": (297, 375),
    "Text Settings": (297, 190),
    "Colour Settings": (297, 280),
    "Back": (297, 380)
}

# Add the Tutorial Button to the main menu
button_positions["Tutorial"] = (297, 315)
button_positions["Back"] = (297, 450)

def draw_tutorial():

    # Background for tutorial screen
    screen.fill("black")  
    pygame.draw.rect(screen, "pink", (80, 50, 740, 500), border_radius = 30)
    
    # Get the current font settings from 'Settings'
    current_font = pygame.font.SysFont(
        settings_menu.get_current_font(), 
        settings_menu.get_current_font_size(), 
        bold=True)
    
    # Tutorial text
    tutorial_text = [
        "TUTORIAL",
        "How to get the Tower radius to appear:",
        "1. Click the selected Tower.",
        "2. A white transparent circle will appear",
        "\nHow to Upgrade a Tower",
        "1. Click on a tower you placed",
        "2. If you have enough money, click the selected tower and an upgrade button will appear",
        "\nHow Fast-Forward Works:",
        "Click and hold 'Fast Forward' to speed up enemies."
    ]
    
    # Starting position for text
    y_offset = 80  
    for line in tutorial_text:
        draw_text(line, current_font, "black", 120, y_offset)
        y_offset += 40
    
    # Back button to retun to main main menu
    if draw_text_button("Back", button_positions["Back"], current_font):
        return "main"
    
    return "tutorial"

#######################################################################################
# Font for despaying text on screen 
text_font = pygame.font.SysFont("consolas", 24, bold = True)
big_font = pygame.font.SysFont("consolas", 36)

# Outputs text on screen
def draw_text(text, font, text_col, x, y):
    text = font.render(text, True, text_col)
    screen.blit(text, (x, y))
########################################################################################


########################################################################################
# A fucntion to place towers on grass
def create_towers(mouse_pos):
    mouse_tile_x = mouse_pos[0] // tile_size
    mouse_tile_y = mouse_pos[1] // tile_size

    # Check if the tile is grass
    if level_layout[mouse_tile_y][mouse_tile_x] == 0:
        
        # Check that there isn't already a turret there
        is_space_free = True
        for tower in tower_group:
            if (mouse_tile_x, mouse_tile_y) == (tower.tile_x, tower.tile_y):
                is_space_free = False

        # If the space is free, create the turret
        if is_space_free:
            new_tower = Towers(tower_spritesheets, mouse_tile_x, mouse_tile_y)
            tower_group.add(new_tower)

            # Deduct cost of towers
            current_level.cash -= con.BUY_TOWER_COST
######################################################################################


def display_data():
    # Draw panals 
    pygame.draw.rect(screen, "pink", (screen_width, 0, con.SIDE_PANEL, screen_height))
    pygame.draw.rect(screen, "grey0", (screen_width, 0, con.SIDE_PANEL, 400), 2)


    draw_text("LEVEL: " + str(current_level.round), text_font, "grey0", screen_width + 10, 10)

    screen.blit(HP_image, (screen_width + 10, 44))
    draw_text(str(current_level.health), text_font, "grey100", screen_width + 50, 40)

    screen.blit(money_image, (screen_width + 10, 74))
    draw_text(str(current_level.cash), text_font, "grey100", screen_width + 50, 70)
   


##################################################################################################

def selected_tower(mouse_pos):
    mouse_tile_x = mouse_pos[0] // tile_size
    mouse_tile_y = mouse_pos[1] // tile_size
    for tower in tower_group:
        if (mouse_tile_x, mouse_tile_y) == (tower.tile_x, tower.tile_y):
            return tower
        

def clear_selected_range():
    for tower in tower_group:
        tower.selected = False

###################################################################################################

# Game loop
running = True
while running:

    clock.tick(con.FPS)  # set fps for game

    # Define the current font before any button rendering
    current_font = pygame.font.SysFont(
        settings_menu.get_current_font(),
        settings_menu.get_current_font_size(),
        bold=True
    )  

    if not is_game_paused:
        current_level.draw(screen)  # draws current level

        # Update section
        if not is_game_over:
            if current_level.health <= 0:
                is_game_over = True
                game_outcome = -1

            if current_level.round > con.TOTAL_LEVELS:
                is_game_over = True
                game_outcome = 1

            enemy_group.update(current_level)  # updates the sprite
            tower_group.update(enemy_group, current_level)  # update the towers

            if is_selected_tower:
                is_selected_tower.selected = True

        # Draw section
        enemy_group.draw(screen)
        for tower in tower_group:
            tower.draw(screen)

        display_data()

        # Draw Text-Based Buttons for Game Actions
        if not is_game_over:
            if not is_level_started:
                if draw_text_button("Start", button_positions["Start"], current_font):
                    is_level_started = True
                    round_start_sound.play()
            else:
                current_level.game_speed = 1
                if draw_text_button("Fast Forward", button_positions["Fast Forward"], current_font):
                    current_level.game_speed = 2

                if pygame.time.get_ticks() - is_last_enemy_spawn > con.SPAWN_COOLDOWN:
                    if current_level.spawned_enemies < len(current_level.enemy_list):
                        enemy_type = current_level.enemy_list[current_level.spawned_enemies]
                        enemy = Enemy(enemy_type, current_level.ordered_waypoints, enemy_type_image)
                        enemy_group.add(enemy)
                        current_level.spawned_enemies += 1
                        is_last_enemy_spawn = pygame.time.get_ticks()

            if current_level.check_if_level_complete():
                round_complete_sound.play()
                current_level.cash += con.COMPETE_LEVEL_PONTS
                current_level.round += 1
                is_level_started = False
                is_last_enemy_spawn = pygame.time.get_ticks()
                current_level.rest_level()
                current_level.process_enemies()

            draw_text(str(con.BUY_TOWER_COST), text_font, "grey100", screen_width + 215, 135)
            screen.blit(money_image, (screen_width + 260, 136))

            if draw_text_button("Buy", button_positions["Buy"], current_font):
                is_placeing_tower = True

            if is_placeing_tower:
                cursor_rect = cursor_tower.get_rect()
                cursor_pos = pygame.mouse.get_pos()
                cursor_rect.center = cursor_pos

                if cursor_pos[0] <= screen_width:
                    screen.blit(cursor_tower, cursor_rect)

                if draw_text_button("Cancel", button_positions["Cancel"], current_font):
                    is_placeing_tower = False

            if is_selected_tower:
                if is_selected_tower.upgrade_level < con.TOWER_LEVELS:
                    draw_text(str(con.UPGRADE_COST), text_font, "grey100", screen_width + 215, 195)
                    screen.blit(money_image, (screen_width + 260, 195))

                    if draw_text_button("Upgrade", button_positions["Upgrade"], current_font):
                        if current_level.cash >= con.UPGRADE_COST:
                            is_selected_tower.tower_upgrade()
                            current_level.cash -= con.UPGRADE_COST

    else:
        # Draw a semi-transparent overlay
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(128)  # Set transparency level
        overlay.fill((0, 0, 0))  # Fill with black color
        screen.blit(overlay, (0, 0))

        # Display the pause menu
        pygame.draw.rect(screen, "pink", (200, 100, 400, 400), border_radius=30)

        current_font = pygame.font.SysFont(settings_menu.get_current_font(), settings_menu.get_current_font_size(), bold=True)  # UPDATED

        # Main Pause Menu
        if main_menu_status == "main":
            if draw_text_button("Tutorial", button_positions["Tutorial"], current_font):
                main_menu_status = "tutorial"

            if draw_text_button("Resume", button_positions["Resume"], current_font):
                is_game_paused = False

            if draw_text_button("Options", button_positions["Options"], current_font):
                main_menu_status = "options"

            if draw_text_button("Quit", button_positions["Quit"], current_font):
                running = False
        
                # Options Menu
        elif main_menu_status == "options":
            if draw_text_button("Text Settings", button_positions["Text Settings"], current_font):
                main_menu_status = "text_settings"

            if draw_text_button("Colour Settings", button_positions["Colour Settings"], current_font):
                print("Colour setting selected")

            if draw_text_button("Back", button_positions["Back"], current_font):
                main_menu_status = "main"

        elif main_menu_status == "text_settings":
            main_menu_status = settings_menu.draw()
        
        elif main_menu_status == "tutorial":
            main_menu_status = draw_tutorial()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                is_game_paused = not is_game_paused

        if event.type == pygame.QUIT:
            running = False

        if not is_game_paused:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[0] < screen_width and mouse_pos[1] < screen_height:
                    is_selected_tower = None
                    clear_selected_range()

                    if is_placeing_tower:
                        if current_level.cash >= con.BUY_TOWER_COST:
                            create_towers(mouse_pos)
                    else:
                        is_selected_tower = selected_tower(mouse_pos)

    # Show pause prompt
    if not is_game_paused:
        draw_text("Press SPACE to pause", current_font, "grey0", screen_width + 10, 500)

    pygame.display.flip()

pygame.quit()
