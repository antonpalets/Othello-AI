# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 13:37:10 2020

@author: anton palets
"""

import numpy as np
import math as m
import time as time
import random as random

class tree:
    
    def __init__(self, state, nodeVal, children=None):
        assert isinstance(state, tuple)
        # to access the black and white coordinate lists
        self.l, self.r = state
        # to access node value in minimax
        self.val = nodeVal
        #print(type(value))
        self.children = []
        if children is not None:
            for i in children:
                self.newchild(i)
            
    def __repr__(self):
        return '{},{}'.format(self.l, self.r)
    
    def __str__(self):
        return '{},{}'.format(self.l, self.r)
    
    def newchild(self, nodes):
        assert isinstance(nodes, tree)
        self.children.append(nodes)
        
        
class oth:
    
    
    def __init__(self, turn='b', depth=6, game_tot=10, visual=False, human=False, max_time=False):
        
        if isinstance(max_time, float) and max_time>0:
            time2depth(max_time, depth)
        
        bwin, wwin, draws = 0,0,0
        toc_game = 0
        
        for game in range(game_tot):
            b,w,d = oth.play(turn, depth, visual, human)
            bwin += b
            wwin += w
            draws +=d
    
        if game_tot>1:
            
            print('{} game runs over:\n   # of B wins {}\n   # of W wins {}\n   # of draws {}'.format(game_tot, bwin, wwin, draws))

        return None

    
    
    def play(turn=False, depth=6, visual=True, human=True):
        # User friendly way
        if not turn:
            turn = input('Who would you like the AI to play for (type b or w):   ')
            dep_or_t = input('Would you like to give a maximum time per move (for AI) or maximum number of turns (plies) to look ahead? Enter t/m.\nIf you enter a time more than 10 seconds, the AI will use a default depth of 6. Otherwise, the time is converted into a corresponding reasonable depth based on testing.   ')

            if dep_or_t == 'm': 
                depth = int(input('Enter the depth (Suggested 6, at 9 AI takes around 10 seconds per move):  '))
            if dep_or_t == 't':
                max_time = int(input('Enter the maximum time AI can take per move:    '))
                depth = time2depth(max_time, depth)
                
                    
            print('If you would like to play many games, or would like to turn board representation on/off, reffer to the documentation and use the __init__ method passing in relevant parameters')
            
        count = 1
        pl='White (O)'
        if turn == 'w': pl='Black (X)'
        if turn != 'b' and turn!='w': return None 
        print("You're playing as {}".format(pl))
        
       
        
        
        
        if turn == 'b': 
            turn = True
            oppTurn = 2
            myTurn = 1
            inVal = -m.inf
        elif turn == 'w': 
            turn = False
            oppTurn = 1
            myTurn = 2
            inVal = m.inf
        else:
            return None
        bwin, wwin, draws = 0,0,0
        toc_game = 0
        state = tree(([(4,3),(3,4)], [(3,3),(4,4)]), inVal)
        assert isinstance(state, tree)
        check=False
        j=0
        tic_game = time.perf_counter()
        toc_turn = 0
        while not term(state):
            
            # MINIMAX TURN
            if turn and len(actions(state, myTurn))!=0:
                if visual: print('My move:')
                tic_turn = time.perf_counter()
                state = minimax(state, depth, -m.inf, m.inf, True, oppTurn, depth)
                if visual: print(vis(state), '\nTime taken:  {} seconds'.format(time.perf_counter() - tic_turn))
                state=tree(state, 0)
                check=True
                toc_turn += time.perf_counter() - tic_turn
            # HUMAN or RANDOM TURN
            elif not turn and len(actions(state, oppTurn))!=0:
                
                # Initial print forhow the game looks, but only if not minimax is deciding moves
                if len(state.l)+len(state.r)==4 and visual: print(vis((state.l, state.r)))
                act = actions(state, oppTurn)
                # If the moves are inputted as a string, i.e. 'g1'
                if human:
                    move = None
                    # Forces the human to enter moves until they make a legal one
                    while move==None or move not in act:
                        move = move2tup(input('Enter your <{}> move (e.g. g1) :   '.format(pl)))
                        if move not in act: print('Please make a legal move! You have {} legal moves'.format(len(act)))
                    assert isinstance(move, tuple)
                    state = tree(result(state.l, state.r, move, oppTurn), 0)
                    
                else:
                    # For making a random legal move
                    ind = list(range(len(act)))
                    random.shuffle(ind)
                    state = tree(result(state.l, state.r, act[ind[0]], oppTurn), 0)
                    if visual: print('Your move: ')
                    
                if visual: print(vis((state.l, state.r)))
                check=True
            if visual:
                if check:
                    print('Move #{}; Total B(X) = {}; Total W(O) = {}'.format(count, len(state.l), len(state.r)))
                else:
                    j+=1
                    print("The player didn't have a legal move! This has happened {} times".format(j))
            turn = not turn
            count+=1
            check=False
       # avg_turn_time = (0.5*toc_turn)/count  
        toc_game += time.perf_counter() - tic_game
        
        b,w = state.l, state.r
        
        if len(b)>len(w): 
            bwin=1
            print('Black won with score {} against {}.'.format(len(b),len(w)))
        if len(b)<len(w): 
            wwin+=1
            print('White won with score {} against {}.'.format(len(w), len(b)))
        if len(b)==len(w): 
            draws+=1
            print("It's a draw! Both have {} tiles.".format(len(b)))
                
        #avg_game_time = toc_game / game_tot
        return bwin, wwin, draws
        
            
            
            
def time2depth(time, inDepth):
    depth = inDepth
    if time >= 10: print('Too long time, playing on default depth <{}>'.format(depth))
    else:
        if time < 10:    depth = 8
        if time < 1.8:   depth = 7
        if time < 1:     depth = 6
        if time < 0.3:   depth = 5
        if time < 0.15:  depth = 4
        if time < 0.025: depth = 3        
    return depth
        
    
def move2tup(stringmove):
    if len(stringmove) != 2: return None
    col = int(ord(stringmove[0])-97)
    row = int(stringmove[1])-1
    return row, col  

def actions(state, turn):
    assert isinstance(state, tree)
    b = state.l
    w = state.r
    assert isinstance(b, list)
    assert isinstance(w, list)
    act = []
    for i in range(8):
        for j in range(8):
            #move = i,j
            if isinstance(result(b,w, (i,j), turn), tuple): act.append((i,j))
    return act
                            
def term(state):
    assert isinstance(state, tree)
    if len(actions(state,1))==0 and len(actions(state,2))==0: return True
    else: return False

def evl(state, turn):
    b,w = state.l, state.r
    if turn == 1:
        mine, their = b,w
    else:
        their, mine = b,w
    k1, k2, k3 = 2,9, 1.5
    M =   np.array([[30 , -25, 10, 5, 5, 10, -25, 30 ], 
                    [-25, -25, 1 , 1, 1,  1, -25, -25], 
                    [10 ,   1,  5, 2, 2, 5 ,   1, 10 ], 
                    [  5,   1,  2, 1, 1,  2,   1, 5  ],
                    [  5,   1,  2, 1, 1,  2,   1, 5  ],
                    [ 10,   1,  5, 2, 2,  5,   1, 10 ],
                    [-25, -25,  1, 1, 1,  1,  -25, -25], 
                    [ 30, -25, 10, 5, 5, 10, -25, 30 ]])
    if term(tree((b,w), 0)):
        if len(mine) >  len(their): return  m.inf
        if len(mine) <= len(their): return -m.inf
    
    else:     
        
        if len(mine)+len(their) < 32 :
            num_adv = k1*(len(their) - len(mine))
        else:
            num_adv = k2*(len(mine) - len(their))
        pos_adv = k3*(sum(M[i,j] for (i,j) in mine )) #- sum(M[i,j] for (i,j) in their ))
        return pos_adv + num_adv


def minimax(state, depth, alpha, beta, maxPlayer, opp, initDepth):
    
    assert isinstance(state, tree)    
    # Node evaluation if terminal or depth zero
    if depth == 0 or term(state):
        turn = 1
        if opp==1: turn=2
        
        return tree((state.l, state.r), evl(state, turn))
    
    
    me=1
    if opp == 1: me = 2
    # Player AI is playing for
    if maxPlayer:
        state.val = -m.inf 
        # Create legally accesible game state as children of current state
        for (i,j) in actions(state, me): state.newchild(tree(result( state.l, state.r, (i,j), me  ) , state.val))
        for child in state.children:
            child.val = max(child.val, minimax(child, depth-1, alpha, beta, False, opp, initDepth).val )
            alpha = max(alpha, child.val)
            if alpha>=beta: break
        # To pass on the turn to the opponent if there are no legal moves for current player
        if len(state.children)==0: 
            child = state
            child.val = minimax(child, depth-1, alpha, beta, False, opp, initDepth).val
        # Output the game state with the best value to the initial call of minimax
        if depth == initDepth:
            
            state.val = max([child.val for child in state.children])    
            for child in state.children:
                if child.val == state.val: return child.l, child.r
           
         
         
        return tree((child.l, child.r), child.val)
    # AI's opponent
    else:
        state.val = m.inf
        for (i,j) in actions(state, opp): state.newchild(tree(result(state.l, state.r, (i,j), opp ), state.val))
        for child in state.children:    
            child.val = min(child.val, minimax(child, depth-1, alpha, beta, True, opp, initDepth).val )
            beta = min(beta, child.val)
            if alpha>=beta: break
        if len(state.children)==0:
            child = state
            child.val = minimax(child, depth-1, alpha, beta, True, opp, initDepth).val
        
        return tree((child.l, child.r), child.val)
    
        


def vis(state,board=8):
    b,w = state
    pic = ' abcdefgh\n'
    for row in range(0,board):
        pic+='{}'.format(row+1)
        for col in range(0,board):
            if (row, col) not in b and (row, col) not in w: pic += '.'
            elif (row, col) in b: pic += 'X'
            else: pic += 'O'
        pic += '\n'
    return pic
            
    

def result(b, w, move, turn, board=8):
    assert isinstance(b, list)
    assert isinstance(w, list)
    row, col = move
    if turn == 1: 
        mine = b.copy()
        their = w.copy() 
    else:
        mine = w.copy()
        their = b.copy()
    
    
    if (move not in mine) and (move not in their):
    # row right    
        if col+1<board and (row, col+1) in their:
            #print('boo1')
            i = col+2
            while i<board:
                if (row,i) in mine:
                    for j in range(col+1, i):
                        mine.append((row, j))
                        their.remove((row, j))
                    break
                if (row, i) not in mine and (row, i) not in their: break
                i+=1
                
    # row left
        
        if col-1>=0 and (row, col-1) in their:
            #print('boo2')
            i = col-2
            while i >= 0:
                #print('woo')
                if (row,i) in mine:
                    #print('ffs')
                    for j in range(i+1, col):
                        #print('nah man')
                        mine.append((row, j))
                        their.remove((row, j))
                    break
                if (row, i) not in mine and (row, i) not in their: 
                    #print('aaa')
                    break        
                i-=1
                
    # column up
            
        if row-1>=0 and (row-1, col) in their:
            #print('boo3')
            i = row-2
            while i>=0:
                if (i, col) in mine:
                    for j in range(i+1, row):
                        mine.append((j, col))
                        their.remove((j, col))
                    break
                if (i, col) not in mine and (i,col) not in their: break
                i-=1
    
    # column down
    
        if row+1<board and (row+1, col) in their:
            #print('boo4')
            i = row+2
            while i<board:
                if (i, col) in mine:
                    for j in range(row+1, i):
                        mine.append((j, col))
                        their.remove((j, col))
                    break
                if (i, col) not in mine and (i, col) not in their: break
                i+=1
            
            
        # diagonals ... up right
        
        if row-1>=0 and col+1<board and (row-1, col+1) in their:
           # print('boo5')
            i,j = row-2, col+2
            while i>=0 and j < board:
                if (i,j) in mine:
                    k, l = row-1, col+1
                    while k>i and l<j:
                        mine.append((k,l))
                        their.remove((k,l))
                        k-=1
                        l+=1
                    break
                if (i,j) not in mine and (i,j) not in their: 
                    break
                i-=1
                j+=1
        
        # diagonals ... up left
            
        if (row-1, col-1) in their:
            #print('boo6')
            i,j = row-2, col-2
            while i>=0 and j < board:
                if (i,j) in mine:
                    k, l = row-1, col-1
                    while k>i and l>j:
                        mine.append((k,l))
                        their.remove((k,l))
                        k-=1
                        l-=1
                    break
                if (i,j) not in mine and (i,j) not in their: 
                    break
                i-=1
                j-=1
                
                
        # diagonals ... down left
        
        if (row+1, col-1) in their:
            #print('boo7')
            i,j = row+2, col-2
            while i<board and j >= 0:
                if (i,j) in mine:
                    k, l = row+1, col-1
                    while k<i and l>j:
                        mine.append((k,l))
                        their.remove((k,l))
                        k+=1
                        l-=1
                    break
                if (i,j) not in mine and (i,j) not in their: 
                    break
                i+=1
                j-=1
                    
        # diagonals ... down right
        
        if row+1<board and col+1<board and (row+1, col+1) in their:
            #print('boo8')
            i,j = row+2, col+2
            while i<board and j < board:
                if (i,j) in mine:
                    k, l = row+1, col+1
                    while k<i and l<j:
                        mine.append((k,l))
                        their.remove((k,l))
                        k+=1
                        l+=1
                    break
                if (i,j) not in mine and (i,j) not in their: 
                    break
                i+=1
                j+=1
            
    
    
        
        # returns false if illegal move, return tuple of strings with current tiles for each side (black, white). 
        # Note black always first 
            
        if (turn == 1 and mine == b) or (turn == 2 and mine == w): return False
        elif turn == 1: 
            mine.append(move)
            return (mine, their)
        else:
            mine.append(move)
            return (their, mine)
    else: return False
            











# ⚪ ⚫                   