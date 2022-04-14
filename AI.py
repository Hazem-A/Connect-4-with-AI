import pygame
from copy import deepcopy
from Game.Connect import drop_piece,full_column,win_state





def minimax(position,depth,max_player,ai_player):
    if depth == 0 or win_state(position,1) or win_state(position,2):
        return evaluate(position, ai_player), position;

    if max_player:
        maxEval = float('-inf')
        best_position = None
        player = 0
        if ai_player == 1:
            player = 1
        else:
            player = 2
        for i in range (7):
            #check to make sure that the move being made is legal
            temp = position.copy()
            valid = full_column(temp,i)
            if not valid:
                continue
            #drop the piece in the temp board
            temp = drop_piece(temp,i,player-1)
            evaluation = minimax(temp,depth-1,False,ai_player)[0]
            if i == 3:
                evaluation+= 4
            maxEval = max(evaluation,maxEval)
            if maxEval == evaluation:
                best_position=temp
        return maxEval,best_position
    else:
        minEval = float('inf')
        best_position = None
        player = 0
        if ai_player == 1:
            player = 2
        else:
            player = 1
        for i in range (7):
            #check to make sure that the move being made is legal
            temp = position.copy()
            valid = full_column(temp,i)
            if not valid:
                continue
            #drop the piece in the temp board
            temp = drop_piece(temp,i,player-1)
            evaluation = minimax(temp,depth-1,True,ai_player)[0]
            evaluation *= -1
            if i == 3:
                evaluation-= 4
            minEval = min(evaluation,minEval)
            if minEval == evaluation:
                best_position=temp
        return minEval,best_position








