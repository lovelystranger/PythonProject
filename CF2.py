import pandas as pd
from pandas import Series,DataFrame
import numpy as np
import time
rnames = ['user_id','movie_id','rating','timestamp']
ratings = pd.read_table(r'u1.dat',sep = None,header = None, names = rnames, engine = 'python')
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
		else:
			continue
		if test.count(axis = 1).iloc[0] > 50:
			count1 = test.count(axis = 1).iloc[0]
			corr = data.loc[ud].corr(data.loc[i])
			if corr > 0.1:
		   		b = (i,corr,count1)
		   		aggr.append(b)
	aggr_1 = sorted(aggr,key = lambda x:x[1],reverse = True)
	print(aggr_1)
	aggr_2 = aggr_1[0:5:1]
	print(aggr_2)
	data_1 = data.copy()
	def estivul(i,j):
		list1 = []#存放j项目与m项目的相似度，格式为（m，corr）
		test = data.reindex([i])
		#对i用户所有未评分的电影填充为3分
		for k in range(data.shape[1]):
			if test.loc[i].isnull()[k+1] == True:
				test.loc[i,k+1] = 3
    	#计算j电影与其他电影的相似度，并将相似度大于0.1的电影放入list1
		for m in range(data.shape[1]):
			if m !=j:
				corr = data.loc[:,j].corr(data.loc[:,m+1])
				if corr > 0.3:
					a = (m+1,corr)
					list1.append(a)
    	#计算评分
		if list1:
			result = sum([test.loc[i,n]*weight for n,weight in list1])/sum([pair[1] for pair in list1])
		else:
			result = 3
		return result
	m = 0
	for pair in aggr_2:
		check_size = 50
		for j in range(data.shape[1]):
			if data.loc[ud].isnull()[j+1] == True and data.loc[pair[0]].isnull()[j+1] == True:
				continue
			if data.loc[ud].isnull()[j+1] == False and data.loc[pair[0]].isnull()[j+1] == True:
				data_1.loc[pair[0],j+1] = estivul(pair[0],j+1)
				m += 1
				check_size -= 1
			if data.loc[ud].isnull()[j+1] == True and data.loc[pair[0]].isnull()[j+1] == False:
				data_1.loc[ud,j+1] = estivul(ud,j+1)
				m += 1
				check_size -= 1
			if not check_size:
				break
	print(m)
	a1 = []
	list1 = []
	a1.append(data.loc[ud,md])
	data_1.loc[ud,md] = None
	for i in range(data_1.shape[0]):
		if data_1.loc[:,md].isnull()[i+1] == True and i != ud-1:
			data_1.loc[i+1,md] = 3
	for pair in aggr_2:
		corr_1 = data_1.loc[ud].corr(data_1.loc[pair[0]])
		if corr_1 > 0.1:
			a = (pair[0],corr,data_1.loc[pair[0],md])
			list1.append(a)
	print(list1)
	if list1:
		result = sum([rate*weight for n,weight,rate in list1])/sum([pair[1] for pair in list1])
		a1.append(result)

	return a1

m = rate(919,1)
print(m)





 