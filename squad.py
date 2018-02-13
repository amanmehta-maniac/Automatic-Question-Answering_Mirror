import pandas as pd 
import numpy as np
import xgboost as xgb

train = pd.read_csv("final_qid_train.csv",header=None)
test = pd.read_csv("final_qid_test.csv",header=None)
# print train.shape, test.shape

train_ids = train[0]
y_train = train[11]
x_train = train.drop([0,11],axis = 1)

test_ids = test[0]
y_test = test[11]
# print test[11]
x_test = test.drop([0,11],axis = 1)

print x_train.shape,y_train.shape,x_test.shape,y_test.shape

xgb_params = {
    'eta': 0.01,
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

num_boost_rounds = 150
print("num_boost_rounds="+str(num_boost_rounds))

# train model
print( "\nTraining XGBoost ...")
model = xgb.train(dict(xgb_params, silent=1), dtrain, num_boost_round=num_boost_rounds)

print( "\nPredicting with XGBoost ...")
xgb_pred1 = model.predict(dtest)
print xgb_pred1

print type(xgb_pred1),type(y_test)
# for i in range(len(xgb_pred1)):
#   # if xgb_pred1[i] != y_test[i]:
#   print xgb_pred1[i],y_test[i]
        # c += 1
c=0
print c
list1 = []
listf = []
max_val = -1000000
max_index = 0
total = 0
for i in range(len(test_ids)-1):
    if test_ids[i] == test_ids[i+1]:
        if xgb_pred1[i] > max_val:
            max_index = i
            max_val = xgb_pred1[i]
        list1.append(xgb_pred1[i])

    else:
        print "max_index = 0",max_index
        total += 1
        if y_test[max_index] == 1:
            c += 1
        max_index = i
        max_val = -1000000
        listf.append(list1)
        list1 = []
print c, "out of", total
# print listf
