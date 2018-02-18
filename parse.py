import re

P = ["He", "he", "Him", "him", "She", "she", "Her","her", "It", "it", "They", "they"]
R = ["Himself", "himself", "Herself", "herself","Itself", "itself", "Themselves", "themselves"]

def read_words(words_file):
    return [word for line in open(words_file, 'r') for word in line.split()]

p_indxs = []
r_indxs = []
words = read_words("test")
abhi_tak = ""

with open("test") as f:
    text = f.read()

lines = re.split(r' *[\.\?!][\'"\)\]]* *', text)
spans = []

for line in lines:
	abhi_tak += line+". "
	w_line = line.split(" ") 
	for p in P:
		if p in w_line:
			spans.append(abhi_tak)
print spans

for ind,i in enumerate(spans):
	f = open("spans/"+str(ind)+".txt","w")
	f.write(i)

for indx,word in enumerate(words):
	# print indx,word
	if word in P:
		p_indxs.append(indx)

	if word in R:
		r_indxs.append(indx)

print p_indxs,r_indxs
