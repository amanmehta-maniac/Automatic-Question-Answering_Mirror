import re,sys

P = ["He", "he", "Him", "him", "She", "she", "Her","her", "It", "it", "They", "they"]
R = ["Himself", "himself", "Herself", "herself","Itself", "itself", "Themselves", "themselves"]

def read_words(words_file):
    return [word for line in open(words_file, 'r') for word in line.split()]

p_indxs = []
r_indxs = []
abhi_tak = ""

chapNum = (int)(sys.argv[1])
classIdentifier = "i"

if chapNum > 8:
	chapNum -= 8
	classIdentifier = "j"

words = read_words("./Dataset_NCERT/Dataset-txt/"+classIdentifier+"ess30"+str(chapNum)+".txt")
# words = read_words()
# sentences = file.read()
# file.close()
# sentences = re.split(r' *[\.\?!][\'"\)\]]* *', sentences)
# for i, s in enumerate(sentences):
# 	s = s.replace("\n", " ")
# 	# print POS
# 	sentences[i] = s

# lines = sentences
# lines = re.split(r' *[\.\?!][\'"\)\]]* *', text)
spans = []
pros = []
start = 0
end = 0

# for i,line in enumerate(lines):
# 	abhi_tak = ""
# 	for ind in range(start,i+1):
# 		abhi_tak += lines[ind] + ". "
# 	w_line = line.split(" ") 
# 	for p in P:
# 		if p in w_line:
# 			spans.append(abhi_tak)
# 			pros.append(p)
# 	start = max(start,i-5);
# print spans

# for ind,i in enumerate(spans):
# 	f = open("spans/"+str(ind)+".txt","w")
# 	f.write(i)
# 	f = open("pros/"+str(ind)+".txt","w")
# 	f.write(pros[ind])


for indx,word in enumerate(words):
	# print indx,word
	if word in P:
		p_indxs.append(indx)

	if word in R:
		r_indxs.append(indx)

print p_indxs,r_indxs

f = open("1.out","r")
lines = f.readlines()
gen = []
for line in lines:
	line = line.strip()
	gen.append(line)
print gen
print len(words),len(gen),len(p_indxs)
for ind, i in enumerate(p_indxs):
	# print "1",gen[ind]
	# print "2",words[i]
	words[i] = gen[ind]
print 
print words