import pygame

class levels:
    def __init__(self, layout, tile_size, tile_image):
        self.layout = layout #list that repsents the grid  
        self.tile_size = tile_size #size of each tile
        self.tile_image = tile_image #a dictionary of tile images
        self.waypoints = [] #genrates waypoints

    #generates list of waypoints based on the grid 
    def generate_waypoints(self): 
        self.waypoints = []
        for row_index, row in enumerate(self.layout):
            for col_index, tile in enumerate(row):
                if tile == 2:  # Start tile
                    x = col_index * self.tile_size + self.tile_size // 2
                    y = row_index * self.tile_size + self.tile_size // 2
                    self.waypoints.append((x, y))
                if tile == 1:  # Path tile
                    x = col_index * self.tile_size + self.tile_size // 2
                    y = row_index * self.tile_size + self.tile_size // 2
                    self.waypoints.append((x, y))
                if tile == 3:  # End tile
                    x = col_index * self.tile_size + self.tile_size // 2
                    y = row_index * self.tile_size + self.tile_size // 2
                    self.waypoints.append((x, y))

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
        

    