# this section was refenced form coding with russ (not all)
import pygame
from pygame.math import Vector2
import math

class Enemy(pygame.sprite.Sprite):

    def __init__(self, waypoints, image):
        pygame.sprite.Sprite.__init__(self)
        self.waypoints = waypoints #uses the wapoints list 
        print(waypoints)
        self.pos = Vector2(self.waypoints[0]) #changing the start point of enemy
        self.target_waypoint = 1 #seting a taget wapoint
        self.speed = 2 #set speed of enemy
        self.angle = 0 #sets angale of image
        self.original_image = image #stores original image
        self.image = pygame.transform.rotate(self.original_image, self.angle) #updates the origianl image  
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self):
        self.move()
        self.rotation()

    def move(self):
        self.target = Vector2(self.waypoints[self.target_waypoint])#seting target waypoint
        direction = self.target - self.pos #calculates the distance of vector

        if direction.length() < 2: #checks if the enemy is close to a target waypoint
            self.target_waypoint += 1

            if self.target_waypoint >= len(self.waypoints): #if all waypoints are meet, kill sprit
                self.kill()
                return #kills the sprite if reach end
        
        if direction.length() > 0: #normalize and move the enemys is dirction of vector is not 0 

            direction = direction.normalize() #normalises the direction and moves the enemy
            self.pos += direction * self.speed
        
        self.rect.center = self.pos #updates the sprite's position

    def rotation(self):
        direction = self.target - self.pos #clalulate distnace to next waypoint
        angle = math.degrees(math.atan2(-direction.y, direction.x))  #use distance to calculate the angle
        self.image = pygame.transform.rotate(self.original_image, angle) #rotates the image
        self.rect = self.image.get_rect(center=self.rect.center) #updates the rectangel so the sprites is centered
        self.rect.center = self.pos