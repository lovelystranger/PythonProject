import pandas as pd
from pandas import Series,DataFrame
import numpy as np
import time
rnames = ['user_id','movie_id','rating','timestamp']
ratings = pd.read_table(r'u1.dat',sep =None,header = None, names = rnames, engine = 'python')
data = ratings.pivot(index = 'user_id',columns = 'movie_id',values = 'rating')
a = []
for i in range(1,1651):
    a.append(i)
data.columns = a


def rate(ud,md):
	aggr = []
	for i in data.index:
	    if i != ud:
		    test = data.reindex([ud],columns = data.loc[ud][data.loc[i].notnull()].dropna().index)
	    else:continue
	    if test.count(axis = 1).iloc[0] > 50:
		    count1 = test.count(axis = 1).iloc[0]
		    b = (i,count1)
		    aggr.append(b)
	aggr_1 = sorted(aggr,key = lambda x:x[1],reverse = True)
	aggr_2 = aggr_1[0:5:1]
	data_1 = data.copy()
	a1 = []
	a1.append(data.loc[ud,md])
	
	list2 = [] #存放i用户与m用户的相似度，格式为（m，corr）
	data_1.loc[ud,md] = None
	for i in range(data.shape[0]):
		if data.loc[:,md].isnull()[i+1] == True and i != ud-1:
			data_1.loc[i+1,md] = 3
	for pair in aggr_2:
		corr_2 = data_1.loc[ud].corr(data_1.loc[pair[0]])
		if corr_2 > 0.1:
			a = (pair[0],corr_2,data_1.loc[pair[0],md])
			list2.append(a)
	if list2:
		result = sum([rate*weight for n,weight,rate in list2])/sum([pair[1] for pair in list2])
		a1.append(result)
	return a1
m = rate(1,14)
print(m)
