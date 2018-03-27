import gensim, json
import re
from keras.layers import Input, Dense, LSTM
import keras.backend as K
from keras.models import Model, Sequential
import numpy as np
import tensorflow as tf

def cos_distance(y_true, y_pred):
    def l2_normalize(x, axis):
        norm = K.sqrt(K.sum(K.square(x), axis=axis, keepdims=True))
        return K.maximum(x, K.epsilon()) / K.maximum(norm, K.epsilon())
    # y_true = l2_normalize(y_true, axis=-1)
    # y_pred = l2_normalize(y_pred, axis=-1)
    # return -K.mean(y_true * y_pred, axis=-1)

    return tf.keras.losses.cosine_proximity(y_true,y_pred)


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

word_to_int = ""
int_to_word = ""
def data_for_lstm():
    word_set = set()
    f = open("contexts_squad.txt","r")
    lines = f.readlines()
    seq_len = 8
    dataX = []
    dataY = []
    for line in lines:
        for word in line.strip().split():
            word_set.add(word.lower())
    print "vocabsize:",len(word_set)
    global word_to_int,int_to_word
    word_to_int = dict((c, i) for i, c in enumerate(word_set))
    int_to_word = dict((i, c) for i, c in enumerate(word_set))
    for line in lines:
        words = line.strip().split()
        for i in range(0,len(words)-seq_len):
            seq_in = words[i:i + seq_len]
            seq_out = words[i + seq_len]
            dataX.append([word_to_int[word.lower()] for word in seq_in])
            dataY.append(word_to_int[seq_out.lower()])
    return dataX, dataY

def training_generator(dataX,dataY,flag,batch_size):
    # print "yaha to aaya bhai"
    wordModel = gensim.models.Word2Vec.load("word2vec")
    # print "loaded"
    if flag==1:
        # print "yaha bhi aaya bhai "
        dataY = dataY[int(0.2*len(dataY)):]
        dataX = dataX[int(0.2*len(dataX)):]
    else:
        dataY = dataY[:int(0.2*len(dataY))]
        dataX = dataX[:int(0.2*len(dataX))]
    x=1
    while True:
        # print "while 1 mein"
        i=0
        while i+batch_size<len(dataX):
            # print "batch wale mein"
            X = []
            y = []
            extension = 0
            # print "asdf",range(i,i+batch_size)
            for ind in range(i,i+batch_size+extension):
                skip = 0
                x_chota = dataX[ind]
                temp = []
                for k in x_chota:
                    if int_to_word[k].lower() not in wordModel.wv:
                        extension += 1
                        skip = 1
                        break
                    temp.append(wordModel.wv[int_to_word[k].lower()])
                if skip:
                    continue
                X.append(temp)
                y_chota = dataY[ind]
                temp = []
                # for k in y_chota:
                if int_to_word[y_chota].lower() not in wordModel.wv:
                    extension += 1 
                    skip = 1
                    X.pop()
                if skip:
                    continue
                # temp.append(wordModel.wv[int_to_word[y_chota].lower()])
                y.append(wordModel.wv[int_to_word[y_chota].lower()])
            yield np.array(X),np.array(y)
        i = ind
            
model = Sequential()
model.add(LSTM(16, input_shape=(8,20),dropout=0.5))
# model.add(Dropout(0.2))
model.add(Dense(20))

model.compile(loss='mean_squared_error', optimizer='adam')
batch_size = 32
dataX,dataY = data_for_lstm()
print "data done!"
print 0.8*len(dataX)/batch_size
# st = int(0.8*len(dataX)/batch_size)
st = 20000
# st2 = int(0.2*len(dataY)/batch_size)
st2 = 5000
model.fit_generator(epochs=10,generator=training_generator(dataX,dataY,1,batch_size),steps_per_epoch=st,validation_data=training_generator(dataX,dataY,2,batch_size), validation_steps=st2)
print "returned"

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



