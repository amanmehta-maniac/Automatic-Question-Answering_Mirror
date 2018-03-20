import gensim
from scipy import spatial
import re
 
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
        sentences[i] = s.lower().split(" ")
    # print sentences
    return sentences



stop = []
f = open('stop_words.txt','r')
lines = f.readlines()
for line in lines:
	line = line.strip()
	stop.append(line)
stop.append(" ")

sentences = []
for i in range(4,5):
	sentences += extract_sentences(i,1)


thresh = 0
print "sentence done"
# train word2vec on the two sentences
model = gensim.models.Word2Vec(sentences, min_count=1)

print "model done"

def cosine(a,b):
	# print a,b
	result = 1.0 - spatial.distance.cosine(a, b)
	return result




def get_ans(avg2):
	ret = []
	maxi = 1001023
	for sent in sentences:
		avg = 0
		cnt = 0
		# print sent
		for word in sent:
			cnt += 1
			word = word.lower()
			if word not in model.wv:
				print word
				continue
			if word in stop:
				continue
			if type(avg) == int:
				avg = model.wv[word]
			else:
				avg += model.wv[word]
		avg /= float(cnt)
		sim = cosine(avg, avg2)
		if sim > thresh:
			ret.append([" ".join(sent),sim])
	ret.sort(key=lambda x: x[1])
	# print ret[-1:]
	# print [i[0] for i in ret[-10:]]
	return " ".join([i[0] for i in ret[-10:]])


# for index in range(len(whip)):
# 	paras = whip[index]['paragraphs']
# 	for para in paras:
# 		train_x = []
# 		train_y = []
# 		c = para['context']
# 		c = c.split('.')
# 		for q in para['qas']:
# 			# qid+=1 
# 			# for ci in c:
# 			# 	if ci != "":
# 			# 		feat_final = [qid]+[q['question'],ci]
# 			# 		write_str += str(qid)+",'"+q['question']+"','"+ci+"'\n"
while(1):
	q = raw_input().strip()
	avg = 0
	cnt = 0
	ques = q.split(" ")
	for word in ques:
		cnt += 1
		# print word
		word = word.lower()
		if word not in model.wv:
			print word
			continue
		if word in stop:continue
		if type(avg) == int: 
			avg = model.wv[word]
		else:
			avg += model.wv[word]
	avg /= float(cnt)

	ans = get_ans(avg)
	print "QUESTION"
	print q
	print "ANSWER"
	print ans
	print

