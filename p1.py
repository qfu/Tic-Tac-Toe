# -*- coding: utf-8 -*-
__author__ = 'Qianran Fu,Xueyang Li,Zhengkun Tan'
__email__ = 'qfu@ucsd.edu,xul008@ucsd.edu, z2tan@ucsd.edu'
 
from assignment2 import Player, State, Action
 
class MinimaxPlayer(Player):
    def move(self, state):
        # function maxValue(state)
        # the Maximazier 
        # inputs: state
        # returns: v
        def maxValue(state):
            if state.is_terminal(): 
                return state.utility(self) 
            v = -(float("inf"))
            possibleMoves = state.actions()
            for action in possibleMoves:
                v = max(v,minValue(state.result(action)))
            return v
        # function minValue(state)
        # the Minimazer
        # inputs: state
        # returns: v
        def minValue(state):
            if state.is_terminal(): 
                return state.utility(self) 
            v = float("inf")
            possibleMoves = state.actions()
            for action in possibleMoves:
                v = min(v,maxValue(state.result(action)))
            return v
        #start the minimax algorithm
        possibleMoves = state.actions()
        values = -(float("inf"))
        for action in possibleMoves:
            nextState = state.result(action)
            prevvalues = values
            values = max(values,minValue(nextState))
            if values > prevvalues:
                bestaction = action 
        return bestaction