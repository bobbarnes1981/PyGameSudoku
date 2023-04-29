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
    def is_complete_cell(self, row, col):
        """Check if the cell (row, col) is complete; if it has only one possibility."""
        return self._cells[row][col].is_complete()
    def is_complete_row(self, row):
        """Check if all the cells in the row containing (row, col) are complete;
           if they have only one possibility."""
        for i in range(0, 9):
            if not self._cells[row][i].is_complete():
                return False
        return True
    def is_complete_col(self, col):
        """Check if all the cells in the col containing (row, col) are complete;
           if they have only one possibility."""
        for i in range(0, 9):
            if not self._cells[i][col].is_complete():
                return False
        return True
    def is_complete_sub(self, row, col):
        """Check if all the cells in the sub grid containing (row, col) are complete;
           if they have only one possibility."""
        col_offset = (col // 3) * 3
        row_offset = (row // 3) * 3
        for row_count in range(0, 3):
            for col_count in range(0, 3):
                if not self._cells[row_offset+row_count][col_offset+col_count].is_complete():
                    return False
        return True
    def is_complete_grid(self):
        """Check if all cells in the grid are complete; if they have only one possibility."""
        for row_count in range(0, 9):
            for col_count in range(0, 9):
                if not self._cells[row_count][col_count].is_complete():
                    return False
        return True
    def has(self, row, col, val):
        """Check if 'val' is a possible number for the cell (row, col)."""
        return self._cells[row][col].has(val)
    def set(self, row, col, val):
        """Set 'val' as the only valid number for the cell (row, col)."""
        self._cells[row][col].set(val)
    def get(self, row, col):
        """Get the value for the cell (row, col). Returns zero if not yet complete."""
        return self._cells[row][col].get()
    def remove(self, row, col, val):
        """Remove the number 'val' from the possible numbers for the cell (row, col)."""
        self._cells[row][col].remove(val)

class Cell():
    """Represents a cell in a sudoku grid."""
    def __init__(self):
        self._numbers = []
        for _ in range(0, 9):
            self._numbers.append(True)
    def is_complete(self):
        """Check if this cell is complete; if it has only one possibility."""
        return self._numbers.count(True) == 1
    def has(self, val):
        """Check if 'val' is a possible number for this cell."""
        if val not in range(1, 10):
            raise Exception("invalid val {0}".format(val))
        return self._numbers[val-1]
    def set(self, val):
        """Set 'val' as the only valid number for this cell."""
        if val not in range(1, 10):
            raise Exception("invalid val {0}".format(val))
        for i in range(0, 9):
            if i == val-1:
                self._numbers[i] = True
            else:
                self._numbers[i] = False
    def get(self):
        """Get the value for this cell. Returns zero if not yet complete."""
        if not self.is_complete():
            return 0
        return self._numbers.index(True)+1
    def remove(self, val):
        """Remove the number 'val' from the possible numbers for this cell."""
        if val not in range(1, 10):
            raise Exception("invalid val {0}".format(val))
        self._numbers[val-1] = False
