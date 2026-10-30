import time
import pygame

game_window = None

window_width = 600
window_height = 600

grid_size = 3
grid_width = window_width // grid_size
grid_height = window_height // grid_size


winner = ''

font = None
smallfont = None

game_over = False
x_placed = False
o_placed = False

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

board = None

def initialize_game_values():
    global board
    global game_over
    global x_placed
    global o_placed
    global winner
    global clock

    game_over = False
    x_placed = False
    o_placed = False
    winner = ''

    board = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]

    clock = pygame.time.Clock()

def initialize_game():
    global game_window
    global font
    global smallfont

    initialize_game_values()
    pygame.init()
    game_window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption('tic-tac-toe')

    font = pygame.font.Font(None, 150)
    smallfont = pygame.font.Font(None, 50)
    return game_window

game_window = initialize_game()


def is_winning_move(player, row, col):
    n = len(board)
    if all(board[row][j] == player for j in range(n)):
        return True
    
    if all(board[i][col] == player for i in range(n)):
        return True
    
    if row == col and all(board[i][i] == player for i in range(n)):
        return  True
    
    if row + col == n - 1 and all(board[i][n - i - 1] == player for i in range(n)):
        return True
    return False

def get_empty_position():
    empty_position = []
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == 0:
                empty_position.append((i, j))
    return empty_position

def run_better_algorithm_to_place_0():
    # Simple AI: take center if available, otherwise first empty cell.
    empty_positions = get_empty_position()
    if not empty_positions:
        return False

    center = len(board) // 2
    if board[center][center] == 0:
        board[center][center] = "O"
        return True

    # try to win: place O in a spot that makes O win
    for row, col in empty_positions:
        board[row][col] = "O"
        if is_winning_move("O", row, col):
            return True
        board[row][col] = 0

    # block X if needed
    for row, col in empty_positions:
        board[row][col] = "X"
        if is_winning_move("X", row, col):
            board[row][col] = "O"
            return True
        board[row][col] = 0

    # fallback: first empty
    r, c = empty_positions[0]
    board[r][c] = "O"
    return True
    
def cheak_if_anyone_won():
    global winner

    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != 0:
            winner = board[row][0]
            return True
        
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != 0:
            winner = board[0][col]
            return True
        
    if board[0][0] == board[1][1] == board[2][2] != 0:
        winner = board[0][0]
        return True
    if board[0][2] == board[1][1] == board[2][0] != 0:
        winner = board[0][2]
        return True
    
    return False

def cheak_if_board_is_full():
    for row in range(3):
        for col in range(3):
            if board[row][col] == 0:
                return False
    return True


def cheak_if_draw():
    return not (cheak_if_anyone_won()) and cheak_if_board_is_full()

def draw_game_over_screen():
    game_window.fill(WHITE)
    if winner == "X":
        text = font.render('X wins!', True, BLACK)
    elif winner == "O":
        text = font.render('O wins!', True, BLACK)
    else:
        text = font.render('draw!', True, BLACK)
    
    playagaintext = smallfont.render('play again (y/n)?', True, BLACK)

    game_window.blit(text, (window_width/2 -200,window_height/2 - 100))

    game_window.blit(playagaintext,
                     (window_width/2 - 200, window_height/2 + 50))
    
def draw_game_board_square(row, col):
    rect = pygame.Rect(int(col * grid_width), int(row * grid_height), int(grid_width), int(grid_height))
    pygame.draw.rect(game_window, BLACK, rect, 3)

def draw_the_board():
    for row in range(grid_size):
        for col in range(grid_size):
            draw_game_board_square(row, col)
            # Render letter X
            if (board[row][col] == "X"):
                draw_tic_tac_toe_letter(row, col, 'X')
           # Render letter O
            if (board[row][col] == "O"):
                draw_tic_tac_toe_letter(row, col, 'O')    

    
def draw_tic_tac_toe_letter(row, col, letter):
    letter_peice = font.render(letter, True, BLACK)
    game_window.blit(
        letter_peice, (col * grid_width + grid_width/4,
                       row * grid_height + grid_height/4))
    
def handle_mouse_down_for_x():
    x, y = pygame.mouse.get_pos()
    row = int(y // grid_height)
    col = int(x // grid_width)
    if 0 <= row < grid_size and 0 <= col < grid_size and board[row][col] == 0:
        board[row][col] = "X"

def cheak_for_quit_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_y:
                initialize_game_values()
                game_window.fill(WHITE)
                return True
            elif event.key == pygame.K_n:
                pygame.quit()
                quit()

def run_event_processing():
    global x_placed
    global game_over

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_down_for_x()
            x_placed = True

def cheak_for_win_or_draw():
    global game_over
    global winner
    if (cheak_if_anyone_won()):
        game_over = True
    elif (cheak_if_draw()):
        game_over = True
        winner = 'nobody'
    
    return game_over

while True:
    if game_over:
        pygame.display.flip()
        pygame.time.delay(1000)
        draw_game_over_screen()
        cheak_for_quit_event()

    else:
        game_window.fill(WHITE)
        run_event_processing()
        game_over = cheak_for_win_or_draw()
        draw_the_board()
        pygame.display.flip()

        if game_over:
            continue

        if x_placed:
            pygame.time.delay(500)
            o_placed = run_better_algorithm_to_place_0()
            game_over = cheak_if_anyone_won()
            draw_the_board()
            x_placed = False

    pygame.display.flip()
    clock.tick(60)