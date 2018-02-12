import pandas as pd 
import numpy as np
import xgboost as xgb

df = pd.read_csv("final_train.csv",header=None)

msk = np.random.rand(len(df)) < 0.8
train = df[msk]
test = df[~msk]

y_train = train[10]
x_train = train.drop([10],axis = 1)

y_test = test[10]
x_test = test.drop([10],axis = 1)

print x_train.shape,y_train.shape,x_test.shape,y_test.shape

xgb_params = {
    'eta': 0.037,
    'max_depth': 5,
    'subsample': 0.80,
    'objective': 'reg:linear',
    'eval_metric': 'mae',
    'lambda': 0.8,   
    'alpha': 0.4, 
    'base_score': 0.5,
    'silent': 1
}

x_train = x_train.values
y_train = y_train.values
x_test = x_test.values
y_test = y_test.values

dtrain = xgb.DMatrix(x_train, y_train)
dtest = xgb.DMatrix(x_test)
# dvalid = xgb.DMatrix(x_valid)

num_boost_rounds = 1000
print("num_boost_rounds="+str(num_boost_rounds))

# train model
print( "\nTraining XGBoost ...")
model = xgb.train(dict(xgb_params, silent=1), dtrain, num_boost_round=num_boost_rounds)

print( "\nPredicting with XGBoost ...")
c=0
xgb_pred1 = model.predict(dtest)

print type(xgb_pred1),type(y_test)
for i in range(len(xgb_pred1)):
	# if xgb_pred1[i] != y_test[i]:
	print xgb_pred1[i],y_test[i]
		# c += 1
print c

