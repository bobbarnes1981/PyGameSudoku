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
COL_TEXT = SOLARIZED_BASE1
COL_TEXT2 = SOLARIZED_BLUE
COL_TEXT3 = SOLARIZED_GREEN
COL_CHECK = SOLARIZED_BASE02
COL_CHECKING = SOLARIZED_MAGENTA
COL_AREA = SOLARIZED_YELLOW

if CELL_THICKNESS%2 == 0:
    raise Exception("CELL_THICKNESS must be odd")
if GRID_THICKNESS%2 == 0:
    raise Exception("GRID_THICKNESS must be odd")

class App():
    """Represents the pygame application."""
    def __init__(self, data, delay: float, exit: bool) -> None:
        self._delay = delay
        self._exit = exit
        self._grid = sudoku.Grid()
        if len(data) != 9:
            raise Exception("Incorrect number of rows {0}"
                            .format(len(data)))
        for row in range(0, 9):
            if len(data[row]) != 9:
                raise Exception("Incorrect number of cols {0} in row {1}"
                                .format(len(data[row]), row))
        for row in range(0, 9):
            for col in range(0, 9):
                if data[row][col] != 0:
                    self._grid.set(row, col, data[row][col])

        self._running = True
        self._display_surf = None
        self._width = (CELL_WIDTH*9*3)+(8*CELL_THICKNESS)+(2*(GRID_THICKNESS-CELL_THICKNESS))
        self._height = (CELL_HEIGHT*9*3)+(8*CELL_THICKNESS)+(2*(GRID_THICKNESS-CELL_THICKNESS))
        self._size = (self._width, self._height)
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
        self._render_selected = True
        self._complete = False
        self.font_s = None
        self.font_l = None
    def is_complete(self):
        return self._complete
    def get_solution(self):
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
                    if self._exit:
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
            self._check_cell_col+=1
            logging.info('increment col %i', self._check_cell_col)
            if self._check_cell_col >= 9:
                self._check_cell_col = 0
                self._check_cell_row+=1
                logging.info('increment row %i', self._check_cell_row)
                if self._check_cell_row >= 9:
                    self._check_cell_row = 0
        return False
    def check_cell(self) -> bool:
        """Based on the current _checking state, check the required area of the grid."""
        logging.info('check cell %i,%i', self._check_cell_row, self._check_cell_col)
        if not self._grid.is_complete_cell(self._check_cell_row, self._check_cell_col):
            return True
        if self._checking == "ROW":
            self._render_check = True
            if self._grid.is_complete_row(self._check_cell_row):
                self._checking = "COL"
                self._render_check = False
                return False
            self.check_cell_row()
        if self._checking == "COL":
            self._render_check = True
            if self._grid.is_complete_col(self._check_cell_col):
                self._checking = "SUB"
                self._render_check = False
                return False
            self.check_cell_col()
        if self._checking == "SUB":
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
            self.check_cell_sub()
        # not completed
        return False
    def check_cell_row(self) -> None:
        """Check the cells within the row."""
        self._counter_col += 1
        if self._counter_col >= 9:
            self._counter_col = -1
            self._checking = "COL"
        logging.info('check row %i,%i', self._check_cell_row, self._counter_col)
        if self._check_cell_col != self._counter_col:
            if not self._grid.is_complete_cell(self._check_cell_row, self._counter_col):
                self._grid.remove(self._check_cell_row,
                                  self._counter_col,
                                  self._grid.get(self._check_cell_row, self._check_cell_col))
    def check_cell_col(self) -> None:
        """Check the cells within the column."""
        self._counter_row += 1
        if self._counter_row >= 9:
            self._counter_row = -1
            self._checking = "SUB"
        logging.info('check col %i,%i', self._counter_row, self._check_cell_col)
        if self._check_cell_row != self._counter_row:
            if not self._grid.is_complete_cell(self._counter_row, self._check_cell_col):
                self._grid.remove(self._counter_row,
                                  self._check_cell_col,
                                  self._grid.get(self._check_cell_row, self._check_cell_col))
    def check_cell_sub(self) -> None:
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
    def get_left_for_cell_index(self, cell_x_index: int):
        """Calculate the left pixel for the cell x index."""
        return ((CELL_WIDTH*3*cell_x_index)+
                (cell_x_index*CELL_THICKNESS)+
                ((cell_x_index//3)*(GRID_THICKNESS-CELL_THICKNESS)))
    def get_top_for_cell_index(self, cell_y_index: int):
        """Calculate the top pixel for the cell y index."""
        return ((CELL_HEIGHT*3*cell_y_index)+
                (cell_y_index*CELL_THICKNESS)+
                ((cell_y_index//3)*(GRID_THICKNESS-CELL_THICKNESS)))
    def draw_selected_cell(self) -> None:
        """Draw border on the cell being checked."""
        if not self._render_selected:
            return
        left = self.get_left_for_cell_index(self._check_cell_col)
        top = self.get_top_for_cell_index(self._check_cell_row)
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
        if self._checking == "ROW":
            left = self.get_left_for_cell_index(self._counter_col)
            top = self.get_top_for_cell_index(self._check_cell_row)
        if self._checking == "COL":
            left = self.get_left_for_cell_index(self._check_cell_col)
            top = self.get_top_for_cell_index(self._counter_row)
        if self._checking == "SUB":
            (row_val, col_val) = self.get_sub_vals()
            left = self.get_left_for_cell_index(col_val)
            top = self.get_top_for_cell_index(row_val)
        width = CELL_WIDTH*3
        height = CELL_HEIGHT*3
        pygame.draw.rect(self._display_surf, COL_CHECK, (left, top, width, height), 0)
    def draw_checking_area(self) -> None:
        """Draw border on the area being checked."""
        if not self._render_check:
            return
        if self._checking == "ROW":
            top = self.get_top_for_cell_index(self._check_cell_row)
            pygame.draw.rect(self._display_surf,
                             COL_AREA,
                             (0, top, self._width, CELL_HEIGHT*3),
                             AREA_THICKNESS)
        if self._checking == "COL":
            left = self.get_left_for_cell_index(self._check_cell_col)
            pygame.draw.rect(self._display_surf,
                             COL_AREA,
                             (left, 0, CELL_WIDTH*3, self._height),
                             AREA_THICKNESS)
        if self._checking == "SUB":
            (row_offset, col_offset) = self.get_sub_offsets()
            left = self.get_left_for_cell_index(col_offset)
            top = self.get_top_for_cell_index(row_offset)
            pygame.draw.rect(self._display_surf,
                             COL_AREA,
                             (left, top, SUB_WIDTH, SUB_HEIGHT),
                             AREA_THICKNESS)
    def draw_lines(self) -> None:
        """Draw the grid lines."""
        right = (CELL_WIDTH*9*3)+(8*CELL_THICKNESS)+(2*(GRID_THICKNESS-CELL_THICKNESS))
        bottom = (CELL_HEIGHT*3*9)+(8*CELL_THICKNESS)+(2*(GRID_THICKNESS-CELL_THICKNESS))
        for row in range(1, 9):
            v_thickness = GRID_THICKNESS if row % 3 == 0 else CELL_THICKNESS
            v_line = self.get_top_for_cell_index(row)-(v_thickness//2)-1
            pygame.draw.line(self._display_surf, COL_LINE, (0,v_line), (right,v_line), v_thickness)
            for col in range(1, 9):
                h_thickness = GRID_THICKNESS if col % 3 == 0 else CELL_THICKNESS
                h_line = self.get_left_for_cell_index(col)-(h_thickness//2)-1
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
        left = self.get_left_for_cell_index(col)
        top = self.get_top_for_cell_index(row)
        if self._grid.is_complete_cell(row, col):
            left += 15
            top += 10
            img = self.font_l.render(str(self._grid.get(row, col)), True, COL_TEXT)
            self._display_surf.blit(img, (left, top))
        else:
            left += 5
            top += 4
            count = 1
            for subrow in range(0, 3):
                for subcol in range(0, 3):
                    colour = COL_TEXT2
                    if (self._checking == "ROW" and
                        self._check_cell_row == row and
                        self._counter_col == col):
                        colour = COL_TEXT3
                    if (self._checking == "COL" and
                        self._counter_row == row and
                        self._check_cell_col == col):
                        colour = COL_TEXT3
                    (sub_row, sub_col) = self.get_sub_vals()
                    if (self._checking == "SUB" and
                        sub_row == row and
                        sub_col == col):
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
            colour = (COL_BACK)
        else:
            colour = (COL_BACK2)
        left = self.get_left_for_cell_index(col)
        top = self.get_top_for_cell_index(row)
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
