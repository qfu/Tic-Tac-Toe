# -*- coding: utf-8 -*-
__author__ = 'Qianran Fu,Xueyang Li,Zhengkun Tan'
__email__ = 'qfu@ucsd.edu,xul008@ucsd.edu, z2tan@ucsd.edu'
from assignment2 import Player, State, Action
 
class AlphaBetaPlayer(Player):
    def move(self, state):
        #The two function are meant to check
        #if the state is already in the transposition
        #table if so we return v directly 
        transposition_table = {}
        # function add_transposition(state,utility)
        # add into the tt table
        # inputs: state,utility
        # returns: 
        def add_transposition(state,utility):
            s = ''.join(str(i) for i in state.board)
            if transposition_table.get(s) is None:
                transposition_table[''.join(str(i) for i in state.board)] = utility
        # function is_in_table(state)
        # check if in the table
        # inputs: state
        # returns: -10 if not in table; otherwise return the value
        def is_in_table(state):
            s = ''.join(str(i) for i in state.board)
            if transposition_table.get(s) is not None:
                return transposition_table[s]
            else:
                return -10
        # function maxValue(state)
        # the Maximazier 
        # inputs: state
        # returns: v
        def maxValue(state,alpha,beta):
            if state.is_terminal(): 
                return state.utility(self) 
            v = -(float("inf"))
            possibleMoves = state.actions()
            for action in possibleMoves:
                trans = is_in_table(state.result(action))
                if trans != -10:
                    v = trans
                else:
                    v = max(v,minValue(state.result(action),alpha,beta))
                if v >= beta:
                    return v
                alpha = max(alpha,v)
                add_transposition(state.result(action),v)
            return v
        # function minValue(state)
        # the Minimazer
        # inputs: state
        # returns: v
        def minValue(state,alpha,beta):
            if state.is_terminal(): 
                return state.utility(self) 
            v = float("inf")
            possibleMoves = state.actions()
            for action in possibleMoves:
                trans = is_in_table(state.result(action))
                if trans != -10:
                    v = trans
                else:
                    v = min(v,maxValue(state.result(action),alpha,beta))
                if v <= alpha:
                    return v
                beta = min(beta,v)
                add_transposition(state.result(action),v)
            return v
        #start the minimax with alpha-beta pruning 
        possibleMoves = state.actions()
        values = -(float("inf"))
        alpha = -(float("inf"))
        beta = float("inf")
        for action in possibleMoves:
            nextState = state.result(action)
            prevvalues = values
            values = max(values,minValue(nextState,alpha,beta))
            if values > prevvalues:
                bestaction = action 
            if values >= beta:
                return bestaction
            alpha = max(alpha,values)
        return bestaction 