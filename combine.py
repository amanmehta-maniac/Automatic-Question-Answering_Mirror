import pandas as pd 
from pathlib import Path

for i in range(1,89):
	my_file = Path("final_con/"+str(i)+".csv")
	if i==1:
		final = pd.read_csv("final_con/"+str(i)+".csv",header=None)
	if my_file.is_file():
		# feature = pd.read_csv("features3/"+str(i)+".csv",header=None)
		new = pd.read_csv("final_con/"+str(i)+".csv",header=None)
		final = pd.concat([final, new])
		# print result
		# break
final.to_csv("final_qid_train.csv",header=None,index=None)
