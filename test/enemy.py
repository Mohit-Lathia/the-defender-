# enemy.py

class Enemy:
    """
    Represents an enemy moving along a predefined path.
    """
    def __init__(self, path):
        """
        Initializes the enemy with a path.

        Args:
            path (list of tuple): The list of coordinates the enemy follows.
        """
        self.path = path
        self.current_index = 0
        self.position = self.path[self.current_index]

    def move(self):
        """
        Moves the enemy to the next position along the path.
        """
        if self.current_index < len(self.path) - 1:
            self.current_index += 1
            self.position = self.path[self.current_index]

    def is_at_end(self):
        """
        Checks if the enemy has reached the end of the path.

        Returns:
            bool: True if the enemy is at the end of the path, False otherwise.
        """
        return self.current_index == len(self.path) - 1
