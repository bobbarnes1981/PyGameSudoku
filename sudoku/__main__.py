import logging
import pygame
import time
from pygame.locals import *

logging.basicConfig(level=logging.INFO)

cell_width = 20
cell_height = 20
COL_BACK = (0,0,0)
COL_TEXT = (25,25,112)
COL_YELLOW = (255,255,0)
DELAY = 0.5
CELL_THICKNESS = 5
GRID_THICKNESS = 11

# TODO: incorporate grid wall thickness into render

if CELL_THICKNESS%2 == 0:
    raise Exception("CELL_THICKNESS must be odd")
if GRID_THICKNESS%2 == 0:
    raise Exception("GRID_THICKNESS must be odd")

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
        self._size = ((cell_width*9*3)+(8*CELL_THICKNESS), (cell_height*9*3)+(8*CELL_THICKNESS))
        self._grid = Grid()
        self._time = time.time()
        self._counter = 0
        self._checking = "ROW"
        self._counter_row = -1
        self._counter_col = -1
        self._counter_sub_row = -1
        self._counter_sub_col = -1
        self._check_cell_row = 0
        self._check_cell_col = 0
        self._render_check = True
        logging.info('Loading grid')
        for row in range(0, 9):
            for col in range(0, 9):
                if TEST_DATA[row][col] != 0:
                    self._grid.set(row, col, TEST_DATA[row][col])
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self._size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        #self.font = pygame.font.SysFont('courier.ttf', 72)
        font_name = pygame.font.get_default_font()
        logging.info("System font: {0}".format(font_name))
        self.font_s = pygame.font.SysFont(None, 22)
        self.font_l = pygame.font.SysFont(None, 66)
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == 27:
                self._running = False
        else:
            logging.debug(event)
    def on_loop(self, elapsed):
        self._counter+=elapsed
        if self._counter > DELAY:
            logging.info("tick")
            self._counter = 0
            self.check_grid()
    def check_grid(self):
        logging.info('Check grid')
        if self._grid.is_complete_grid():
            return
        finished_check = self.check_cell()
        logging.info('finished check {0}'.format(finished_check))
        if finished_check:
            self._check_cell_col+=1
            logging.info('increment col')
            if self._check_cell_col >= 9:
                self._check_cell_col = 0
                self._check_cell_row+=1
                logging.info('increment row')
                if self._check_cell_row >= 9:
                    self._check_cell_row = 0
    def check_cell(self):
        logging.info('Check cell')
        if not self._grid.is_complete_cell(self._check_cell_row, self._check_cell_col):
            return True
        # col
        if self._checking == "ROW":
            logging.info('Check row')
            self._render_check = True
            if self._grid.is_complete_row(self._check_cell_row):
                self._checking = "COL"
                self._render_check = False
                return False
            self._counter_col += 1
            if self._counter_col >= 9:
                self._counter_col = -1
                self._checking = "COL"
            if self._check_cell_col != self._counter_col:
                if not self._grid.is_complete_cell(self._check_cell_row, self._counter_col):
                    self._grid.remove(self._check_cell_row, self._counter_col, self._grid.get(self._check_cell_row, self._check_cell_col))
        # row
        if self._checking == "COL":
            logging.info('Check col')
            self._render_check = True
            if self._grid.is_complete_col(self._check_cell_col):
                self._checking = "SUB"
                self._render_check = False
                return False
            self._counter_row += 1
            if self._counter_row >= 9:
                self._counter_row = -1
                self._checking = "SUB"
            if self._check_cell_row != self._counter_row:
                if not self._grid.is_complete_cell(self._counter_row, self._check_cell_col):
                    self._grid.remove(self._counter_row, self._check_cell_col, self._grid.get(self._check_cell_row, self._check_cell_col))
        # subgrid
        if self._checking == "SUB":
            logging.info('Check sub')
            self._render_check = True
            if self._grid.is_complete_sub(self._check_cell_row, self._check_cell_col):
                self._checking = "ROW"
                self._render_check = False
                # completed
                return True
            self._counter_sub_col += 1
            if self._counter_sub_col >= 3:
                self._counter_sub_col = -1
                self._counter_sub_row += 1
                if self._counter_sub_row >= 3:
                    self._counter_sub_row = -1
                    self._checking = "ROW"
                    # completed
                    return True
            if self._counter_sub_col == -1:
                self._counter_sub_col+=1
            if self._counter_sub_row == -1:
                self._counter_sub_row+=1
            (row_val, col_val) = self.get_sub_vals()
            if self._check_cell_row != row_val or self._check_cell_col != col_val:
                if not self._grid.is_complete_cell(row_val, col_val):
                    self._grid.remove(row_val, col_val, self._grid.get(self._check_cell_row, self._check_cell_col))
        # not completed
        return False
    def get_sub_vals(self):
        col_offset = (self._check_cell_col // 3) * 3
        row_offset = (self._check_cell_row // 3) * 3
        col_val = col_offset + self._counter_sub_col
        row_val = row_offset + self._counter_sub_row
        return (row_val, col_val)
    def on_render(self):
        self._display_surf.fill(COL_BACK)
        self.draw_cells()
        self.draw_lines()
        self.draw_check_cell()
        self.draw_checking()
        self.draw_numbers()
        pygame.display.update()
    def draw_check_cell(self):
        left = (cell_width*3*self._check_cell_col)+(self._check_cell_col*CELL_THICKNESS)
        top = (cell_height*3*self._check_cell_row)+(self._check_cell_row*CELL_THICKNESS)
        width = cell_width*3
        height = cell_height*3
        pygame.draw.rect(self._display_surf, COL_YELLOW, (left, top, width, height), 2)
    def draw_checking(self):
        if not self._render_check:
            return
        if self._checking == "COL":
            left = (cell_width*3*self._check_cell_col)+(self._check_cell_col*CELL_THICKNESS)
            top = (cell_height*3*self._counter_row)+(self._counter_row*CELL_THICKNESS)
        if self._checking == "ROW":
            left = (cell_width*3*self._counter_col)+(self._counter_col*CELL_THICKNESS)
            top = (cell_height*3*self._check_cell_row)+(self._check_cell_row*CELL_THICKNESS)
        if self._checking == "SUB":
            (row_val, col_val) = self.get_sub_vals()
            left = (cell_width*3*col_val)+(col_val*CELL_THICKNESS)
            top = (cell_height*3*row_val)+(row_val*CELL_THICKNESS)
        width = cell_width*3
        height = cell_height*3
        pygame.draw.rect(self._display_surf, (0,255,0), (left, top, width, height), 0)
    def draw_lines(self):
        right = (cell_width*9*3)+(8*CELL_THICKNESS)
        bottom = (cell_height*3*9)+(8*CELL_THICKNESS)
        for row in range(1, 9):
            v_line = (cell_height*3*row)+(row*CELL_THICKNESS)-(CELL_THICKNESS//2)-1
            pygame.draw.line(self._display_surf, (255,0,0), (0,v_line), (right,v_line), CELL_THICKNESS if row % 3 == 0 else CELL_THICKNESS)
            for col in range(1, 9):
                h_line = (cell_width*3*col)+(col*CELL_THICKNESS)-(CELL_THICKNESS//2)-1
                pygame.draw.line(self._display_surf, (255,0,0), (h_line, 0), (h_line,bottom), CELL_THICKNESS if col % 3 == 0 else CELL_THICKNESS)
    def draw_numbers(self):
        for row in range(0, 9):
            for col in range(0, 9):
                self.draw_number(row, col)
    def draw_number(self, row, col):
        x = (cell_width*3*col)+(col*CELL_THICKNESS)
        y = (cell_height*3*row)+(row*CELL_THICKNESS)
        if self._grid.is_complete_cell(row, col):
            x += 15
            y += 10
            img = self.font_l.render(str(self._grid.get(row, col)), True, COL_TEXT)
            self._display_surf.blit(img, (x, y))
        else:
            x += 5
            y += 4
            count = 1
            for subrow in range(0, 3):
                for subcol in range(0, 3):
                    img = self.font_s.render(str(count if self._grid.has(row, col, count) else ' '), True, COL_TEXT)
                    self._display_surf.blit(img, (x+(subcol*cell_width), y+(subrow*cell_height)))
                    count+=1
    def draw_cells(self):
        for row in range(0, 9):
            for col in range(0, 9):
                self.draw_cell(row, col)
    def draw_cell(self, row, col):
        if self._grid.is_complete_cell(row, col):
            colour = (0,0,0)
        else:
            colour = (80,80,80)
        left = (cell_width*3*(col))+(col*CELL_THICKNESS)
        top = (cell_height*3*(row))+(row*CELL_THICKNESS)
        width = cell_width*3
        height = cell_height*3
        pygame.draw.rect(self._display_surf, colour, (left, top, width, height), 0)
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
    def is_complete_cell(self, row, col):
        return self._cells[row][col].is_complete()
    def is_complete_row(self, row):
        for i in range(0, 9):
            if not self._cells[row][i].is_complete():
                return False
        return True
    def is_complete_col(self, col):
        for i in range(0, 9):
            if not self._cells[i][col].is_complete():
                return False
        return True
    def is_complete_sub(self, row, col):
        col_offset = (col // 3) * 3
        row_offset = (row // 3) * 3
        for r in range(0, 3):
            for c in range(0, 3):
                if not self._cells[row_offset+r][col_offset+c].is_complete():
                    return False
        return True
    def is_complete_grid(self):
        for r in range(0, 9):
            for c in range(0, 9):
                if not self._cells[r][c].is_complete():
                    return False
        return True
    def has(self, row, col, val):
        return self._cells[row][col].has(val)
    def set(self, row, col, val):
        self._cells[row][col].set(val)
    def get(self, row, col):
        return self._cells[row][col].get()
    def remove(self, row, col, val):
        self._cells[row][col].remove(val)
class Cell(object):
    def __init__(self):
        self._numbers = []
        for i in range(0, 9):
            self._numbers.append(True)
    def is_complete(self):
        return self._numbers.count(True) == 1
    def has(self, val):
        if val not in range(1, 10):
            raise Exception("invalid val {0}".format(val))
        return self._numbers[val-1]
    def set(self, val):
        if val not in range(1, 10):
            raise Exception("invalid val {0}".format(val))
        for i in range(0, 9):
            if i == val-1:
                self._numbers[i] = True
            else:
                self._numbers[i] = False
    def get(self):
        if not self.is_complete():
            return 0
        return self._numbers.index(True)+1
    def remove(self, val):
        if val not in range(1, 10):
            raise Exception("invalid val {0}".format(val))
        self._numbers[val-1] = False

if __name__ == '__main__':
    a = App()
    a.on_execute()

