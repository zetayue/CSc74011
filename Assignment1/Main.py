#Main class to complete the 8-puzzle assignment

from State import *
from AStar import *
from DFB import *
from IDA import *
import numpy as np

def printResults(i,x,y):
    '''function print the results'''
    method_list = ['A*_misplace','A*_Manhattan','IDA*','DFBnB']
    print '================================================'
    print '{0:^20} {1:^20} '.format('Method',method_list[i])
    print '{0:^20} {1:^20} '.format('# of Nodes Expanded',x)
    print '{0:^20} {1:^20} '.format('Total time(s)',y)
    print '================================================'
    
def printSolutionPath(startNode,path):
    '''function print the Solution Path'''
    print "Solution path is:"
    print startNode
    for node in path:
        print node
    print "Path length is ", str(len(path))
    print '================================================'

def main():
    #store the states
    goal = State(np.array([[1,2,3],[8,0,4],[7,6,5]]))
    easy = State(np.array([[1,3,4],[8,6,2],[7,0,5]]))
    medium = State(np.array([[2,8,1],[0,4,3],[7,6,5]]))
    hard = State(np.array([[2,8,1],[4,6,3],[0,7,5]]))
    worst = State(np.array([[5,6,7],[4,0,8],[3,2,1]]))

    #Guidance of how to use this program
    while True:
        choice = int(raw_input("Please choose the difficulty, 0:= easy, 1:= medium, 2:=hard, 3:= worst, 4: exit\n"))
        while not 0<=choice<=4:
            print 'Please enter an integer between 0 to 4\n'
            choice = int(raw_input("Please choose the difficulty, 0:= easy, 1:= medium, 2:=hard, 3:= worst, 4: exit\n"))
            
        #set the first state
        if choice == 0:
            firststate = easy
        elif choice == 1:
            firststate = medium
        elif choice == 2:
            firststate = hard
        elif choice == 3:
            firststate = worst
        else:
            break

        #choose the method
        method = int(raw_input("Please choose the method, 0:= A*_Misplace, 1:= A*_Manhattan, 2:= IDA*, 3:= DFB, 4: return\n"))
        while not 0<=method<=4:
            print 'Please enter an integer between 0 to 4\n'
            method = int(raw_input("Please choose the method, 0:= A*_Misplace, 1:= A*_Manhattan, 2:= IDA*, 3:= DFB, 4: return\n"))
        
        #Do search with the given method
        if method == 4:
            continue 
        elif method == 0:
            result = AStarsearch(firststate,goal,hMisplace)
            result[0].reverse()
            path = result[0]
            expand_nodes = result[1]
            total_time = result[2]
        elif method == 1:
            result = AStarsearch(firststate,goal)
            result[0].reverse()
            path = result[0]
            expand_nodes = result[1]
            total_time = result[2]
        elif method == 2:
            result = IDA(firststate,goal)
            result[0].reverse()
            path = result[0]
            expand_nodes = result[1]
            total_time = result[2]
        else:
            result = DFB(firststate,goal)
            result[0].reverse()
            path = result[0]
            expand_nodes = result[1]
            total_time = result[2]
            DFB_time = result[3]
        printResults(method,expand_nodes,total_time)
        if method == 3:
            print 'Optimal time of DFB is '+str(DFB_time)+' seconds.'
            print '================================================'
        printSolutionPath(firststate,path)

if __name__ == "__main__":
    main()