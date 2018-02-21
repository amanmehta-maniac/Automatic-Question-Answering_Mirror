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

def extract_features(query,candidate):
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
	except Exception as e:
		print e
		feature_vector = [0,0,0,0,0,0,0,0,0,0]
	return feature_vector

s = open('train-v1.1.json', 'r').read()
whip = eval(s)

whip = whip["data"]
print type(whip)
# for k in whip:
# 	break
# print type(whip[0])
# for k in whip[0]:
# 	print k
#print whip[0]['paragraphs'][0]
# print whip[0]['title']
paras = whip[0]['paragraphs']
train_x = []
train_y = []
train = []
k = 0	
x = 0
num_calls = 0
qid=0
write_str = ""
for index in range(len(whip)):
	paras = whip[index]['paragraphs']
	for para in paras:
		x += 1 
		
		####### 61 ke baad 70#########

		# if x < 70:
		# 	continue
		train_x = []
		train_y = []
		c = para['context']
		c = c.split('.')
		# print c
		for q in para['qas']:
			qid+=1 
			for ci in c:
				if ci != "":
					num_calls += 1
					# train.append([q['question'],ci,q['answers'][0]['text']])
					############### isko comment karke ek file bana jisme question ids ho bas##############
					#feat = extract_features(q['question'],ci)
					feat_final = [qid]+[q['question'],ci]
					write_str += str(qid)+","+q['question']+","+ci+"\n"
					#if q['answers'][0]['text'] in ci:
					#	train_x.append(feat_final)
					#	train_y.append(1)
					#else:
					#	train_x.append(feat_final)
					#	train_y.append(0)
					# print "done for",k,q['question'],ci,q['answers'][0]['text']
					k+=1
			# break
		#f = open("features/"+str(x)+".csv","w")
		f = open("question_list.csv","w")
		final = ""
		for i in range(len(train_x)):
			for j in train_x[i]:
				final +=  str(j)+","
			final += str(train_y[i])+"\n"
		print final
		f.write(write_str)
		print "done writing for ",x
		break
print num_calls
