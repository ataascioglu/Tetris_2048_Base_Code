import lib.stddraw as stddraw  # used for drawing the tiles to display them
from constants import BACKGROUND_COLOR, FOREGROUND_COLOR # used for coloring the tiles
from lib.color import Color  # used for coloring the tiles
import random  # used for randomly choosing the number on the tile


# A class for modeling numbered tiles as in 2048
class Tile:
    # Class variables shared among all Tile objects
    # ---------------------------------------------------------------------------
    # the value of the boundary thickness (for the boxes around the tiles)
    boundary_thickness = 0.004
    # font family and font size used for displaying the tile number
    font_family, font_size = "Arial", 14

    # A constructor that creates a tile with 2 as the number on it
    def __init__(self):
        # set the number on this tile
        self.number = random.choice([2, 4])  # randomly choose 2 or 4
        self.update_color(self.number)

    # A method for drawing this tile at a given position with a given length
    def draw(self, position, length=1):  # length defaults to 1
        # draw the tile as a filled square
        stddraw.setPenColor(self.background_color)
        stddraw.filledSquare(position.x, position.y, length / 2)

        stddraw.setPenColor(Color(128, 128, 128))  # Choose a contrasting color for the border
        # draw the bounding box around the tile as a square
        stddraw.setPenRadius(Tile.boundary_thickness)
        stddraw.square(position.x, position.y, length / 2)
        stddraw.setPenRadius()  # reset the pen radius to its default value
        # draw the number on the tile
        stddraw.setPenColor(self.foreground_color)
        stddraw.setFontFamily(Tile.font_family)
        stddraw.setFontSize(Tile.font_size)
        stddraw.text(position.x, position.y, str(self.number))

        # Method for checking two tiles for merging

    def merge_matches(self, tile):
        # if the number on the tile is equal to the number on the current tile
        if self.number == tile.number and self.number < 2048:
            # set the number on the current tile to the sum of the two numbers
            self.number = self.number * 2
            # increase the score by the value of the number on the current tile
            # Remove the tile and update the color of the current tile
            tile.number = None

            # Update the color of the current tile
            self.update_color(self.number)
            # return True to indicate that the tiles were matched
            return self.number
        # return False to indicate that the tiles were not matched
        else:
            return 0

    # A method for merging two matching tiles
    def merge_tiles(tile_matrix, score):
        rows = len(tile_matrix)
        cols = len(tile_matrix[0])

        for col in range(cols):
            for row in range(rows):
                current_tile = tile_matrix[row][col]

                if current_tile is not None:
                    # Merge with top neighbor if possible
                    if row < rows - 1 and tile_matrix[row + 1][col] is not None and current_tile.number == \
                            tile_matrix[row + 1][col].number:
                        score += current_tile.merge_matches(tile_matrix[row + 1][col])
                        tile_matrix[row + 1][col] = None

                        # Move merged tile down
                        for down_row in range(row + 1, rows):
                            if tile_matrix[down_row][col] is not None:
                                tile_matrix[down_row - 1][col] = tile_matrix[down_row][col]
                                tile_matrix[down_row][col] = None

                    # Check neighboring tiles and move current tile if possible
                    if row > 0:
                        right_empty = row + 1 >= rows or tile_matrix[row + 1][col] is None
                        left_empty = row - 1 < 0 or tile_matrix[row - 1][col] is None
                        up_empty = col + 1 >= cols or tile_matrix[row][col + 1] is None
                        down_empty = col - 1 < 0 or tile_matrix[row][col - 1] is None

                        if right_empty and left_empty and up_empty and down_empty:
                            tile_matrix[row - 1][col] = current_tile
                            tile_matrix[row][col] = None
                            row -= 1

                    row += 1

        return score

    # A method for updating the color of this tile based on the number on it
    def update_color(self, number):
        self.background_color = BACKGROUND_COLOR[number]
        self.foreground_color = FOREGROUND_COLOR[number]