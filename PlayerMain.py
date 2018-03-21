#TO RUN THIS FILE:
#Make sure to change the import statements in MancalaBoard.py and MancalaGUI.py
#from 'from Player import *' to 'from gmr4417 import *'

#Run the following commands (for human vs. custom player):
#execute("MancalaGUI.py")
#player1 = Create_Player(1,PlayerMain.HUMAN)
#player2 = Create_Player(2,PlayerMain.CUSTOM)
#startGame(player1, player2)



from random import *
from decimal import *
from copy import *
from MancalaBoard import *

# a constant
INFINITY = 1.0e400

class Player:
    """ A basic AI (or human) player """
    HUMAN = 0
    RANDOM = 1
    MINIMAX = 2
    ABPRUNE = 3
    CUSTOM = 4
    
    def __init__(self, playerNum, playerType, ply=0):
        """Initialize a Player with a playerNum (1 or 2), playerType (one of
        the constants such as HUMAN), and a ply (default is 0)."""
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply

    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.num)
        
    def minimaxMove(self, board, ply):
        """ Choose the best minimax move.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move 
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValue(nb, ply-1, turn)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def maxValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m) 
            s = opponent.minValue(nextBoard, ply-1, turn)
            #print "s in maxValue is: " + str(s)
            if s > score:
                score = s
        return score
    
    def minValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValue(nextBoard, ply-1, turn)
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s
        return score


    # The default player defines a very simple score function
    # You will write the score function in the MancalaPlayer below
    # to improve on this function.
    def score(self, board):
        """ Returns the score for this player given the state of the board """
        if board.hasWon(self.num):
            return 100.0
        elif board.hasWon(self.opp):
            return 0.0
        else:
            return 50.0

    # You should not modify anything before this point.
    # The code you will add to this file appears below this line.

    # You will write this function (and any helpers you need)
    # You should write the function here in its simplest form:
    #   1. Use ply to determine when to stop (when ply == 0)
    #   2. Search the moves in the order they are returned from the board's
    #       legalMoves function.
    # However, for your custom player, you may copy this function
    # and modify it so that it uses a different termination condition
    # and/or a different move search order.

    #Alpha-Beta pruning is an optimization of the minimax search algorithm. We use two additional values, alpha-
    # which represents the maximum value of lower bound of board state scores and beta- which represents the maximum
    #value of lower bound of board state scores. The algorithm follows the same flow as minimax aside from this addition
    #which allows us to prune away branches which would not yield more optimal results, thus reducing the search space.
    #The following implementation is a modification of the minimax implementation provided above.
    def alphaBetaMove(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        alpha = score
        beta = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  
            nb = deepcopy(board)
            nb.makeMove(self, m)
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minimizeAlphaBeta(nb, ply-1, turn, alpha, beta)
            #highest score obtained from all moves checked is stored
            if s > score:
                move = m
                score = s
        #return the best score and move so far
        return score, move



    def minimizeAlphaBeta(self, board, ply, turn, alpha, beta):
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            #If we have reached maximum move depth, evaluate current board state and return score.
            if ply == 0:
                return turn.score(board)
            opponent = Player(self.opp, self.type, self.ply)
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maximizeAlphaBeta(nextBoard, ply-1, turn, alpha, beta)
            if s < score:
                score = s
            #Beta is minimum upper bound of scores of possible moves.
            #Beta is set to the lowest score found among all processed board states at minimizing step.
            if score < beta:
                beta = score
            #Prune remaining childen/branches when value of minimum upper bound (of score values) falls 
            #below the maximum lower bound 
            if beta <= alpha:
                break;
        return score



    def maximizeAlphaBeta(self, board, ply, turn, alpha, beta):
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            #If we have reached maximum move depth, evaluate current board state and return score.
            if ply == 0:
                return turn.score(board)
            opponent = Player(self.opp, self.type, self.ply)
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minimizeAlphaBeta(nextBoard, ply-1, turn, alpha, beta)
            if s > score:
                score = s
            #Alpha is the maximum lower bound of scores of possible moves.
            #Alpha is set to the highest score found among all procesed board sates at maximizing step.
            if score > alpha:
                alpha = score
            #Prune remaining childen/branches when value of minimum upper bound (of score values) falls 
            #below the maximum lower bound 
            if beta <= alpha:
                break;
        return score



                
    def chooseMove(self, board):
        """ Returns the next move that this player wants to make """
        if self.type == self.HUMAN:
            move = input("Please enter your move:")
            while not board.legalMove(self, move):
                print move, "is not valid"
                move = input( "Please enter your move" )
            return move
        elif self.type == self.RANDOM:
            move = choice(board.legalMoves(self))
            print "[RANDOM]- chose move", move
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimaxMove(board, self.ply)
            print "[MINIMAX]- chose move", move, " with value", val
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alphaBetaMove(board, self.ply)
            print "[ABPRUNE]- chose move", move, " with value", val
            return move
        elif self.type == self.CUSTOM:
            val, move = self.alphaBetaMove(board, 9)
            print "[CUSTOM]- chose move", move, " with value", val
            return move
        else:
            print "Unknown player type"
            return -1



class Create_Player(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """

    def score(self, board):
        """ Evaluate the Mancala board for this player """
        #Heuristic works as follows:
        #- Checks for winning/losing board state. If winning statefound, returns a score of 100 indicating
        #  a sure win. If board state is in a loss configuration, returns score of -100 indicating ceratin loss 
        #- Else the following steps are followed to determine score:
        #- Number of stones in all cups are found for each player
        #- Number of stones in Mancalas are found for each player 
        #- Number of stones in player2's mancala are subtracted from number of stones in player 1's mancala
        #- Number of stones in all cups of player 2 are subtracted from player1's
        #- Results are summed. Higher score equates to a better move according to this heuristic 
        if board.hasWon(self.num):
            return 100
        elif board.hasWon(self.opp):
            return -100
        else:
            dif_mancalas = board.scoreCups[1] - board.scoreCups[0]
            dif_cups = sum(board.getPlayersCups(self.num)) - sum(board.getPlayersCups(self.opp))
            move_score = dif_mancalas + dif_cups
        return move_score
        
