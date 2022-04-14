import numpy as np
import pygame
import sys
import math
from Game.AI import minimax

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

SQUARESIZE = 100


def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

def print_board(board):
	print(np.flip(board, 0))

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
            int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

def full_column(board,column):
    #check to see if a piece can be placed in that column
    i = 5;
    valid = False;
    while (i > -1):
        if (board[i][int(column)]==1 or board[i][int(column)]==2):
            i-=1
        else:
            valid=True
            break

    return valid


def win_state(board,player):
    #will check to see if the player that just moves made a winning move
    check = 0
    game_over = False;
    if (player == 1):
        check = 2
    else:
        check = 1

    #check horizontally first

    for i in range(6):
        for j in range(4):
            if board[i][j]==check:
                if (board[i][j+1]==check and board[i][j+2]==check and board[i][j+3]==check):
                    game_over = True;
                    print("Player " + str(player) + "won")
                    return game_over;

    #check vertically
    for j in range(7):
        for i in range(3):
            if board[i][j]==check:
                if (board[i+1][j]==check and board[i+2][j]==check and board[i+3][j]==check):
                    game_over = True;
                    print("Player " + str(player) + "won")
                    return game_over;

    #check diagonals from bottom left corner going up
    for i in range(3):
        for j in range(4):
            if (board[i][j]==check):
                if (board[i+1][j+1] == check and board[i+2][j+2] == check and board[i+3][j+3] == check):
                    game_over = True;
                    print("Player " + str(player) + " won")
                    return game_over;

    #checks the diagonals starting from the top left corner going down
    j = 0
    i = 5
    while (j < 4):
        while (i > 2):
            if (board[i][j]==check):
                if (board[i-1][j+1] == check and board[i-2][j+2] == check and board[i-3][j+3] == check):
                    game_over = True;
                    print("Player " + str(player) + "won")
                    return game_over;
            i-=1
        j+=1
        i=5

    return game_over

def drop_piece(board,column,player):
    i = 0
    while (i < 7):
        if (board[i][column] == 0):
            if (player == 1):
                board[i][column] = 2

                # # removes column if the piece was placed at the top
                # if (i == 0):
                #     valid_columns.remove(str(column))
                break
            else:
                board[i][column] = 1
                # if (i == 0):
                #     valid_columns.remove(str(column))
                break
        i += 1
    return board

board = create_board()
print_board(board)
game_over = False
turn = 0

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

screen = pygame.display.set_mode(size)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)



while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            # player 2 input

        if event.type == pygame.MOUSEBUTTONDOWN:
            if turn == 1:
                posx = event.pos[0]
                # convert to a column
                col = int(math.floor(posx / SQUARESIZE))

                valid = full_column(board, col)
                if (valid):
                    board = drop_piece(board, col, turn)
                    draw_board(board)
                    game_over = win_state(board, turn)
                    turn = 0
            else:
                break

    if turn == 0 and not game_over:
        value,board = minimax(board,4,True,1)
        print(value)
        draw_board(board)
        game_over = win_state(board, turn)
        turn = 1

    if game_over:
        pygame.time.delay(5000)


