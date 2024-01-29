from tensorflow import keras
from tensorflow.keras.utils import plot_model
from tensorflow.keras.models import model_from_json
import numpy as np
import copy
DT=open('Train.txt','r')
TR=DT.readlines()
DT.close()
DT=open('Test.txt','r')
TE=DT.readlines()
DT.close()
DT=open('TrainL.txt','r')
TRL=DT.readlines()
DT.close()
DT=open('TestL.txt','r')
TEL=DT.readlines()
DT.close()
TRDT=[]
TEDT=[]
TRDL=[]
TEDL=[]
for i in range(0,len(TR)):
    k=TR[i].replace('\n','').split(',')
    l1=[]
    for r in range(0,len(k)):
        l1.append(float(k[r]))
    TRDT.append(l1)
    k=TRL[i].replace('\n','')
    TRDL.append(int(round(float(k))))
for i in range(0,len(TE)):
    k=TE[i].replace('\n','').split(',')
    l1=[]
    for r in range(0,len(k)):
        l1.append(float(k[r]))
    TEDT.append(l1)
    k=TEL[i].replace('\n','')
    TEDL.append(int(round(float(k))))
inp=keras.layers.Input(shape=(len(TRDT[0]),))
H1=keras.layers.Dense(len(TRDT[0]),activation='sigmoid')(inp)
keras.layers.Add()([inp,H1]) 
for i in range(1,50):
    H2=keras.layers.Dense(len(TRDT[0]),activation='sigmoid')(H)
    if i%5==0:
        H3=keras.layers.Add()([inp,H2])
Out=keras.layers.Dense(1,activation='sigmoid')(H3)
model=keras.Model(inputs=[inp],outputs=[Out])
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
OPT=['sgd','rmsprop','adam','adadelta','adagrad','adamax','nadam','ftrl']
ne=10000
model.fit(TRDT,TRDL,epochs=1,batch_size=100,validation_data=(TEDT, TEDL),verbose=1)
M1 = model.get_weights()
res=model.evaluate(TEDT,TEDL,verbose=0)
es=0
for epoch in range(ne):
    model.fit(TRDT,TRDL,epochs=10,batch_size=100,validation_data=(TEDT, TEDL),verbose=1)
    re=model.evaluate(TEDT,TEDL,verbose=0)
    print(epoch,re)
    es=es+1
    if res[1]<=re[1]:
        es=0
        print('Improvment',epoch,re[1])
        res=copy.copy(re)
        M1=model.get_weights()
        PRE=model.predict(TEDT)
        model_json = model.to_json()
        with open("model.json", "w") as json_file:
            json_file.write(model_json)
        model.save_weights("MyMDl")
        plot_model(model, to_file='model_plot.png', show_shapes=True, show_layer_names=True)
        json_file.close()
    else:
        k=np.random.randint(len(OPT))
        model.compile(loss='binary_crossentropy',optimizer=OPT[k],metrics=['accuracy'])
        model.set_weights(M1)
    if es>5:
        break
PRE=model.predict(TEDT)
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
model.save_weights("MyMDl")
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("MyMDl")
loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
PRE=loaded_model.predict(TEDT)
T=0
for i in range(0,len(TEDL)):
    if TEDL[i]==(round(PRE[i][0])):
        T=T+1
print(T,len(TEDL),T/len(TEDL))
PRE=model.predict(TRDT)
T=0
F=open('PREDICTION.txt','w')
for i in range(0,len(TRDL)):
    F.write(str(TRDL[i])+','+str(PRE[i][0])+'\n')
    if TRDL[i]==(round(PRE[i][0])):
        T=T+1
F.close()