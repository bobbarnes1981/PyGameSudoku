"""Represents a sudoku grid."""

class Grid():
    """Represents a sudoku grid."""
    def __init__(self):
        self._cells = []
        for row in range(0, 9):
            self._cells.append([])
            for col in range(0, 9):
                self._cells[row].append([])
                self._cells[row][col] = Cell()
    def is_complete_cell(self, row: int, col: int) -> bool:
        """Check if the cell (row, col) is complete; if it has only one possibility."""
        return self._cells[row][col].is_complete()
    def is_complete_row(self, row: int) -> bool:
        """Check if all the cells in the row containing (row, col) are complete;
           if they have only one possibility."""
        for i in range(0, 9):
            if not self._cells[row][i].is_complete():
                return False
        return True
    def is_complete_col(self, col: int) -> bool:
        """Check if all the cells in the col containing (row, col) are complete;
           if they have only one possibility."""
        for i in range(0, 9):
            if not self._cells[i][col].is_complete():
                return False
        return True
    def is_complete_sub(self, row: int, col: int) -> bool:
        """Check if all the cells in the sub grid containing (row, col) are complete;
           if they have only one possibility."""
        col_offset = (col // 3) * 3
        row_offset = (row // 3) * 3
        for row_count in range(0, 3):
            for col_count in range(0, 3):
                if not self._cells[row_offset+row_count][col_offset+col_count].is_complete():
                    return False
        return True
    def is_complete_grid(self) -> bool:
        """Check if all cells in the grid are complete; if they have only one possibility."""
        for row_count in range(0, 9):
            for col_count in range(0, 9):
                if not self._cells[row_count][col_count].is_complete():
                    return False
        return True
    def has(self, row: int, col: int, val: int) -> bool:
        """Check if 'val' is a possible number for the cell (row, col)."""
        return self._cells[row][col].has(val)
    def set(self, row: int, col: int, val: int) -> None:
        """Set 'val' as the only valid number for the cell (row, col)."""
        self._cells[row][col].set(val)
    def get(self, row: int, col: int) -> int:
        """Get the value for the cell (row, col). Returns zero if not yet complete."""
        return self._cells[row][col].get()
    def predefined(self, row: int, col: int) -> bool:
        """Check if the cell is a predefined cell"""
        return self._cells[row][col].predefined()
    def remove(self, row: int, col: int, val: int) -> None:
        """Remove the number 'val' from the possible numbers for the cell (row, col)."""
        self._cells[row][col].remove(val)
    def to_lists(self):
        l = []
        for row in range(0, 9):
            l.append([])
            for col in range(0, 9):
                l[row].append(self._cells[row][col].get())
        return l

class Cell():
    """Represents a cell in a sudoku grid."""
    def __init__(self):
        self._numbers = []
        for _ in range(0, 9):
            self._numbers.append(True)
        self._is_predefined = False
    def is_complete(self) -> bool:
        """Check if this cell is complete; if it has only one possibility."""
        return self._numbers.count(True) == 1
    def has(self, val: int) -> bool:
        """Check if 'val' is a possible number for this cell."""
        if val not in range(1, 10):
            raise Exception("invalid val {0}".format(val))
        return self._numbers[val-1]
    def set(self, val: int) -> None:
        """Set 'val' as the only valid number for this cell."""
        if val not in range(1, 10):
            raise Exception("invalid val {0}".format(val))
        for i in range(0, 9):
            if i == val-1:
                self._numbers[i] = True
            else:
                self._numbers[i] = False
        self._is_predefined = True
    def get(self) -> int:
        """Get the value for this cell. Returns zero if not yet complete."""
        if not self.is_complete():
            return 0
        return self._numbers.index(True)+1
    def predefined(self) -> bool:
        """Check if the cell is a predefined cell"""
        return self._is_predefined
    def remove(self, val: int) -> None:
        """Remove the number 'val' from the possible numbers for this cell."""
        if val not in range(1, 10):
            raise Exception("invalid val {0}".format(val))
        self._numbers[val-1] = False