def evaluate(board,player):
    #will check to see if the player that just moves made a winning move
    check = 0
    if (player == 1):
        check = 2
        opp = 1
    else:
        check = 1
        opp = 2

    evaluation = 0
    #check horizontally first

    for i in range(6):
        for j in range(4):
            if board[i][j]==check:
                #check to see if any player has won
                if (board[i][j+1]==check and board[i][j+2]==check and board[i][j+3]==check):
                    evaluation += 10000000000;
                    return evaluation
                if (board[i][j+1]==check and board[i][j+2]==check):
                    temp_e = 0
                    temp_e=backtrack_horizontal(board,i,j)
                    if temp_e:
                        evaluation+= temp_e
                        return evaluation
                temp_e = 0
                evaled = False
                temp_e,evaled = eval_line_3_horizontal(board,player,i,j)
                if evaled:
                    evaluation+=temp_e
                    break
                temp_e, evaled = eval_horizontal_line2(board, player, i, j)
                if evaled:
                    evaluation += temp_e
                    break
            elif(board[i][j]==opp):
                if (board[i][j+1]==opp and board[i][j+2]==opp and board[i][j+3]==opp):
                    evaluation -= 100000000000000;
                    return evaluation
                if (board[i][j+1]==opp and board[i][j+2]==opp):
                    temp_e = 0
                    temp_e = backtrack_horizontal_opp(board,i,j)
                    if temp_e:
                        evaluation += temp_e
                        return evaluation
                temp_e = 0
                evaled = False
                temp_e,evaled = eval_line_3_horizontal_opp(board,player,i,j)
                if evaled:
                    evaluation+=temp_e
                    break
                temp_e, evaled = eval_horizontal_line2_opp(board, player, i, j)
                if evaled:
                    evaluation += temp_e
                    break

    #check vertically
    for j in range(7):
        for i in range(3):
            if board[i][j]==check:
                if (board[i+1][j]==check and board[i+2][j]==check and board[i+3][j]==check):
                    evaluation += 10000000
                    return evaluation
                if (board[i+1][j]==check and board[i+2][j]==check and board[i+3][j]!=opp):
                    evaluation+=5
                    break
                if (board[i+1][j]==check and board[i+2][j]!=opp):
                    evaluation+=2
                    break
            elif (board[i][j]==opp):
                if (board[i + 1][j] == opp and board[i + 2][j] == opp and board[i + 3][j] == opp):
                    evaluation -= 100000000
                    return evaluation
                if (board[i+1][j]==opp and board[i+2][j]==opp and board[i+3][j]!=check):
                    evaluation -= 100
                    break
                if (board[i+1][j]==opp and board[i+2][j]!=check):
                    evaluation-=2
                    break

    #check diagonals from bottom left corner going up
    for i in range(3):
        for j in range(4):
            if (board[i][j]==check):
                if (board[i+1][j+1] == check and board[i+2][j+2] == check and board[i+3][j+3] == check):
                    evaluation += 10000000000
                    return evaluation
                temp_e = 0
                evaled = False
                temp_e, evaled = eval_diagonal_positive_3(board, player, i, j)
                if evaled:
                    evaluation += temp_e
                    break
                temp_e, evaled = eval_diagonal_positive_2(board, player, i, j)
                if evaled:
                    evaluation += temp_e
                    break
            elif(board[i][j]==opp):
                temp_e = 0
                evaled = False
                if (board[i+1][j+1] == opp and board[i+2][j+2] == opp and board[i+3][j+3] == opp):
                    evaluation -= 10000000
                    return evaluation
                temp_e, evaled = eval_diagonal_positive_3_opp(board, player, i, j)
                if evaled:
                    evaluation += temp_e
                    break
                temp_e, evaled = eval_diagonal_positive_2_opp(board, player, i, j)
                if evaled:
                    evaluation += temp_e
                    break

    #checks the diagonals starting from the top left corner going down
    j = 0
    i = 5
    while (j < 4):
        while (i > 2):
            if (board[i][j]==check):
                if (board[i-1][j+1] == check and board[i-2][j+2] == check and board[i-3][j+3] == check):
                    evaluation += 10000000000
                    return evaluation
                temp_e = 0
                evaled = False
                temp_e, evaled = evaluate_diagonal_3(board, player, i, j)
                if evaled:
                    evaluation += temp_e
                    break
                temp_e, evaled = evaluate_diagonal_2(board, player, i, j)
                if evaled:
                    evaluation += temp_e
                    break
            elif (board[i][j]==opp):
                temp_e = 0
                evaled = False
                if (board[i-1][j+1] == opp and board[i-2][j+2] == opp and board[i-3][j+3] == opp):
                    evaluation -= 1000000
                    return evaluation
                temp_e, evaled = evaluate_diagonal_3_opp(board, player, i, j)
                if evaled:
                    evaluation += temp_e
                    break
                temp_e, evaled = evaluate_diagonal_2_opp(board, player, i, j)
                if evaled:
                    evaluation += temp_e
                    break
            i-=1
        j+=1
        i=5

    return evaluation






def eval_line_3_horizontal(board,player,i,j):
    evaluation = 0
    evaled = False
    if (player == 1):
        check = 2
        opp = 1
    else:
        check = 1
        opp = 2
    if (board[i][j + 1] == check and board[i][j + 2] == check and board[i][j + 3] != opp):
        evaluation += 5
        evaled=not evaled

    if (board[i][j + 1] != opp and board[i][j + 2] == check and board[i][j + 3] == check):
        evaluation += 5
        evaled = not evaled
    if (board[i][j + 1] == check and board[i][j + 2] != opp and board[i][j + 3] == check):
        evaluation += 5
        evaled = not evaled
    return evaluation, evaled

def eval_horizontal_line2(board,player,i,j):
    evaluation = 0
    evaled = False
    if (player == 1):
        check = 2
        opp = 1
    else:
        check = 1
        opp = 2
    if (board[i][j + 1] == check and board[i][j + 2] != opp and board[i][j + 3] != opp):
        # only check if
        evaluation += 2
        evaled = not evaled

    if (board[i][j + 1] != opp and board[i][j + 2] == check and board[i][j + 3] != opp):
        # only
        evaluation += 2
        evaled = not evaled
    if (board[i][j + 1] != opp and board[i][j + 2] != opp and board[i][j + 3] == check):
        evaluation += 2
        evaled = not evaled
    return evaluation, evaled


