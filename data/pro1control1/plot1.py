from matplotlib import pylab as plt
import cPickle as pickle
def plot_raw(fileName=None,outName=None,title=None):
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
    plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
    plt.setp([a.get_yticklabels() for a in f.axes], visible=False)
    plt.show(False)
    f.savefig(outName)
if __name__ == '__main__':
    plot_raw('cpt_pro.dat','pro.png','pro raw cpt EEG data')
    plot_raw('cpt_13.dat','control.png','control raw cpt EEG data')
