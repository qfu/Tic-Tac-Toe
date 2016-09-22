# -*- coding: utf-8 -*-
__author__ = 'Qianran Fu,Xueyang Li,Zhengkun Tan'
__email__ = 'qfu@ucsd.edu,xul008@ucsd.edu, z2tan@ucsd.edu'
 
from assignment2 import Player, State, Action
 
class PikachuPlayer(Player):
 
 
    @property
    def name(self):
        """Returns the name of this agent. Try to make it unique!"""
        return 'Pikachu'
 
    def move(self, state):
        """Calculates the absolute best move from the given board position using magic.
        
        Args:
            state (State): The current state of the board.
 
        Returns:
            your next Action instance
        """
 
       #Inialize the depth and the depthMax
        my_move = (state.actions()[0],-20.0)
        
        #depthMax = state.M * state.N - state.ply
        depth Max = 2
        depth = 1
 
        # Flag[0] means find a win move
        # Flag[1] means time out
        # Flage[2] means we have to block 
        Flag = [False,False, False]
 
        # Set the block limit. when reach the limit we need to block the opponent
        block_limit = 0
        if max(state.M - state.K, state.N - state.K) < 2:
            if state.M == state.N and state.M == state.K and state. K == 3:
                block_limit = (state.K - 0.0)/state.K
            else:
                block_limit = (state.K - 1.0)/state.K    
        else:
            block_limit = (state.K - 2.0)/state.K
 
 
        #print "block_limit: ", block_limit
        #If it is the first move, return a random move
        if state.ply < 1:
            return Action(self.color, (state.M/2, state.N/2))
 
        Alert = []
        # A loop ends when the time is up or hit the depth limit
        while not self.is_time_up():
            # Do some thinking here
 
            if self.is_time_up():
                break
            while depth <= depthMax:
                #print "depth is: ", depth
                move = self.do_the_magic(state, depth, Flag, my_move, block_limit, Alert)
 
                # If we have to block opponent, we block it, no need further search
                if Flag[2]:
                    return move[0]
 
                # If it is time out, we need to return the current best move
                if Flag[1]:
                    #print "end"
                    if move is None:
                        return my_move[0]
                    else:
                        return move[0]
 
                # If it is a win move, take it
                if Flag[0]:
                    return move[0]
 
                my_move = move
                #print "tmp get: ", (my_move[0])
                depth += 1
 
            break
        # Time's up, return your move
        # You should only do a small amount of work here, less than one second.
        # Otherwise a random move will be played!
        #print "normal get: ", (my_move[0])
        return my_move[0]
 
 
 
    # function do_the_magic(self, state, depth, Flag, my_premove, block_limit, Alert)
    # return a move 
    # inputs: state
    #         depth: the current depth
    #         Flag: The Flag to indicate different suitation.
    #               Flag [0]: we get a win move
    #               Flage[1]: time out
    #               Flag[2]: we need to block opponent
    #         my_premove: my current best move
    #         Alert: A list hold the block move. it should always be either empty or length of 1
    #         block lmit: if block is Ture and reach the block limit, add it to Alert
    # returns: v: value
    def do_the_magic(self, state, depth, Flag, my_premove, block_limit, Alert):
        # Do the magic, return the first available move!
 
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
        #         alpha
        #         beta
        #         depth: the current depth
        #         me: slef color
        #         opponent: opponent color
        #         Alert: A list hold the block move. it should always be either empty or length of 1
        #         block: indicate is we need to check the block move
        #         block lmit: if block is Ture and reach the block limit, add it to Alert
        # returns: v: value
        def maxValue(state,alpha,beta, depth, me, opponent, Alert, block, block_limit):
 
            # Check if it is time out. Return 100 if it is out of time
            if self.is_time_up():
                #print "max return"
                return 100
 
            # Check if it is terminal
            if state.is_terminal():
                v = state.utility(self)
 
                # We need to convert the lose utility to -10.0. Means it is very very bad
                if v == -1.0:
                    v = -10.0
 
                    # It is the value to indicate the block value, set to 100 make it absulotly out of block limit 
                    y = 100
 
                    # We need to check block
                    if block:
 
                        # If the list has a value, pop it and new location
                        if len(Alert) != 0:
                            Alert.pop()
                            Alert.append((state.last_action.location,y))
                            #print "higher y: ", y, " with location:", state.last_action.location
 
                        # If the list is empty, add it
                        else:
                            Alert.append((state.last_action.location,y)) 
                            #print "Now y:", y, " with location:", state.last_action.location         
                add_transposition(state,v)
                return v
 
            # We reach the depth limit
            if depth == 0:
 
                # We calculate the desirability of the agent
                x = evaluation(state, me, opponent, state.K)
 
                # If time out, quick return
                if x == 100:
                    #print "eva return"
                    return 100
 
                # We check the desirability of the opponent
                y = evaluation(state, opponent, me, state.K)
 
                # If time out, quick return
                if y == 100:
                    #print "eva return"
                    return 100
 
                # If the opponent reach the block limit
                if y >= block_limit:
                    #print "it is alert:", state.last_action.location
 
                    # Add to Alert if we should block it and the list is empty
                    if block and len(Alert) == 0:
                        Alert.append((state.last_action.location,y))
 
                    # Or check if the opponent's desirability is larger than the one in the list
                    # If it is larger, replace it
                    else:
                        if block and y > Alert[0][1]:
                            Alert.pop()
                            Alert.append((state.last_action.location,y))
                            #print "higher y: ", y, " with location:", state.last_action.location
                        #print "Alert of it: ", len(Alert)
 
                    # We return -5.0 to indicate it is kind of bad
                    if y >= block_limit + (1/state.K):
                        return -5.0
 
                # We use this function to get the total desirability of the state. It may be negative
                v = x - 0.5*y
                #print "~~~~~~~~~~~~~~~~~~~~the eval is ", v
 
 
                add_transposition(state,v)
                #print "add to utility: ", v
                return v
 
 
            v = -(float("inf"))
            legalActions = state.actions()
            # Loop through every possible action
            for action in legalActions:
 
                # IF the action is too far from the stones, ignore this move
                if not close(action, state):
                    continue
 
                # Check the transtable
                trans = is_in_table(state.result(action))
                if trans != -10:
                    v = trans
                    #print "max in the tans: ", v
 
                # calculte the value
                else:
                    r = minValue(state.result(action),alpha,beta, depth - 1, me, opponent, Alert, block, block_limit)
 
                    # If time out, quick return
                    if r == 100:
                        #print "min return"
                        return 100
 
                    v= max(r,v)
                if v >= beta:
                    return v
                alpha = max(alpha,v)
                add_transposition(state.result(action),v)
                #print "add in utility: ", v
            return v
 
        # function maxValue(state)
        # the Maximazier 
        # inputs: state
        #         alpha
        #         beta
        #         depth: the current depth
        #         me: slef color
        #         opponent: opponent color
        #         Alert: A list hold the block move. it should always be either empty or length of 1
        #         block: indicate is we need to check the block move
        #         block lmit: if block is Ture and reach the block limit, add it to Alert
        # returns: v: value
        def minValue(state,alpha,beta, depth, me, opponent, Alert, block, block_limit):
 
            # check time out
            if self.is_time_up():
                #print "min return"
                return 100
 
            # check terminal
            if state.is_terminal(): 
                v = state.utility(self)
                if v == -1.0:
                    v = -10.0
                add_transposition(state,v)
                return v
            v = float("inf")
            legalActions = state.actions()
 
            # calculate desirability, same as before
            if depth == 0:
                x = evaluation(state, me, opponent, state.K)
                if x == 100:
                    #print "eva return"
                    return 100
                y = evaluation(state, opponent, me, state.K)
 
                if y == 100:
                    #print "eva return"
                    return 100
                if y >= block_limit+ (1/state.K):
                    return -5.0
                v = x - 0.5*y
                #print "~~~~~~~~~~~~~~~~~~~~the eval is ", v
                add_transposition(state,v)
                #print "the return valu is", v, "at location: ", state.last_action.location
                return v
 
            # Loop to expand the statem same as before
            for action in legalActions:
                if not close(action, state):
                    continue
                trans = is_in_table(state.result(action))
                if trans!= -10:
                    v = trans
                    #print "in the tans: ", v
                else:
                    r = maxValue(state.result(action),alpha,beta, depth-1, me, opponent, Alert, block, block_limit)
                    #print "length of it: ", len(Alert)
                    if r == 100:
                        #print "min return"
                        return 100
 
                    v = min(r,v)
 
                if v <= alpha:
                    return v
                beta = min(beta,v)
                add_transposition(state.result(action),v)
            return v
 
        # function evaluation(state, me, opponent, K)
        # the evaluation
        # inputs: state
        #  me: The self color
        #  opponent: the opponent's color
        #  K: the K-th connected
        # returns: v: value
        def evaluation(state, me, opponent, K):
 
            if self.is_time_up():
                #print "eva return"
                return 100
           # function checkRow(board, me, opponent, K, limit)
           # check the streak along the row direction
           # inputs: board
           #          me: The self color
           #          opponent: the opponent's color
           #          K: the K-th connected
           #          limit: the lower bound
           # returns: the possible number of streak, excluding those cannot achieve K
            def checkRow(board, me, opponent, K, limit = 0):
                board = state.board
                result = 0
                M = len(board)
                N = len(board[0])
                x = 0
                y = 0
 
                pre = 0
 
                # Loop through the loop to get the count
                while x < M:
                    if self.is_time_up():
                        #print "row return"
                        return 100
                    count = 0
                    potential = 0
                    y = 0
                    tmp = 0
                    pre = 0
                    while y < N:
                        if self.is_time_up():
                            #print "row return"
                            return 100
 
                        if board[x] [y] == me:
                            tmp += 1
                            potential += 1
                            if y == N - 1:
                                if potential >= K:
                                    tmp += pre
                                    count = max(count, tmp)
 
                        if board [x] [y] == 0:
                            potential += 1
                            if tmp == 0:
                                y += 1
                                continue
 
                            i = y + 1
                            while potential < K and i < N:
                                if board [x] [i] == opponent or board [x] [y] == 9:
                                    tmp = 0
                                    potential = 0
                                    pre = 0
                                    y = i
                                    break
                                potential += 1
                                i += 1
 
                            if potential >= K:
                                tmp += pre
                                tmp += 0.25
                                count = max(count, tmp)
                                tmp = 0
                            pre = 0.25
 
                        if board [x] [y] == opponent or board [x] [y] == 9:
                            if potential >= K:
                                tmp += pre
                                count = max(count, tmp)
                            pre = 0
                            tmp = 0
                            potential = 0
 
                            if y + 1 >= N - limit:
                                break
 
                        y += 1
 
                    result = max(result, count)
                    x += 1
 
                return result
 
            # function checkColumn(board, me, opponent, K, limit)
            # check the streak along the row direction
            # inputs: board
            #          me: The self color
            #          opponent: the opponent's color
            #          K: the K-th connected
            #          limit: the lower bound
            # returns: the possible number of streak, excluding those cannot achieve K
            def checkColumn(board, me, opponent, K, limit = 0):
                result = 0
                M = len(board)
                N = len(board[0])
                x = 0
                y = 0
                pre = 0
                # Loop through the loop to get the count
                while y < N:
                    if self.is_time_up():
                        #print "col return"
                        return 100
                    count = 0
                    potential = 0
                    x = 0
                    tmp = 0
                    pre = 0
                    while x < M:
                        if self.is_time_up():
                            #print "col return"
                            return 100
                        if board[x] [y] == me:
                            tmp += 1
                            potential += 1
                            if x == M - 1:
                                if potential >= K:
                                    tmp += pre
                                    count = max(count, tmp)
 
                        if board [x] [y] == 0:
                            potential += 1
                            if tmp == 0:
                                x += 1
                                continue
 
                            i = x + 1
                            while potential < K and i < M:
                                if board [i] [y] == opponent or board [x] [y] == 9:
                                    tmp = 0
                                    potential = 0
                                    x = i
                                    pre = 0
                                    break
                                potential += 1
                                i += 1
                            if potential >= K:
                                tmp +=0.25
                                tmp += 0.25
                                count = max(count, tmp)
                                tmp = 0
                            pre = 0.25
 
                        if board [x] [y] == opponent or board [x] [y] == 9:
                            if potential >= K:
                                tmp += pre
                                count = max(count, tmp)
                            if x + 1 >= M - limit:
                                break
                            tmp = 0
                            potential = 0
                            pre = 0
 
                        x += 1
 
                    result = max(result, count)
                    y += 1
 
                return result
 
            # function checkDiag(board, me, opponent, K, limit)
            # check the streak along the row direction
            # inputs: board
            #          me: The self color
            #          opponent: the opponent's color
            #          K: the K-th connected
            #          limit: the lower bound
            # returns: the possible number of streak, excluding those cannot achieve K
            def checkDiag(board, me, opponent, K, limit = 0):
                result = 0
 
                M = len(board)
                N = len(board[0])
 
                if M < limit and N < limit:
                    return 0
 
                x = min (M - limit - 1, M - K )
                y = 0
 
                pre = 0
                # Loop through the loop to get the count
                while x >= 0:
                    if self.is_time_up():
                        #print "d1 return"
                        return 100
                    r = x
                    c = y
 
                    count = 0
                    potential = 0
                    tmp = 0
 
                    pre = 0
                    while r < M and c < N:
                        if self.is_time_up():
                            #print "d1 retun"
                            return 100
                        if board [r] [c] == me:
                            tmp += 1.1
                            potential += 1
                            if r == M -1 or c == N - 1:
                                if potential >= K:
                                    tmp += pre
                                    count = max(count, tmp)
 
                        if board [r] [c] == 0:
                            potential += 1
                            if tmp == 0:
                                r+=1
                                c+=1
                                continue
                            i = r + 1
                            j = c + 1
                            while potential < K and i < M and j < N:
                                if board [i] [j] == opponent or board [x] [y] == 9:
                                    tmp = 0
                                    potential = 0
                                    r = i
                                    c = j
                                    pre = 0
                                    break
                                potential += 1
                                i += 1
                                j += 1
                            if potential >= K:
                                tmp += pre
                                tmp += 0.25
                                count = max(count, tmp)
                                tmp = 0
                            pre = 0.25
 
                        if board [r] [c] == opponent or board [x] [y] == 9:
                            if potential >= K:
                                tmp += pre
                                count = max(count, tmp)
                            tmp = 0
                            pre = 0
                            potential = 0
 
                        r += 1
                        c += 1
 
                    result = max(result, count)
                    x -= 1
 
                x = 0
                y = min (N - limit - 1, N - K) 
 
                # Loop through the loop to get the count
                while y >= 1:
                    if self.is_time_up():
                        #print "d1 return"
                        return 100
                    r = x
                    c = y
 
                    count = 0
                    potential = 0
                    tmp = 0
                    pre = 0
                    while r < M and c < N:
                        if self.is_time_up():
                            #print "d1 return"
                            return 100
                        if board [r] [c] == me:
                            tmp += 1.1
                            potential += 1
                            if r == M -1 or c == N - 1:
                                if potential >= K:
                                    tmp += pre
                                    count = max(count, tmp)
 
                        if board [r] [c] == 0:
                            potential += 1
                            if tmp == 0:
                                r+=1
                                c+=1
                                continue
                            i = r + 1
                            j = c + 1
                            while potential < K and i < M and j < N:
                                if board [i] [j] == opponent or board [x] [y] == 9:
                                    tmp = 0
                                    potential = 0
                                    r = i
                                    c = j
                                    pre = 0
                                    break
                                potential += 1
                                i += 1
                                j += 1
                            if potential >= K:
                                tmp += 0.25
                                tmp += pre
                                count = max(count, tmp)
                                tmp = 0
                            pre = 0.25
 
 
                        if board [r] [c] == opponent or board [x] [y] == 9:
                            if potential >= K:
                                tmp += pre
                                count = max(count, tmp)
                            tmp = 0
                            potential = 0
                            pre = 0
 
                        r += 1
                        c += 1
 
                    result = max(result, count)
                    y -= 1
 
                return result
 
            # function checkReverseDiag(board, me, opponent, K, limit)
            # check the streak along the row direction
            # inputs: board
            #          me: The self color
            #          opponent: the opponent's color
            #          K: the K-th connected
            #          limit: the lower bound
            # returns: the possible number of streak, excluding those cannot achieve K
            def checkReverseDiag(state, me, opponent, K, limit = 0):
                result = 0
                board = state.board
                M = len(board)
                N = len(board[0])
 
                if M < limit and N < limit:
                    return 0
 
                x = max(limit, K - 1) 
                y = 0
                pre = 0
                # Loop through the loop to get the count
                while x < M:
                    if self.is_time_up():
                        #print "d2 return"
                        return 100
                    r = x
                    c = y
 
                    count = 0
                    potential = 0
                    tmp = 0
                    pre = 0
                    while r >= 0 and c < N:
                        if self.is_time_up():
                            #print "d2 return"
                            return 100
                        if board [r] [c] == me:
                            #print r,c
                            tmp += 1.1
                            potential += 1
                            if r == 0 or c == N - 1:
                                if potential >= K:
                                    tmp += pre
                                    count = max(count, tmp)
 
                        if board [r] [c] == 0:
                            potential += 1
                            if tmp == 0.0:
                                r-=1
                                c+=1
                                continue
                            i = r - 1
                            j = c + 1
                            while potential < K and i >= 0 and j < N:
                                if board [i] [j] == opponent or board [x] [y] == 9:
                                    tmp = 0
                                    potential = 0
                                    r = i
                                    c = j
                                    pre = 0
                                    break
                                potential += 1
                                i -= 1
                                j += 1
                            if potential >= K:
                                tmp += pre
                                tmp += 0.25
                                count = max(count, tmp)
                                tmp = 0
                            pre = 0.25
 
                        if board [r] [c] == opponent or board [x] [y] == 9:
                            if potential >= K:
                                tmp += pre
                                count = max(count, tmp)
                            tmp = 0
                            potential = 0
                            pre = 0
 
                        r -= 1
                        c += 1
 
                    result = max(result, count)
                    x += 1
 
                x = M - 1
                y = min(N - limit - 1, N - K)
                # Loop through the loop to get the count
                while y >= 1:
                    if self.is_time_up():
                        #print "d2 return"
                        return 100
                    r = x
                    c = y
 
                    count = 0
                    potential = 0
                    tmp = 0
                    pre = 0
                    while r >= 0 and c < N:
                        if self.is_time_up():
                            #print "d2 return"
                            return 100
                        if board [r] [c] == me:
                            #print r,c
                            tmp += 1.1
                            potential += 1
                            if r ==0  or c == (N - 1):
                                if potential >= K:
                                    count = max(count, tmp)
 
                        if board [r] [c] == 0:
                            potential += 1
                            if tmp == 0:
                                r-=1
                                c+=1
                                continue
                            i = r - 1
                            j = c + 1
                            while potential < K and i >= 0 and j < N:
                                if board [i] [j] == opponent or board [x] [y] == 9:
                                    tmp = 0
                                    potential = 0
                                    r = i
                                    c = j
                                    pre = 0
                                    break
                                potential += 1
                                i -= 1
                                j += 1
                            if potential >= K:
                                tmp += pre
                                tmp += 0.25
                                count = max(count, tmp)
                                tmp = 0
                            pre = 0.25
 
                        if board [r] [c] == opponent or board [x] [y] == 9:
                            if potential >= K:
                                tmp += pre
                                count = max(count, tmp)
                            pre = 0
                            tmp = 0
                            potential = 0
 
                        r -= 1
                        c += 1
 
                    result = max(result, count)
                    y -= 1
                return result
 
           # Get the result the four diffrent counts
            value = checkRow(state.board, me, opponent, K, 0)
            if value == 100:
                #print "check row return"
                return 100
            value = max(value, checkColumn(state.board, me, opponent, K, int(value)))
            if value == 100:
                #print "check row return"
                return 100
            value = max(value, checkDiag (state.board, me, opponent, K, int(value)))
            if value == 100:
                #print "check row return"
                return 100
            value = max(value, checkReverseDiag (state, me, opponent, K, int(value)))
            if value == 100:
                #print "check row return"
                return 100
 
           # return the value
            return (value*1.0)/K
 
 
        # function close(action, state)
        # check the action is too far form the stones
        # inputs: action
        #         state
        # returns: True if a 3*3 are from the current action has any stones
        #          Otherwise, False. It is too far        
        def close(action, state):
            x = action.location [0]
            y = action.location [1]
 
            # The range we want to check
            t = max(x - 1, 0)
            b = min(x + 1, state.M - 1)
            l = max(y - 1, 0)
            r = min(y + 1, state.N - 1)
 
            i = t
            j = l
 
            while i <= b:
                j = l
                while j <= r:
                    if state.board [i] [j] != 0:
                        return True
 
                    j +=1
 
                i+=1
 
            return False
 
 
        me = self.color
        opponent = 3 - me
 
        # start loop all the states and get the best state
        legalActions = state.actions()
        score = my_premove[1]
        alpha = -(float("inf"))
        beta = float("inf")
        block = False
 
        # only when depth limit is 2, do we check the block
        if depth == 2:
            block = True
 
        # current best move
        bestaction = my_premove[0]
 
        # For all possible action
        for action in legalActions:
 
            # skip it if it is too far
            if not close(action, state):
                #print "impossible action: ", action.location
                continue
 
            # Get the state
            nextState = state.result(action)
 
            # IF we win, then take this move
            if nextState.is_win():
                Flag[0] = True
                return (action,100)
            #print "possible action: ", action.location
            prevscore = score
 
            # If time out, then return a move
            if self.is_time_up():
                Flag[1] = True
                #print "oo return"
                if Flag[2]:
                    return (Action(self.color,Alert[0][0]),100)
                return (bestaction,score)    
 
            # do the calculation work        
            r = minValue(nextState,alpha,beta, depth - 1, me, opponent, Alert, block, block_limit)
 
            # Out of time check
            if r == 100:
                Flag[1] = True
                #print "ob return"
                if Flag[2]:
                    return (Action(self.color,Alert[0][0]),100)
                return (bestaction,score)
 
            # If we have to block opponent
            if len(Alert) == 1:
                Flag[2] = True
                continue
                #print "Alert!!!!!!!!!!!"
                #return (Action(self.color,Alert[0][0]),100)
            score = max(score,r)
 
            if score > prevscore:
                bestaction = action 
            #print "!!!!!!!!!!!!depth is", depth
            #print "score is ", score, "the location is: ", bestaction.location
            if score >= beta:
                return (bestaction,score)
            alpha = max(alpha,score)
 
        # We get a block move, must take it
        if len(Alert) == 1:
            #print "Alert!!!!!!!!!!!"
            return (Action(self.color,Alert[0][0]),100)
        return (bestaction, score) 
 
        #return state.actions()[0]