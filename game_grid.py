import lib.stddraw as stddraw  # used for displaying the game grid
from lib.color import Color  # used for coloring the game grid
from point import Point  # used for tile positions
import numpy as np  # fundamental Python module for scientific computing
from tile import Tile


# A class for modeling the game grid
def get_next_display_dict(grid_width):
    pass


class GameGrid:
    # A constructor for creating the game grid based on the given arguments
    def __init__(self, grid_h, grid_w, info_w, next_tetromino=None):
        # set the dimensions of the game grid as the given arguments
        self.grid_height = grid_h
        self.grid_width = grid_w
        self.info_width = info_w

        # create a tile matrix to store the tiles locked on the game grid
        self.tile_matrix = np.full((grid_h, grid_w), None)
        # create the tetromino that is currently being moved on the game grid
        self.current_tetromino = None
        # create the tetromino that will enter the game grid next
        self.next_tetromino = next_tetromino
        # the game_over flag shows whether the game is over or not
        self.game_over = False
        # set the color used for the empty grid cells
        self.empty_cell_color = Color(206, 195, 181)
        # set the colors used for the grid lines and the grid boundaries
        self.line_color = Color(185, 171, 158)
        self.boundary_color = Color(132, 122, 113)
        # thickness values used for the grid lines and the grid boundaries
        self.line_thickness = 0.002
        self.box_thickness = 10 * self.line_thickness
        self.info_line_thickness = 2 * self.line_thickness
        # the score of the game starts from 0
        self.score = 0

    # A method for displaying the game grid
    def display(self):
        # clear the background to empty_cell_color
        stddraw.clear(self.empty_cell_color)
        # draw the game grid
        self.draw_grid()
        # draw the current/active tetromino if it is not None
        # (the case when the game grid is updated)
        if self.current_tetromino is not None:
            self.current_tetromino.draw()
        # draw a box around the game grid
        self.draw_boundaries()
        # show the resulting drawing with a pause duration = 250 ms
        stddraw.show(250)
        self.score = Tile.merge_tiles(self.tile_matrix, self.score)
        # draw the score and the next tetromino
        self.draw_info()
        # draw a box around the game grid
        self.draw_boundaries()

    # A method for drawing the cells and the lines of the game grid
    def draw_grid(self):
        # for each cell of the game grid
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                # if the current grid cell is occupied by a tile
                if self.tile_matrix[row][col] is not None:
                    # draw this tile
                    self.tile_matrix[row][col].draw(Point(col, row))
        # draw the inner lines of the game grid
        stddraw.setPenColor(self.line_color)
        stddraw.setPenRadius(self.line_thickness)
        # x and y ranges for the game grid
        start_x, end_x = -0.5, self.grid_width - 0.5
        start_y, end_y = -0.5, self.grid_height - 0.5
        for x in np.arange(start_x + 1, end_x, 1):  # vertical inner lines
            stddraw.line(x, start_y, x, end_y)
        for y in np.arange(start_y + 1, end_y, 1):  # horizontal inner lines
            stddraw.line(start_x, y, end_x, y)
        stddraw.setPenRadius()  # reset the pen radius to its default value

    def draw_info(self, cp=None):
        # info grid settings
        stddraw.setPenColor(Color(167, 160, 151))
        stddraw.filledRectangle(self.grid_width - 0.5, -0.5, self.info_width, self.grid_height)
        info_center_x_scale = (self.grid_width + self.info_width / 2) - 0.5
        info_score_y_scale = (self.grid_height - 2)
        # draw the score
        stddraw.setPenColor(Color(255, 255, 255))
        stddraw.setFontFamily("Arial")
        stddraw.setFontSize(25)
        stddraw.boldText(info_center_x_scale, info_score_y_scale, "Score")
        stddraw.boldText(info_center_x_scale, info_score_y_scale - 0.75, str(self.score))
        # draw the next tetromino
        stddraw.boldText(info_center_x_scale, 5, "Next")
        if self.next_tetromino is not None:
            next_display = cp.deepcopy(self.next_tetromino)
            next_display.bottom_left_cell = Point()
            tile_next_display = get_next_display_dict(self.grid_width)
            next_display.bottom_left_cell.x = tile_next_display[next_display.type]['x']
            next_display.bottom_left_cell.y = tile_next_display[next_display.type]['y']
            next_display.draw()
   
    # A method for drawing the boundaries around the game grid
    def draw_boundaries(self):
        # draw a bounding box around the game grid as a rectangle
        stddraw.setPenColor(self.boundary_color)  # using boundary_color
        # set the pen radius as box_thickness (half of this thickness is visible
        # for the bounding box as its lines lie on the boundaries of the canvas)
        stddraw.setPenRadius(self.box_thickness)
        # the coordinates of the bottom left corner of the game grid
        pos_x, pos_y = -0.5, -0.5
        stddraw.rectangle(pos_x, pos_y, self.grid_width, self.grid_height)
        stddraw.setPenRadius()  # reset the pen radius to its default value

    # A method used checking whether the grid cell with the given row and column
    # indexes is occupied by a tile or not (i.e., empty)
    def is_occupied(self, row, col):
        # considering the newly entered tetrominoes to the game grid that may
        # have tiles with position.y >= grid_height
        if not self.is_inside(row, col):
            return False  # the cell is not occupied as it is outside the grid
        # the cell is occupied by a tile if it is not None
        return self.tile_matrix[row][col] is not None

    # A method for checking whether the cell with the given row and col indexes
    # is inside the game grid or not
    def is_inside(self, row, col):
        if row < 0 or row >= self.grid_height:
            return False
        if col < 0 or col >= self.grid_width:
            return False
        return True

    # A method that locks the tiles of a landed tetromino on the grid checking
    # if the game is over due to having any tile above the topmost grid row.
    # (This method returns True when the game is over and False otherwise.)
    def update_grid(self, tiles_to_lock, blc_position):
        # necessary for the display method to stop displaying the tetromino
        self.current_tetromino = None
        # lock the tiles of the current tetromino (tiles_to_lock) on the grid
        n_rows, n_cols = len(tiles_to_lock), len(tiles_to_lock[0])
        for col in range(n_cols):
            for row in range(n_rows):
                # place each tile (occupied cell) onto the game grid
                if tiles_to_lock[row][col] is not None:
                    # compute the position of the tile on the game grid
                    pos = Point()
                    pos.x = blc_position.x + col
                    pos.y = blc_position.y + (n_rows - 1) - row
                    if self.is_inside(pos.y, pos.x):
                        self.tile_matrix[pos.y][pos.x] = tiles_to_lock[row][col]
                    # the game is over if any placed tile is above the game grid
                    else:
                        self.game_over = True
        # return the value of the game_over flag
        return self.game_over





    def remove_full_lines(self):
        # Identify full rows
        full_rows = np.all(self.tile_matrix != None, axis=1)
        full_indices = np.where(full_rows)[0]  # Get indices of full rows

        # Check if any full lines are detected
        if len(full_indices) > 0:
            # Create a new grid excluding full rows
            non_full_rows = self.tile_matrix[~full_rows]

            # Calculate number of new empty rows to add at the top
            num_new_rows = self.grid_height - non_full_rows.shape[0]

            # Create new empty rows
            new_rows = np.full((num_new_rows, self.grid_width), None)

            # Combine new empty rows with the non-full rows to form the updated grid
            self.tile_matrix = np.vstack((non_full_rows, new_rows))

            # Shift down tiles above the cleared lines
            for i in range(full_indices[0] - 1, -1, -1):
                for j in range(self.grid_width):
                    if self.tile_matrix[i, j] is not None:
                        self.tile_matrix[i + num_new_rows, j] = self.tile_matrix[i, j]
                        self.tile_matrix[i, j] = None

        return len(full_indices)  # Return the number of lines cleared