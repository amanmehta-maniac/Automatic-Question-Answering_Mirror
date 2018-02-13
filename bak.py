import pandas as pd 


for i in range(71,89):
	feature = pd.read_csv("features3/"+str(i)+".csv",header=None)
	qid = pd.read_csv("qid3/"+str(i)+".csv",header=None)
	if feature.shape[0]!=qid.shape[0]:
		print "goneeeedd",i,feature.shape[0],qid.shape[0]