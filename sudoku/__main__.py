import pygame
import time
from pygame.locals import *

cell_width = 20
cell_height = 20
BACK_COL = (80,80,80)
TEXT_COL = (25,25,112)
DELAY = 0.5

TEST_DATA = [
    [0,5,0,3,0,0,0,6,0],
    [9,2,0,0,0,1,4,5,3],
    [4,0,0,2,5,6,9,0,8],
    [7,0,4,0,9,8,6,2,1],
    [2,0,0,7,0,0,0,8,0],
    [0,0,0,0,0,0,7,9,4],
    [0,6,0,0,0,7,1,3,0],
    [0,4,2,0,1,0,0,0,6],
    [1,0,0,0,0,0,0,0,2],
]

class App(object):
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._size = self.width, self.height = cell_width*9*3, cell_height*9*3
        self._grid = Grid()
        self._time = time.time()
        self._counter = 0
        self._checking = "ROW"
        self._counter_row = -1
        self._counter_col = -1
        self._check_cell_row = 0
        self._check_cell_col = 0
        for row in range(0, 9):
            for col in range(0, 9):
                if TEST_DATA[row][col] != 0:
                    self._grid.set(row, col, TEST_DATA[row][col])
#                    self._grid.check(row, col)
        
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self._size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        #self.font = pygame.font.SysFont('courier.ttf', 72)
        font_name = pygame.font.get_default_font()
        print("System font: {0}".format(font_name))
        self.font_s = pygame.font.SysFont(None, 22)
        self.font_l = pygame.font.SysFont(None, 66)
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
    def on_loop(self, elapsed):
        self._counter+=elapsed
        if self._counter > DELAY:
            self._counter = 0;
            self.check_grid()
    def check_grid(self):
        print(self._check_cell_row, self._check_cell_col)
        finished_check = self.check_cell()
        if finished_check:
            self._check_cell_col+=1
            if self._check_cell_col >= 9:
                self._check_cell_col = 0
                self._check_cell_row+=1
                if self._check_cell_row >= 9:
                    self._check_cell_row = 0
    def check_cell(self):
        if not self._grid.is_complete(self._check_cell_row, self._check_cell_col):
            return True
        # row
        if self._checking == "ROW":
            self._counter_row += 1
            if self._counter_row >= 9:
                self._counter_row = -1
                self._checking = "COL"
            if self._check_cell_row != self._counter_row:
                print("\tcheck {0}, count {1}".format(self._check_cell_row, self._counter_row))
                print(self._grid.get(self._check_cell_row, self._check_cell_col))
                if not self._grid.is_complete(self._counter_row, self._check_cell_col):
                    self._grid.remove(self._counter_row, self._check_cell_col, self._grid.get(self._check_cell_row, self._check_cell_col))
        # col
        if self._checking == "COL":
            self._counter_col += 1
            if self._counter_col >= 9:
                self._counter_col = -1
                self._checking = "SUB"
        # subgrid
        if self._checking == "SUB":
            # todo: cycle cells,then return True
            self._checking = "ROW"
            return True
        # completed
        return False
    def on_render(self):
        self._display_surf.fill(BACK_COL)
        self.draw_cell()
        self.draw_checking()
        self.draw_lines()
        self.draw_grid()
        pygame.display.update()
    def draw_cell(self):
        left = cell_width*3*self._check_cell_col
        top = cell_height*3*self._check_cell_row
        width = cell_width*3
        height = cell_height*3
        pygame.draw.rect(self._display_surf, (255,255,0), (left, top, width, height), 0)
    def draw_checking(self):
        if self._checking == "ROW":
            left = cell_width*3*self._check_cell_col
            top = cell_height*3*self._counter_row
        if self._checking == "COL":
            left = cell_width*3*self._counter_col
            top = cell_height*3*self._check_cell_row
        width = cell_width*3
        height = cell_height*3           
        pygame.draw.rect(self._display_surf, (0,255,0), (left, top, width, height), 0)
            
    def draw_lines(self):
        for row in range(0, 9):
            pygame.draw.line(self._display_surf, (255,0,0), (0,cell_height*3*row), (cell_width*9*3,cell_height*3*row), 5 if row % 3 == 0 else 1)
            for col in range(0, 9):
                pygame.draw.line(self._display_surf, (255,0,0), (cell_width*3*col, 0), (cell_width*3*col,cell_height*3*9), 5 if col % 3 == 0 else 1)
    def draw_grid(self):
        for row in range(0, 9):
            for col in range(0, 9):
                x = cell_width*3*col
                y = cell_height*3*row
                if self._grid.is_complete(row, col):
                    img = self.font_l.render(str(self._grid.get(row, col)), True, TEXT_COL)
                    self._display_surf.blit(img, (x, y))
                else:
                    count = 1
                    for subrow in range(0, 3):
                        for subcol in range(0, 3):
                            img = self.font_s.render(str(count), True, TEXT_COL)
                            self._display_surf.blit(img, (x+(subcol*cell_width), y+(subrow*cell_height)))
                            count+=1
    def on_cleanup(self):
        pygame.quit()
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        while self._running:
            current = time.time()
            elapsed = current - self._time
            self._time = current
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop(elapsed)
            self.on_render()
        self.on_cleanup()

class Grid(object):
    def __init__(self):
        self._cells = []
        for row in range(0, 9):
            self._cells.append([])
            for col in range(0, 9):
                self._cells[row].append([])
                self._cells[row][col] = Cell()
    def is_complete(self, row, col):
        return self._cells[row][col].is_complete()
    def set(self, row, col, val):
        self._cells[row][col].set(val)
    def get(self, row, col):
        return self._cells[row][col].get()
    def remove(self, row, col, val):
        self._cells[row][col].remove(val)
#    def check(self, row, col):
#        val = self._cells[row][col].get()
#        self.check_row(row, col, val)
#        self.check_col(row, col, val)
#        self.check_subgrid(row, col, val)
#    def check_row(self, row, col, val):
#        for c in range(0, 9):
#            if c != col:
#                self._cells[row][c].remove(val)
#    def check_col(self, row, col, val):
#        for r in range(0, 9):
#            if r != row:
#                self._cells[r][col].remove(val)
#    def check_subgrid(self, row, col, val):
#        r_min = (row % 3) * 3
#        r_max = r_min + 3
#        c_min = (col % 3) * 3
#        c_max = c_min + 3
#        for r in range(r_min, r_max):
#            for c in range(c_min, c_max):
#                if r != row or c != col:
#                    self._cells[r][c].remove(val)
class Cell(object):
    def __init__(self):
        self._numbers = []
        for i in range(0, 9):
            self._numbers.append(True)
    def is_complete(self):
        return self._numbers.count(True) == 1
    def set(self, val):
        count = 1
        for i in range(0, 9):
            if count != val:
                self._numbers[i] = False
            else:
                self._numbers[i] = True
            count+=1
    def get(self):
        if not self.is_complete():
            return 0
        count = 1
        for i in range(0, 9):
            if self._numbers[i] == True:
                return count
            count+=1
        return -1
    def remove(self, val):
        count = 1
        for i in range(0, 9):
            if count == val:
                self._numbers[i] = False
                break
            count+=1

if __name__ == '__main__':
    a = App()
    a.on_execute()

