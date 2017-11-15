#A* search algorithm

from State import *
from Queue import PriorityQueue
import time

def AStarsearch(state,goal,heuristic=hManhattan):
    '''A* search algorithm
       state:= the starting state
       goal:= the goal state
       heuristic:= heuristics method used
    '''
    start_time = time.time()                        #timer 
    openlist = PriorityQueue()                      #store the fringe in openlist with PriorityQueue
    closelist = []                                  #store the node expanded in closelist
    openlist.put(state)                             #store the start state in openlist
    expandedCount = 0                               #count the # of nodes expanded 
    
    while not openlist.empty():
        if (time.time()-start_time) >= 1800:        #terminate when time >= 30 min, 
                print 'Out of time!'
                exit()
        curNode = openlist.get()                    #get the node with the lowest fval to be expanded
        expandedCount = expandedCount + 1           #counter +1
        closelist.append(curNode)                   #store the node in closelist
        
        if (np.all(curNode.matrix==goal.matrix)):   #check if the current expanded node is goal
            if len(closelist) > 0:                  #get the results of 8-puzzle
                return curNode.generatePath([]),expandedCount,(time.time()-start_time)
            else:
                return [curNode],expandedCount,(time.time()-start_time)
            
        else:                                       #if the current expanded node is not goal
            moves = curNode.extendMove()            #expand the node and store the successors in moves
            for move in moves:
                h = heuristics(move,goal,heuristic) #get h of each move
                #check if the move has already been evaluated
                if move in openlist.queue: 
                    openlistnode = openlist.queue[openlist.queue.index(move)]
                    if move.cost < openlistnode.cost:
                        openlistnode.cost = move.cost
                        openlistnode.parent = move.parent
                    else:
                        continue 
       
                elif move in closelist:
                    closelistnode = closelist[closelist.index(move)]
                    if move.cost < closelistnode.cost:
                        move.hval = h
                        closelist.remove(closelistnode)
                        openlist.put(move)
                    else:
                        continue 
                else:
                    move.hval = h
                    openlist.put(move)              #store the move in openlist for next loop
        
    return [],0,(time.time()-start_time)