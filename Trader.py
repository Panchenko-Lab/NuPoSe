def GetData():
    Ndt=open('FTP','r')
    NNdt=open('FTN','r')
    DT1=Ndt.readlines()
    DT2=NNdt.readlines()
    Ndt.close()
    NNdt.close()
    TRDT=[]
    TEDT=[]
    TRDL=[]
    TEDL=[]
    for i in range(0,round(len(DT1)*0.8)):
        k=DT1[i].split(',')
        ls=[]
        for j in range(0,len(k)-1):
            ls.append(float(k[j]))
        TRDT.append(ls)
        TRDL.append(1)
    for i in range(round(len(DT1)*0.8),len(DT1)):
        k=DT1[i].split(',')
        ls=[]
        for j in range(0,len(k)-1):
            ls.append(float(k[j]))
        lls=len(ls)
        TEDT.append(ls)
        TEDL.append(1)
    for i in range(0,round(len(DT2)*0.8)):
        k=DT2[i].split(',')
        ls=[]
        for j in range(0,len(k)-1):
            ls.append(float(k[j]))
        TRDT.append(ls)
        TRDL.append(0)
    for i in range(round(len(DT2)*0.8),len(DT2)):
        k=DT2[i].split(',')
        ls=[]
        for j in range(0,len(k)-1):
            ls.append(float(k[j]))
        TEDT.append(ls)
        TEDL.append(0)
    return TRDT,TEDT,TRDL,TEDL

def initial(nob,F,NOF):
    branches=np.zeros([nob,NOF+3])
    for i in range(0,nob):
        for j in range(0,NOF):
            branches[i][j]=random.randint(0,F-1)
    return branches


def score(ARG):
    inx=ARG[0]
    CS=ARG[1]
    global TRDT,TEDT,TRDL,TEDL, SL
    CL=svm.SVC()
    TR=[]
    TD=[]
    for i in range(0,len(TRDT)):
        lst=[]
        for j in range(0,len(CS)-3):
            lst.append(TRDT[i][int(CS[j])])
        TR.append(lst)
    for i in range(0,len(TEDT)):
        lse=[]
        for j in range(0,len(CS)-3):
            lse.append(TEDT[i][int(CS[j])])
        TD.append(lse)
    CL.fit(TR,TRDL)
    PRE=CL.predict(TD)
    T=0
    for i in range(0,len(TD)):
        if TEDL[i]==PRE[i]:
            T=T+1
    SL.append([inx,T/len(TD)])


def profit(branches):
    r=len(branches)
    b=len(branches[0])
    global SL
    SL=[]
    THP=[]
    for i in range(0,r):
        TH=threading.Thread(target=score,args=([i,branches[i]],))
        THP.append(TH)
        TH.start()
    for TH in THP:
        TH.join()
    for i in range(0,len(SL)):
        branches[SL[i][0]][b-1]=SL[i][1]
    return branches


def SelectBests(branches,nog):
    bests=[]
    c=len(branches[0])-1
    for j in range(0,nog):
        ma=branches[0][c]
        inx=0
        for i in range(1,len(branches)):
            if (branches[i][c]>ma)&(j not in bests):
                inx=i
                ma=branches[i][c]
        bests.append(inx)
    return bests


def grouping(branches,nog):
    bests=SelectBests(branches,nog)
    c=len(branches[0])-1
    for i in range(0,len(branches)):
        if i in bests:
            branches[i][c-2]=i
        else:
            branches[i][c-2]=bests[random.randint(1,len(bests))-1]
    return branches


def distributing(branches):
    c=len(branches[0])-1
    r=len(branches)
    for i in range(0,r):
        if i != branches[i][c-2]:
            k=random.randint(1,int(round(c*0.2)))
            for j in range(0,k):
                s=int(random.randint(0,c))
                branches[i][s]=branches[int(branches[i][c-2])][s]
    return branches


def retailing(branches,itr,AllF,noi):
    c=len(branches[0])-1
    r=len(branches)
    for i in range(0,r):
        k=int(max(1,100-round(itr/noi*100)))
        for j in range(0,k):
            s=int(random.randint(0,c))
            branches[i][s]=int(random.randint(0,AllF-1))
    return branches


def CheckImprovments(branches,BR):
    r=len(branches)
    c=len(branches[0])-1
    for i in range(0,r):
        if BR[i][c]>branches[i][c]:
            branches[i]=BR[i]
    return branches


def GetMax(branches):
    c=len(branches[0])-1
    ma=branches[0][c]
    for i in range(1,len(branches)):
        if branches[i][c]>ma:
            ma=branches[i][c]
    return ma


def ReadCSs(nob,F,NOF):
    branches=np.zeros([nob,NOF+3])
    F=open('SF.txt')
    l=F.readlines()
    for i in range(0,nob):
        s=l[i].replace('\n','').split(',')
        for j in range(0,len(s)):
            if j<NOF+2:
                branches[i,j]=int(s[j])
            else:
                branches[i,j]=float(s[j])
    F.close()
    return branches


from sklearn import svm
import numpy as np
import random
import multiprocessing as mp
import threading
import matplotlib.pyplot as plt
import copy
from multiprocessing import set_start_method
import os
global branches,TRDT,TEDT,TRDL,TEDL
TRDT,TEDT,TRDL,TEDL=GetData()
nob=100
NOF=50
if os.path.exists('SF.txt'):
    branches=ReadCSs(nob,len(TRDT[0]),NOF)
else:
    branches=initial(nob,len(TRDT[0]),NOF)
branches=(branches)
noi=100
ham=[]
nog=10
for i in range(0,noi):
    branches=grouping(branches,nog)
    BR=copy.deepcopy(branches)
    BR=distributing(BR)
    BR=profit(BR)
    branches=CheckImprovments(branches,BR)
    BR=copy.deepcopy(branches)
    BR=retailing(BR,i,len(TRDT[0]),noi)
    BR=profit(BR)
    branches=CheckImprovments(branches,BR)
    V=GetMax(branches)
    ham.append(V)
    print(i,V)
    F=open('Convergence.txt','a')
    F.write(str(V)+"\n")
    F.close()
    F=open('SF.txt','w')
    fi=len(branches[0])
    for i in range(0,len(branches)):
        for j in range(0,fi-1):
            F.write(str(branches[i][j])+",")
        F.write(str(branches[i][fi-1])+'\n')
    F.close()