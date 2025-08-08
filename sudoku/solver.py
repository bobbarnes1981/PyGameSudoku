"""Solve sudoku"""

import logging
import time
import pygame
import sudoku

SOLARIZED_BASE03 = (0,43,54)
SOLARIZED_BASE02 = (7,54,66)
SOLARIZED_BASE01 = (88,110,117)
SOLARIZED_BASE00 = (101,123,131)
SOLARIZED_BASE0 = (131,148,150)
SOLARIZED_BASE1 = (147,161,161)
SOLARIZED_BASE2 = (238,232,213)
SOLARIZED_BASE3 = (253,246,227)
SOLARIZED_YELLOW = (181,137,0)
SOLARIZED_ORANGE = (203,75,22)
SOLARIZED_RED = (220,50,47)
SOLARIZED_MAGENTA = (211,54,130)
SOLARIZED_VIOLET = (108,113,196)
SOLARIZED_BLUE = (38,139,210)
SOLARIZED_CYAN = (42,161,152)
SOLARIZED_GREEN = (133,153,0)

CELL_THICKNESS = 3
GRID_THICKNESS = 7
AREA_THICKNESS = 3
SELECTED_THICKNESS = 3

CELL_WIDTH = 20
CELL_HEIGHT = 20
SUB_WIDTH = (CELL_WIDTH*3*3)+(CELL_THICKNESS*2)
SUB_HEIGHT = (CELL_HEIGHT*3*3)+(CELL_THICKNESS*2)

COL_WHITE = (255,255,255)
COL_LINE = SOLARIZED_BASE01
COL_BACK = SOLARIZED_BASE03
COL_BACK2 = SOLARIZED_BASE03
COL_TEXT0 = SOLARIZED_BASE2
COL_TEXT1 = SOLARIZED_BASE1
COL_TEXT2 = SOLARIZED_BLUE
COL_TEXT3 = SOLARIZED_GREEN
COL_CHECK = SOLARIZED_BASE02
COL_CHECKING = SOLARIZED_MAGENTA
COL_AREA = SOLARIZED_YELLOW

class SudokuConfigurationException(Exception):
    """Sudoku configuration exception"""

class SudokuDataException(Exception):
    """Sudoku data exception"""

if CELL_THICKNESS%2 == 0:
    raise SudokuConfigurationException("CELL_THICKNESS must be odd")
if GRID_THICKNESS%2 == 0:
    raise SudokuConfigurationException("GRID_THICKNESS must be odd")

