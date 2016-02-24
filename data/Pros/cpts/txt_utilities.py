#Author: liuliu

import logging, re, os.path, StringIO, itertools
from ConfigParser import SafeConfigParser
import numpy as np
import sys
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from pylab import plot,show
from analytics_engine import windowlizeChannel
import glob
from time import time
import re


def get_whole(fName):
    '''
    automate the process of 1-5 section dividing.
    '''
    start = time()

    #fName = 'cpt1_Ryan_Dungey.TXT'
    subject_num = fName.split('.')[0]
    '''
    fNames =glob.glob('*.TXT')
    for fName in fNames:
        pattern = re.compile(r'([^\_]+).TXT')
        match = pattern.match(headerName)
        subject_num =  int(match.group(2))
    '''
    lines = None
    with open(fName,'r') as f:
        for line in f:
            if lines is None:
                lines = [[item] for item in line.split()]
            else:
                for i in xrange(len(line.split())):
                    lines[i].append(line.split()[i])
    data = lines
    data = np.array(data)
    data = data.astype(float)
    print 'read data finished. ',time()-start
    start = time()
    #now we need to get the exact cpt section
    cpt_data = data
    whole = [windowlizeChannel(w,sampleRate=250) for w in cpt_data]
    pickle.dump(whole,open('../prowffts/whole_'+str(subject_num)+'.wfft','w'))
    print 'saving whole finished.',str(subject_num),time()-start


def get_data(fName):
    '''
    Get data from txt file, return as numpy array in data. 

    '''
    lines = None
    with open(fName,'r') as f:
        for line in f:
            if lines is None:
                lines = [[item] for item in line.split()]
            else:
                for i in xrange(len(line.split())):
                    lines[i].append(line.split()[i])
    lines= np.array(lines)
    lines = lines.astype(float)
    return lines


def main(fName):
    '''
    automate the process of 1-5 section dividing.
    '''
    start = time()

    #fName = 'cpt1_Ryan_Dungey.TXT'
    subject_num = fName.split('.')[0]
    '''
    fNames =glob.glob('*.TXT')
    for fName in fNames:
        pattern = re.compile(r'([^\_]+).TXT')
        match = pattern.match(headerName)
        subject_num =  int(match.group(2))
    '''
    data = get_data(fName)
    print 'read data finished. ',time()-start
    start = time()
    #now we need to get the exact cpt section
    cpt_data = data
    print 'chopping cpt data finished. ',time()-start
    start = time()
    #now we need to divide up the cpt interval, we know there are 5.
    interval_times = [int(len(cpt_interval_data)/5) for cpt_interval_data in cpt_data]
    easy1 = [cpt_data[i][0:interval_times[i]] for i in xrange(len(cpt_data))]
    easy2 = [cpt_data[i][interval_times[i]:2*interval_times[i]] for i in xrange(len(cpt_data))]
    hard1 = [cpt_data[i][interval_times[i]*2:interval_times[i]*3] for i in xrange(len(cpt_data))]
    hard2 = [cpt_data[i][interval_times[i]*3:interval_times[i]*4] for i in xrange(len(cpt_data))]
    easy3 = [cpt_data[i][interval_times[i]*4:] for i in xrange(len(cpt_data))]
    print 'dividing cpt data finished. ',time()-start
    start = time()
    #now we need to do rolling window and fft  on those
    easy1_wfft = [windowlizeChannel(e,sampleRate=250) for e in easy1]
    easy2_wfft = [windowlizeChannel(e,sampleRate=250) for e in easy2]
    hard1_wfft = [windowlizeChannel(h,sampleRate=250) for h in hard1]
    hard2_wfft = [windowlizeChannel(h,sampleRate=250) for h in hard2]
    easy3_wfft = [windowlizeChannel(e,sampleRate=250) for e in easy3]
    print 'windowlize fft finished. ',time()-start
    start = time()
    import cPickle as pickle
    pickle.dump(easy1_wfft,open('../prowffts/easy1_'+str(subject_num)+'.wfft','w'))
    pickle.dump(easy2_wfft,open('../prowffts/easy2_'+str(subject_num)+'.wfft','w'))
    pickle.dump(easy3_wfft,open('../prowffts/easy3_'+str(subject_num)+'.wfft','w'))
    pickle.dump(hard1_wfft,open('../prowffts/hard1_'+str(subject_num)+'.wfft','w'))
    pickle.dump(hard2_wfft,open('../prowffts/hard2_'+str(subject_num)+'.wfft','w'))
    print 'write divided window fft data finished. ',time()-start
    start = time()

if __name__ == '__main__':
    import glob
    fNames = glob.glob('*.TXT')
    for fName in fNames:
        main(fName)
