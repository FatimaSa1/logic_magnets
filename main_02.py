from copy import deepcopy
from collections import deque
from queue import LifoQueue

class LogicMagnetsGame:
    def __init__(self, board_size, num_gray, num_purple, num_red, board_customized):
        self.board_size = board_size
        self.total_pieces = num_red + num_gray + num_purple
        self.target_positions = [] #set()

        self.board = board_customized
        self.target_positions = self.initialize_board(board_customized)
        self.states = []
        self.states.append(board_customized)
        self.final_solution = []

    def initialize_board(self, board_customized):
        target_positions = [] #set()
        for row_index, row in enumerate(board_customized):
            for col_index, element in enumerate(row):
                if element == 'W':
                    # target_positions.add((row_index, col_index))
                    target_positions.append((row_index, col_index))
                    self.board[row_index][col_index] = ' '
                elif element == 'GG':
                    # target_positions.add((row_index, col_index))
                    target_positions.append((row_index, col_index))
                    self.board[row_index][col_index] = 'G'   
                elif element == 'RR':
                    # target_positions.add((row_index, col_index))
                    target_positions.append((row_index, col_index))
                    self.board[row_index][col_index] = 'R'
                elif element == 'PP':
                    # target_positions.add((row_index, col_index))
                    target_positions.append((row_index, col_index))
                    self.board[row_index][col_index] = 'P'
        return target_positions

    def check_final_solution(self):
        for (x, y) in self.target_positions:
            if self.board[x][y] == ' ':
                return False
        return True

    def move_piece(self, current_x, current_y, new_x, new_y):
        piece = self.board[current_x][current_y]
        if piece not in ['R', 'P']:
            print("Error! Please select Only red or purple pieces to move :(")
            return False

        if not self.can_move_to(piece, new_x, new_y):
            return False
        # تغيير المكان 
        self.board[current_x][current_y] = ' '
        self.board[new_x][new_y] = piece

        # تأثير القطعة يلي نقلتا
        if piece == 'R':
            self.attract_gray_pieces(new_x, new_y)
        elif piece == 'P':
            self.push_gray_pieces(new_x, new_y)

        return True
    
    # def attract_gray_pieces(self, x, y):
    #     for i in range(self.board_size):
    #         if self.board[x][i] == 'G':
    #             self.move_gray_piece(x, i, x, y)
    #         if self.board[i][y] == 'G':
    
    def attract_gray_pieces(self, x, y):
        for i in range(y+1, self.board_size, +1):
            # if self.board[x][i] == 'G':
            if self.board[x][i] != ' ':
                self.move_gray_piece(x, i, x, y)
        # for i in range(y, -1, -1):
        for i in range(y-1, -1, -1):
            # if self.board[x][i] == 'G':
            if self.board[x][i] != ' ':
                self.move_gray_piece(x, i, x, y)
        for i in range(x+1, self.board_size, +1):
            # if self.board[x][i] == 'G':
            if self.board[i][y] != ' ':
                self.move_gray_piece(i, y, x, y)
        # for i in range(x, -1, -1):
        for i in range(x-1, -1, -1):
            # if self.board[x][i] == 'G':
            if self.board[i][y] != ' ':
                self.move_gray_piece(i, y, x, y)

    def push_gray_pieces(self, x, y):
        for i in range(self.board_size-1, y, -1):
            # if self.board[x][i] == 'G':
            if self.board[x][i] != ' ':
                self.move_gray_piece(x, i, x, y, push=True)
        for i in range(y):
            # if self.board[x][i] == 'G':
            if self.board[x][i] != ' ':
                self.move_gray_piece(x, i, x, y, push=True)
        for i in range(self.board_size-1, x, -1):
            # if self.board[x][i] == 'G':
            if self.board[i][y] != ' ':
                self.move_gray_piece(i, y, x, y, push=True)
        for i in range(x):
            # if self.board[x][i] == 'G':
            if self.board[i][y] != ' ':
                self.move_gray_piece(i, y, x, y, push=True)

    def move_gray_piece(self, gx, gy, x, y, push=False):
        if x == gx:
            # التحريك عال x
            reference = y
            if gy < reference:
                new_y = gy - 1 if push else gy + 1
            else:
                new_y = gy + 1 if push else gy - 1
            if 0 <= new_y < self.board_size and self.board[x][new_y] == ' ':
                self.board[x][new_y] = self.board[gx][gy]
                self.board[gx][gy] = ' '
                self.states.append(deepcopy(self.board))
                # self.board[x][new_y] = 'G'
        elif y == gy:
            # التحريك عال y
            reference = x
            if gx < reference:
                new_x = gx - 1 if push else gx + 1
            else:
                new_x = gx + 1 if push else gx - 1
            if 0 <= new_x < self.board_size and self.board[new_x][y] == ' ':
                self.board[new_x][y] = self.board[gx][gy]
                self.board[gx][gy] = ' '
                self.states.append(deepcopy(self.board))
                # self.board[new_x][y] = 'G'

    def can_move_to(self, piece, new_x, new_y):
        if 0 <= new_x < self.board_size and 0 <= new_y < self.board_size:
            if self.board[new_x][new_y] == ' ':
                return True
            else:
                print("Error! Invalid move - The destination is not empty :(")
        else:
            print("Error! Invalid move - The destination is out of bounds/range :(")
        return False

    def generate_all_possible_states(self):
        pass

    def compare_two_states(self):
        pass

    def generate_possible_moves(self):

        curr_positions = []
        able_positions = []
        new_states = []

        for row_index, row in enumerate(self.board):
            for col_index, element in enumerate(row):
                if element in ['R', 'P']:
                    curr_positions.append((row_index, col_index))
        for curr_position in curr_positions:
            for new_x, row1 in enumerate(self.board):
                for new_y, element1 in enumerate(row1):
                    if self.can_move_to(curr_position, new_x, new_y):
                        # able_positions.append(((curr_position[0], curr_position[1]), (new_x, new_y)))
                        able_positions.append((curr_position, (new_x, new_y)))

        # print(able_positions)

        return able_positions

    def apply_move(self, move):
        #(current_x, current_y) = curr[0]
        #(new_x, new_y) = move
        (current_x, current_y), (new_x, new_y) = move

        new_game_state = deepcopy(self)
        new_game_state.move_piece(current_x, current_y, new_x, new_y)
        return new_game_state

   

