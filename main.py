#some part of the code was inspired by code with russ
import pygame
import constants as con
from enemy import *
from map import *

#initialize Pygame
pygame.init()

#create clock
clock = pygame.time.Clock()

#initialize screen
screen = pygame.display.set_mode((con.SCREEN_WIDTH, con.SCREEN_HEIGHT))
pygame.display.set_caption("The Defender")

#tile size and level resouse
tile_size = 64 #set the size of tiles

#load tile images
grass_tile_1 = pygame.image.load("assets/tiles/towerDefense_tile119.png").convert_alpha()
path_tile_1 = pygame.image.load("assets/tiles/towerDefense_tile158.png").convert_alpha()
start_tile = pygame.image.load("assets/tiles/towerDefense_tile061.png").convert_alpha()
end_tile = pygame.image.load("assets/tiles/towerDefense_tile067.png").convert_alpha()

#define tile image 
tile_image_level_1 = {
    0: grass_tile_1,
    1: path_tile_1,
    2: start_tile,
    3: end_tile,
}

#layout for each level
level_1_layout = [
    [0, 0, 0, 2, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 3, 0, 0, 0, 0],
]

#loads the level
level_manager = level_manager(tile_size)
level_manager.add_level(level_1_layout, tile_image_level_1)
current_level = level_manager.get_level(0) #select the current level (level 0 for now)

#initialize level
current_level = levels(level_1_layout, tile_size, tile_image_level_1)
current_level.generate_waypoints()

#load sprites
enemy_image = pygame.image.load("assets/enemys/enemy_1.png").convert_alpha()
enemy_group = pygame.sprite.Group() #creates a group 
enemy_group = pygame.sprite.Group()
enemy = Enemy(current_level.waypoints, enemy_image)
enemy_group.add(enemy)

#game loop
running = True
while running:
   
    clock.tick(con.FPS)  #set fps for game

    screen.fill("gray100") #fill the screen

    current_level.draw(screen) #draws curent level

    enemy_group.update() #updates the spite
    enemy_group.draw(screen) #creates a immage of enemy 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #update the display
    pygame.display.flip()

pygame.quit()