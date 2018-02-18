# f = open("test","r")
# lines = f.readlines()

# print lines
p = ["He", "he", "Him", "him", "She", "she", "Her","her", "It", "it", "They", "they"]
r = ["Himself", "himself", "Herself", "herself","Itself", "itself", "Themselves", "themselves"]

def read_words(words_file):
    return [word for line in open(words_file, 'r') for word in line.split()]

p_indxs = []
r_indxs = []
words = read_words("test")
for indx,word in enumerate(words):
	print indx,word
	if word in p:
		p_indxs.append(indx)
	if word in r:
		r_indxs.append(indx)

print p_indxs,r_indxs
