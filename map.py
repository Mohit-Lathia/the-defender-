import pygame
import numpy

class levels:
    def __init__(self, layout, tile_size, tile_image):
        self.layout = layout #list that repsents the grid  
        self.tile_size = tile_size #size of each tile
        self.tile_image = tile_image #a dictionary of tile images
        self.unordered_waypoints = [] #genrates waypoints
        self.ordered_waypoints = []

    #generates list of waypoints based on the grid 
    def generate_waypoints(self): 
        self.unordered_waypoints = []
        self.start = 0
        self.end = 0
        
        for row_index, row in enumerate(self.layout):
            for col_index, tile in enumerate(row):
                if tile == 1:  # Path tile
                    x = col_index * self.tile_size + self.tile_size // 2
                    y = row_index * self.tile_size + self.tile_size // 2
                    self.unordered_waypoints.append((x, y))

                if tile == 2:  # Start tile
                    x = col_index * self.tile_size + self.tile_size // 2
                    y = row_index * self.tile_size + self.tile_size // 2
                    self.start_waypoint = (x, y)

                if tile == 3:  # End tile
                    x = col_index * self.tile_size + self.tile_size // 2
                    y = row_index * self.tile_size + self.tile_size // 2
                    self.end_waypoint = (x, y)
        
        self.order_waypoints()
        

    def order_waypoints(self):
        
        current_waypoint = self.start_waypoint
        remaining_waypoints = self.unordered_waypoints
        self.ordered_waypoints = [self.start_waypoint]

        while len(remaining_waypoints) > 0:
            print(f"cw: {current_waypoint}\n rw: {remaining_waypoints}\n ow: {self.ordered_waypoints}")

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

        self.ordered_waypoints.append(self.end_waypoint)


    #draws the grid using the provided tile images
    def draw(self, screen):
        for row_index, row in enumerate(self.layout):
            for col_index, tile in enumerate(row):
                x = col_index * self.tile_size
                y = row_index * self.tile_size

                tile_image = self.tile_image.get(tile, None)
                if tile_image:
                    screen.blit(tile_image, (x, y))


class level_manager:
    def __init__(self, tile_size): #manages levels and allows to switch between then
        self.levels = [] #stores the levels 
        self.tile_size = tile_size
        
    def add_level(self, layout, tile_image): #adds levels to the game 
        new_level = levels(layout, self.tile_size, tile_image)
        self.levels.append(new_level)

    def get_level(self, index): #gets specific level by itd index
        
        if 0 <= index < len(self.levels):
            return self.levels[index]
        else:
            raise IndexError("level is not aviable")
        

    