def evaluate_diagonal_3(board,player,i,j):
    evaluation = 0
    evaled = False
    if (player == 1):
        check = 2
        opp = 1
    else:
        check = 1
        opp = 2

    if (board[i - 1][j + 1] == check and board[i - 2][j + 2] == check and board[i - 3][j + 3] != opp):
        evaluation += 5
        evaled = not evaled
    if (board[i - 1][j + 1] == check and board[i - 2][j + 2] != opp and board[i - 3][j + 3] == check):
        evaluation += 5
        evaled = not evaled
    if (board[i - 1][j + 1] != opp and board[i - 2][j + 2] == check and board[i - 3][j + 3] == check):
        evaluation += 5
        evaled = not evaled
    return evaluation, evaled

def evaluate_diagonal_2(board,player,i,j):
    evaluation = 0
    evaled = False
    if (player == 1):
        check = 2
        opp = 1
    else:
        check = 1
        opp = 2

    if (board[i - 1][j + 1] == check and board[i - 2][j + 2] != opp and board[i - 3][j + 3] != opp):
        evaluation += 2
        evaled = not evaled
    if (board[i - 1][j + 1] != opp and board[i - 2][j + 2] != opp and board[i - 3][j + 3] == check):
        evaluation += 2
        evaled = not evaled
    if (board[i - 1][j + 1] != opp and board[i - 2][j + 2] == check and board[i - 3][j + 3] != opp):
        evaluation += 2
        evaled = not evaled
    return evaluation, evaled

def eval_diagonal_positive_3(board,player,i,j):
        evaluation = 0
        evaled = False
        if (player == 1):
            check = 2
            opp = 1
        else:
            check = 1
            opp = 2
        if (board[i + 1][j + 1] == check and board[i + 2][j + 2] == check and board[i + 3][j + 3] != opp):
            evaluation += 5
            evaled = not evaled
        if (board[i + 1][j + 1] == check and board[i + 2][j + 2] != opp and board[i + 3][j + 3] == check):
            evaluation += 5
            evaled = not evaled
        if (board[i + 1][j + 1] != opp and board[i + 2][j + 2] == check and board[i + 3][j + 3] == check):
            evaluation += 5
            evaled = not evaled
        return evaluation, evaled


def eval_diagonal_positive_2(board,player,i,j):
        evaluation = 0
        evaled = False
        if (player == 1):
            check = 2
            opp = 1
        else:
            check = 1
            opp = 2
        if (board[i + 1][j + 1] == check and board[i + 2][j + 2] != opp and board[i + 3][j + 3] != opp):
            evaluation += 2
            evaled = not evaled
        if (board[i + 1][j + 1] != opp and board[i + 2][j + 2] != opp and board[i + 3][j + 3] == check):
            evaluation += 2
            evaled = not evaled
        if (board[i + 1][j + 1] != opp and board[i + 2][j + 2] == check and board[i + 3][j + 3] != opp):
            evaluation += 2
            evaled = not evaled
        return evaluation,evaled




#Opponent defined functions

def eval_line_3_horizontal_opp(board,player,i,j):
    evaluation = 0
    evaled = False
    if (player == 1):
        check = 2
        opp = 1
    else:
        check = 1
        opp = 2
    if (board[i][j + 1] == check and board[i][j + 2] == check and board[i][j + 3] != opp):
        evaluation -= 100
        evaled=not evaled

    if (board[i][j + 1] != opp and board[i][j + 2] == check and board[i][j + 3] == check):
        evaluation -= 100
        evaled = not evaled
    if (board[i][j + 1] == check and board[i][j + 2] != opp and board[i][j + 3] == check):
        evaluation -= 100
        evaled = not evaled
    return evaluation, evaled

def eval_horizontal_line2_opp(board,player,i,j):
    evaluation = 0
    evaled = False
    if (player == 1):
        check = 2
        opp = 1
    else:
        check = 1
        opp = 2
    if (board[i][j + 1] == check and board[i][j + 2] != opp and board[i][j + 3] != opp):
        # only check if
        evaluation -= 2
        evaled = not evaled

    if (board[i][j + 1] != opp and board[i][j + 2] == check and board[i][j + 3] != opp):
        # only
        evaluation -= 2
        evaled = not evaled
    if (board[i][j + 1] != opp and board[i][j + 2] != opp and board[i][j + 3] == check):
        evaluation -= 2
        evaled = not evaled
    return evaluation, evaled


