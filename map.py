import random
import numpy
from enemy_data import *
import constants as con

class Level:
    def __init__(self, layout, tile_size, tile_image):

        # Initializes a level with given pramiters 
        self.round = 1
        self.game_speed = 1
        self.health = con.PLAYER_HEALTH
        self.cash = con.CASH
        self.enemy_list = []
        self.spawned_enemies = 0 
        self.killed_enemies = 0
        self.missed_enemies = 0

        self.layout = layout # List the grid strucher of level
        self.tile_size = tile_size # Size of each tiles
        self.tile_image = tile_image # A dictionaty maping tiles to their images 
        self.unordered_waypoints = []
        self.ordered_waypoints = []


    def generate_waypoints(self): 

        # Generates waypoints based on the grid layout
        self.unordered_waypoints = []
        self.start_waypoint = 0
        self.end_waypoint = 0
        
        for row_index, row in enumerate(self.layout):
            for col_index, tile in enumerate(row):
                if tile == 1:  # Path tile
                    x = col_index * self.tile_size + self.tile_size // 2
                    y = row_index * self.tile_size + self.tile_size // 2
                    self.unordered_waypoints.append((x, y))

                if tile == 2:  # Start tile
                    x = col_index * self.tile_size + self.tile_size // 2
                    y = row_index * self.tile_size + self.tile_size // 2
                    self.start_waypoint_waypoint = (x, y)

                if tile == 3:  # End tile
                    x = col_index * self.tile_size + self.tile_size // 2
                    y = row_index * self.tile_size + self.tile_size // 2
                    self.end_waypoint_waypoint = (x, y)
        
        self.order_waypoints()


    def order_waypoints(self):

        # Oreders waypoints start to end based on prximity
        current_waypoint = self.start_waypoint_waypoint
        remaining_waypoints = self.unordered_waypoints
        self.ordered_waypoints = [self.start_waypoint_waypoint]

        while len(remaining_waypoints) > 0:
            closest_waypoint_index = 0
            closest_waypoint_distance = 100000

            for waypoint_index, waypoint in enumerate(remaining_waypoints):
                waypoint_distance = numpy.sqrt((current_waypoint[0] - waypoint[0]) ** 2 + (current_waypoint[1] - waypoint[1]) ** 2)

                if waypoint_distance < closest_waypoint_distance:
                    closest_waypoint_index = waypoint_index
                    closest_waypoint_distance = waypoint_distance

            self.ordered_waypoints.append(remaining_waypoints[closest_waypoint_index])
            current_waypoint = remaining_waypoints[closest_waypoint_index]

            del remaining_waypoints[closest_waypoint_index]
        self.ordered_waypoints.append(self.end_waypoint_waypoint)


    def process_enemies(self):

        # Processs and randomizes the list of enemies to be spawnd for the current round
        enemies = ENEMY_SPAWN_DATA[self.round - 1]
        for enemy_type in enemies:
            enemies_to_spawn = enemies[enemy_type]
            for enemy in range(enemies_to_spawn):
                self.enemy_list.append(enemy_type)
                
        random.shuffle(self.enemy_list) 


    def check_if_level_complete(self):
        if (self.killed_enemies + self.missed_enemies) == len(self.enemy_list):
            return True


    def rest_level(self):

        #
        self.enemy_list = []
        self.spawned_enemies = 0 
        self.killed_enemies = 0
        self.missed_enemies = 0

    def draw(self, screen):

        # Draws the grid using the provide tile images
        for row_index, row in enumerate(self.layout):
            for col_index, tile in enumerate(row):
                x = col_index * self.tile_size
                y = row_index * self.tile_size

                tile_image = self.tile_image.get(tile, None)
                if tile_image:
                    screen.blit(tile_image, (x, y))

