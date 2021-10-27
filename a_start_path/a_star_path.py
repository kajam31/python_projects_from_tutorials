import pygame as pg
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pg.display.set_mode((WIDTH, WIDTH))
pg.display.set_caption("A* path finding algoritm")


# colors #
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


# Spot = Node #
class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        # because we are visualising this using a grid with squares of a certain 
        #  the position isn't the normal one but the position times the with of each node/square
        self.x = row*width
        self.y = col*width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col
    
    # have we already looked at you?
    # we will be using the colors instead of normal state values
    def is_close(self):
        return self.color == RED
    def is_open(self):
        return self.color == GREEN
    def is_barrier(self):
        return self.color == BLACK
    def is_start(self):
        return self.color == ORANGE
    def is_end(self):
        return self.color == TURQUOISE
    def reset (self):
        self.color = WHITE
        
    def make_closed(self):
        self.color = RED
    def make_open(self):
        self.color = GREEN
    def make_barrier (self):
        self.color = BLACK
    def make_end(self):
        self.color = TURQUOISE
    def make_start(self):
        self.color = ORANGE
    def make_path(self):
        self.color= PURPLE
    
    def draw(self, win):
        pg.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        
    def update_neighbors (self, grid):
        pass
    
    def __lt__(self, other):
        return False 
    
# we wil be using manhatten distance, this doesn't calculate the diagonal distance between to points
# it will add the y2-y1 and x2-x1   
def h(p1, p2):
    x1,y1 = p1
    x2,y2 = p2
    return abs(x1-x2) + abs(y1-y2)

def make_grid(rows, width):
    grid = []
    GAP = width // rows #this is the width of each cube
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i,j,GAP,rows)
            grid[i].append(spot)
    return grid

def draw_grid(win, rows, width):
    GAP = width // rows
    
    for i in range(rows):
        pg.draw.line(win, GREY, (0,i*GAP),(width, i*GAP))
        
    ## not sure if this has to be in the loop
        for j in range(rows):
            pg.draw.line(win, GREY, (j*GAP, 0),(j*GAP, width))
            
            
def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    # loops trough all the places in the grid and makes it the color that they are supposed to be
    draw_grid(win, rows, width)
    pg.display.update()
    
def get_clicked_pos(pos, rows, width):
    GAP = width // rows
    y,x = pos
    row = y // GAP
    col = x // GAP
    return row, col


def main(win, width):
    ROWS = 50
    grid= make_grid(ROWS, width)
    start = None
    end = None
    
    run = True
    started = False
    
    while run:
        draw(win,grid,ROWS, width)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            # this makes it so that if the algoritm is running you can't do anything else except for pressing quit
            # it is no longer possible to draw anything else
            if started:
                continue
            
            if pg.mouse.get_pressed()[0]:# if left mouse button was pressed
                pos = pg.mouse.get_pos()
                row,col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot != end and spot != start:
                    spot.make_barrier()
                    
           
            elif pg.mouse.get_pressed()[2]: # if right mouse buttton was pressed
                pos = pg.mouse.get_pos()
                row,col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                if spot == end:
                    end = None
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and not started:
                    
                    
                
    pg.quit()
    
    
main(WIN, WIDTH)
    
    
    
    
    
    
    
    
    
    