def get_left_for_cell_index(cell_x_index: int):
    """Calculate the left pixel for the cell x index."""
    return ((CELL_WIDTH*3*cell_x_index)+
            (cell_x_index*CELL_THICKNESS)+
            ((cell_x_index//3)*(GRID_THICKNESS-CELL_THICKNESS)))

def get_top_for_cell_index(cell_y_index: int):
    """Calculate the top pixel for the cell y index."""
    return ((CELL_HEIGHT*3*cell_y_index)+
            (cell_y_index*CELL_THICKNESS)+
            ((cell_y_index//3)*(GRID_THICKNESS-CELL_THICKNESS)))

def get_width():
    return (CELL_WIDTH*9*3)+(8*CELL_THICKNESS)+(2*(GRID_THICKNESS-CELL_THICKNESS))

def get_height():
    return (CELL_HEIGHT*9*3)+(8*CELL_THICKNESS)+(2*(GRID_THICKNESS-CELL_THICKNESS))

class SudokuCheckerRow:
    def __init__(self):
        self._counter_row = -1
        self._counter_col = -1

        self._check_cell_row = 0
        self._check_cell_col = 0

    def check(self, grid:sudoku.Grid):
        """Check the cells within the row."""
        ret = False
        self._counter_col += 1
        if self._counter_col >= 9:
            self._counter_col = -1
            ret = True
        logging.info('examining cell %i,%i', self._counter_col, self._check_cell_row)
        if self._check_cell_col != self._counter_col:
            if not grid.is_complete_cell(self._check_cell_row, self._counter_col):
                grid.remove(self._check_cell_row,
                            self._counter_col,
                            grid.get(self._check_cell_row, self._check_cell_col))
        return ret
    def is_complete(self, grid:sudoku.Grid) -> bool:
        return grid.is_complete_row(self._check_cell_row)
    def get_left_and_top(self):
        left = get_left_for_cell_index(self._counter_col)
        top = get_top_for_cell_index(self._check_cell_row)
        return left, top
    def get_check_rects(self) -> list[tuple]:
        top = get_top_for_cell_index(self._check_cell_row)
        return [
            (0, top, get_width(), CELL_HEIGHT*3)
        ]
    def is_cell(self, row:int, col:int) -> bool:
        return self._check_cell_row == row and self._counter_col == col
    def inc_row(self):
        self._check_cell_row+=1
    def inc_col(self):
        self._check_cell_col+=1
    def get_row(self) -> int:
        return self._check_cell_row
    def get_col(self) -> int:
        return self._check_cell_col
    def reset_row(self):
        self._check_cell_row = 0
    def reset_col(self):
        self._check_cell_col = 0

class SudokuCheckerCol:
    def __init__(self):
        self._counter_row = -1
        self._counter_col = -1

        self._check_cell_row = 0
        self._check_cell_col = 0

    def check(self, grid:sudoku.Grid):
        """Check the cells within the column."""
        ret = False
        self._counter_row += 1
        if self._counter_row >= 9:
            self._counter_row = -1
            ret = True
        logging.info('examining cell %i,%i', self._counter_row, self._check_cell_col)
        if self._check_cell_row != self._counter_row:
            if not grid.is_complete_cell(self._counter_row, self._check_cell_col):
                grid.remove(self._counter_row,
                            self._check_cell_col,
                            grid.get(self._check_cell_row, self._check_cell_col))
        return ret
    def is_complete(self, grid:sudoku.Grid) -> bool:
        return grid.is_complete_col(self._check_cell_col)
    def get_left_and_top(self):
        left = get_left_for_cell_index(self._check_cell_col)
        top = get_top_for_cell_index(self._counter_row)
        return left, top
    def get_check_rects(self) -> list[tuple]:
        left = get_left_for_cell_index(self._check_cell_col)
        return [
            (left, 0, CELL_WIDTH*3, get_height())
        ]
    def is_cell(self, row:int, col:int) -> bool:
        return self._counter_row == row and self._check_cell_col == col
    def inc_row(self):
        self._check_cell_row+=1
    def inc_col(self):
        self._check_cell_col+=1
    def get_row(self) -> int:
        return self._check_cell_row
    def get_col(self) -> int:
        return self._check_cell_col
    def reset_row(self):
        self._check_cell_row = 0
    def reset_col(self):
        self._check_cell_col = 0

class SudokuCheckerSub:
    def __init__(self):
        self._counter_row = -1
        self._counter_col = -1

        self._check_cell_row = 0
        self._check_cell_col = 0

    def check(self):
        """Check the cells within the sub grid."""
        if self._counter_sub_col == -1:
            self._counter_sub_col+=1
        if self._counter_sub_row == -1:
            self._counter_sub_row+=1
        (row_val, col_val) = self.get_sub_vals()
        logging.info('check sub %i,%i', row_val, col_val)
        if self._check_cell_row != row_val or self._check_cell_col != col_val:
            if not self._grid.is_complete_cell(row_val, col_val):
                self._grid.remove(row_val,
                                  col_val,
                                  self._grid.get(self._check_cell_row, self._check_cell_col))
    def is_complete(self, grid:sudoku.Grid, row:int, col:int) -> bool:
        if grid.is_complete_sub(row, col):
            self._counter_sub_col += 1
            if self._counter_sub_col >= 3:
                self._counter_sub_col = -1
                self._counter_sub_row += 1
                if self._counter_sub_row >= 3:
                    self._counter_sub_row = -1
                    self._checking = "ROW"
                    return True
        return False
    def get_left_and_top(self):
        (row_val, col_val) = self.get_sub_vals()
        left = get_left_for_cell_index(col_val)
        top = get_top_for_cell_index(row_val)
        return left, top
    def get_check_rects(self) -> list[tuple]:
        (row_offset, col_offset) = self.get_sub_offsets()
        left = get_left_for_cell_index(col_offset)
        top = get_top_for_cell_index(row_offset)
        return [
            (left, top, SUB_WIDTH, SUB_HEIGHT)
        ]
    def is_cell(self, row:int, col:int) -> bool:
        (sub_row, sub_col) = self.get_sub_vals()
        return sub_row == row and sub_col == col
    def inc_row(self):
        self._check_cell_row+=1
    def inc_col(self):
        self._check_cell_col+=1
    def get_row(self) -> int:
        return self._check_cell_row
    def get_col(self) -> int:
        return self._check_cell_col
    def reset_row(self):
        self._check_cell_row = 0
    def reset_col(self):
        self._check_cell_col = 0
    def get_sub_offsets(self):
        """Get the top and left indexes of the sub grid that
           contains (check_cell_row, check_cell_col)."""
        col_offset = (self._check_cell_col // 3) * 3
        row_offset = (self._check_cell_row // 3) * 3
        return (row_offset, col_offset)
    def get_sub_vals(self):
        """Get the global (row, col) indexes for the sub grid local indexes."""
        (row_offset, col_offset) = self.get_sub_offsets()
        col_val = col_offset + self._counter_sub_col
        row_val = row_offset + self._counter_sub_row
        return (row_val, col_val)

class App():
    """Represents the pygame application."""
    def __init__(self, data, delay: float, exit_on_complete: bool) -> None:
        self._delay = delay
        self._exit_on_complete = exit_on_complete
        self._grid = sudoku.Grid()
        if len(data) != 9:
            raise SudokuDataException(f"Incorrect number of rows {len(data)}")
        for row in range(0, 9):
            if len(data[row]) != 9:
                raise SudokuDataException(f"Incorrect number of cols {len(data[row])} in row {row}")
        for row in range(0, 9):
            for col in range(0, 9):
                if data[row][col] != 0:
                    self._grid.set(row, col, data[row][col])

        self._running = True
        self._display_surf = None
        self._size = (get_width(), get_height())
        self._time = time.time()
        self._counter = 0
        self._checking = 0
        self._counter_sub_row = -1
        self._counter_sub_col = -1
        self._render_check = True
        self._render_selected = True
        self._complete = False
        self.font_s = None
        self.font_l = None
        self._checkers = [
            SudokuCheckerRow(),
            SudokuCheckerCol(),
            SudokuCheckerSub(),
        ]
    def is_complete(self) -> bool:
        """Check if is complete"""
        return self._complete
    def get_solution(self):
        """Get the solution"""
        return self._grid.to_lists()
    def on_init(self) -> bool:
        """Initialise solver."""
        pygame.init()
        pygame.display.set_caption("Sudoku")
        self._display_surf = pygame.display.set_mode(self._size,
                                                     pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        #self.font = pygame.font.SysFont('courier.ttf', 72)
        font_name = pygame.font.get_default_font()
        logging.info("System font: %s", font_name)
        self.font_s = pygame.font.SysFont(None, 22)
        self.font_l = pygame.font.SysFont(None, 66)
        return True
    def on_event(self, event: pygame.event.Event) -> None:
        """Process the pygame events."""
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == 27:
                self._running = False
        else:
            logging.debug(event)
    def on_loop(self, elapsed: float) -> None:
        """When counter elapses check a cell in the grid."""
        self._counter+=elapsed
        if self._counter > self._delay:
            logging.info("tick")
            self._counter = 0
            if not self._complete:
                if self.check_grid():
                    self._complete = True
                    if self._exit_on_complete:
                        self._running = False
    def check_grid(self) -> bool:
        """Check the grid until completed."""
        logging.info('check grid')
        if self._grid.is_complete_grid():
            self._render_check = False
            self._render_selected = False
            logging.info('grid complete')
            return True
        finished_check = self.check_cell()
        logging.info('finished check %s', finished_check)
        if finished_check:
            self._checkers[self._checking].inc_col()
            logging.info('increment col %i', self._checkers[self._checking].get_col())
            if self._checkers[self._checking].get_col() >= 9:
                self._checkers[self._checking].reset_col()
                self._checkers[self._checking].inc_row()
                logging.info('increment row %i', self._checkers[self._checking].get_row())
                if self._checkers[self._checking].get_row() >= 9:
                    self._checkers[self._checking].reset_row()
        return False
    def check_cell(self) -> bool:
        """Based on the current _checking state, check the required area of the grid."""
        logging.info('checking relationships for cell %i,%i', self._checkers[self._checking].get_row(), self._checkers[self._checking].get_col())
        if not self._grid.is_complete_cell(self._checkers[self._checking].get_row(), self._checkers[self._checking].get_col()):
            logging.info('cell %i,%i not complete, skipping', self._checkers[self._checking].get_row(), self._checkers[self._checking].get_col())
            return True
        logging.info('cell %i,%i complete, running checks', self._checkers[self._checking].get_row(), self._checkers[self._checking].get_col())
        
        self._render_check = True
        if self._checkers[self._checking].is_complete(self._grid):
            self._checking+=1
            if self._checking >= len(self._checkers):
                return True
            self._render_check = False
            return False
        if self._checkers[self._checking].check(self._grid):
            self._checking+=1
            if self._checking >= len(self._checkers):
                return True

        # not completed
        return False
    def on_render(self) -> None:
        """Render the game."""
        self._display_surf.fill(COL_WHITE)
        self.draw_cells()
        self.draw_lines()
        self.draw_checking()
        self.draw_numbers()
        self.draw_checking_area()
        self.draw_selected_cell()
        pygame.display.update()
    def draw_selected_cell(self) -> None:
        """Draw border on the cell being checked."""
        if not self._render_selected:
            return
        left = get_left_for_cell_index(self._checkers[self._checking].get_col())
        top = get_top_for_cell_index(self._checkers[self._checking].get_row())
        width = CELL_WIDTH*3
        height = CELL_HEIGHT*3
        pygame.draw.rect(self._display_surf,
                         COL_CHECKING,
                         (left, top, width, height),
                         SELECTED_THICKNESS)
    def draw_checking(self) -> None:
        """Set the background colour on the cell being checked."""
        if not self._render_check:
            return
        (left, top) = self._checkers[self._checking].get_left_and_top()
        width = CELL_WIDTH*3
        height = CELL_HEIGHT*3
        pygame.draw.rect(self._display_surf, COL_CHECK, (left, top, width, height), 0)
    def draw_checking_area(self) -> None:
        """Draw border on the area being checked."""
        if not self._render_check:
            return
        rects = self._checkers[self._checking].get_check_rects()
        for rect in rects:
            pygame.draw.rect(self._display_surf,
                        COL_AREA,
                        rect,
                        AREA_THICKNESS)
    def draw_lines(self) -> None:
        """Draw the grid lines."""
        right = (CELL_WIDTH*9*3)+(8*CELL_THICKNESS)+(2*(GRID_THICKNESS-CELL_THICKNESS))
        bottom = (CELL_HEIGHT*3*9)+(8*CELL_THICKNESS)+(2*(GRID_THICKNESS-CELL_THICKNESS))
        for row in range(1, 9):
            v_thickness = GRID_THICKNESS if row % 3 == 0 else CELL_THICKNESS
            v_line = get_top_for_cell_index(row)-(v_thickness//2)-1
            pygame.draw.line(self._display_surf, COL_LINE, (0,v_line), (right,v_line), v_thickness)
            for col in range(1, 9):
                h_thickness = GRID_THICKNESS if col % 3 == 0 else CELL_THICKNESS
                h_line = get_left_for_cell_index(col)-(h_thickness//2)-1
                pygame.draw.line(self._display_surf,
                                 COL_LINE,
                                (h_line, 0),
                                (h_line,bottom),
                                h_thickness)
    def draw_numbers(self) -> None:
        """Draw all the numbers."""
        for row in range(0, 9):
            for col in range(0, 9):
                self.draw_number(row, col)
    def draw_number(self, row: int, col: int) -> None:
        """Draw the number for cell (row, col)."""
        left = get_left_for_cell_index(col)
        top = get_top_for_cell_index(row)
        if self._grid.is_complete_cell(row, col):
            left += 15
            top += 10
            colour = COL_TEXT1
            if self._grid.predefined(row, col):
                colour = COL_TEXT0
            img = self.font_l.render(str(self._grid.get(row, col)), True, colour)
            self._display_surf.blit(img, (left, top))
        else:
            left += 5
            top += 4
            count = 1
            for subrow in range(0, 3):
                for subcol in range(0, 3):
                    colour = COL_TEXT2
                    if self._checkers[self._checking].is_cell(row, col):
                        colour = COL_TEXT3
                    num_text = str(count if self._grid.has(row, col, count) else ' ')
                    img = self.font_s.render(num_text, True, colour)
                    img_left = left+(subcol*CELL_WIDTH)
                    img_top = top+(subrow*CELL_HEIGHT)
                    self._display_surf.blit(img, (img_left, img_top))
                    count+=1
    def draw_cells(self) -> None:
        """Draw all the cells."""
        for row in range(0, 9):
            for col in range(0, 9):
                self.draw_cell(row, col)
    def draw_cell(self, row: int, col: int) -> None:
        """Draw a single cell for (row, col)."""
        if self._grid.is_complete_cell(row, col):
            colour = COL_BACK
        else:
            colour = COL_BACK2
        left = get_left_for_cell_index(col)
        top = get_top_for_cell_index(row)
        width = CELL_WIDTH*3
        height = CELL_HEIGHT*3
        pygame.draw.rect(self._display_surf, colour, (left, top, width, height), 0)
    def on_cleanup(self) -> None:
        """Cleanup."""
        pygame.quit()
    def on_execute(self) -> None:
        """Execute application."""
        if not self.on_init():
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
