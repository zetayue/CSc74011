#Define state in 8-puzzle problem

import numpy as np
import math

def hManhattan(val,goal_val,r,c,goal_r,goal_c):
    '''function to calculate the h function by Manhattan distance'''
    return(abs(r-goal_r)+abs(c-goal_c))

def hMisplace(val,goal_val,r,c,goal_r,goal_c):
    '''function to calculate the h function by the # of misplaced tiles'''
    return(1-int(val==goal_val))
    
def heuristics(state, goal, heuristic):
    '''function to calculate the h function'''
    h = 0
    for r in range(3):
        for c in range(3):
            val  = state.getVal(r,c)
            if val !=0:
                goal_row, goal_col= goal.find(val)
                goal_val = goal.getVal(r,c)
                h = h + heuristic(val,goal_val,r,c,goal_row,goal_col)
            else:
                continue 
    return h

def getString(x):
    '''function to get a string'''
    if x==0:
        return ' '
    else:
        return str(x)

class State:
    '''The State class to represent the 8 puzzle problem'''
    def __init__(self,startstate):
        self.hval = None                 #set the heuristic value
        self.cost = 0                    #set the g value/cost
        self.parent = None               #set the parent node 
        self.matrix = startstate         #store the state
        
    def __str__(self):
        '''function to show the state'''
        s = ''
        for row in range(3):
            s+= ' '.join(map(getString,self.matrix[row]))
            s+= '\r\n'
        return s
        
    def __eq__(self, other):
        '''function to check the equality of two states'''
        if self.__class__ != other.__class__:
            return False
        else:
            return np.all(self.matrix == other.matrix)
            
    def __cmp__(self,other):
        '''function to compare two states according to their f'''
        return cmp((self.hval + self.cost),(other.hval + other.cost))   
        
    def copy(self):
        '''function to make a copy of current state'''
        c = State(self.matrix.copy())
        c.parent = self.parent
        c.hval = self.hval
        c.cost = self.cost
        return c
        
    def getFval(self):
        '''function to get f'''
        return self.hval + self.cost
        
    def getVal(self,r,c):
        '''function to get the value of (row,col) of current state'''
        assert(r <= 2), 'Wrong value for row!'
        assert(c <= 2), 'Wrong value for col!'
        return self.matrix[r,c]
        
    def setVal(self,r,c,val):
        '''function to set the value of (row,col) of current state'''
        assert(r <= 2), 'Wrong value for row!'
        assert(c <= 2), 'Wrong value for col!'
        assert(0<=val <= 8), 'Wrong value for val!'
        self.matrix[r,c] = val
        
    def find(self,val):
        '''function to find the location (row,col) of a value x'''
        assert(0<=val <= 8), 'Wrong value for val!'
        count = 0
        for i in self.matrix.flat:
            if i == val:
                break
            else:
                count = count + 1
        row = count / 3
        col = count % 3
        return row,col 
        
    def swap(self, pos_x, pos_y):
        '''function to swap values at location x and y'''
        temp = self.getVal(*pos_x)
        self.setVal(pos_x[0],pos_x[1],self.getVal(*pos_y))
        self.setVal(pos_y[0],pos_y[1],temp)
        
    def getMoves(self):
        '''function to get next moves of current state'''
        row, col = self.find(0)
        moves = []
        if col < 2:
            moves.append((row,col + 1)) #right
        if row < 2:
            moves.append((row + 1,col)) #down
        if col > 0:
            moves.append((row,col - 1)) #left
        if row > 0:
            moves.append((row - 1,col)) #up
        return moves
        
    def extendMove(self):
        '''function to expand current node'''
        moves = self.getMoves()
        empty_tile = self.find(0)
        
        def generateNode(x,y):
            '''function to genarate one possible move from state'''
            gNode = self.copy()
            gNode.swap(x,y)
            gNode.cost = gNode.cost + 1
            gNode.parent = self
            return gNode
            
        return map(lambda move: generateNode(empty_tile,move),moves)
    
    def generatePath(self,path):
        '''function to genarate the solution path'''
        if self.parent==None:
            return path
        else:
            path.append(self)
            return self.parent.generatePath(path)