import pygame
import time


def find_path(grid):
    path = []
    for row_index, row in enumerate(grid):
        for col_index, tile in enumerate(row):
            if tile in [1, 2, 3]:  # Include path, start, and end
                path.append((row_index, col_index))
    return path

# Get the path
path_coordinates = find_path(grid)
print("Enemy Path:", path_coordinates)


# Enemy class
class Enemy:
    def __init__(self, path):
        self.path = path
        self.current_index = 0
        self.position = self.path[self.current_index]

    def move(self):
        if self.current_index < len(self.path) - 1:
            self.current_index += 1
            self.position = self.path[self.current_index]

# Initialize enemy with the path
enemy = Enemy(path_coordinates)


# Initialize Pygame
pygame.init()

# Constants
TILE_SIZE = 40
SCREEN_WIDTH = TILE_SIZE * len(grid[0])
SCREEN_HEIGHT = TILE_SIZE * len(grid)

# Colors
COLORS = {
    0: (200, 200, 200),  # Empty space
    1: (100, 100, 250),  # Path
    2: (0, 255, 0),      # Start
    3: (255, 0, 0),      # End
}

# Enemy color
ENEMY_COLOR = (255, 255, 0)  # Yellow

# Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Enemy Path Movement")

# Enemy object
enemy = Enemy(path_coordinates)

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the enemy
    enemy.move()

    # Draw the grid
    screen.fill((0, 0, 0))  # Clear the screen
    for row_index, row in enumerate(grid):
        for col_index, tile in enumerate(row):
            color = COLORS[tile]
            rect = pygame.Rect(col_index * TILE_SIZE, row_index * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Grid lines

    # Draw the enemy
    enemy_row, enemy_col = enemy.position
    enemy_rect = pygame.Rect(
        enemy_col * TILE_SIZE + TILE_SIZE // 4,
        enemy_row * TILE_SIZE + TILE_SIZE // 4,
        TILE_SIZE // 2,
        TILE_SIZE // 2
    )
    pygame.draw.ellipse(screen, ENEMY_COLOR, enemy_rect)

    pygame.display.flip()  # Update the screen
    clock.tick(2)  # Control the enemy speed

pygame.quit()
