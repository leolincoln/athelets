from matplotlib import pylab as plt
import cPickle as pickle
import numpy as np
def average_array(a,average):
    result = []
    i= 0
    while i<len(a) and i+average-1<len(a):
        result.append(float(sum(a[i:i+average-1]))/average)
        i +=average
    return result
def cut_array(a,cut):
    result = []
    i= 0
    while i<len(a) and i+cut/2<len(a):
        result.append(a[i+cut/2])
        i +=cut
    return result

def plot_raw_channel(channel,fileName=None,outName=None,title=None,sample_rate = None,average=None,cut=None,ratio=1,xlim=None):
    channel = int(channel)
    if fileName == None:
        fileName = 'cpt_pro.dat'
    if outName == None:
        outName = 'test.png'
    if sample_rate is None:
        sample_rate = 1
    sample_rate = float(sample_rate)
    pro = pickle.load(open(fileName,'r'))
    if average is not None:
        average = float(average)
        pro_average=[]
        for a in pro:
            pro_average.append(average_array(a,average))
        pro = pro_average
    if cut is not None:
        cut = float(cut)
        pro_cut=[]
        for a in pro:
            pro_cut.append(cut_array(a,cut))
        pro = pro_cut
    if cut is not None:
        pro_cut = []
    f, ax = plt.subplots()
    if xlim is None:
        ax.set_xlim(0,1200)
    else:
        ax.set_xlim(0,float(xlim))
    ax.set_ylim(-50,50)
    ax.autoscale(enable=False,axis='y')
    ax.plot(np.arange(len(pro[channel]))/sample_rate,np.array(pro[channel])*ratio)
    if title is not None:
        ax.set_title(title)
    plt.show(False)
    f.savefig(outName)
        

#TODO: add code for cutting 4 or average 4 for different sample rate, and unify the unit to be seconds. 
def plot_raw(fileName=None,outName=None,title=None,sample_rate = None,average=None,cut=None,ratio=1):
    if fileName == None:
        fileName = 'cpt_pro.dat'
    if outName == None:
        outName = 'test.png'
    if sample_rate is None:
        sample_rate = 1
    sample_rate = float(sample_rate)
    pro = pickle.load(open(fileName,'r'))
    if average is not None:
        average = float(average)
        pro_average=[]
        for a in pro:
            pro_average.append(average_array(a,average))
        pro = pro_average
    if cut is not None:
        cut = float(cut)
        pro_cut=[]
        for a in pro:
            pro_cut.append(cut_array(a,cut))
        pro = pro_cut
    if cut is not None:
        pro_cut = []
    f, axes = plt.subplots(len(pro), sharex=True, sharey=True)
    
    for i in xrange(len(axes)):
        axes[i].set_xlim(0,1200)
        axes[i].set_ylim(-50, 50)
        axes[i].autoscale(enable=False, axis='y', tight=None)
        print np.array(pro[i][1000:1010])*ratio
        axes[i].plot(np.arange(len(pro[i]))/sample_rate,np.array(pro[i])*ratio) 
    if title is not None:
        axes[0].set_title(title)
    
    # Fine-tune figure; make subplots close to each other and hide x ticks for
    # all but bottom plot.
    f.subplots_adjust(hspace=0)
    #set the xticks to be actual time for sample_rate
    #default sample_rate is 1. 
    #print axes[-1].get_xticklabels()
    #labels = [str(float(item.get_text())/sample_rate) for item in axes[-1].get_xticklabels()]
    #axes[-1].set_xticklabels(labels)
    plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
    plt.setp([a.get_yticklabels() for a in f.axes], visible=False)
    plt.show(False)
    f.savefig(outName)
if __name__ == '__main__':
    #plot_raw(fileName = 'cpt_13.dat',outName='control_average.png',average=4,sample_rate=250,ratio=0.00488281)
    #plot_raw(fileName = 'cpt_13.dat',outName='control.png',sample_rate=1000,ratio=0.00488281)
    plot_raw(fileName='cpt_control.dat',outName='control.png',sample_rate=1000)
    plot_raw_channel(2,fileName = 'cpt_control.dat',outName='control_channel.png',sample_rate=1000,ratio=0.00488281,xlim=5)
    #plot_raw_channel(2,fileName='cpt_pro.dat',outName='pro_channel.png',sample_rate=250,xlim=5)
