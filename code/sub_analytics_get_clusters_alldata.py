from threading import Thread
from analytics_engine import cross_athelets_ssCluster
intervals = [50,60,70]
spaces = [5,10,15]

if __name__=='__main__':
    for interval in intervals:
        for space in spaces: 
            cross_athelets_ssCluster(interval,space)
