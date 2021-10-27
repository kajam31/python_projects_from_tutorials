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
    def make_barrier(self):
        self.color = BLACK
    def make_end(self):
        self.color = TURQUOISE
    def make_start(self):
        self.color = ORANGE
    def make_path(self):
        self.color= PURPLE
    
    def draw(self, win):
        pg.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        
    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): #down
            self.neighbors.append(grid[self.row + 1][self.col])
            
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): #up
            self.neighbors.append(grid[self.row - 1][self.col]) #it's self.row -1 to check above you because you start the count in the upper left corner
            
        if self.col < self.total_rows - 1 and not grid[self.row ][self.col +1].is_barrier(): #right
            self.neighbors.append(grid[self.row][self.col + 1])
            
        if self.col > 0 and not grid[self.row][self.col-1].is_barrier(): #left
            self.neighbors.append(grid[self.row][self.col -1 ])
    
    def __lt__(self, other):
        return False 
    
# we wil be using manhatten distance, this doesn't calculate the diagonal distance between to points
# it will add the y2-y1 and x2-x1   
def h(p1, p2):
    x1,y1 = p1
    x2,y2 = p2
    return abs(x1-x2) + abs(y1-y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start)) #the 0 is here the f_score
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row} #current shortest distance from start to end
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos()) #h() => calculated the haristic (oproqimate/estimate distance)
    # also maks it so then when you reach the end node it doesn't automaticaly think that it is the best score
    
    open_set_hash = {start}
    
    while not open_set.empty(): #if it is empty it means that we have considered every possible path and didn't find any path
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
        current = open_set.get()[2] #means we are looking at the node that has the lowest current f_score
        open_set_hash.remove(current)
        
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True # make path
        for neighbor in current.neighbors: #makes it so it won't consider 1 note twice (if it notices that all the neigbors are worse than this one it will end)
            temp_g_score = g_score[current] +1 #this is the part that looks if the neighbor is closer to the target or further
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(),end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
                    #this makes it so that the node that has a better path/ is closer to the end is now an open element => 
                    # it is now green and will be considered next time when we are looking at the nodes to find better neigbors
        draw()
        if current != start:
            current.make_closed()
            
    return False
            
    
    
    
    
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
                if event.key == pg.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                            
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    
                    
                if event.key == pg.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)           
    pg.quit()
    
    
main(WIN, WIDTH)
    
    
    
    
    
    
    
    
    
    