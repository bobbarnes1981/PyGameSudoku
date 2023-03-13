
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
