import pickle
from analytics_engine import cross_athelets_channelDistanceMap,plotDistanceHeatmap,athelet_pair_jaccard
import pickle;
import csv
import cPickle as pickle
import sys
import scipy.cluster.hierarchy as hac

intervals = [50,60,70]
spaces = [5,10,15]
#threshold for not cluster together. 
#this threshold is used for splitting results using the hierachcical clustering. 
#if the distance between 2 clusters are greater than 0.5, we dont cluster them together. 
#e.g. if we have linkage return a matrix of 0,1,0.6,2
#then we should return [[0],[1]]
#however if we have linkage return a matrix of  0,1,0.3,2
#then we should return [[0,1]]
threshold = 0.8

#input: 
#result -- the result list of list to modify and then return 
#e.g. result = [[0],[1],[2],[3],[4],[5].....]
#clusterRecord -- the list of leaves(channels) of each step coming from hierachcical clustering. 
#first -- the first channel to combine. Note it is a number, can be greater than the total channel length. 
#second -- the second channel to bine. Note it is a number, can be greater than the total channel length. 
def combineLeaves(result,clusterRecord,first,second):
    newResult = []
    firstChannels = clusterRecord[first]
    secondChannels = clusterRecord[second]
    for channels in result:
        newChannels = []
        #remove the channel in first or second. 
        for channel in channels: 
            if channel not in firstChannels and channel not in secondChannels:
                newChannels.append(channel)
        if len(newChannels)>0:
            newResult.append(newChannels)
    firstChannels.extend(secondChannels)
    #there should not be any overlap between first and second channel at this point. 
    newResult.append(firstChannels)
    return newResult

# This is the finalResults dictionary for all rolling windows. 
# we can use this to calculate the distances between each rolling windows. 
finalResults = {}
for interval in intervals:
    for space in spaces:
        fName = str(interval)+'_'+str(space)+'_'+'allData.dat'
        data = pickle.load(open(fName,'r'))
        distance = cross_athelets_channelDistanceMap(data);
        z = hac.linkage(distance,method='single')
        #now 0-len(z) is the actual channel numbers. 
        #e.g. if len(z) = 19, then channels are from 0-19. 
        result=[]
        #clusterRecord records each line of the hac output 
        #e.g. if we have 0,1,0.5,2 at ith position of z, 
        #then clusterRecord[len(z)+i+1] = [0,1]
        # of course, clusterRecord[0]=[0], clusterRecord[1] = [1], clusterRecord[2] = [2],clusterRecord[3] = [3] 
        clusterRecord = {}
        for i in xrange(len(z)+1):
            result.append([i])
            clusterRecord[i+0.0]=[i]
            clusterRecord[i+len(z)]=[]
        for i in xrange(len(z)):
            clusterRecord[i+1.0+len(z)].extend(clusterRecord[z[i][0]])
            clusterRecord[i+1.0+len(z)].extend(clusterRecord[z[i][1]])
        #e.g. if we have 0-19, then now result is [[0],[1],[2],[3],.... [19]]
        for cluster in z:
            #examing the first cluster. 
            first = cluster[0]
            #examing the second cluster
            second = cluster[1]
            #examing the distance between first and second
            dis = cluster[2]
            if dis<threshold:
                result = combineLeaves(result,clusterRecord,first,second)
            #so now the result should contain the clustered records of channels using the threshold specified, and its a list. 
            #now we can form our final result using the interval and space as we defined at line 19 and 20. 
        finalResults[str(interval)+'_'+str(space)] = result
        #zDendrogram = hac.dendrogram(z)
        from analytics_engine import athelet_pair_visualize1
        dis,athelets = athelet_pair_visualize1(data=finalResults,name='rolling_windows')
        dist = jacc2disMat(dis)





