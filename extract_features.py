import sys
sys.path.append('./Features/LCS')
sys.path.append('./Features/headRelated')
sys.path.append('./Features/ngramOverlap')
sys.path.append('./Features/skipBigram')
sys.path.append('./Features/synHypOverlap')
sys.path.append('./Features/treeKernel')
import os
import re
import pickle
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import pandas as pd
	
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

def extract_features(inp):
	qid,query,candidate = inp
	print "doing for ",qid,query,candidate
	feature_vector = []
	try:
		feature_vector += list(lcs_wlcs(query, candidate))
		feature_vector += list(head_related(query, candidate))
		feature_vector.append(ngram_overlap(query, candidate))
		feature_vector.append(skip_bigram(query, candidate))
		feature_vector += list(syn_hyp_overlap(query, candidate))
		feature_vector.append(syn_tree_kernel(query, candidate))
	except Exception as e:
		print e
		feature_vector = [0,0,0,0,0,0,0,0,0,0]
	return [qid]+feature_vector+[query]+[candidate]


# pool = mp.Pool(processes=12)
# features = pool.map(extract_features, candidates)

s = open('train-v1.1.json', 'r').read()
whip = eval(s)

whip = whip["data"]
print len(whip)
paras = whip[0]['paragraphs']

def give_QApairs(qid,a):
	ret = []
	# for index in range(a,b):
	paras = whip[a]['paragraphs']
	for para in paras:
		# x += 1 
		train_x = []
		train_y = []
		c = para['context']
		c = c.split('.')
		for q in para['qas']:
			qid+=1 
			for ci in c:
				if ci != "":
					# num_calls += 1
					feat_final = [qid]+[q['question'],ci]
					ret.append([qid,q['question'],ci])
					# k+=1
				break
			break
		break
		# print "done writing for ",x
	return qid,ret


l = len(whip)
y = 0
qid = 0

while y<l:
	qid,list_QA = give_QApairs(qid,y)
	print "got ",len(list_QA)," QA pairs"
	# print list_QA
	pool = mp.Pool(processes=1)
	features = pool.map(extract_features,  list_QA)
	print features
	write_karo = "\n".join(["\t".join(map(str,i)) for i in features])
	f = open("squad_features/"+str(y)+".csv","w")
	f.write(write_karo)
	f.close()
	y+=1 
