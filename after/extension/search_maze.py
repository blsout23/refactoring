
import turtle
import time
from playsound import playsound
from multiprocessing import Process

class Maze:
    
    def __init__(self, turt, grid):
        this.steps = 0
        this.turt = turt
        this.grid = grid

    def draw_grid(self, x_pos, y_pos, tile_size):
        ''' draws a grid at x_pos, y_pos with a specific tile_size '''

        # turn off tracer for fast drawing
        window.tracer(False)
        
        colors = { 
            'X':['grey',"black"],
            'S':['grey',"yellow"],
            'E':['grey',"red"],
            'P':['grey',"royalblue"],
            'T':['grey',"light blue"],
            'D':['gainsboro',"gray"],
            '0':['grey',"white"]
        }
        
        # colors.update({'X':['grey','black']})
        
        # move turtle to initial drawing position
        this.turt.up()
        this.turt.goto(x_pos, y_pos)
        this.turt.down()
        
        # go over every cell in the grid
        for row in range(len(this.grid)):
            for col in range(len(this.grid[row])):
                
                # move turtle to the position of the cell in the grid
                this.turt.up()
                this.turt.goto(x_pos + col * tile_size, y_pos -row * tile_size)
                this.turt.down()

                # color cell according to maze
                this.turt.color(colors[grid[row][col]][0],colors[grid[row][col]][1])
                this.turt.stamp()
            
            # turn tracer back on
            window.tracer(True)


    def find_start(self):
        ''' finds the start position (S) in the grid
        returns a tuple of start row and col
        '''

        # go over every cell in the grid
        for row in range(len(this.grid)):
            for col in range(len(this.grid[0])):

                # cell at row, col is 'S' return row and col as a tuple
                if this.grid[row][col] == 'S':
                    return (row, col)
    
    def search_from(grid, row, col):
    ''' recursive function to search the grid for the end (E) '''

        this.steps += 1

        # make sure row and col are valid points on the grid
        if row < 0 or col < 0 or row == len(grid) or col == len(grid[0]):
            # return False if not valid
            return False

        # check that the grid cell at row and col is not obstacle, tried, or deadend
        if grid[row][col] == 'X' or grid[row][col] == 'T' or grid[row][col] == 'D':
            # return False if obstacle, tried, or deadend
            return False

        # If end is found at row, col return True
        if grid[row][col] == 'E':
            return True
        
        # If the cell at row, col is not the start cell, mark the cell as tried (T)
        if grid[row][col] != 'S':
            grid[row][col] = 'T'

        # draw the grid
        draw_grid(grid, turt, x_offset, y_offset, tile_size)

        # pause the program for a short duration, try 0.5 and 0.01 seconds
        time.sleep(0.25)

        # recursively search differnt directions adjacent to current row, col (up, down, left, right)
        found = (search_from(grid, row-1, col)
                or search_from(grid, row+1, col)
                or search_from(grid, row, col-1)
                or search_from(grid, row, col+1)
                )

        # if any of the 4 directions returns True, mark the cel at row, col as part of the path and return True
        if found and grid[row][col] != 'S':
            grid[row][col] = 'P'
            return True
        # else, if the cell at row, col is not the start cell (S), mark it as a deadend
        elif grid[row][col] != 'S':
            grid[row][col] = 'D'


def read_grid(file_name):
    ''' reads a maze file and initializes a gird with its contents '''

    # create an empty grid (an empty list called grid)
    grid = []

    # open the text file
    file = open(file_name)

    # read a line from the file
    line = file.readline()

    # replace \n with nothing
    line = line.replace('\n', '')

    while line:
        # split the line into tokens
        tokens = line.split(',')

        # add the tokens to the grid as a single row
        grid.append(tokens)

        line = file.readline()
        
        # replace \n with nothing
        line = line.replace('\n', '')

    # return the grid
    return grid

    

def background_music():
    ''' plays tetris music in the background '''

    playsound('Tetris.mp3')    


def main():
    ''' reads a maze file and sets the search parameters '''
    turt = turtle.Turtle()
    window = turtle.getscreen()
    window.bgcolor('slate gray')
    turtle.hideturtle()
    turt.hideturtle()
    turt.shape('square')
    turt.shapesize(2.5, 2.5)

    # set offsets and tile size for drawing the grid
    x_offset = -150
    y_offset = 200
    tile_size = 50

    # create an int variable for counting steps
    steps = 0

    # read maze file and create playground grid
    playground = read_grid("maze2.txt")

    # find start position
    row, col = find_start(playground)

    # call the search function, it takes the grid, row, column, and steps
    search_from(playground, row, col)

    # create a list of tuples representing the path
    path = []
    for row in range(len(playground)):
        for col in range(len(playground[0])):
            if playground[row][col] == 'P':
                path.append((row, col))

    # print path length
    print('path length:', len(path))

    # draw the final grid
    draw_grid(playground, turt, x_offset, y_offset, tile_size)
    
    # pause the grid drawing for 4 seconds
    time.sleep(4)

    # print the number of steps taken to find the path
    print("number of steps taken to reach answer:", steps)
    


if __name__ == "__main__":

    p = Process(target=background_music, args=())
    p.start()
    main()
    p.terminate()

