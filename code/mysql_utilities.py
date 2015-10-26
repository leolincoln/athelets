# -*- coding: utf-8 -*-
"""
Created on Sun Dec  7 13:18:15 2014

@author: leoliu
"""

def createEngine(host = None,database=None,tableName =None,userName=None,passWord=None):
    '''
    create a session to connect with the database system given host and database
    '''
    from file_utilities import readYaml
    cred = readYaml('db.yaml')
    if host is None:
        host = cred['address']
    if database is None:
        database = cred['database']
    if tableName is None:
        tableName = cred['tablename']
    if userName is None:
        userName = cred['username']
    if passWord is None:
        passWord = cred['password']
    import sqlalchemy as sa
    metadata = sa.MetaData()
    neuroData = sa.Table(tableName,metadata,sa.Column('channel',sa.Float,primary_key=True),sa.Column('time',sa.Float,primary_key=True),sa.Column('voltage',sa.Float),sa.Column('name',sa.Unicode(length=200),primary_key=True))
    engine = sa.create_engine("mysql://"+userName+":"+passWord+"@"+host+"/"+database)
    #check first before creating table. This is for preventing multiple create table
    metadata.create_all(engine,checkfirst=True)
    return engine,neuroData
'''
	input: [[1,2,3,4,5,6,7],[1,2,3,4,5,6,7]]
    output: [{'voltage': 1, 'channel': 1, 'time': 1},
             {'voltage': 2, 'channel': 1, 'time': 2},
             {'voltage': 3, 'channel': 1, 'time': 3}, 
	]
'''
#row.append(dict(zip(('channel','time','voltage'),[i,j,data[i][j]])))

def dataToRow(data,name):
    row=[]
    for i in xrange(len(data)):
        print 'reading channel: '+str(i)
        for j in xrange(len(data[i])):
            row.append(dict(zip(('channel','time','voltage','name'),[i,j,data[i][j],name])))
    return row

#Note this B is upper case
def loadRowToDB(rows):
    loadNum = 100000
    engine,neuroData = createEngine()
    for i in xrange(len(rows)/loadNum+1):
        print 'chunk import to db: '+str(i)
        if i*loadNum+loadNum<=len(rows):
            engine.execute(neuroData.insert(), rows[i*loadNum:i*loadNum+loadNum])
        else:
            engine.execute(neuroData.insert(),rows[i*loadNum:])


def createTable(tableName = None):
    if tableName is None:
        from file_utilities import readYaml
        tableName = readYaml('db.yaml')['tablename']
    engine,neuroData = createEngine(tableName = tableName)
    print 'created db '+tableName

def loadDataToDB(data,name,tableName=None):
    if tableName is None:
        from file_utilities import readYaml
        tableName = readYaml('db.yaml')['tablename']
    name= unicode(name)
    loadNum = 50000
    engine,neuroData = createEngine(tableName=tableName)
    rows = dataToRow(data,name)
    try:
        for i in xrange(len(rows)/loadNum+1):
            if i*loadNum+loadNum<=len(rows):
                engine.execute(neuroData.insert(), rows[i*loadNum:i*loadNum+loadNum])
            else:
                engine.execute(neuroData.insert(),rows[i*loadNum:])
    except Exception as e:
        print 'unable to load data to db'
        print e
        import traceback
        print traceback.format_exc()
        return

#e.g. ../Victoria_Azarenka/Victoria_Azarenka.TXT --> Victoria_Azarenka
def getNameFromFile(fName):
    return fName.split('/')[-1].split('.')[0]

def loadData(data):
    return data
