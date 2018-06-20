import pandas as pd
from pandas import Series,DataFrame
import numpy as np
import time
rnames = ['user_id','movie_id','rating','timestamp']
ratings = pd.read_table(r'u1.dat',sep = '::',header = None, names = rnames, engine = 'python')
data = ratings.pivot(index = 'user_id',columns = 'movie_id',values = 'rating')
a = []
for i in range(3706):
    a.append(i)
data.columns = a

#找出与用户userid共同评分超过k个的用户
def findintersetcion(userid,k):
    aggr = []
    for i in data.index:
        if i != userid:
            test = data.reindex([userid],columns = data.loc[userid][data.loc[i].notnull()].dropna().index)
        else:
            continue
        #print(test)
        #print(test.count(axis = 1).iloc[0])
        if test.count(axis = 1).iloc[0] > k:
            aggr.append(i)
    return aggr


#填充并集里的空值
def fillthenon(userid,k):
    data_1 = data.copy()
    aggr = findintersetcion(userid,k)
    for i in aggr:
        for j in range(data.shape[1]):
            if data.iloc[userid].isnull()[j] == True and data.iloc[i].isnull()[j] == True:
                continue
            if data.iloc[userid].isnull()[j] == False:
                data_1.iloc[i,j] = estivul(i,j)
            else:
                data_1.iloc[userid,j] = estivul(userid,j)

#计算项目相似度并评分
def estivul(i,j):
	data_2 = data.copy()
	list1 = []#存放j项目与m项目的相似度，格式为（m，corr）
	test = data_2.reindex([i])
	#对i用户所有未评分的电影填充为3分
	for k in range(data.shape[1]):
		if test.loc[i].isnull()[k] == True:
			test.loc[i,k] = 3
    #计算j电影与其他电影的相似度，并将相似度大于0.1的电影放入list1
	for m in range(data.shape[1]):
		if m !=j:
			corr = data_2.iloc[:,j].corr(data_2.iloc[:,m])
			if corr > 0.3:
				a = (m,corr)
				list1.append(a)
    #计算评分
	if list1:
		result = sum([test.loc[i,n]*weight for n,weight in list1])/sum([pair[1] for pair in list1])
	else:
		result = 3
	return result

def rate(i,j,k):
	a = []
	a.append(data.iloc[i-1,j])
	findintersetcion(i,k)
	fillthenon(i,k)
	list2 = [] #存放i用户与m用户的相似度，格式为（m，corr）
	data_1.iloc[i-1,j] = None
	for m in agrr:
		corr = data_1.iloc[i-1].corr(data_1.iloc[m-1])
		if corr > 0.1:
			a = (m,corr)
			list2.append(a)
	if list2:
		result = sum([data_1.iloc[n-1,j]*weight for n,weight in list2])/sum([pair[1] for pair in list2])
	a.append(result)
	return a


start = time.clock()
rate(10,0,200)
print(a)
end = time.clock()
print("耗费时间： %f s" % (end - start))

	



