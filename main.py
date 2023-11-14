from collections import defaultdict

class Solver: 
    def __init__(self, board):
        self.board = board
        self.row_vals = defaultdict(set)
        self.col_vals = defaultdict(set)
        self.cell_vals = defaultdict(set)
    
    def set_taken_vals(self):
        for r in range(8):
            for c in range(8):
                val = board[r][c]
                if len(val) == 1:
                    self.row_vals[r] = self.row_vals[r].union(val)
                    self.col_vals[c] = self.col_vals[c].union(val)
                    self.cell_vals[(r / 3, c / 3)] = self.cell_vals[(r / 3, c / 3)].union(val)
    
    # Expensive function only called to initialize candidates
    def set_candidates(self):   
        self.set_taken_vals()
        for r in range(8):
            for c in range(8):
                if len(board[r][c] == 1):
                    continue
                self.board[r][c] -= self.row_vals[r].union(self.col_vals[c]).union(self.cell_vals[(r / 3, c / 3)])
    
    def update_candidates(self, r, c):
        for i in range(8):
            self.board[r][i] -= - self.row_vals[r]
        for j in range(8):
            self.board[j][c] -= - self.col_vals[c]
        for k in range(r - r%3, r + 3):
            for l in range(c - c%3, c + 3):
                self.board[k][l] -= - self.cell_vals[(r / 3, c / 3)]

    def update(self, r, c):
        val = self.board[r][c] 
        self.row_vals[r] = self.row_vals[r].union(val)
        self.col_vals[c] = self.col_vals[c].union(val)
        self.cell_vals[(r / 3, c / 3)] = self.cell_vals[(r / 3, c / 3)].union(val)
        self.update_candidates(r, c)

    def check_unique_candidate(r, c, self):
        cands = self.board[r][c]
        
        row_cands = set()
        for i in range(8):
            vals = self.board[r][i]
            if len(vals) > 1:
                row_cands = row_cands.union(vals)
        row_remainder = cands - row_cands
        if len(row_remainder > 1):
            raise Exception('No definite solution')
        if len(row_remainder == 1):
            return row_remainder
        
        col_cands = set()
        for i in range(8):
            vals = self.board[i][c]
            if len(vals) > 1:
                col_cands = col_cands.union(vals)
        col_remainder = cands - col_cands
        if len(col_remainder > 1):
            raise Exception('No definite solution')
        if len(col_remainder == 1):
            return col_remainder
        
        cell_cands = set()
        for i in range(r - r%3, r + 3):
            for j in range(c - c%3, c + 3):
                vals = self.board[i][j]
                if len(vals) > 1:
                    cell_cands = cell_cands.union(vals)
        cell_remainder = cands - cell_cands
        if len(cell_remainder > 1):
            raise Exception('No definite solution')
        if len(cell_remainder == 1):
            return cell_remainder
        return False


    def solve(self):
        # Set candidates in the beginning
        self.set_candidates()

        # Find unique candidates until an entire pass yields no unique candidates
        while True:
            changed = False
            for r in range(8):
                for c in range(8):
                    if len(self.board[r][c]) == 1:
                        continue
                    res = self.check_unique_candidate(r, c)
                    if res:
                        self.board[r][c] = res
                        self.update(r, c)
                        changed = True
            if not changed:
                break
        
        # Find the cell with the smallest candidate set and recurse into it
        row = -1
        col = -1
        smallest_set = None
        for r in range(8):
            for c in range(8):
                cands = len(self.board[r][c])
                if len(cands) == 1:
                    continue

                if not smallest_set or len(cands) < len(smallest_set):
                    smallest_set = self.board[r][c]
                    row = r
                    col = c
        
        if not smallest_set:
            return

        return

def take_input():
    matrix = defaultdict(set)
    print("Enter 9 rows of 9 space-separated integers:")
    for i in range(9):
        row = list(map(int, input().split()))
        if len(row) != 9:
            print("Error: Each row must have 9 integers. Please try again.")
            return take_input() 
        for idx, x in enumerate(row):
            if x == 0:
                matrix[(i, idx)] = matrix[(i, idx)].union({1, 2, 3, 4, 5, 6, 7, 8, 9})
            else:
                matrix[(i, idx)] = matrix[(i, idx)].union({x})
    return matrix

if __name__ == '__main__':
    board = take_input()
    s = Solver(board=board)
    s.solve()
    print(s.board)

