# -*- coding: utf-8 -*-
__author__ = 'Qianran Fu,Xueyang Li,Zhengkun Tan'
__email__ = 'qfu@ucsd.edu,xul008@ucsd.edu, z2tan@ucsd.edu'
 
import heapq
 
from assignment2 import Player
 
 
class EvaluationPlayer(Player):
    def move(self, state):
        """Calculates the best move after 1-ply look-ahead with a simple evaluation function.
 
        Args:
            state (State): The current state of the board.
 
        Returns:
            the next move (Action)
        """
 
        # *You do not need to modify this method.*
        best_move = None
        max_value = -1.0
        my_color = state.to_play.color
 
        for action in state.actions():
            if self.is_time_up():
                break
 
            result_state = state.result(action)
            print "result_state",result_state
            value = self.evaluate(result_state, my_color)
            if value > max_value:
                max_value = value
                best_move = action
 
        # Return the move with the highest evaluation value
        return best_move
 
    def evaluate(self, state, color):
        # function pre_action(state,color)
        # get all the indices with the color
        # inputs: state,color
        # returns: indices
        def pre_action(state,color):
            return [(i, j) for i, row in enumerate(state.board)
                    for j,v in enumerate(row) if v == color]
        indices = pre_action(state,color)
 
        # function checkRow(index)
        # check the streak along the row direction
        # inputs: index
        # returns: the possible number of streak
        def checkRow(index):
            dirs = ((1,0),(-1,0))
            count = 0
            for d in dirs:
                x,y = index
                while True:
                    if(x+d[0],y+d[1]) in indices:
                        x += d[0]
                        y += d[1]
                        count += 1
                    else:
                        break
            return count 
        # function checkColumn(index)
        # check the streak along the column direction
        # inputs: index
        # returns: the possible number of streak
        def checkColumn(index):
            dirs = ((0,1),(0,-1))
            count = 0
            for d in dirs:
                x,y = index
                while True:
                    if(x+d[0],y+d[1]) in indices:
                        x += d[0]
                        y += d[1]
                        count += 1
                    else:
                        break
            return count 
        # function checkDiag(index)
        # check the streak along the diagonal direction
        # inputs: index
        # returns: the possible number of streak
        def checkDiag(index):
            dirs = ((-1,1),(1,-1))
            count = 0
            for d in dirs:
                x,y = index
                while True:
                    if(x+d[0],y+d[1]) in indices:
                        x += d[0]
                        y += d[1]
                        count += 1
                    else:
                        break
            return count 
        # function checkReverseDiag(index)
        # check the streak along the other diagonal direction
        # inputs: index
        # returns: the possible number of streak
        def checkReverseDiag(index):
            dirs = ((-1,-1),(1,1))
            count = 0
            for d in dirs:
                x,y = index
                while True:
                    if(x+d[0],y+d[1]) in indices:
                        x += d[0]
                        y += d[1]
                        count += 1
                    else:
                        break
            return count
        # function findValue(indices)
        # find the longest streak
        # inputs: index
        # returns: the largest number of streak
        def findValue(indices):
            returnBuffer = []
            for index in indices:
                returnBuffer.append(max(checkRow(index),checkColumn(index),checkDiag(index),checkReverseDiag(index)))
            return max(returnBuffer) + 1
        return (findValue(indices)* 1.0)/state.K
        findValue(indices)