cost = {
    'pawn': 1,
    'rook': 4,
    'knight': 3,
    'bishop': 4,
    'queen': 5,
    'king': 10
}
board = [['1  ', 'wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
         ['2  ', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
         ['3  ', '. ', '. ', '. ', '. ', '. ', '. ', '. ', '. '],
         ['4  ', '. ', '. ', '. ', '. ', '. ', '. ', '. ', '. '],
         ['5  ', '. ', '. ', '. ', '. ', '. ', '. ', '. ', '. '],
         ['6  ', '. ', '. ', '. ', '. ', '. ', '. ', '. ', '. '],
         ['7  ', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
         ['8  ', 'bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
         ['   ', ' A', ' B', ' C', ' D', ' E', ' F', ' G', ' H']]

turn = 0
checkmate = False

# function to find if board has checkmated - TODO

# prints the chess board
def print_board(board):
    print("--------------------------------------")
    print("Output: ")
    for row in range(len(board)):
        for col in range(len(board[row])):
            print(board[row][col], end=' ')
        print('')
    print("--------------------------------------")
# 
def is_valid_move_pawn(prev_row, prev_col, new_row, new_col, board):
    # check if the pawn is moving straight ahead
    pawn_color = board[prev_row][prev_col][0]
    
    # Check if the move is a valid pawn move
    if pawn_color == 'b':
        # Check if the white pawn is moving straight ahead
        if prev_col == new_col and board[new_row][new_col] == '. ':
            if prev_row - new_row == 1:
                return True
            # Check if it's the white pawn's first move, it can move 2 squares forward
            elif prev_row == 6 and ((prev_row - new_row) == 2) and board[prev_row - 1][new_col] == '. ':
                return True
            # Check for diagonal attack
        elif abs(prev_col - new_col) == 1 and prev_row - new_row == 1:
            if board[new_row][new_col].strip() != '.' and board[new_row][new_col][0] != pawn_color:
                return True
        return False
    elif pawn_color == 'w':
        # Check if the black pawn is moving straight ahead
        if prev_col == new_col and board[new_row][new_col] == '. ':
            if new_row - prev_row == 1:
                return True
            # Check if it's the black pawn's first move, it can move 2 squares forward
            elif prev_row == 1 and ((new_row - prev_row) == 2) and board[prev_row + 1][new_col] == '. ':
                return True
            # Check for diagonal attack
        elif abs(prev_col - new_col) == 1 and new_row - prev_row == 1:
            if board[new_row][new_col].strip() != '.' and board[new_row][new_col][0] != pawn_color:
                return True
        return False
    return False

def is_valid_move_rook(prev_row, prev_col, new_row, new_col, board):

    prev_pawn_color = board[prev_row][prev_col][0]
    new_location_color = board[new_row][new_col][0]
    if prev_row != new_row and prev_col != new_col:
        return False

    # Check that there are no pieces blocking the rook's path
    if prev_row == new_row:
        # Horizontal move
        min_col = min(prev_col, new_col)
        max_col = max(prev_col, new_col)
        for col in range(min_col + 1, max_col):
            if board[prev_row][col] != '. ':
                return False
    else:
        # Vertical move
        min_row = min(prev_row, new_row)
        max_row = max(prev_row, new_row)
        for row in range(min_row + 1, max_row):
            if board[row][prev_col] != '. ':
                return False

    # Check that the end square is either empty or contains an opposing piece
    if board[new_row][new_col] == '. ' or (prev_pawn_color != new_location_color):
        return True
    else:
        return False

def is_valid_move_bishop(prev_row, prev_col, new_row, new_col, board):
    prev_pawn_color = board[prev_row][prev_col][0]
    new_location_color = board[new_row][new_col][0]
     # Check if the move is diagonal
    if abs(prev_row - new_row) != abs(prev_col - new_col):
        return False

    if (prev_pawn_color != new_location_color):

        # Check if there are any pieces in the way
        row_step = 1 if new_row > prev_row else -1
        col_step = 1 if new_col > prev_col else -1
        current_row, current_col = prev_row + row_step, prev_col + col_step
        
        while (current_row < new_row) or (current_col < new_col):
            if (board[current_row][current_col] != '. '):
                return False
            current_row += row_step
            current_col += col_step

        # Check if the ending position has an opposing piece or is empty, accounting for diagonal attacks
        if (board[new_row][new_col] == '. ' or prev_pawn_color != new_location_color):
            return True
        else:
            return False
    return False

def is_valid_move_knight(prev_row, prev_col, new_row, new_col, board):
    if abs(new_col - prev_col) == 2 and abs(new_row - prev_row) == 1:
        if board[new_row][new_col][0] != board[prev_row][prev_col][0]:
            return True
        
    elif abs(new_col - prev_col) == 1 and abs(new_row - prev_row) == 2:
        if board[new_row][new_col][0] != board[prev_row][prev_col][0]:
            return True
    return False

def is_valid_move_queen(prev_row, prev_col, new_row, new_col, board):
    return is_valid_move_bishop(prev_row, prev_col, new_row, new_col, board) or is_valid_move_rook(prev_row, prev_col, new_row, new_col, board)

def is_valid_move_king(prev_row, prev_col, new_row, new_col, board):
    if abs(new_row - prev_row) <= 1 and abs(new_col - prev_col) <= 1:
        if board[new_row][new_col][0] != board[prev_row][prev_col][0]:
            return True
    # check for castling move
    if abs(new_col - prev_col) == 2:
        return is_valid_castling(prev_row, prev_col, new_row, new_col, board[prev_col][prev_row], board)
    return False

# helper function to parse a move
def parse_moves(move):
    arr = move.split()
    prev_move = arr[0]
    new_move = arr[1]

    return prev_move, new_move

def parse_move_to_index(prev_move, new_move):
    
    prev_row = int(prev_move[1]) - 1
    prev_col = ord(prev_move[0]) - ord('A')
    new_row = int(new_move[1]) - 1
    new_col = ord(new_move[0]) - ord('A')
    
    return prev_row, prev_col, new_row, new_col 
    
# check if prev/new moves are out of range
def is_in_range(move):
    # check if input is formatted
    if len(move.split()) != 2 or len(move) != 5:
        return False
    
    prev_move, new_move = parse_moves(move)
    # True if within range
    if (prev_move[0] >= 'A' and prev_move[0] <= 'H') and (prev_move[1:] >= '1') and (prev_move[1:] <='8') and (new_move[0] >= 'A' and new_move[0] <= 'H') and  (new_move[1:]>= '1') and (new_move[1:]<= '8'):
        return True    
    
    return False

# check if move is valid
def validate_move(prev_row, prev_col, new_row, new_col, board):
    piece = board[prev_row][prev_col]

    # validate all different piece moves
    if piece[1] == 'P':
        return is_valid_move_pawn(prev_row, prev_col, new_row, new_col, board)
    elif piece[1] == 'R':
        return is_valid_move_rook(prev_row, prev_col, new_row, new_col, board)
    elif piece[1] == 'N':
        return is_valid_move_knight(prev_row, prev_col, new_row, new_col, board)
    elif piece[1] == 'B':
        return is_valid_move_bishop(prev_row, prev_col, new_row, new_col, board)
    elif piece[1] == 'Q':
        return is_valid_move_queen(prev_row, prev_col, new_row, new_col, board)
    elif piece[1] == 'K':
        return is_valid_move_king(prev_row, prev_col, new_row, new_col, board)

    return False

# check if input is valid
def validate_input(move, color):

    # check for castling
    if move == '0-0' or move == '0-0-0':
        if (is_valid_castling(move, color, board)):
            update_board_castle(move, color, board)
            return True
        else:
            return False
        
    # if move is within board
    if not is_in_range(move):
        print("not in range")
        return False
    
    # parse row and col into array indices
    prev_move, new_move = parse_moves(move)    
    prev_row, prev_col, new_row, new_col = parse_move_to_index(prev_move, new_move)
    prev_col = prev_col + 1
    new_col = new_col + 1

    piece = board[prev_row][prev_col]
    # if piece is not real
    if piece == '. ':
        return False
    
    if color != board[prev_row][prev_col][0]:
        return False

    # validate piece move
    return(validate_move(prev_row, prev_col, new_row, new_col, board))

# adjust the game board from after move
# TODO: adjust weight for minmax
def update_board(move, board):
    prev_move, new_move = parse_moves(move)    
    prev_row, prev_col, new_row, new_col = parse_move_to_index(prev_move, new_move)

    board[new_row][new_col+1] = board[prev_row][prev_col+1]
    board[prev_row][prev_col+1] = '. '

    return

# check if oposite piece reached end
def is_promotion(board):
    for i, piece in enumerate(board[0]):
        if piece == 'bP':
            board[0][i] = 'bQ'
            
    for i, piece in enumerate(board[7]):
        if piece == 'wP':
            board[7][i] = 'wQ'

def is_valid_castling(move, color, board):
    # Check that the king has not moved before
    if color == 'w':
        king_row = 0
        king_col = 5
        rook_col_1 = 1
        rook_col_2 = 8

    if color == 'b':
        king_row = 7
        king_col = 5
        rook_col_1 = 1
        rook_col_2 = 8
    
    # Check that the king is not in check or passing through check
    if is_in_check(color, board, (king_row, king_col)):
        print("King is in check! ")
        return False
    
    # right side castling
    if move == '0-0':
        # if new position is in check
        if is_in_check(color, board, (king_row, king_col+2)):
            print("King is in check! ")
            return False
        
        if color == 'w':
            if board[king_row][king_col+1] == '. ' and \
                board[king_row][king_col+2] == '. ' and \
                board[king_row][rook_col_2] == color + 'R' and \
                board[king_row][king_col] == color + 'K':
                return True
        else:
            if board[king_row][king_col+1] == '. ' and \
                board[king_row][king_col+2] == '. ' and \
                board[king_row][rook_col_2] == color + 'R' and \
                board[king_row][king_col] == color + 'K':
                return True
    
    # left side castling
    elif move == '0-0-0':
        if is_in_check(color, board, (king_row, king_col-2)):
            print("King is in check! ")
            return False
        if color == 'w':
            if board[king_row][king_col-1] == '. ' and \
                board[king_row][king_col-2] == '. ' and \
                board[king_row][king_col-3] == '. ' and \
                board[king_row][rook_col_2] == color + 'R' and \
                board[king_row][king_col] == color + 'K':
                return True
        else:
            if board[king_row][king_col-1] == '. ' and \
                board[king_row][king_col-2] == '. ' and \
                board[king_row][king_col-3] == '. ' and \
                board[king_row][rook_col_1] == color + 'R' and \
                board[king_row][king_col] == color + 'K':
                return True
            
    return False
def update_board_castle(move, color, board):
    # Check that the king has not moved before
    if color == 'w':
        king_row = 0
        king_col = 5
        rook_col_1 = 1
        rook_col_2 = 8

    if color == 'b':
        king_row = 7
        king_col = 5
        rook_col_1 = 1
        rook_col_2 = 8
    
    # right side castling
    if move == '0-0':
        if color == 'w':
            board[king_row][king_col + 2] = color + 'K'
            board[king_row][king_col + 1] = color + 'R'
            board[king_row][king_col] = '. '
            board[king_row][rook_col_2] = '. '
        elif color == 'b':
            board[king_row][king_col + 2] = color + 'K'
            board[king_row][king_col + 1] = color + 'R'
            board[king_row][king_col] = '. '
            board[king_row][rook_col_2] = '. '
            
    # left side castling
    elif move == '0-0-0':
        if color == 'w':
            board[king_row][king_col - 2] = color + 'K'
            board[king_row][king_col - 1] = color + 'R'
            board[king_row][king_col] = '. '
            board[king_row][rook_col_1] = '. '
        elif color == 'b':
            board[king_row][king_col - 2] = color + 'K'
            board[king_row][king_col - 1] = color + 'R'
            board[king_row][king_col] = '. '
            board[king_row][rook_col_1] = '. '

def is_in_check(color, board, king_pos):
    # Get the color of the king based on its position
    row, col = king_pos

    opposite_color = 'w' if color == 'b' else 'b'

    # check rook and queen
    # horzontal 
    direction = [-1, 1]
    for i in direction:
        col_idx = col + i
        while 0 <= col_idx <= 8:
            if board[row][col_idx][0] == '.':
                col_idx += i
                continue        
            elif board[row][col_idx][0] == opposite_color:
                if board[row][col_idx][1] == 'R' or board[row][col_idx][1] == 'Q':
                    return True
            elif board[row][col_idx][0] == color:
                break
            col_idx += i

    # vertical
    for i in direction:
        row_idx = row + i
        while 0 <= row_idx <= 7:
            if board[row_idx][col][0] == '.':
                row_idx += i
                continue        
            elif board[row_idx][col][0] == opposite_color:
                if board[row_idx][col][1] == 'R' or board[row_idx][col][1] == 'Q':
                    return True
            elif board[row_idx][col][0] == color:
                break
            row_idx += i
    
    # check bishop and queen
    direction = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    for row_idx, col_idx in direction:
        r = row + row_idx
        c = col + col_idx
        while 0 <= c <= 8 and 0 <= r <= 7:
            if board[r][c][0] == ".":
                r += row_idx
                c += col_idx
                continue
            elif board[r][c][0] == opposite_color:
                if board[r][c][1] == 'B' or board[r][c][1] == 'Q':
                    return True
            elif board[r][c][0] == color:
                break
            r += row_idx
            c += col_idx

    # check knight
    direction = [(2, 1), (1, 2), (-1, 2), (-2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)]
    for row_idx, col_idx in direction:
        r = row + row_idx
        c = col + col_idx
        if 0 <= c <= 8 and 0 <= r <= 7:
            if board[r][c][0] == ".":
                continue
            elif board[r][c][0] == opposite_color:
                if board[r][c][1] == 'N':
                    return True
            elif board[r][c][0] == color:
                continue            

    # check pawn
    direction = [(-1, 1), (1, 1)] if color == 'w' else [(-1, -1), (1, -1)]
    for row_idx, col_idx in direction:
        r = row + row_idx
        c = col + col_idx
        if 0 <= c <= 8 and 0 <= r <= 7:
            if board[r][c][0] == ".":
                continue
            elif board[r][c][0] == opposite_color:
                if board[r][c][1] == 'P':
                    return True
            elif board[r][c][0] == color:
                continue
            
    # check king
    direction = [(-1, -1), (0, 1), (-1, 1), (1, 0), (1, 1), (-1, 0), (1, -1)]
    for row_idx, col_idx in direction:        
        r = row + row_idx
        c = col + col_idx
        if 0 <= c <= 8 and 0 <= r <= 7:
            if board[r][c][0] == ".":
                continue
            elif board[r][c][0] == opposite_color:
                if board[r][c][1] == 'K':
                    return True
            elif board[r][c][0] == color:
                continue

    return False

def find_king(board, color):
    for i in range(len(board)):
        for j, piece in enumerate(board[i]):
            if piece == color + 'K':
                return i, j
    return None

# find all legal moves on a board
def is_stalemate(board, player_color):

    # Check if the player has any legal moves left
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col][0] == player_color:
                for new_row in range(len(board)):
                    for new_col in range(len(board[0])):
                        if validate_move(row, col, new_row, new_col, board):
                            return False

    # If there are no legal moves left, then the game is in stalemate
    return True

def is_checkmate(color, board):
    # Get the positions of all pieces of the given color
    positions = []
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece[0] == color:
                positions.append((row, col))

    # Check if the king is in check
    king_pos = next((pos for pos in positions if board[pos[0]][pos[1]][1] == 'K'), None)
    if king_pos is None:
        return True
    if is_in_check(color, board, king_pos):
        # Check if the king can move to a safe square
        for row_idx in range(-1, 2):
            for col_idx in range(-1, 2):
                if row_idx == 0 and col_idx == 0:
                    continue
                r = king_pos[0] + row_idx
                c = king_pos[1] + col_idx
                if 0 <= r <= 7 and 0 <= c <= 8 and board[r][c][0] != color:
                    # Make a copy of the board to test the move
                    temp_board = [row[:] for row in board]
                    temp_board[r][c] = temp_board[king_pos[0]][king_pos[1]]
                    temp_board[king_pos[0]][king_pos[1]] = '.'
                    if not is_in_check(color, temp_board, (r, c)):
                        return False

        # Check if any piece can block or capture the attacking piece
        for pos in positions:
            piece_type = board[pos[0]][pos[1]][1]
            if piece_type == 'K':
                continue
            for row_idx in range(-1, 2):
                for col_idx in range(-1, 2):
                    if row_idx == 0 and col_idx == 0:
                        continue
                    r = pos[0] + row_idx
                    c = pos[1] + col_idx
                    if 0 <= r <= 7 and 0 <= c <= 8 and board[r][c][0] != color:
                        # Make a copy of the board to test the move
                        temp_board = [row[:] for row in board]
                        temp_board[r][c] = temp_board[pos[0]][pos[1]]
                        temp_board[pos[0]][pos[1]] = '.'
                        if not is_in_check(color, temp_board, king_pos):
                            return False

        # If none of the above conditions are met, it's checkmate
        return True

    # If the king is not in check, it's not checkmate
    return False
# print_board(board)
num_players = ''
color_player = ''
color_piece = ''
# main loop
while (not checkmate):

    if not find_king(board, 'w'):
        turn -= 1
        checkmate = False
        break
    if not find_king(board, 'b'):
        turn -= 1
        checkmate = False
        break
    # user enter 1 or 2
    while (num_players != '1' and num_players != '2'):
        num_players = input("Would you like this game to be 1-player or 2 players? (Enter 1 or 2): ")
    # playing against AI: ask for black or white
    if (num_players == '1'):
        while (color_player != 'black' and color_player != 'white'):
            color_player = input("Would you like to be black or white? (Enter black or white): ")
        # play against AI - TODO
    
    turn = 1 if color_player == 'black' else 0
    
    print_board(board)
    if(turn % 2 == 0):
        print('White to play')
        color_piece = 'w'
        turn += 1
    else:
        print('Black to play')
        color_piece = 'b'
        turn += 1

    move = input("Input: ")
    if (not validate_input(move, color_piece)):
        print("invalid move, enter again")
        turn -= 1
        continue
    # after validate the move, update board accordingly
    if(move != '0-0' and move != '0-0-0'):
        update_board(move, board)
    # check for promotion
    is_promotion(board)
    # find current player's king position

    # if checkmate
    if (is_checkmate(color_piece, board)):
        checkmate = False
        break
    # if king not found
    if not find_king(board, color_piece):
        checkmate = False
        break
    else:
        row, col = find_king(board, color_piece)
        # if checkmate
        if (is_checkmate(color_piece, board)):
            checkmate = False
            break
        if(not is_in_check(color_piece, board, (row, col))):
            # check for stalemate
            if is_stalemate(board, color_piece):
                print("Stalemate!")
                print("Draw!")
                checkmate = False
                break

print("Checkmate!")

if(turn % 2 == 0):
    print('Black Win')
else:
    print('White Win')