def evaluate_diagonal_3_opp(board,player,i,j):
    evaluation = 0
    evaled = False
    if (player == 1):
        check = 2
        opp = 1
    else:
        check = 1
        opp = 2

    if (board[i - 1][j + 1] == check and board[i - 2][j + 2] == check and board[i - 3][j + 3] != opp):
        evaluation -= 100
        evaled = not evaled
    if (board[i - 1][j + 1] == check and board[i - 2][j + 2] != opp and board[i - 3][j + 3] == check):
        evaluation -= 100
        evaled = not evaled
    if (board[i - 1][j + 1] != opp and board[i - 2][j + 2] == check and board[i - 3][j + 3] == check):
        evaluation -= 100
        evaled = not evaled
    return evaluation, evaled

def evaluate_diagonal_2_opp(board,player,i,j):
    evaluation = 0
    evaled = False
    if (player == 1):
        check = 2
        opp = 1
    else:
        check = 1
        opp = 2

    if (board[i - 1][j + 1] == check and board[i - 2][j + 2] != opp and board[i - 3][j + 3] != opp):
        evaluation -= 2
        evaled = not evaled
    if (board[i - 1][j + 1] != opp and board[i - 2][j + 2] != opp and board[i - 3][j + 3] == check):
        evaluation -= 2
        evaled = not evaled
    if (board[i - 1][j + 1] != opp and board[i - 2][j + 2] == check and board[i - 3][j + 3] != opp):
        evaluation -= 2
        evaled = not evaled
    return evaluation, evaled

def eval_diagonal_positive_3_opp(board,player,i,j):
        evaluation = 0
        evaled = False
        if (player == 1):
            check = 2
            opp = 1
        else:
            check = 1
            opp = 2
        if (board[i + 1][j + 1] == check and board[i + 2][j + 2] == check and board[i + 3][j + 3] != opp):
            evaluation -= 100
            evaled = not evaled
        if (board[i + 1][j + 1] == check and board[i + 2][j + 2] != opp and board[i + 3][j + 3] == check):
            evaluation -= 100
            evaled = not evaled
        if (board[i + 1][j + 1] != opp and board[i + 2][j + 2] == check and board[i + 3][j + 3] == check):
            evaluation -= 100
            evaled = not evaled
        return evaluation, evaled


def eval_diagonal_positive_2_opp(board,player,i,j):
        evaluation = 0
        evaled = False
        if (player == 1):
            check = 2
            opp = 1
        else:
            check = 1
            opp = 2
        if (board[i + 1][j + 1] == check and board[i + 2][j + 2] != opp and board[i + 3][j + 3] != opp):
            evaluation -= 2
            evaled = not evaled
        if (board[i + 1][j + 1] != opp and board[i + 2][j + 2] != opp and board[i + 3][j + 3] == check):
            evaluation -= 2
            evaled = not evaled
        if (board[i + 1][j + 1] != opp and board[i + 2][j + 2] == check and board[i + 3][j + 3] != opp):
            evaluation -= 2
            evaled = not evaled
        return evaluation,evaled


def backtrack_horizontal(board,i,j):
    #check to see if there is a two in a row and that the spot to the left of position (i,j) is a winning spot
    temp_e = 0
    if not j:
        return temp_e
    if not i:
        if (board[i-1][j]==0):
            temp_e+=10000000000
            return temp_e
    else:
        if(board[i][j]==0 and board[i-1][j]!=0):
            temp_e+=10000000000
            return temp_e
    return temp_e

def backtrack_horizontal_opp(board,i,j):
    #check to see if there is a two in a row and that the spot to the left of position (i,j) is a winning spot
    temp_e = 0
    if not j:
        return temp_e
    if not i:
        if (board[i-1][j]==0):
            temp_e-=10000000
            return temp_e
    else:
        if(board[i][j]==0 and board[i-1][j]!=0):
            temp_e-=10000000
            return temp_e
    return temp_e



