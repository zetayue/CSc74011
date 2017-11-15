# -*- coding: utf-8 -*-
import numpy as np
from EM import *

def main():
    '''
    Main class to preform E-M algorithm
    '''
    starting_paras = [0.7,0.8,0.4,0.7,0.3]
    em1 = EM('./hw2dataset_10.txt', *starting_paras)
    em2 = EM('./hw2dataset_30.txt', *starting_paras)
    em3 = EM('./hw2dataset_50.txt', *starting_paras)
    em4 = EM('./hw2dataset_70.txt', *starting_paras)
    em5 = EM('./hw2dataset_100.txt', *starting_paras)
    em_instances = [em1,em2,em3,em4,em5]
    
    while True:
        choice = int(raw_input("Enter integer to choose the case: 0:= 10%, 1:= 30%, 2:= 50%, 3:= 70%, 4:= 100%, 5:= Exit\n"))
        while not 0<=choice<=5:
            print 'Wrong, please enter an integer between 0 to 5!'
            choice = int(raw_input("Enter integer to choose the case: 0:= 10%, 1:= 30%, 2:= 50%, 3:= 70%, 4:= 100%, 5：= Exit\n"))
        if choice == 5:
            break
        print '================================Results=========================================='
        print 'Starting parameters are: '
        print '{0:^15} {1:^15} {2:^15} {3:^15} {4:^15}'.format('P_G0','PW0|G0','PW0|G1','PH0|G0','PH0|G1')
        print '-' * 80
        print '{0:^15} {1:^15} {2:^15} {3:^15} {4:^15}'.format(str(starting_paras[0]),str(starting_paras[1]),str(starting_paras[2]),str(starting_paras[3]),str(starting_paras[4]))
        em_instances[choice].do_EM()
           
if __name__ == "__main__":
    main()