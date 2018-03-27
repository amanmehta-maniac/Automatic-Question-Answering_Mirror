import os
import re
import pickle
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

s = open('train-v1.1.json', 'r').read()
whip = eval(s)

whip = whip["data"]
print type(whip)

paras = whip[0]['paragraphs']

final = ""
for index in range(len(whip)):
	paras = whip[index]['paragraphs']
	for para in paras:
		c = para['context']
		final += c + "\n"
f = open("contexts_squad.txt","w")
f.write(final)