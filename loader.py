import gensim, json
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


def iter2(): 
	q_final = []
	a_final = []
	batch_size = 32;
	model = gensim.models.Word2Vec.load("word2vec")
	with open('qa_pair_squad.json', 'r') as f:
	     data = json.load(f)
	q = []
	a = []
	stop = []
	f = open('stop_words.txt','r')
	lines = f.readlines()
	for line in lines:
		line = line.strip()
		stop.append(line)
	stop.append(" ")
	for d in data:

		qwords = d[0].split()
		awords = d[1].split()
		# print qwords,awords
		avg = 0
		cnt = 0
		for w in qwords:
			w = w.lower()
			if w in stop:
				continue
			if w not in model.wv:
				# print w
				continue
			if type(avg) == int:
				avg = model.wv[w]
			else:
				avg += model.wv[w]
			cnt += 1
		if cnt == 0:
			continue
		avg /= float(cnt)
		# print "q avg", avg
		q.append(avg)

		avg = 0
		cnt = 0
		for w in awords:
			w = w.lower()
			if w in stop:
				continue
			if w not in model.wv:
				# print w
				continue
			if type(avg) == int:
				avg = model.wv[w]
				x = model.wv[w]
				x.tolist()
				# print "aashay bkl: ", len(x)
			else:
				avg += model.wv[w]
			cnt += 1
		if cnt == 0:
			del q[-1]
			continue
		avg /= float(cnt)
		# print "a avg", avg
		a.append(avg)
		# print q
		if len(q)==batch_size:
			# print "lol",q,a
			q_final.append(q)
			a_final.append(a)
			# yield q,a
			q = []
			a = []
	return q_final, a_final



