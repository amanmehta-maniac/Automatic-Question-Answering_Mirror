from keras.layers import Input, Dense
import keras.backend as K
from keras.models import Model
from loader import iter2
import gensim
import json
import numpy as np


def cosine(a,b):
	# print a,b
	result = 1.0 - spatial.distance.cosine(a, b)
	return result

# for x,y in iter2():
# 	print x,y
# 	break
model = gensim.models.Word2Vec.load("word2vec")

encoding_dim = 32  # 32 floats -> compression of factor 24.5, assuming the input is 784 floats

# this is our input placeholder
input_img = Input(shape=(None,100))
# "encoded" is the encoded representation of the input
encoded = Dense(encoding_dim, activation='relu', name='layer1')(input_img)
# "decoded" is the lossy reconstruction of the input
decoded = Dense(100, activation='sigmoid')(encoded)

# this model maps an input to its reconstruction
autoencoder = Model(input_img, decoded)

encoder = Model(input_img, encoded)
# create a placeholder for an encoded (32-dimensional) input
encoded_input = Input(shape=(encoding_dim,))
# retrieve the last layer of the autoencoder model
decoder_layer = autoencoder.layers[-1]
# create the decoder model
decoder = Model(encoded_input, decoder_layer(encoded_input))

q,a = iter2()
# print "behenchod ", len(a), len(a[0][0])
# print q[0],a[0]
autoencoder.compile(optimizer='adadelta', loss='MAE')
autoencoder.fit(q[:1737],q[:1737], batch_size=32, epochs=2,validation_data=(q[1737:], q[1737:]))

# encoding_dim = 32  # 32 floats -> compression of factor 24.5, assuming the input is 784 floats

# this is our input placeholder
input_img2 = Input(shape=(None,100))
# "encoded" is the encoded representation of the input
encoded2 = Dense(encoding_dim, activation='relu', name='layer2')(input_img2)
# "decoded" is the lossy reconstruction of the input
decoded2 = Dense(100, activation='sigmoid', name='layer3')(encoded2)

# this model maps an input to its reconstruction
autoencoder2 = Model(input_img2, decoded2)

encoder2 = Model(input_img2, encoded2)
# create a placeholder for an encoded (32-dimensional) input
encoded_input2 = Input(shape=(encoding_dim,))
# retrieve the last layer of the autoencoder2 model
decoder_layer2 = autoencoder2.layers[-1]
# create the decoder model
decoder2 = Model(encoded_input2, decoder_layer2(encoded_input2))

# q,a = iter2()
# print q[0],a[0]
autoencoder2.compile(optimizer='adadelta', loss='MAE')
autoencoder2.fit(a[:1737],a[:1737], batch_size=32, epochs=2,validation_data=(a[1737:], a[1737:]))


i = Input(shape=(None,encoding_dim))
dense = Dense(encoding_dim,activation='relu')(i)
f = Model(i,dense)

# autoencoder.predict(q[:1737])
# x = K.eval(autoencoder.layers[1].output)

# autoencoder2.predict(a[:1737])
# y = K.eval(autoencoder2.layers[1].output)

# print x,y
# autoencoder.predict(q[1737:])
# x_v = K.eval(autoencoder.layers[1].output)
# autoencoder2.predict(a[1737:])
# y_v = K.eval(autoencoder2.layers[1].output)
intermediate_layer_model = Model(inputs=autoencoder.input,
                                 outputs=autoencoder.get_layer('layer1').output)
x = intermediate_layer_model.predict(q[:1737])

print "len of x:", len(x[0])

intermediate_layer_model = Model(inputs=autoencoder2.input,
                                 outputs=autoencoder2.get_layer('layer2').output)
y = intermediate_layer_model.predict(a[:1737])


intermediate_layer_model = Model(inputs=autoencoder.input,
                                 outputs=autoencoder.get_layer('layer1').output)
x_v = intermediate_layer_model.predict(q[1737:])

intermediate_layer_model = Model(inputs=autoencoder2.input,
                                 outputs=autoencoder2.get_layer('layer2').output)
y_v = intermediate_layer_model.predict(a[1737:])
# print "yahaL: ", len(a[0])

f.compile(optimizer='adadelta', loss='MAE')
f.fit(x,y,batch_size=32,epochs=2,validation_data=(x_v,y_v))


with open('qa_pair_squad.json', 'r') as file1:
	data = json.load(file1)

stop = []
file2 = open('stop_words.txt','r')
lines = file2.readlines()
for line in lines:
	line = line.strip()
	stop.append(line)
stop.append(" ")

while(1):
	q = raw_input("question: ").strip().split()
	chap = raw_input()
	avg = 0
	cnt = 0
	for w in q:
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

	print avg, type(avg), "wahaL: ", len(avg)

	intermediate_layer_model = Model(inputs=autoencoder.input,
	                                 outputs=autoencoder.get_layer('layer1').output)
	mid1 = intermediate_layer_model.predict(np.array([[avg]]))
	print "mid1 done!"
	mid2 = f.predict(mid1)
	print "mid2 done!"
	intermediate_layer_model2 = Model(outputs=autoencoder2.output,
	                                 inputs=autoencoder2.get_layer('layer3').input)
	final = intermediate_layer_model2.predict(mid2)

	# for i in 
	Sent = extract_sentences(chap,1)
	print "extraction done!"
	savg = 0
	cnt = 0
	ret = []
	for s in Sent:
		for w in s.strip().split():
			w = w.lower()
			if w in stop:
				continue
			if w not in model.wv:
				# print w
				continue
			if type(savg) == int:
				savg = model.wv[w]
			else:
				savg += model.wv[w]
			cnt += 1
		if cnt == 0:
			continue
		savg /= float(cnt)
		savg.tolist()
	# for s in Sent:

		sim = cosine(final, avg2)
		if sim > thresh:
			ret.append([" ".join(s),sim])
	print "sim done!"
	ret.sort(key=lambda x: x[1])
	print " ".join([i[0] for i in ret[-10:]])
		# print "yaha pohoch gaya mai:", len(sim)
		# print len(sim),type(sim)
	# if sim > thresh:
	# ret.append([" ".join(sent),sim])
	# ret.sort(key=lambda x: x[1])






