import pandas as pd
from pandas import Series,DataFrame
import numpy as np 
rnames = ['user_id','movie_id','rating','timestamp']
ratings = pd.read_table(r'ratings.dat',sep = '::',header = None,names = rnames,engine = 'python')
data =ratings.pivot(index = 'user_id',columns = 'movie_id',values = 'rating')
a = data.loc[4169].corr(data.loc[424])
test = data.reindex([424,4169],columns = data.loc[4169][data.loc[424].notnull()].dropna().index)
check_size = 1000
check = {}
check_data = data.copy()#复制一份data用于检验，以免篡改数据
check_data = check_data.loc[check_data.count(axis=1) > 200]#滤除评价数小于200的用户
for user in np.random.permutation(check_data.index):
	movie = np.random.permutation(check_data.loc[user].dropna().index)[0]
	check[(user,movie)] = check_data.loc[user,movie]
	check_data.loc[user,movie] = np.nan
	check_size -= 1
	if not check_size:
		break

corr = check_data.T.corr(min_periods = 200)
corr_clean = corr.dropna(how = 'all')
corr_clean = corr_clean.dropna(axis = 1,how = 'all')#删除全空的行或列
check_ser = Series(check)
result = Series(np.nan,index = check_ser.index)
for user,movie in result.index:
	prediction = []
	if user in corr_clean.index:
	    corr_set = corr_clean[user][corr_clean[user]>0.1].dropna()#仅限大于0.1的用户
	else:continue
	for other in corr_set.index:
		if not np.isnan(data.loc[other,movie]) and other != user:#注意bool（np.nan) == True
		    prediction.append((data.loc[other,movie],corr_set[other]))
	if prediction:
		result[(user,movie)] = sum([value*weight for value,weight in prediction])/sum([pair[1] for pair in prediction])

result.dropna(inplace= True)
sim = result.corr(check_ser.reindex(result.index))

print((result - check_ser.reindex(result.index)).abs().describe())
