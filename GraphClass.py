#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 13:26:21 2022

@author: noahzahn
"""


import numpy as np
import matplotlib.pyplot as plt
from scipy import stats as stat
from matplotlib import cm
import csv


class plot():
    def __init__(self):
        plt.rcParams.update({'font.family':'Times New Roman'})
        
        self.n_grp = int(input('Enter number of data groups: '))
        self.n_trt = int(input('Enter number of treatments per group: '))
        self.n_data = int(input('Enter number of data points per treatment: '))
        self.test, self.control = self.make_data()
        self.p = self.p()
        self.xlabels = ['']
        greys = cm.get_cmap('Greys')
        colorb = greys(np.linspace(.8,.3,3))
        ctest = []
        while len(self.xlabels) <= self.n_grp:
            self.xlabels.append('')
            ctest.append(colorb)
        self.ctest = np.array(ctest)
        self.labels = ['']
        while len(self.labels) < self.n_trt:
            self.labels.append('')
        self.y_title = ''
        self.x_title = ''
        self.title = ''
        
        print('\nEnter [self].menu() to bring up menu')
        
    def menu(self):
        print('Enter the following to format plot:\n')
        print('--Group Labels & Colors: [self].x_labels_colors()\n')
        print('--Treatment Labels: [self].set_labels()\n')
        print('--Title: [self].set_title()\n')
        print('--Y-title: [self].set_y_title()\n')
        print('--X-title : [self].set_x_title()\n')
        print('--To make the plot: [self].get_plot()\n')
        
        
        
        
    @staticmethod
    def get_values_csv(filename):
        test = []
        with open(filename, 'r') as file:
            csv_reader = csv.reader(file)
            for i in csv_reader:
                for j in i:
                    if j.isdigit():
                        test.append(j)
                    else:
                        continue
        return [int(i) for i in test]
    def make_data(self):
        test = []
        control = []
        print('Note: For csv files please have control data in a column to the right of treatment data')
        route = int(input('Indicate how data is being entered: \n1 = via csv \n2 = manually \n: '))
        if route == 1:
            filename = input('Please type filename (include the .csv extension): ')
            data = self.get_values_csv(filename)
            for i in range(len(data)):
                if i % 2 ==0:
                    test.append(data[i])
                else:
                    control.append(data[i])
            test = np.array(test)
            test = test.reshape([self.n_grp, self.n_trt, self.n_data])
            control = np.array(control)
            control = control.reshape([self.n_grp, self.n_trt, self.n_data])
            return test, control
        if route == 2:
            m_grp = 1
            m_trt = 1
            m_data = 1
            while (m_grp <= self.n_grp) and (m_data <= self.n_data):
                data = int(input('For group {}, treatment {}, enter data point {}: '.format(m_grp, m_trt, m_data)))
                test.append(data)
                m_data += 1
                if m_data > self.n_data:
                    m_trt +=1
                    m_data = 1
                if m_trt > self.n_trt:
                    m_grp +=1
                    m_trt = 1
                    m_data =1
            mc_grp = 1
            mc_trt = 1
            mc_data = 1
            while (mc_grp <= self.n_grp) and (mc_data <= self.n_data):
                data = int(input('For control group {}, treatment {}, enter data point {}: '.format(mc_grp, mc_trt, mc_data)))
                control.append(data)
                mc_data += 1
                if mc_data > self.n_data:
                    mc_trt +=1
                    mc_data = 1
                if mc_trt > self.n_trt:
                    mc_grp +=1
                    mc_trt = 1
                    mc_data =1
            test = np.array(test)
            test = test.reshape([self.n_grp, self.n_trt, self.n_data])
            control = np.array(control)
            control = control.reshape([self.n_grp, self.n_trt, self.n_data])
            return test, control
    def avg(self, array):
        avg = []
        for i in range(self.n_grp):
            for j in range(self.n_trt):
                avg.append(np.average(array[i,j]))
        return avg
    def stdev(self, array):
        stdev = []
        for i in range(self.n_grp):
            for j in range(self.n_trt):
                stdev.append(stat.tstd(array[i,j]))
        return stdev
    def p(self):         
        pvals = []
        for i in range(self.n_grp):
            for j in range(self.n_trt):
                var_test = stat.tvar(self.test[i,j])
                var_control = stat.tvar(self.control[i,j])
                ratio = var_test / var_control
                equal = True
                if ratio >= 4 or ratio <= .25:
                    equal = False
                t, p = stat.ttest_ind(self.test[i,j], self.control[i,j], equal_var = equal)
                pvals.append(p)
        return pvals

    def x_labels_colors(self):
        x_label = []
    
        greens = cm.get_cmap('Greens')
        oranges = cm.get_cmap('Oranges')
        purples = cm.get_cmap('Purples')
        blues = cm.get_cmap('Blues')
        reds = cm.get_cmap('Reds')
    
        color1 = greens(np.linspace(.8,.3,3))
        color2 = oranges(np.linspace(.8,.3,3))
        color3 = purples(np.linspace(.8,.3,3))
        color4 = blues(np.linspace(.8,.3,3))
        color5 = reds(np.linspace(.8,.3,3))
    
        colors = [color1, color2, color3, color4, color5]
    
        ctest = []
    
        m_grp = 1
        while m_grp <= self.n_grp:
            x = input('Enter the label for group {}: '.format(m_grp))
            c = int(input('Enter color for for group{} (Enter 1-5):  '.format(m_grp)))
            ctest.append(colors[c-1])
            x_label.append(x)
            m_grp += 1
        x_label.append('')
        ctest = np.array(ctest)
        self.xlabels =x_label
        self.ctest = ctest
        

    def set_labels(self):
        labels = []
        m_trt = 1
        while m_trt <= self.n_trt:
            l = input('Enter the label for treatment {}: '.format(m_trt))
            labels.append(l)
            m_trt +=1
        self.labels = labels
        

    def set_y_title(self):
        self.y_title = input('Enter title for y-axis: ')
        
    
    def set_x_title(self):
        self.x_title = input('Enter title for x-axis: ')
        
    
    def set_title(self):
        self.title = input('Enter title for plot: ')
        
    def get_plot(self):
        avgd = self.avg(self.test)
        stdevs = self.stdev(self.test)
        bar_groups = np.arange(self.n_grp + 1)
        bar_width = 0.25
        j = -1
        n = -1
        sig = self.p
        plt.figure(figsize=(8,6))
        
        for i in range(self.n_grp * self.n_trt):
            if i % 3 == 0:
                n+=1
                j = 0
            plt.bar(bar_groups[n] + (j)*bar_width, avgd[i], bar_width, label = self.labels[i%3], color = self.ctest[n,j])
            plt.errorbar(bar_groups[n]+j*bar_width, avgd[i], yerr= stdevs[i], color = 'black', fmt = 'o', markersize = 3, capsize = 3)
            if (sig[i] <= .05) and (sig[i] >.01):
                plt.annotate('*', xy = (-.0125+ n + .25 * j, avgd[i]+3), fontsize = 7)
            elif (sig[i] <= .01) and (sig[i] > .001):
                plt.annotate('**', xy = (-.02 + n + .25 * j, avgd[i]+3), fontsize = 7)
            elif sig[i] <= .001:
                plt.annotate('***', xy = (-.025+ n + .25 * j, avgd[i]+3), fontsize = 7)
            else:
                plt.annotate('N.S.', xy = (-.025+ n + .25 * j, avgd[i]+3), fontsize = 7)
            j+= 1
        
        plt.ylabel(self.y_title, fontsize = 25, fontweight = 'bold')
        plt.xlabel(self.x_title, fontsize = 25, fontweight = 'bold')
        plt.title(self.title, fontweight = 'bold', fontsize = 27)
        plt.xticks(bar_groups + 2* bar_width / 2, self.xlabels, fontsize = 18, fontweight = 'bold')
        plt.yticks(np.arange(110, step = 10), fontweight = 'bold', fontsize = 18)
        
        plt.legend(loc='best', frameon= False)

        plt.show()
        

