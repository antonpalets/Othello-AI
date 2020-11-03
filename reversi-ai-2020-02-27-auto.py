# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 20:05:58 2020

@author: Carl-Fredrik
"""

import numpy as np
import copy
import random
import time

class ReversiBoard:
    def __init__(self,first_player=-1):
        self.player = first_player
        # placed tiles. format: [x,y,colour].
        self.tiles = [[3,3,1], [4,3,-1], [3,4,-1], [4,4,1]]
        self.last_move = None

    def show(self):
        board = np.zeros((8,8),dtype=np.int8)
        for tile in self.tiles:
            board[tile[1],tile[0]] = tile[2]
        print(" 01234567")
        i = 0
        for line in board:
            print(i,end="")
            i += 1
            for point in line:
                if point == 0:
                    print(".",end="")
                elif point == 1:
                    print("o",end="")
                else:
                    print("x",end="")
            print()

    def check_legal(self,colour,x,y):
        if self.place_tile(colour,x,y,check_only=True):
            return 1
        return 0

    def get_legal_moves(self, colour):
        legal = []
        for x in range(8):
            for y in range(8):
                if self.check_legal(colour, x, y):
                    legal.append((x, y, colour))
        return legal

    def place_tile(self, colour, x, y, check_only=False, show_board=False):
        """
        Places a tile of colour `colour` if the move is legal. Terrible design.
        """
        if colour=="w" or colour=="x":
            colour = -1
        elif colour=="b" or colour=="o":
            colour = 1
        col_tiles = [tile for tile in self.tiles if tile[2]==colour and (tile[0] == x or tile[1] == y or (tile[0]-x) == (tile[1]-y) or (tile[0]-x) == (y-tile[1]))]
        #other = [tile for tile in self.tiles if tile[2]!=colour]
        for tile in self.tiles:
            if tile[0] == x and tile[1] == y:
                if check_only:
                    return False
                return
        change_made = False
        changes_to_make = []
        for tile in col_tiles:
            if tile[0] == x:
                #print("X")
                m, M = min(tile[1],y), max(tile[1],y)
                r = range(m+1,M)
                temp = [(j,t) for j, t in enumerate(self.tiles) if t[2]!=colour and t[0] == x and (t[1] in r)]
                #print(temp,r)
                found = False
                if len(temp) == len(r):
                    found = True
                if found:
                    for j,_ in temp:
                        #self.tiles[j][2] = colour
                        changes_to_make.append(j)
                        change_made = True
            elif tile[1] == y:
                #print("Y")
                m, M = min(tile[0],x), max(tile[0],x)
                r = range(m+1,M)
                temp = [(j,t) for j, t in enumerate(self.tiles) if t[2]!=colour and t[1] == y and (t[0] in r)]
                found = False
                if len(temp) == len(r):
                    found = True
                if found:
                    for j,_ in temp:
                        #self.tiles[j][2] = colour
                        changes_to_make.append(j)
                        change_made = True
            elif (tile[0]-x) == (tile[1]-y):
                #print("Z")
                mx, Mx = min(x,tile[0]), max(x,tile[0])
                my, My = min(y,tile[1]), max(y,tile[1])
                rx = range(mx+1,Mx)
                ry = range(my+1,My)
                #print(mx,Mx,my,My)
                temp = [(j,t) for j, t in enumerate(self.tiles) if t[2]!=colour and t[0]-x == t[1]-y and (t[0] in rx) and (t[1] in ry)]
                #print(temp)
                found = False
                if len(temp) == len(rx):
                    found = True
                if found:
                    for j,_ in temp:
                        #self.tiles[j][2] = colour
                        changes_to_make.append(j)
                        change_made = True
            elif (tile[0]-x) == (y-tile[1]):
                #print("Z")
                mx, Mx = min(x,tile[0]), max(x,tile[0])
                my, My = min(y,tile[1]), max(y,tile[1])
                rx = range(mx+1,Mx)
                ry = range(my+1,My)
                #print(mx,Mx,my,My)
                temp = [(j,t) for j, t in enumerate(self.tiles) if t[2]!=colour and t[0]-x == y-t[1] and (t[0] in rx) and (t[1] in ry)]
                #print(temp)
                found = False
                if len(temp) == len(rx):
                    found = True
                if found:
                    for j,_ in temp:
                        #self.tiles[j][2] = colour
                        changes_to_make.append(j)
                        change_made = True
        if change_made:
            if check_only:
                return True
            else:
                self.tiles.append([x,y,colour])
        if check_only:
            return False
        self.player *= -1
        for ind in changes_to_make:
            self.last_move = [x,y,colour]
            self.tiles[ind][2] = colour
        if show_board:
            self.show()

    def score(self, colour=1):
        if colour == "b" or colour == "o":
            colour = 1
        elif colour == "w" or colour == "x":
            colour = -1
        return sum([tile[2] for tile in self.tiles])*colour

    def check_game_over(self):
        temp = False
        for colour in [-1,1]:
            for x in range(8):
                for y in range(8):
                    temp = temp or self.check_legal(colour,x,y)
        if temp:
            return False
        return True

    def play(self, require_keypress_to_exit=False):
        print("x = white, o = black.\nScore is relative to black. (i.e. positive score means black has more tiles")
        print("Coordinates are given as 'x,y' without the quotes.")
        print("To exit the game immediately, enter 'exit' without the quotes")
        self.show()
        print("Current score: {}".format(self.score()))
        colour = -1
        while not self.check_game_over():
            if colour == -1:
                colstr = "white"
            else:
                colstr = "black"
            coordstr = input("Input coordinate, {}: ".format(colstr))
            if coordstr == "exit" or coordstr == "Exit":
                exited = True
                break
            coords = [int(n) for n in coordstr.split(",")]
            while not self.check_legal(colour, *coords):
                coordstr = input("Error: Illegal move.\nInput coordinate, {}: ".format(colstr))
                coords = [int(n) for n in coordstr.split(",")]
            self.place_tile(colour,*coords)
            self.show()
            print("Current score: {}".format(self.score()))
            colour *= -1
        if not exited:
            print("Game over!")
            if self.score() < 0:
                winstr = "White"
            elif self.score > 0:
                winstr = "Black"
            else:
                winstr = "Nobody"
            print("Winner: {}".format(winstr))
            if require_keypress_to_exit:
                input("Input any string to exit...")


class Node:
    def __init__(self, value=0, weight=0, label="", parent=None):
        """
        Creates a node in a tree-like structure.
        
        Parameters
        ----------
        value : number
            Any value meant to be stored as the "value" or "worth" of the node.
        weight : number
            The weight associated with the edge between the node and its parent.
        label : string
            The label to be assigned to the node for a nice string representation.
            In particular, when one prints `Node(value,weight,label)`,
            one will see `label(weight,value)`
        parent : Node
            The parent node. Is None if the node is the start of the tree.
        
        Methods
        -------
        add_child(child)
            Adds the node `child` as a child of self.
        add_children(children)
            Adds the nodes in children as child nodes of self.
        remove_child(child_index)
            Removes the child in the `child_index` position in the list of children.
        create_child(value=0,weight=0)
            Creates a child of self with the given parameters.
        show_children()
            Recursively prints all children and subchildren of the current node.
        list_children()
            Recursively creates a list of all the children and subchildren
            of the current node.
        path_from_root()
            Generates a path in the form of a list from the root of the tree
            to this node. Is the empty list when the node is already the root.
            Uses indexes, so it is sensitive to sorting/reordering.
        get_root()
            Returns the root node of the tree this node is in.
        """
        self.weight = weight
        self.value = value
        self.label = label
        self.parent = parent
        self.other_data = None
        self.children = []
        if parent==None:
            self.depth = 0
        else:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "{}({},{})".format(self.label,self.weight,self.value)

    def __str__(self):
        return "{}({},{})".format(self.label,self.weight,self.value)

    def __getitem__(self,key):
        if type(key)==int:
            return self.children[key]
        elif type(key)==str:
            for child in self.children:
                if child.label == key:
                    return child
            raise KeyError("Not a valid label.")
        elif isinstance(key, list) or isinstance(key, tuple):
            current = self
            for k in key:
                current = current[k]
            return current
        else:
            raise TypeError("The key is not an int or string.")

    def __delitem__(self,key):
        """
        Deletes the child node at position `key` or the first node with label `'key'`.
        """
        if type(key)==int:
            del self.children[key]
        elif type(key)==str:
            for i in range(len(self.children)):
                if self.children[i].label == key:
                    del self.children[i]
                    return
            raise KeyError("Not a valid label.")
        else:
            raise TypeError("The key is not an int or string.")
        

    def add_child(self,child):
        if child.parent == None:
            child.parent = self
            child.depth = self.depth + 1
            self.children.append(child)
        else:
            raise Exception("Children cannot already have a parent.")

    def add_children(self,children):
        for node in children:
            if node.parent==None:
                node.parent=self
                node.depth = self.depth + 1
            else:
                raise Exception("Children cannot already have a parent.")
        self.children.extend(children)
        

    def remove_child(self,child_index):
        del self.children[child_index]

    def create_child(self,value=0,weight=0,label=""):
        self.add_child(Node(value,weight,label))

    def show_children(self):
        if len(self.children) == 0:
            print(self,"--> None")
        else:
            print(self, "-->", *self.children)
            for child in self.children:
                child.show_children()

    def list_children(self):
        """
        Recursively creates a list of all children of the node.
        """
        chlst = []
        if len(self.children) == 0:
            return []
        for child in self.children:
            chlst.append(child)
            chlst.extend(child.list_children())
        return chlst

    def path_from_root(self):
        """
        Generates a list of moves to traverse from the root of the tree to this
        node. Requires that the lists of children for each node in the tree
        has unchanging order, i.e. sorting the children after running this function
        will require running it again to get an accurate path.
        Returns an empty list if it is already the root.
        """
        movelist = []
        if self.parent == None:
            return movelist
        last_node = self
        current_node = self.parent
        while current_node != None:
            for i,child in enumerate(current_node.children):
                if child == last_node:
                    movelist.append(i)
                    last_node = current_node
                    current_node = current_node.parent
                    break
        return movelist[::-1]

    def get_root(self):
        """
        Returns the root of the tree this node is in. Returns `self` if the
        node is already the root.
        """
        current_node = self
        while current_node.parent != None:
            current_node = current_node.parent
        return current_node

    def get_depth(self):
        return len(self.path_from_root())


def get_game_tree(GameBoard, max_depth=5, current_depth=0, starttime=None, maxtime=None):
    tree = Node(label=str(GameBoard.last_move))
    tree.other_data = GameBoard
    legal_moves = GameBoard.get_legal_moves(GameBoard.player)
    if current_depth == max_depth or len(legal_moves) == 0:
        return []
    for move in legal_moves:
        if not (maxtime == None):
            if time.time() - starttime > maxtime:
                break
        NewBoard = ReversiBoard()
        NewBoard.tiles = copy.deepcopy(GameBoard.tiles)
        NewBoard.player *= -GameBoard.player
        #NewBoard.last_move = GameBoard.last_move
        #NewBoard = copy.deepcopy(GameBoard)
        NewBoard.place_tile(move[2],move[0],move[1])
        child = Node(label=str(NewBoard.last_move))
        child.other_data = NewBoard
        child.add_children(get_game_tree(NewBoard, max_depth, current_depth+1))
        tree.children.append(child)
    if current_depth == 0:
        for child in tree.children:
            child.parent = tree
        return tree
    return tree.children

def eval_tree(GameNode, maximizing=True):
    func = lambda n: n.other_data.score()
    if len(GameNode.children) == 0:
        GameNode.value = func(GameNode)
        return
    depth = GameNode.get_depth()
    if not maximizing:
        depth += 1
    for child in GameNode.children:
        eval_tree(child, maximizing)
    if depth % 2: # maximizing
        GameNode.value = max([SubNode.value for SubNode in GameNode.children])
    else: # minimizing
        GameNode.value = min([SubNode.value for SubNode in GameNode.children])

ai_is = 1

scoremat = np.array([[5, -1,  0,  0,  0,  0 ,-1,  5],
                     [-1,-6, -4, -4, -4, -4, -6, -1],
                     [0, -4,  0,  0,  0,  0, -4,  0],
                     [0, -4,  0,  0,  0,  0, -4,  0],
                     [0, -4,  0,  0,  0,  0, -4,  0],
                     [0, -4,  0,  0,  0,  0, -4,  0],
                     [-1,-5, -4, -4, -4, -4, -5, -1],
                     [5, -1,  0,  0,  0,  0, -1,  5]])

def eval_func(node):
    brd = node.other_data
    lgl_mov_1 = len(brd.get_legal_moves(ai_is))
    lgl_mov_2 = len(brd.get_legal_moves(-ai_is))
    tiles_placed = len(brd.tiles)
    if tiles_placed < 40:
        retval = lgl_mov_1 - lgl_mov_2
    else:
        retval = (lgl_mov_1 - lgl_mov_2)*brd.score(ai_is)
    lm = brd.last_move
    return retval + scoremat[lm[1],lm[0]]

def eval_tree2(GameNode, a, b, depth=0, maxdepth=5, maximizing=True, starttime=None, maxtime=None):
    #func = lambda n: n.other_data.score(n.other_data.player)
    func = eval_func
    if not (maxtime == None):
        if time.time() - starttime > maxtime:
            GameNode.value = func(GameNode)
            return
    if len(GameNode.children) == 0 or depth==maxdepth:
        GameNode.value = func(GameNode)
        return
    for child in GameNode.children:
        eval_tree2(child, a, b, depth+1, maxdepth, not maximizing)
    if maximizing:
        v = -np.inf
        for child in GameNode.children:
            v = max(v, child.value)
            a = max(a, v)
            if a >= b:
                break
    else:
        v = np.inf
        for child in GameNode.children:
            v = min(v, child.value)
            b = min(b,v)
            if a >= b:
                break
    GameNode.value = v

def make_choice(GameNode, player_first=True):
    eval_tree(GameNode, player_first)
    for c in GameNode.children:
        if c.value == GameNode.value:
            return c

def make_choice2(GameNode, maximizing=True, max_depth=7, starttime=None, maxtime=None):
    eval_tree2(GameNode, a=-np.inf, b=np.inf, maximizing=maximizing, maxdepth=max_depth, starttime=starttime, maxtime=maxtime)
    for c in GameNode.children:
        if c.value == GameNode.value:
            return c

def play_ai():
    gb = ReversiBoard()
    print("x = white, o = black.\nScore is relative to black. (i.e. positive score means black has more tiles")
    print("Coordinates are given as 'x,y' without the quotes.")
    maxlevel = input("How many steps ahead should the A.I. check at most? (Recommended: 4)\nInput: ")
    maxlevel = int(maxlevel)
    timestr = input("Do you want to restrict the amount of time the A.I. can think? [y/n]\nInput: ")
    if timestr == "Y" or timestr == "y":
        timebool = True
    elif timestr == "N" or timestr == "n":
        timebool == False
    if timebool:
        string = "Note that this is not a hard limit, and in my experience it can sometimes spend up to a little over two times the given time."
        max_time = input("How much time should the A.I. have? (Give in seconds)\n{}\nInput: ".format(string))
        max_time = int(max_time)
    else:
        max_time = None
    startstr = input("Do you want to play first? [y/n]\nInput: ")
    if startstr == "y":
        playerstarted = True
        playerturn = True
        ai_is = 1
    elif startstr == "n":
        playerstarted = False
        playerturn = False
        ai_is = -1
    else:
        print("Invalid answer. Exiting...")
    while not gb.check_game_over():
        gb.show()
        print("Current score: {}".format(gb.score()))
        if playerturn:
            coordstr = input("Input coordinates: ")
            if coordstr == "exit":
                return
            coord = [int(n) for n in coordstr.split(",")]
            while not gb.check_legal(gb.player, *coord):
                coordstr = input("Error: Illegal move.\nInput: ")
                coord = [int(n) for n in coordstr.split(",")]
            gb.place_tile(gb.player, *coord)
        else:
            if timebool:
                stt = time.time()
                time_split = 0.75 # % time that should be spent on tree.
                gt = get_game_tree(gb, max_depth=maxlevel, starttime=time.time(), maxtime=max_time*time_split)
                if gt == []:
                    gb.player *= -1
                else:
                    ch = make_choice2(gt,max_depth=maxlevel, starttime=time.time(), maxtime=max_time*(1-time_split))
                    gb.place_tile(gb.player, ch.other_data.last_move[0], ch.other_data.last_move[1])
                    print("A.I. took {}s to make move".format(time.time() - stt))
                    del ch
            else:
                gt = get_game_tree(gb, max_depth=maxlevel)
                if gt == []:
                    print("A.I. could not make move. Your turn.")
                    gb.player *= -1
                else:
                    ch = make_choice2(gt,max_depth=maxlevel)
                    gb.place_tile(gb.player, ch.other_data.last_move[0], ch.other_data.last_move[1])
                    del ch
            del gt
            print()
        playerturn = not playerturn
    gb.show()
    print("\nGame over!")
    if playerstarted:
        if gb.score() < 0:
            print("You won!")
        elif gb.score == 0:
            print("No one won.")
        else:
            print("You lost...")
    else:
        if gb.score() > 0:
            print("You won!")
        elif gb.score == 0:
            print("No one won.")
        else:
            print("You lost...")

def ai_vs_random():
    gb = ReversiBoard()
    print("x = white, o = black.\nScore is relative to black. (i.e. positive score means black has more tiles")
    maxlevel = input("How many steps ahead should A.I. check at most? (Recommended: 4)\nInput: ")
    maxlevel1 = int(maxlevel)
    timestr = input("Do you want to restrict the amount of time the A.I. 1 can think? [y/n]\nInput: ")
    if timestr == "Y" or timestr == "y":
        timebool1 = True
    elif timestr == "N" or timestr == "n":
        timebool1 = False
    if timebool1:
        max_time1 = input("How much time should the A.I. have? (Give in seconds)\nInput: ")
        max_time1 = int(max_time1)
    else:
        max_time1 = None
    first = input("Should A.I. go first? [y/n]")
    if first == "Y" or first == "y":
        turn = True
        ai_is = -1
    else:
        turn = False
        ai_is = 1
    gb.show()
    print("Current score: {}".format(gb.score()))
    while not gb.check_game_over():
        if turn:
            if timebool1:
                time_split = 0.75 # % time that should be spent on tree.
                gt = get_game_tree(gb, max_depth=maxlevel1, starttime=time.time(), maxtime=max_time1*time_split)
                if gt == []:
                    gb.player *= -1
                else:
                    ch = make_choice2(gt,max_depth=maxlevel1, starttime=time.time(), maxtime=max_time1*(1-time_split))
                    gb.place_tile(gb.player, ch.other_data.last_move[0], ch.other_data.last_move[1])
                    del ch
            else:
                gt = get_game_tree(gb, max_depth=maxlevel1)
                if gt == []:
                    gb.player *= -1
                else:
                    ch = make_choice2(gt,max_depth=maxlevel1)
                    gb.place_tile(gb.player, ch.other_data.last_move[0], ch.other_data.last_move[1])
                    del ch
            del gt
            print()
        else:
            legal_moves = gb.get_legal_moves(-ai_is)
            try:
                choice = legal_moves[random.randint(0, len(legal_moves)-1)]
                gb.place_tile(-ai_is, choice[0], choice[1])
            except:
                continue
            print()
        gb.show()
        print("Current score: {}".format(gb.score()))
        turn = not turn
    print("Game over!")
    if gb.score() < 0:
        print("A.I. 1 won!")
    elif gb.score == 0:
        print("No one won.")
    else:
        print("A.I. 2 won!")

def ai_vs_ai():
    gb = ReversiBoard()
    print("x = white, o = black.\nScore is relative to black. (i.e. positive score means black has more tiles")
    maxlevel = input("How many steps ahead should A.I. 1 check at most? (Recommended: 4)\nInput: ")
    maxlevel1 = int(maxlevel)
    maxlevel = input("How many steps ahead should A.I. 2 check at most? (Recommended: 4)\nInput: ")
    maxlevel2 = int(maxlevel)
    timestr = input("Do you want to restrict the amount of time the A.I. 1 can think? [y/n]\nInput: ")
    if timestr == "Y" or timestr == "y":
        timebool1 = True
    elif timestr == "N" or timestr == "n":
        timebool1 == False
    if timebool1:
        max_time1 = input("How much time should the A.I. have? (Give in seconds)\nInput: ")
        max_time1 = int(max_time1)
    else:
        max_time1 = None
    timestr = input("Do you want to restrict the amount of time the A.I. 2 can think? [y/n]\nInput: ")
    if timestr == "Y" or timestr == "y":
        timebool2 = True
    elif timestr == "N" or timestr == "n":
        timebool2 == False
    if timebool2:
        max_time2 = input("How much time should the A.I. have? (Give in seconds)\nInput: ")
        max_time2 = int(max_time2)
    else:
        max_time2 = None
    turn = True
    gb.show()
    print("Current score: {}".format(gb.score()))
    while not gb.check_game_over():
        if turn:
            ai_is = -1
            if timebool1:
                time_split = 0.75 # % time that should be spent on tree.
                gt = get_game_tree(gb, max_depth=maxlevel1, starttime=time.time(), maxtime=max_time1*time_split)
                if gt == []:
                    gb.player *= -1
                else:
                    ch = make_choice2(gt,max_depth=maxlevel1, starttime=time.time(), maxtime=max_time1*(1-time_split))
                    gb.place_tile(gb.player, ch.other_data.last_move[0], ch.other_data.last_move[1])
                    del ch
            else:
                gt = get_game_tree(gb, max_depth=maxlevel1)
                if gt == []:
                    gb.player *= -1
                else:
                    ch = make_choice2(gt,max_depth=maxlevel1)
                    gb.place_tile(gb.player, ch.other_data.last_move[0], ch.other_data.last_move[1])
                    del ch
            del gt
            print()
        else:
            ai_is = 1
            if timebool2:
                time_split = 0.75 # % time that should be spent on tree.
                gt = get_game_tree(gb, max_depth=maxlevel2, starttime=time.time(), maxtime=max_time2*time_split)
                if gt == []:
                    gb.player *= -1
                else:
                    ch = make_choice2(gt,max_depth=maxlevel2, starttime=time.time(), maxtime=max_time2*(1-time_split))
                    gb.place_tile(gb.player, ch.other_data.last_move[0], ch.other_data.last_move[1])
                    del ch
            else:
                gt = get_game_tree(gb, max_depth=maxlevel2)
                if gt == []:
                    gb.player *= -1
                else:
                    ch = make_choice2(gt,max_depth=maxlevel2)
                    gb.place_tile(gb.player, ch.other_data.last_move[0], ch.other_data.last_move[1])
                    del ch
            del gt
            print()
        gb.show()
        print("Current score: {}".format(gb.score()))
        turn = not turn
    print("Game over!")
    if gb.score() < 0:
        print("A.I. 1 won!")
    elif gb.score == 0:
        print("No one won.")
    else:
        print("A.I. 2 won!")

play_ai()
