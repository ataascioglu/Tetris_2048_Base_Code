################################################################################
#                                                                              #
# The main program of Tetris 2048 Base Code                                    #
#                                                                              #
################################################################################

import lib.stddraw as stddraw  # for creating an animation with user interactions
from lib.picture import Picture  # used for displaying an image on the game menu
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid  # the class for modeling the game grid
from tetromino import Tetromino  # the class for modeling the tetrominoes
import random  # used for creating tetrominoes with random types (shapes)
from point import Point  # used for the positions of the tetrominoes


# The main function where this program starts execution
def start():
    # set the dimensions of the game grid
    grid_h, grid_w = 20, 12
    # set the size of the drawing canvas (the displayed window)
    canvas_h, canvas_w = 40 * grid_h, 60 * grid_w
    stddraw.setCanvasSize(canvas_w, canvas_h)
    # set the scale of the coordinate system for the drawing canvas
    stddraw.setXscale(-0.5, grid_w + 3.5)
    stddraw.setYscale(-0.5, grid_h - 0.5)

    # set the game grid dimension values stored and used in the Tetromino class
    Tetromino.grid_height = grid_h
    Tetromino.grid_width = grid_w
    # create the game grid
    grid = GameGrid(grid_h, grid_w)
    current_tetromino = create_tetromino()
    grid.current_tetromino = current_tetromino
    next_tetromino = create_tetromino()
    highest_number = None
    # display a simple menu before opening the game
    # by using the display_game_menu function defined below
    speed = display_game_menu(grid_h, grid_w + 4)

    # the main game loop
    while True:
        # check for any user interaction via the keyboard
        if stddraw.hasNextKeyTyped():  # check if the user has pressed a key
            key_typed = stddraw.nextKeyTyped()  # the most recently pressed key
            # if the left arrow key has been pressed
            if key_typed == "left":
                # move the active tetromino left by one
                current_tetromino.move(key_typed, grid)
            # if the right arrow key has been pressed
            elif key_typed == "right":
                # move the active tetromino right by one
                current_tetromino.move(key_typed, grid)
            # if the down arrow key has been pressed
            elif key_typed == "down":
                # move the active tetromino down by one
                # (soft drop: causes the tetromino to fall down faster)
                current_tetromino.move(key_typed, grid)
            # clear the queue of the pressed keys for a smoother interaction

            elif key_typed == "up":
                current_tetromino.rotate_cw(grid)

            elif key_typed == "z":
                current_tetromino.rotate_ccw(grid)

            elif key_typed == "space":
                current_tetromino.hard_drop(grid)

            elif key_typed == "p":
                display_pause_menu(grid_h, grid_w + 4, grid.score, highest_number)

            elif key_typed == "q":
                break

            stddraw.clearKeysTyped()

        # move the active tetromino down by one at each iteration (auto fall)
        success = current_tetromino.move("down", grid)
        # lock the active tetromino onto the grid when it cannot go down anymore
        if not success:
            # get the tile matrix of the tetromino without empty rows and columns
            # and the position of the bottom left cell in this matrix
            tiles, pos = current_tetromino.get_min_bounded_tile_matrix(True)
            # update the game grid by locking the tiles of the landed tetromino
            game_over = grid.update_grid(tiles, pos)
            # end the main game loop if the game is over

            grid.remove_full_rows()

            if game_over:
                speed = display_game_menu(grid_h, grid_w + 4, grid.score, highest_number)
                grid.reset()
                grid = GameGrid(grid_h, grid_w)
                current_tetromino = create_tetromino()
                grid.current_tetromino = current_tetromino

            # create the next tetromino to enter the game grid
            # by using the create_tetromino function defined below
            current_tetromino = next_tetromino
            grid.current_tetromino = current_tetromino
            next_tetromino = create_tetromino()
            highest_number = current_tetromino.get_highest_number()

        # display the game grid with the current tetromino
        grid.display(next_tetromino)

        stddraw.show(speed)

    # print a message on the console when the game is over
    print("Game over")