class LogicMagnetsUI:
    def __init__(self, board=None):
        self.game = None

    # def get_board_information(self):
    #     try:
    #         board_size = int(input("Enter board size (n x n): "))
    #         num_gray = int(input("Enter number of gray pieces: "))
    #         num_purple = int(input("Enter number of purple pieces: "))
    #         num_red = int(input("Enter number of red pieces: "))
    #         return board_size, num_gray, num_purple, num_red
    #     except ValueError:
    #         print("Error! Please enter numbers only :(")
    #         return self.get_board_information()

    def initialize_game(self, board_customized):
        board_size = len(board_customized)

        num_red = 0
        count_target = 0
        num_gray = 0
        num_purple = 0
        for row in board_customized:
            # نحسب عدد كل نوع
            for element in row:
                if element == 'R':
                    num_red += 1
                elif element == '.':
                    count_target += 1
                elif element == 'G':
                    num_gray += 1
                elif element == 'P':
                    num_purple += 1

        self.game = LogicMagnetsGame(board_size, num_gray, num_purple, num_red, board_customized)

    def display_board(self):
        indecies = [i for i in range(self.game.board_size)]
        row_to_print = ['x']
        for i in (indecies):
            row_to_print.append(str(i))
            #row_to_print.append("  ,")
        print(row_to_print)
        row_to_print = []
        for i in range(self.game.board_size):
            row_to_print.append(str(i))
            #row_to_print.append("  ,")

            for j in range(self.game.board_size):
                cell = self.game.board[i][j]
                if (i, j) in self.game.target_positions:
                    if cell == ' ':
                        row_to_print.append('_')
                    else:
                        row_to_print.append(cell+cell)
                else:
                    row_to_print.append(cell)
                #row_to_print.append("  ,")
            print(row_to_print)
            row_to_print = []

    def play(self, board_customized, Automatic = True):
        if Automatic:
            self.initialize_game(board_customized)
            solutions = self.bfs_solve()
            game_copy = deepcopy(self.game)
            for index, solution_path in enumerate(solutions):
                self.game = game_copy
                if solution_path:
                    # print(f"Solution {index+1}!")
                    for step, move in enumerate(solution_path, 1):
                        print(f"Step {step}: Move piece from {move[0]} to {move[1]}")
                        self.game = self.game.apply_move(move)
                        self.display_board()#.game.board)
                    print("Congratulations! You have solved the game :)")
                else:
                    print("No solution found")

        else:    
                self.initialize_game(board_customized)
                while True:
                    if not self.game.check_final_solution():
                        self.display_board()
                        
                        current_x, current_y, new_x, new_y = self.get_user_move()
                        if not self.game.move_piece(current_x, current_y, new_x, new_y):
                            print("Invalid move. Please try again :(")
                    else:
                        self.display_board()
                        break
                # self.solve_bfs(board_customized) 
                # print(self.game.final_solution)
                print("Congratulations! You have solved the game :)")
            # for state in self.game.states:
            #     print(state)

        def get_user_move(self):
            try:
                current_x = int(input("Enter current X position of desired piece to move: "))
                current_y = int(input("Enter current Y position of desired piece to move: "))
                new_x = int(input("Enter new X position to move the piece to it: "))
                new_y = int(input("Enter new Y position to move the piece to it: "))
                return current_x, current_y, new_x, new_y
            except ValueError:
                print("Error! Please enter numbers only :(")
                return self.get_user_move()

    def is_state_in_visited(self, state, visited):
        for visited_state in visited:
            if visited_state.board == state.board:
                return True
        return False
    def bfs_solve(self):
        initial_game = self.game
        queue = deque([(initial_game, [])])
        visited = []
        solutions = []
        while queue:
            current_game, path = queue.popleft()
            # print(path)
            # print(current_game.board)

            if current_game.check_final_solution():
                #return path
                solutions.append(path)
            #curr, moves = current_game.generate_possible_moves()
            able_positions = current_game.generate_possible_moves()
            for move in able_positions:
                new_game_state = current_game.apply_move(move)
                if not self.is_state_in_visited(new_game_state, visited) :
                    visited.append(new_game_state)
                    queue.append((new_game_state, path + [move]))

        return solutions 
    

    def dfs_solve(self):
        initial_game = self.game
        stack = [(initial_game, [])]
        visited = []
        solutions = []
        while stack:
            current_game, path = stack.pop()
            # print(path)
            # print(current_game.board)

            if current_game.check_final_solution():
                #return path
                solutions.append(path)
            #curr, moves = current_game.generate_possible_moves()
            able_positions = current_game.generate_possible_moves()
            for move in able_positions:
                new_game_state = current_game.apply_move(move)
                if not self.is_state_in_visited(new_game_state, visited) :
                    visited.append(new_game_state)
                    stack.append((new_game_state, path + [move]))

        return solutions        


