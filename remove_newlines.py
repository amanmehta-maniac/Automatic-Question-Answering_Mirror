f = open("tempout.txt","r")
lines = f.readlines()


final = []
flag = 0
cnt = 0
for line in lines:
	# print line,flag
	if "(ROOT\n" in line:
		# print "yes"
		flag = 1
	if flag:
		if "(ROOT" not in line:
			final.append(line)
	if "(. .)" in line:
		flag = 0
		cnt += 1
		# print line
cnt2 = 0
for ind,i in enumerate(final):
	if "(. .)" in i: 
		cnt2+=1
		if cnt2 < cnt:
			final[ind] = "(. .)"
		else:
			s = "(. .)"+")"*(cnt)
			final[ind] = s
for ind,i in enumerate(final):
	final[ind] = i.strip()
out = ""
for i in final:
	out += " " +i 
print out  