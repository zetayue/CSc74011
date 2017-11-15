#IDA* search algorithm

from State import *
from Queue import LifoQueue
from DFB import *
import numpy as np
import time

def IDA(state,goal,heuristic=hManhattan):
    '''IDA* search algorithm
       state:= the starting state
       goal:= the goal state
       heuristic:= heuristics method used
    '''
    start_time = time.time()                    #timer
    bound = heuristics(state,goal,heuristic)    #get the initial bound
    flist = []                                  #list of f to update the bound
    solution = None                             #store the solution
    expandedCount = 0                           #count the # of nodes expanded 
                                              
    while solution==None:                     
        openlist = LifoQueue()                  #store the fringe in openlist with LifoQueue
        closelist = []                          #store the node expanded in closelist
        openlist.put(state)                     #store the start state in openlist
                                              
        if len(flist)>1:                        #update the bound with minimum in the flist
            bound = min(flist)
            flist = []
            
        while not openlist.empty():
            if (time.time()-start_time) >= 1800:       #terminate when time >= 30 min, 
                print 'Out of time!'
                exit()
            curNode = openlist.get()            #get the node with the lowest fval to be expanded
            expandedCount = expandedCount + 1   #counter +1
            closelist.append(curNode)           #store the node in closelist
            
            if(np.all(curNode.matrix==goal.matrix)): #check if the current expanded node is goal
                if move.cost < bound:           #compare new cost with bound
                    bound = move.cost           #if new cost is smaller, update the bound
                    solution = curNode          #store this node in the solution
            else:
                moves = curNode.extendMove()        #expand the node and store the successors in moves
                
                #If f is greater than bound, discard the node
                moves_g = []
                for move in moves:
                    h = heuristics(move,goal,heuristic)
                    f = h + move.cost            #get the f of each node
                    if f > bound:
                        flist.append(f)          #add the f to flist if it is greater than bound
                        continue 
                    else:
                        move.hval = h
                        moves_g.append(move)
                    moves_g.sort(reverse=True)   #Sort remaining node in the order of f.

                for move in moves_g:             #check if the node has already been evaluated
                                                 #if not, store the nodes on top of openlist
                    if not ((move in openlist.queue) or (move in closelist)):
                        openlist.put(move)
                    elif move in openlist.queue:
                        openlistnode = openlist.queue[openlist.queue.index(move)]
                        if move.cost < openlistnode.cost:
                            openlist.queue.remove(openlistnode)
                            openlist.put(move)
                        else:
                            continue 
                    elif move in closelist:
                        closelistnode = closelist[closelist.index(move)]
                        if move.cost < closelistnode.cost:
                            closelist.remove(closelistnode)
                            openlist.put(move)
                        else:
                            continue

    return solution.generatePath([]),expandedCount,(time.time()-start_time)