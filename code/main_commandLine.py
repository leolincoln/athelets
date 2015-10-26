# -*- coding: utf-8 -*-
"""
Created on Sun Nov 30 10:58:59 2014

@author: liu
"""
import shlex
from eeg_utilities import read_brainvis_triplet,getNames
from mysql_utilities import loadDataToDB
from file_utilities import readTxt
print('Neuro central cli')
print('Enter a command to do something, e.g. `load Liu PreTest 11-7-14')
print('To get help, enter `help`.')
def loadTxtToDB(fName,edf=False):
    print('processing file: %s'%fName)
    from file_utilities import getNameFromFile
    data = readTxt(fName,edf=edf)
    loadDataToDB(data,name=getNameFromFile(fName))
    print('loading to db %s as %s complete'%(str(fName),str(getNameFromFile(fName))))

def loadFolderToDB(folderName,edf=True):
    print('processing folder : '+folderName)
    from file_utilities import getNamesFromFolder
    fileList = getNamesFromFolder(folderName)
    for fName in fileList:
        loadTxtToDB(fName,edf=edf)
    print('loading folder %s complete\n'%str(folderName))
    print ('list of files: \n')
    print [getNameFromFile(t) for t in fileList]

while True:
    args = shlex.split(raw_input('> '))
    if(len(args)<1): 
        print('more than 1 arguments is needed')        
        continue
    cmd = args[0].lower()
    if cmd=='exit'or cmd=='exit()' or cmd=='quit'or cmd=='q'or cmd=='bye':
        break
    elif cmd=='corr':
        #sample message: corr 0,1,2,3 comma seperated. 
        #or: corr all
        try:
            from analytics_engine import corrChannels
            print "the remaining messages are: ", args[1:]
            if args[1:][0].strip().lower == 'all':
                corrChannels()
            else:
                channelList = args[1].split(',')
                print corrChannels(channelList)
        except Exception as e:
            print 'unknown command for corr', args[1:]
            print e
            import traceback
            print traceback.format_exc()
            continue
    elif cmd=='help':
        print('load -- load a local file e.g. load Liu PreTest 11-7-14')
        print('loaddb -- load data to database e.g loaddb Liu PreTest 11-7-14' )
        print('loadtxttodb -- load data to database from text file.  e.g loadtxttodb ../Victoria_Azarenka/Victoria_Azarenka.TXT')
        print ('corr all -- corrolate all channels. ')
        print('corr #,#,#,# -- correlate the listed channels. e.g. corr 0,1,2,3 ')
        print('corrolate subject # -- corrolate the data for single subject #')
        print('corrolate subjects #,#,#,# -- corrolate the data for multiple subjects #,#,#,#')
    elif cmd == 'load':
        try:
            fName = ' '.join(args[1:])
            temp = getNames(fName)
            header,E,data = read_brainvis_triplet(temp[0],marker_fname=temp[1],eeg_fname = temp[2])
            print('loading '+fName+' complete')
        except Exception as e:
            print('loading '+fName+' failed')
            print e
            import traceback
            print traceback.format_exc()
            continue
    elif cmd == 'loadtxttodb':
        #try:
        from file_utilities import getNameFromFile
        fName = ' '.join(args[1:])
        data = readTxt(fName)
        loadDataToDB(data,name=getNameFromFile(fName))
        print('loading to db '+fName +' complete')
       # except Exception as e:
        #    print('loading txt to db '+fName + ' failed')
         #   print e
          #  continue
    elif cmd=='loadfoldertodb':
        from file_utilities import getNameFromFile,getNamesFromFolder
        try:
            folderName = ' '.join(args[1:])
            edfString = raw_input('Were files converted from edf?').lower()
            if edfString=='yes' or edfString=='true':
                loadFolderToDB(folderName,edf=True)
            else:
                loadFolderToDB(folderName,edf=False)
        except Exception as e:
            print('loading folder failed')
            print e
            import traceback
            print traceback.format_exc()
            continue
    elif cmd=='loaddb':
        try:
            fName = ' '.join(args[1:])
            temp = getNames(fName)
            header, E, data = read_brainvis_triplet(temp[0],marker_fname=temp[1],eeg_fname=temp[2])
            loadDataToDB(data,name=fName)
            print('loading to db '+fName+' complete')
        except Exception as e:
            print('loading to db '+fName+' failed')
            print e 
            import traceback 
            print traceback.format_exc()
            continue
    elif cmd=='cluster':
        print('clustering command received')
        
    # ...

    else:
        print('Unknown command: {}'.format(cmd))
        