# A function for creating random shaped tetrominoes to enter the game grid
def create_tetromino():
    # the type (shape) of the tetromino is determined randomly
    tetromino_types = ['I', 'O', 'Z', 'S', 'T', 'J', 'L']
    random_index = random.randint(0, len(tetromino_types) - 1)
    random_type = tetromino_types[random_index]
    # create and return the tetromino
    tetromino = Tetromino(random_type)
    return tetromino


# A function for displaying a simple menu before starting the game
def display_game_menu(grid_height, grid_width, score=None, highest_number=None):
    # the colors used for the menu
    background_color = Color(42, 69, 99)
    button_color = Color(25, 255, 228)
    text_color = Color(31, 160, 239)
    # clear the background drawing canvas to background_color
    stddraw.clear(background_color)
    # get the directory in which this python code file is placed
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # compute the path of the image file
    img_file = current_dir + "/images/menu_image.png"
    # the coordinates to display the image centered horizontally
    img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
    # the image is modeled by using the Picture class
    image_to_display = Picture(img_file)
    # add the image to the drawing canvas
    stddraw.picture(image_to_display, img_center_x, img_center_y)
    # the dimensions for the start game button
    button_w, button_h = grid_width - 1.5, 2
    # the coordinates of the bottom left corner for the start game button
    button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
    # add the start game button as a filled rectangle
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
    # add the text on the start game button
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(25)
    stddraw.setPenColor(text_color)
    text_to_display = "Click Here to Start the Game"
    stddraw.text(img_center_x, 5, text_to_display)

    if score is not None:
        stddraw.setFontFamily("Arial")
        stddraw.setFontSize(20)
        stddraw.setPenColor(text_color)
        score_text = "Your Score: " + str(score)
        stddraw.text(img_center_x, 7, score_text)

    if highest_number is not None:
        if highest_number >= 2048:
            stddraw.setFontFamily("Arial")
            stddraw.setFontSize(20)
            stddraw.setPenColor(text_color)
            highest_number_text = "Congratulations! You reached 2048!"
            stddraw.text(img_center_x, 8, highest_number_text)

        else:
            stddraw.setFontFamily("Arial")
            stddraw.setFontSize(20)
            stddraw.setPenColor(text_color)
            highest_number_text = "You Lost :("
            stddraw.text(img_center_x, 8, highest_number_text)

    # the user interaction loop for the simple menu
    while True:
        # display the menu and wait for a short time (50 ms)
        stddraw.show(50)
        # check if the mouse has been left-clicked on the start game button
        if stddraw.mousePressed():
            # get the coordinates of the most recent location at which the mouse
            # has been left-clicked
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            # check if these coordinates are inside the button
            if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
                if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
                    speed = display_controls_menu(grid_height, grid_width)
                    return speed


def display_pause_menu(grid_height, grid_width, score=None):
    # the colors used for the menu
    background_color = Color(42, 69, 99)
    button_color = Color(25, 255, 228)
    text_color = Color(31, 160, 239)
    # clear the background drawing canvas to background_color
    stddraw.clear(background_color)
    # get the directory in which this python code file is placed
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # compute the path of the image file
    img_file = current_dir + "/images/menu_image.png"
    # the coordinates to display the image centered horizontally
    img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
    # the image is modeled by using the Picture class
    image_to_display = Picture(img_file)
    # add the image to the drawing canvas
    stddraw.picture(image_to_display, img_center_x, img_center_y)
    # the dimensions for the start game button
    button_w, button_h = grid_width - 1.5, 2
    # the coordinates of the bottom left corner for the start game button
    button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
    # add the start game button as a filled rectangle
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
    # add the text on the start game button
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(25)
    stddraw.setPenColor(text_color)
    text_to_display = "Click Here to Resume the Game"
    stddraw.text(img_center_x, 5, text_to_display)

    if score is not None:
        stddraw.setFontFamily("Arial")
        stddraw.setFontSize(20)
        stddraw.setPenColor(text_color)
        score_text = "Your Score: " + str(score)
        stddraw.text(img_center_x, 7, score_text)

    while True:
        # display the menu and wait for a short time (50 ms)
        stddraw.show(50)
        # check if the mouse has been left-clicked on the start game button
        if stddraw.mousePressed():
            # get the coordinates of the most recent location at which the mouse
            # has been left-clicked
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            # check if these coordinates are inside the button
            if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
                if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
                    break  # break the loop to end the method and start the game


