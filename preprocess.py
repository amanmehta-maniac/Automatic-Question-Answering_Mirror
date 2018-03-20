import sys
import os, json,gensim
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

s = open('train-v1.1.json', 'r').read()
whip = eval(s)

whip = whip["data"]
paras = whip[0]['paragraphs']
train_x = []
train_y = []
train = []
k = 0	
x = 0
num_calls = 0
qid=0
write_str = ""
Final = []
all_para = []
for index in range(len(whip)):
	paras = whip[index]['paragraphs']
	for para in paras:
		x += 1 
		train_x = []
		train_y = []
		c = para['context']
		all_para.append(c)
		c = c.split('.')
		for q in para['qas']:
			qid+=1 
			num_calls += 1
			ques_now = q['question'].lower()
			ans_now = q['answers'][0]['text'].lower()
			Final.append([ques_now,ans_now])
			k+=1

# print all_para[:5]

all_sent = []

for para in all_para:
	sentences = para.split('.')
	# print sentences
	for sen in sentences:
		sen = sen.split()
		all_sent.append(sen)
	# all_sent.append(sentences)


model = gensim.models.Word2Vec(all_sent, min_count=1)
model.save("word2vec")





# with open('qa_pair_squad.json', 'w') as f:
# 	json.dump(Final, f)
with open('qa_pair_squad.json', 'w') as f:
	json.dump(Final, f)


