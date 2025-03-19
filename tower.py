import pygame
import math
import constants as con
from tower_upgrade_data import *


class Towers(pygame.sprite.Sprite):

    def __init__ (self, animation_spritesheets, tile_x, tile_y):

        # Initializes a tower with animation, position, and combat properties
        pygame.sprite.Sprite.__init__(self)

        self.upgrade_level= 1
        self.range = TOWER_GUN_DATA[self.upgrade_level- 1].get("range")
        self.cooldown = TOWER_GUN_DATA[self.upgrade_level- 1].get("cooldown")
        self.last_shot = pygame.time.get_ticks()

        self.selected = False
        self.target= None

        # Coordinates where the towers should be placed
        self.tile_x = tile_x
        self.tile_y = tile_y
  
        self.x = (self.tile_x + 0.5) * con.TILE_SIZE
        self.y = (self.tile_y + 0.5) * con.TILE_SIZE

        # Animation variables
        self.sprite_images = animation_spritesheets # List of spritsheets for animation
        self.animation_list = self.load_images(self.sprite_images[self.upgrade_level- 1])
        self.animation_index = 0
        self.update_png_time = pygame.time.get_ticks()

        # Image and rotation
        self.angle = 90 
        self.original_image= self.animation_list[self.animation_index]
        self.image = pygame.transform.rotate(self.original_image, self.angle)       
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # Range indicator
        self.range_image = pygame.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.range_image, "gray100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center



    def load_images(self, animation_sheet):

        # Loads animation frames from the sprite sheet
        image_size = animation_sheet.get_height()
        animation_list = []
        for x in range(con.ANIMATION_STEPS):
            temp_img = animation_sheet.subsurface(x * image_size, 0, image_size, image_size)
            animation_list.append(temp_img)
        return animation_list



    def update(self, enemy_group, level):
        if self.target:
            self.play_animation()
        elif pygame.time.get_ticks() - self.last_shot > (self.cooldown / level.game_speed):
                self.select_target(enemy_group)


    def select_target(self, enemy_group):

        # Select the nearest enemy within range as a target
        x_dist = 0 
        y_dist = 0

        # Check if in range
        for enemy in enemy_group:
            if enemy.health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range:
                    self.target= enemy
                    self.angle = math.degrees(math.atan2(-y_dist, x_dist))

                    # Damege to ememy
                    self.target.health -= con.TOWER_DAMAGE


    def play_animation(self):

        # Handles animation frame switching and shooting
        self.original_image= self.animation_list[self.animation_index]
        if pygame.time.get_ticks() - self.update_png_time > con.ANIMATION_DELAY:
            self.update_png_time = pygame.time.get_ticks()
            self.animation_index += 1
            if self.animation_index >= len(self.animation_list):
                self.animation_index = 0
                self.last_shot = pygame.time.get_ticks()
                self.target= None


    def tower_upgrade(self):
        
        # Upgrades the tower's level and animation sprites
        self.upgrade_level += 1
        self.range = TOWER_GUN_DATA[self.upgrade_level - 1].get("range")
        self.cooldown = TOWER_GUN_DATA[self.upgrade_level - 1].get("cooldown")
        self.animation_list = self.load_images(self.sprite_images[self.upgrade_level - 1])
        self.original_image= self.animation_list[self.animation_index]

        # Range of circle when upgraded
        self.range_image = pygame.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.range_image, "gray100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center


    def draw(self,surface):

        # Draws the towers and range when selected
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)       
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.range_image, self.range_rect)
