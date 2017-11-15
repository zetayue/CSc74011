#DFBnB search algorithm

from State import *
from Queue import LifoQueue
import numpy as np
import time

def DFB(state,goal,bound = 100000,heuristic=hManhattan):
    '''DFBnB search algorithm
       state:= the starting state
       goal:= the goal state
       bound:= bound value
       heuristic:= heuristics method used
    '''
    start_time = time.time()                      #timer
    openlist = LifoQueue()                        #store the fringe in openlist with LifoQueue
    closelist = []                                #store the node expanded in closelist
    openlist.put(state)                           #store the start state in openlist
    state.hval = heuristics(state,goal,heuristic)
    expandedCount = 0                             #count the # of nodes expanded 
    best_solution = None                          #store the best solution
    optimal_time = None                           #store the optimal time of DFBnB

    while not openlist.empty():
        if (time.time()-start_time) >= 1800:      #terminate when time >= 30 min, 
                print 'Out of time!'
                exit()
        curNode = openlist.get()                  #get the node with the lowest fval to be expanded
        expandedCount = expandedCount + 1         #counter +1
        closelist.append(curNode)                 #store the node in closelist

        if(np.all(curNode.matrix==goal.matrix)):  #check if the current expanded node is goal
            if move.cost < bound:                 #compare new cost with bound
                bound = move.cost                 #if new cost is smaller, update the bound
                best_solution = curNode           #store this node in the best solution
                optimal_time = time.time()-start_time   #store the optimal time so far
        else:
            moves = curNode.extendMove()          #expand the node and store the successors in moves
            
            #If f is greater than bound, discard the node
            moves_g = []
            for move in moves:
                h = heuristics(move,goal,heuristic)
                f = h + move.cost                 #get the f of each node
                if f > bound:
                    continue
                else:
                    move.hval = h
                    moves_g.append(move)
                moves_g.sort(reverse=True)        #Sort remaining node in the order of f.
                
            for move in moves_g:                  #check if the node has already been evaluated
                                                  #if not, store the nodes on top of openlist
                if not ((move in openlist.queue) or (move in closelist)):
                    openlist.put(move)
                elif move in openlist.queue:
                    openlistnode = openlist.queue[openlist.queue.index(move)]
                    if move.cost < openlistnode.cost:
                        openlist.queue.remove(openlistnode)
                        openlist.put(move)
                elif move in closelist:
                    closelistnode = closelist[closelist.index(move)]
                    if move.cost < closelistnode.cost:
                        closelist.remove(closelistnode)
                        openlist.put(move)
            continue

    if not best_solution == None:               #output the optimal path and time
        return best_solution.generatePath([]),expandedCount,(time.time()-start_time),optimal_time
    else:
        return None,(time.time()-start_time)