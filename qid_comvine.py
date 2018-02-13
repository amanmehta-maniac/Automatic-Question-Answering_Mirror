import pandas as pd 
from pathlib import Path

for i in range(71,89):
	# my_file = Path("final_con/"+str(i)+".csv")
	# final = pd.read_csv("final_con/"+str(i)+".csv",header=None)
	feature = pd.read_csv("features3/"+str(i)+".csv",header=None)
	qid = pd.read_csv("qid3/"+str(i)+".csv",header=None)
	result = pd.concat([qid, feature], axis=1)
	result.to_csv("final_con/"+str(i)+".csv",header=None,index=None)
