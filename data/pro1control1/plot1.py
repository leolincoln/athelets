from matplotlib import pylab as plt
import cPickle as pickle

#TODO: add code for cutting 4 or average 4 for different sample rate, and unify the unit to be seconds. 
def plot_raw(fileName=None,outName=None,title=None,sample_rate = 1,average=None,cut=None):
    if fileName == None:
        fileName = 'cpt_pro.dat'
    if outName == None:
        outName = 'test.png'
    if title == None:
        title = 'pro raw EEG data'
    pro = pickle.load(open(fileName,'r'))
    f, axes = plt.subplots(len(pro), sharex=True, sharey=True)
    for i in xrange(len(axes)):
        axes[i].plot(pro[i])
    axes[0].set_title(title)
    # Fine-tune figure; make subplots close to each other and hide x ticks for
    # all but bottom plot.
    f.subplots_adjust(hspace=0)
    #set the xticks to be actual time for sample_rate
    #default sample_rate is 1. 
    labels = [str(float(item)/sample_rate) for item in axes[-1].get_xticklabels()]
    axes[-1].set_xticks(labels)
    plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
    plt.setp([a.get_yticklabels() for a in f.axes], visible=False)
    plt.show(False)
    f.savefig(outName)
if __name__ == '__main__':
    plot_raw('cpt_pro.dat','pro.png','pro raw cpt EEG data')
    plot_raw('cpt_13.dat','control.png','control raw cpt EEG data')
