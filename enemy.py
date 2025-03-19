# This section was referenced form Coding with Russ
import pygame
import math
import constants as con
from enemy_data import *
from pygame.math import Vector2


class Enemy(pygame.sprite.Sprite):

    def __init__(self, enemy_type, waypoints, images):

        # Initializes and enemy sprite with aritabuts based on it type
        pygame.sprite.Sprite.__init__(self)
        self.waypoints = waypoints 
        self.pos = Vector2(self.waypoints[0]) # Initial position at the first waypoint
        self.target_waypoint = 1 # Index of the next waypoints

        self.health = ENEMY_DATA.get(enemy_type)["health"]
        self.speed = ENEMY_DATA.get(enemy_type)["speed"]

        self.angle = 0 #sets angle of image
        self.original_image = images.get(enemy_type)
        
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self, level):

        # Updates the enemy's postion, roation, and if alive each frame
        self.move(level)
        self.rotation()
        self.is_alive(level)


    def move(self, level):

        # Moves the enemy towards the next waypoint
        self.target = Vector2(self.waypoints[self.target_waypoint])
        direction = self.target - self.pos 

        if direction.length() < 2: # Close enough to the waypoint
            self.target_waypoint += 1
            if self.target_waypoint >= len(self.waypoints): # If all waypoints are meet, kill sprit
                self.kill()
                level.health -= 1
                level.missed_enemies += 1
        
        if direction.length() > 0:

            direction = direction.normalize()
            self.pos += direction * (self.speed * level.game_speed)
        
        self.rect.center = self.pos

    def rotation(self):

        # Rotates the enemy sprite to the face the direction of the movement
        direction = self.target - self.pos
        angle = math.degrees(math.atan2(-direction.y, direction.x))
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.center = self.pos

    def is_alive(self, level):
        if self.health <= 0:
            level.killed_enemies += 1
            level.cash += con.KILL_POINTS
            self.kill()