import nltk,sys
import re
import ipdb
from stat_parser import Parser
parser = Parser()


chapNum = (int)(sys.argv[1])
classIdentifier = "i"

if chapNum > 8:
	chapNum -= 8
	classIdentifier = "j"

file = open("./Dataset_NCERT/Dataset-txt/"+classIdentifier+"ess30"+str(chapNum)+".txt")
sentences = file.read()
file.close()
sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', sentences)
for i, s in enumerate(sentences):
	s = s.replace("\n", " ")
	# print POS
	sentences[i] = s




###pos tagging #####
# POS = nltk.pos_tag(nltk.word_tokenize(sentences[0]))
# print sentences[0]
# print POS
# print sentences

print sentences[0]
# print nltk.word_tokenize(sentences[0])
print parser.parse((str)(sentences[0]))
# print parser.parse(str(sentences[0]))
