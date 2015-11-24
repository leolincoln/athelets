from neuro-athelets import csv2matrixi
sample_rate = 1024 # in samples/s. e.g. 1024 samples/second
cut = 60 #in minutes
timeouts_raw = csv2matrix('timeout_chart.csv')
#so now timeouts is a numpy array of arrays. 
#with columns name., timeout, hours_spent
raw_dict = {}
#could use pandas 
for row in timeouts_raw:
    #sample rate is used in here to get the actual data sampling
    raw_dict[row[0]] = tuple(sample_rate * row[1], row[2])

minute_cut = {}
for athlet in raw_dict.keys():
    
