# -*- coding: utf-8 -*-
from numpy import *
import numpy as np

class EM:
    '''
    Class of EM algorithm
    '''
    def __init__(self, filepath, *para):
        '''
        Initializer of EM algorithm
        
        self.data: dataset information from file
        self.p_g: probability of gender(male, female)
        self.p_w_g0: probability of weight(high, low) when gender is male
        self.p_w_g1: probability of weight(high, low) when gender is female
        self.p_h_g0: probability of height(high, low) when gender is male
        self.p_h_g1: probability of height(high, low) when gender is female
        self.missing_index: index of the missing data
        '''
        datafile = open(filepath)
        self.data = np.genfromtxt(datafile, delimiter="\t",missing_values='-',skip_header=1)
        self.p_g = array([para[0], 1-para[0]])
        self.p_w_g0 = array([para[1], 1-para[1]])
        self.p_w_g1 = array([para[2], 1-para[2]])
        self.p_h_g0 = array([para[3], 1-para[3]])
        self.p_h_g1 = array([para[4], 1-para[4]])
        self.missing_index = self.get_missing_index()
        
    def get_missing_index(self):
        '''
        Get the index of the missing data
        '''
        missing = where(isnan(self.data[:,0]))
        missing_index = []
        missing_index_w0h0 = []
        missing_index_w0h1 = []
        missing_index_w1h0 = []
        missing_index_w1h1 = []
        for i in missing[0]:
            if np.allclose(self.data[i,1],0) and np.allclose(self.data[i,2],0):
                missing_index_w0h0.append(i)
            elif np.allclose(self.data[i,1],0) and np.allclose(self.data[i,2],1):
                missing_index_w0h1.append(i)
            elif np.allclose(self.data[i,1],1) and np.allclose(self.data[i,2],0):
                missing_index_w1h0.append(i)
            elif np.allclose(self.data[i,1],1) and np.allclose(self.data[i,2],1):
                missing_index_w1h1.append(i)
        missing_index.append(missing_index_w0h0)
        missing_index.append(missing_index_w0h1)
        missing_index.append(missing_index_w1h0)
        missing_index.append(missing_index_w1h1)
        return missing_index
    
    def E_step(self):
        '''
        E-step of EM algorithm
        '''
        p_wh = hstack((self.p_g[0] * self.p_w_g0[0] * self.p_h_g0, self.p_g[0] * self.p_w_g0[1] * self.p_h_g0))\
        + hstack((self.p_g[1] * self.p_w_g1[0] * self.p_h_g1, self.p_g[1] * self.p_w_g1[1] * self.p_h_g1))
        p_g0_wh = hstack((self.p_g[0] * self.p_w_g0[0] * self.p_h_g0, self.p_g[0] * self.p_w_g0[1] * self.p_h_g0))/p_wh
        for i in range(4):
            if len(self.missing_index[i]) > 0:
                self.data[self.missing_index[i],0] = 1-p_g0_wh[i]
            else:
                continue
        #print self.data
        
    def M_step(self):
        '''
        M-step of EM algorithm
        '''
        self.p_g = self.calculate_p_g()
        self.calculate_p_wh_g()
        self.likelihood = self.calculate_loglikelihood()
        #print 'loglikelihood', self.likelihood
        print self.likelihood
        
    def calculate_p_g(self):
        '''
        Calculate probability of gender
        '''
        new_p_g1 = sum(self.data[:,0])/20.0
        return array([1-new_p_g1, new_p_g1])
        
    def calculate_p_wh_g(self):
        '''
        Calculate conditional probability of weight or height given gender
        '''
        w_count_00 = 0   #count the number of data which weight is 0, gender is 0
        w_count_01 = 0   #count the number of data which weight is 0, gender is 1
        g_count_00 = 0   #count the number of data which height is 0, gender is 0
        g_count_01 = 0   #count the number of data which height is 0, gender is 1
        for i in range(20):
            if self.data[i,0] == 0:
                if (self.data[i,1] == 0):
                    w_count_00 += 1
                if (self.data[i,2] == 0):
                    g_count_00 += 1
            elif self.data[i,0] == 1:
                if (self.data[i,1] == 0):
                    w_count_01 += 1
                if (self.data[i,2] == 0):
                    g_count_01 += 1
            else:
                if (self.data[i,1] == 0):
                    w_count_00 += 1-self.data[i,0]
                    w_count_01 += self.data[i,0]
                if (self.data[i,2] == 0):
                    g_count_00 += 1-self.data[i,0]
                    g_count_01 += self.data[i,0]
        sum_g1 = sum(self.data[:,0])
        sum_g0 = 20.0-sum(self.data[:,0])
        #calculate conditional probabilities
        self.p_w_g0 = array([w_count_00/sum_g0, 1-w_count_00/sum_g0])
        self.p_w_g1 = array([w_count_01/sum_g1, 1-w_count_01/sum_g1])
        self.p_h_g0 = array([g_count_00/sum_g0, 1-g_count_00/sum_g0])
        self.p_h_g1 = array([g_count_01/sum_g1, 1-g_count_01/sum_g1])
        
    def calculate_loglikelihood(self):
        '''
        Calculate loglikelihood
        '''
        likelihood = 0
        for i in range(20):
            likelihood += log(self.calculate_likelihood(self.data[i,:]))
        return likelihood
        
    def calculate_likelihood(self, point):
        '''
        Calculate likelihood of single data
        '''
        w = point[1]
        h = point[2]
        if point[0] == 0:
            likelihood = (self.p_g[0])*self.p_w_g0[int(w)]*self.p_h_g0[int(h)]
        elif point[0] == 1:
            likelihood = (self.p_g[1])*self.p_w_g1[int(w)]*self.p_h_g1[int(h)]
        else:
            likelihood = (self.p_g[1])*self.p_w_g1[int(w)]*self.p_h_g1[int(h)]+(self.p_g[0])*self.p_w_g0[int(w)]*self.p_h_g0[int(h)]
        return likelihood
        
    def do_EM(self):
        '''
        Do E-M steps and print results
        '''
        count = 1
        print '\n'
        print 'Itration: ' + str(count)
        self.E_step()
        self.M_step()
        likelihoods = [self.likelihood]
        old_likelihood = self.likelihood
        
        while True:
            count += 1 
            print 'Itration: ' + str(count)
            self.E_step()
            self.M_step()
            likelihoods.append(self.likelihood)
            if 0.001 > self.likelihood - old_likelihood > 0:
                break
            else:
                old_likelihood = self.likelihood 
        print 'Itration stop!'
        print '\n'
        print 'Final likelihood:' + str(self.likelihood)
        print 'Final Parameters are: '
        print '{0:^15} {1:^15} {2:^15} {3:^15} {4:^15}'.format('P_G0','PW0|G0','PW0|G1','PH0|G0','PH0|G1')
        print '-' * 80

        print '{0:^15} {1:^15} {2:^15} {3:^15} {4:^15}'.format(str(self.p_g[0]),str(self.p_w_g0[0]), str(self.p_w_g1[0]),str(self.p_h_g0[0]), str(self.p_h_g1[0]))
        print '================================================================================='
        return count, likelihoods, self.likelihood, self.p_g[0], self.p_w_g0[0],self.p_w_g1[0],self.p_h_g0[0],self.p_h_g1[0]