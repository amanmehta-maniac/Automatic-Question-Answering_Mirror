import pandas as pd 
import numpy as np
import xgboost as xgb
import sys
sys.path.append('./LCS')
sys.path.append('./headRelated')
sys.path.append('./ngramOverlap')
sys.path.append('./skipBigram')
sys.path.append('./synHypOverlap')
sys.path.append('./treeKernel')
import os
import re
import pickle
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
    
from lxml import etree
from lcs import lcs_wlcs #returns lcs, wlcs
from head import head_related #returns relHeadScore, exactHeadScore
from ngram import ngram_overlap #returns 1gram score
from skip import skip_bigram #returns skip score
from syn import syn_hyp_overlap #returns synOverlap, hypOverlap, glossOverlap
from synTreeKernel import syn_tree_kernel #returns treekernel score
import pickle
import multiprocessing as mp
from nltk.corpus import wordnet as wn
from nltk.tokenize import sent_tokenize, word_tokenize

def extract_features(candidate):
    feature_vector = []
    # global i
    # i += 1
    #print "finding features for", i
    try:
        feature_vector += list(lcs_wlcs(query, candidate))
        feature_vector += list(head_related(query, candidate))
        feature_vector.append(ngram_overlap(query, candidate))
        feature_vector.append(skip_bigram(query, candidate))
        feature_vector += list(syn_hyp_overlap(query, candidate))
        feature_vector.append(syn_tree_kernel(query, candidate))
        feature_vector.append(candidate)
    except Exception as e:
        print e
        feature_vector = [0,0,0,0,0,0,0,0,0,0,candidate]
    return feature_vector

def extract_sentences(chapNum,flag):
    classIdentifier = ""
    if chapNum <= 8:
        classIdentifier = "i"
    else:
        chapNum = chapNum - 8
        classIdentifier = "j"
    if flag==1:
        file = open("./Dataset_NCERT/Dataset-txt/"+classIdentifier+"ess30"+str(chapNum)+".txt")
    else:
        file = open("./Dataset_NCERT/Dataset-txt/"+"map_"+classIdentifier+"ess30"+str(chapNum)+".txt")    
    sentences = file.read()
    file.close()
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', sentences)
    for i, s in enumerate(sentences):
        s = s.replace("\n", " ")
        sentences[i] = s
    # print sentences
    return sentences




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
# x_test = x_test.values
# y_test = y_test.values

dtrain = xgb.DMatrix(x_train, y_train)

# dvalid = xgb.DMatrix(x_valid)

num_boost_rounds = 150
print("num_boost_rounds="+str(num_boost_rounds))

# train model
print( "\nTraining XGBoost ...")
model = xgb.train(dict(xgb_params, silent=1), dtrain, num_boost_round=num_boost_rounds)




print( "\nPredicting with XGBoost ...")


# chapNum = 4 
# query = "What are the main reasons for rapid disappearance of forests."
chapNum = (int)(sys.argv[1])
query = sys.argv[2]

print chapNum, query
candidates2 = extract_sentences(chapNum,1)
candidates = extract_sentences(chapNum,2)
print "This is prev: "
# candidates = ['abc','disappearance']
# print len(candidates)

pool = mp.Pool(processes=8)
features = pool.map(extract_features, candidates)
feat_df = pd.DataFrame(features)
# features = [(x[0], x[1], unicode(x[2], "utf-8")) for x in features]
sents = feat_df[10]
x_test = feat_df.drop([10],axis=1)
x_test = x_test.values
dtest = xgb.DMatrix(x_test)

xgb_pred1 = model.predict(dtest)

# print type(xgb_pred1),type(y_test)
# for i in range(len(xgb_pred1)):
#   # if xgb_pred1[i] != y_test[i]:
#   print xgb_pred1[i],y_test[i]
        # c += 1


sorted_sents = [x for _,x in sorted(zip(xgb_pred1,sents),reverse=True)]
# print sorted_sents
# print xgb_pred1
output = []
print query
final = sorted_sents
x=0
# f = open("maasai.txt","w")
# s=""
# for i in final:
#     s += i + " "
# f.write(s)
# f.close()
for i in final:
    ind = candidates.index(i)
    if x>25:
        break
    x+=1
    output.append(candidates2[ind])

# for ind,i in enumerate(final):
#     if "They defended" in i:
#         print ind,i

print " ".join(map(str, output))



########## Test code for SQuAD ################
# c=0
# print c
# list1 = []
# listf = []
# max_val = -1000000
# max_index = 0
# total = 0
# for i in range(len(test_ids)-1):
#     if test_ids[i] == test_ids[i+1]:
#         if xgb_pred1[i] > max_val:
#             max_index = i
#             max_val = xgb_pred1[i]
#         list1.append(xgb_pred1[i])

#     else:
#         print "max_index = 0",max_index
#         total += 1
#         if y_test[max_index] == 1:
#             c += 1
#         max_index = i
#         max_val = -1000000
#         listf.append(list1)
#         list1 = []
# print c, "out of", total
# print listf
#################################################