import pandas as pd 

for i in range(71,89):
	feature = pd.read_csv("features3/"+str(i)+".csv",header=None)
	qid = pd.read_csv("qid3/"+str(i)+".csv",header=None)
	result = pd.concat([qid, feature], axis=1)
	# print result
	# break
	result.to_csv("final_con/"+str(i)+".csv",header=None,index=None)