if __name__ == "__main__":
    ui = LogicMagnetsUI()
    level_1 = [
        [' ', ' ', ' ', ' '],
        [' ', 'W', 'G', 'W'],
        ['P', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ']
    ]
    level_2 = [
        [' ', ' ', 'W', ' ', ' '],
        [' ', ' ', 'G', ' ', ' '],
        ['W', 'G', 'W', 'G', 'W'],
        [' ', ' ', 'G', ' ', ' '],
        ['P', ' ', 'W', ' ', ' ']
        
    ]
    level_3 = [
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', 'W'],
        [' ', ' ', 'G', ' '],
        ['P', ' ', ' ', 'W']
    ]
    level_4 = [
        ['W', ' ', 'W', ' ', ' '],
        [' ', 'G', ' ', ' ', ' '],
        ['P', ' ', ' ', ' ', ' '],
        [' ', 'G', ' ', ' ', ' '],
        [' ', 'W', ' ', ' ', ' '] 
    ]
    level_5 = [
        ['W', ' ', 'W', ' '],
        ['GG', ' ', 'GG', ' '],
        ['G', ' ', 'G', ' '],
        ['W', 'P', ' ', ' ']
    ]
    level_6 = [
        [' ', ' ', ' ', 'W', ' '],
        [' ', 'G', 'W', 'G', ' '],
        ['P', ' ', ' ', 'W', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '] 
    ]
    level_7 = [
        ['W', ' ', ' ', ' ', ' '],
        ['GG', ' ', ' ', ' ', ' '],
        ['G', 'P', ' ', 'W', ' '],
        [' ', 'G', 'GG', ' ', ' '],
        [' ', ' ', ' ', 'W', ' ']
    ]
    level_8 = [
        ['W', ' ', 'W', ' '],
        [' ', 'G', 'G', ' '],
        ['P', ' ', 'W', ' '],
        [' ', ' ', ' ', ' ']
    ]
    level_9 = [
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['P', 'W', ' ', 'GG', ' ', 'G', 'W'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ']  
    ]
    level_10 = [
        ['P', ' ', ' ', ' '],
        [' ', 'W', ' ', 'W'],
        [' ', ' ', 'G', 'G'],
        ['W', 'G', ' ', 'W']
    ]
    level_11 = [
        ['G', 'W', 'W', 'W', 'G'],
        [' ', ' ', 'R', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '] 
    ]
    level_12 = [
        ['G', ' ', ' ', ' ', ' '],
        ['GG', ' ', ' ', ' ', ' '],
        ['W', ' ', ' ', ' ', ' '],
        [' ', 'R', ' ', ' ', ' '],
        ['W', ' ', 'W', 'G', ' ']
    ]
    level_13 = [
        ['G', ' ', ' ', 'W', 'GG', 'G'],
        [' ', 'W', ' ', ' ', ' ', ' '],
        [' ', 'W', ' ', 'R', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ']   
    ]
    level_14 = [
        [' ', ' ', ' ', 'G'],
        ['W', ' ', 'W', ' '],
        ['G', 'W', 'W', ' '],
        ['G', ' ', ' ', 'R']
    ]
    level_15 = [
        ['W', 'G', 'W', 'G', ' '],
        [' ', ' ', 'P', ' ', 'W'],
        [' ', ' ', 'R', ' ', 'W'],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ']  
    ]
    level_16 = [
        [' ', ' ', ' ', 'W', 'W'],
        [' ', ' ', 'G', ' ', ' '],
        ['R', ' ', ' ', ' ', 'P'],
        [' ', ' ', 'G', ' ', ' '],
        ['W', ' ', ' ', 'W', ' '] 
    ]
    level_17 = [
        ['R', ' ', 'G', ' '],
        [' ', 'W', ' ', 'W'],
        ['G', ' ', 'W', ' '],
        [' ', 'W', ' ', 'P']
    ]
    level_18 = [
        [' ', ' ', ' ', 'G', ' ', ' '],
        [' ', ' ', ' ', 'W', ' ', ' '],
        ['G', 'W', 'W', 'W', ' ', 'GG'],
        [' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', 'R', 'P', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ']   
    ]
    level_19 = [
        [' ', 'G', 'P', 'G', ' '],
        ['W', ' ', ' ', ' ', 'W'],
        [' ', 'W', 'R', ' ', ' '],
        ['W', ' ', 'W', ' ', 'W'],
        [' ', 'G', ' ', 'G', ' '] 
    ]
    level_20 = [
        [' ', 'GG', 'G', 'W', ' '],
        ['W', ' ', ' ', ' ', ' '],
        ['W', ' ', ' ', ' ', ' '],
        ['W', ' ', ' ', ' ', ' '],
        ['G', ' ', 'P', 'R', ' '] 
    ]
    level_21 = [
        [' ', 'G', 'W', ' '],
        ['W', 'GG', 'G', ' '],
        ['PP', 'W', ' ', 'R'],
        [' ', ' ', ' ', ' ']
    ]
    level_22 = [
        ['P', 'W', ' ', 'GG', 'G'],
        ['W', ' ', ' ', ' ', 'W'],
        [' ', 'W', ' ', ' ', ' '],
        ['G', ' ', 'R', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '] 
    ]
    level_23 = [
        [' ', ' ', 'W', 'G', ' '],
        [' ', ' ', ' ', ' ', 'G'],
        ['G', 'W', 'W', 'W', ' '],
        [' ', ' ', 'RR', ' ', 'P'],
        [' ', ' ', ' ', ' ', ' '] 
    ]
    level_24 = [
        [' ', 'G', ' ', 'W', ' '],
        [' ', ' ', ' ', 'G', 'P'],
        [' ', 'W', ' ', 'W', ' '],
        ['R', ' ', ' ', ' ', 'G'],
        [' ', 'W', 'W', ' ', ' '] 
    ]
    level_25 = [
        ['GG', ' ', ' ', 'RR', ' '],
        [' ', ' ', 'G', ' ', ' '],
        ['W', ' ', ' ', ' ', ' '],
        [' ', ' ', 'G', ' ', ' '],
        ['PP', 'W', 'W', 'G', ' ']
    ]
    level_26 = [
        ['R', ' '],
        ['W', 'W']
    ]

    Automatic = True
    
    board_customized = level_3
    # [
    #     [' ', ' ', ' ', 'G'],
    #     ['W', ' ', 'W', ' '],
    #     ['G', 'W', 'W', ' '],
    #     ['G', ' ', ' ', 'R']
    # ]
    ui.play(board_customized, Automatic)


