# pathfinder.py

def find_path(grid):
    """
    Finds the path in the grid.

    Args:
        grid (list of list of int): The grid layout.

    Returns:
        list of tuple: A list of coordinates representing the path.
    """
    path = []
    for row_index, row in enumerate(grid):
        for col_index, tile in enumerate(row):
            if tile in [1, 2, 3]:  # Include path, start, and end points
                path.append((row_index, col_index))
    return path