def display_difficulty_menu(grid_height, grid_width):
    # the colors used for the menu
    background_color = Color(42, 69, 99)
    button_color = Color(25, 255, 228)
    text_color = Color(31, 160, 239)
    # clear the background drawing canvas to background_color
    stddraw.clear(background_color)
    # the dimensions for the difficulty buttons
    button_w, button_h = grid_width - 1.5, 2
    # the coordinates of the bottom left corner for the difficulty buttons
    button_blc_x = (grid_width - 1) / 2 - button_w / 2
    button_blc_y = [grid_height - 10, grid_height - 14, grid_height - 18]  # for easy, medium, hard
    # add the difficulty buttons as filled rectangles
    stddraw.setPenColor(button_color)
    for y in button_blc_y:
        stddraw.filledRectangle(button_blc_x, y, button_w, button_h)
    # add the text on the difficulty buttons
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(25)
    stddraw.setPenColor(text_color)
    difficulties = ["Easy", "Medium", "Hard"]
    for i, difficulty in enumerate(difficulties):
        stddraw.text((grid_width - 1) / 2, button_blc_y[i] + 1, difficulty)
    # the user interaction loop for the difficulty menu
    while True:
        # display the menu and wait for a short time (50 ms)
        stddraw.show(50)
        # check if the mouse has been left-clicked on any difficulty button
        if stddraw.mousePressed():
            # get the coordinates of the most recent location at which the mouse
            # has been left-clicked
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            # check if these coordinates are inside any button
            for i, y in enumerate(button_blc_y):
                if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
                    if mouse_y >= y and mouse_y <= y + button_h:
                        if difficulties[i] == "Easy":
                            speed = 1000
                        elif difficulties[i] == "Medium":
                            speed = 500
                        else:
                            speed = 150
                        return speed


def display_controls_menu(grid_height, grid_width):
    # the colors used for the menu
    background_color = Color(42, 69, 99)
    button_color = Color(25, 255, 228)
    text_color = Color(31, 160, 239)
    # clear the background drawing canvas to background_color
    stddraw.clear(background_color)
    # the dimensions for the controls info box
    box_w, box_h = grid_width - 1.5, 10
    # the coordinates of the bottom left corner for the controls info box
    box_blc_x = (grid_width - 1) / 2 - box_w / 2
    box_blc_y = (grid_height - 1) / 2 - box_h / 2
    # add the controls info box as a filled rectangle
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(box_blc_x, box_blc_y, box_w, box_h)
    # add the text on the controls info box
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(20)
    stddraw.setPenColor(text_color)
    controls_info = ["Controls:", "Left Arrow: Move Left", "Right Arrow: Move Right",
                     "Down Arrow: Soft Drop", "Up Arrow: Rotate Clockwise",
                     "Z: Rotate Counter-Clockwise", "Space: Hard Drop",
                     "P: Pause Game", "Q: Quit Game"]
    for i, info in enumerate(controls_info):
        stddraw.text((grid_width - 1) / 2, box_blc_y + box_h - 1 - i, info)
    # the user interaction loop for the controls menu

    # the dimensions for the choose difficulty button
    button_w, button_h = grid_width - 1.5, 2
    # the coordinates of the bottom left corner for the choose difficulty button
    button_blc_x, button_blc_y = (grid_width - 1) / 2 - button_w / 2, 2
    # add the choose difficulty button as a filled rectangle
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
    # add the text on the choose difficulty button
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(25)
    stddraw.setPenColor(text_color)
    text_to_display = "Choose Difficulty"
    stddraw.text((grid_width - 1) / 2, 3, text_to_display)

    while True:
        # display the menu and wait for a short time (50 ms)
        stddraw.show(50)
        # check if the mouse has been left-clicked anywhere
        if stddraw.mousePressed():
            speed = display_difficulty_menu(grid_height, grid_width)
            return speed


# start() function is specified as the entry point (main function) from which
# the program starts execution
if __name__ == '__main__':
    start()