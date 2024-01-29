def LCS(S1,S2):
    MT=np.zeros([len(S1)+1,len(S2)+1])
    for i in range(1,len(S1)+1):
        for j in range(1,len(S2)+1):
            if S1[i-1]==S2[j-1]:
                MT[i][j]=MT[i-1][j-1]+3
            else:
                MT[i][j]=max(MT[i-1][j]-2,MT[i][j-1]-2,0)
    return np.amax(MT)

def FeatureExtract(PTR,REF,dis):
    from statistics import stdev
    P=len(PTR)
    R=len(REF)
    ls=[]
    for i in range(0,R-P+1):
        if REF[i:i+P]==PTR:
            ls.append(abs(i-dis))
    if len(ls)==0:
        STD,TN,AVG,FLG10=-1,-1,-1,-1
    else:
        TN=len(ls)
        AVG=((sum(ls))/(len(ls)))
        STD=0
        FLG10=0
        for i in range(0,len(ls)):
            for j in range(i+1,len(ls)):
                D=abs(ls[j]-ls[i])
                if (D%10==0)|(D%11==0)|(D%12==0):
                    FLG10=FLG10+1
        if TN>1:
            STD=stdev(ls)
    return [TN,AVG,STD,FLG10,FLG10,FLG10]

def PositionFeatures(PTR,REF,dis,PT):
    P=len(PTR)
    R=len(REF)
    for i in range(0,141):
        if i<=70:
            if REF[i:i+P]==PTR:
                PT[70-i]=1
        else:
            if REF[i:i+P]==PTR:
                PT[i-70]=1
    return PT

def FeatureExtractL(PTR,REF,dis):
    from statistics import stdev
    P=len(PTR)
    R=len(REF)
    ls=[]
    for i in range(0,22):
        if REF[i:i+P]==PTR:
            ls.append(abs(i-dis))
    for i in range(178,200):
        if REF[i:i+P]==PTR:
            ls.append(abs(i-dis))
    if len(ls)==0:
        STD,TN,AVG,FLG10=-1,-1,-1,-1
    else:
        TN=len(ls)
        AVG=((sum(ls))/(len(ls)))
        STD=0
        FLG10=0
        FLG11=0
        FLG12=0
        for i in range(0,len(ls)):
            for j in range(i+1,len(ls)):
                D=abs(ls[j]-ls[i])
                if (D%10==0)|(D%11==0)|(D%12==0):
                    FLG10=FLG10+1
        if TN>1:
            STD=stdev(ls)    
    return [TN,AVG,STD,FLG10,FLG10,FLG10]

def GetF(seq):
    ls=[]
    for i in range(0,140):
        if seq[i:i+4]=='AAAA':
            ls.append(i)
    c=0
    for i in range(0,len(ls)):
        for j in range(i+1,len(ls)):
            if (abs(ls[i]-ls[j])%10==0)|(abs(ls[i]-ls[j])%11==0)|(abs(ls[i]-ls[j])%12==0):
                c=c+1
    ls=[]
    for i in range(0,140):
        if seq[i:i+4]=='CGCG':
            ls.append(i)
    c1=len(ls)
    return [c,c1]

def PositionFeaturesL(PTR,REF,dis,PT):
    P=len(PTR)
    R=len(REF)
    for i in range(0,22):
        if REF[i:i+P]==PTR:
            PT[i]=1
    for i in range(178,200):
        if REF[i:i+P]==PTR:
            PT[199-i]=1
    return PT

def ComSeq(seq):
    s=''
    seq=seq[::-1]
    for i in range(0,len(seq)):
        if seq[i]=='A':
            s=s+'T'
        if seq[i]=='T':
            s=s+'A'
        if seq[i]=='C':
            s=s+'G'
        if seq[i]=='G':
            s=s+'C'
    return s


def SimilarityScore(F,REF1,REF2):
    RE=LCS(REF1,REF2[::-1])
    F=[RE]
    RE=LCS(REF1,ComSeq(REF2))
    F.append(RE)
    return F


def CallFunc(PTR,REF,IDN,PO,dis):
    F=FeatureExtract(PTR,REF,dis)
    PO=PositionFeatures(PTR,REF,IDN,PO)
    return F,PO

def CallFuncL(PTR,REF,IDN,PO,dis):
    F=FeatureExtractL(PTR,REF,dis)
    PO=PositionFeaturesL(PTR,REF,IDN,PO)
    return F,PO


def WriteFeatures(F):
    s=''
    global Fe
    for j in range(0,len(F)):
        s=s+str(F[j])+','
    Fe.write(s)


import sys
import numpy as np
Arg1=sys.argv[1]
D=open(Arg1,'r')
DT=D.readlines()
D.close()
global Fe
Fe=open('F'+Arg1,'w')
P=['A','T','C','G']
for i in range(0,len(DT)):
    PV=0
    print(i)
    dyad=100
    REF=DT[i][dyad-70:dyad+73]
    for a in P:
        for b in P:
            DI=[]
            for s in range(0,71):
                DI.append(0)
            PV=PV+1
            F,DI=CallFunc(a+b,REF,70,DI,70)
            WriteFeatures(F)
            WriteFeatures(DI)
            for c in P:
                TI=[]
                for s in range(0,71):
                    TI.append(0)
                PV=PV+1
                F,TI=CallFunc(a+b+c,REF,70,TI,70)
                WriteFeatures(F)
                WriteFeatures(TI)
    F=[]
    F=SimilarityScore(F,REF[0:70],REF[71:141])
    WriteFeatures(F) 
    REF=DT[i][dyad-100:dyad+103]
    DI=[]
    TI=[]
    PV=0
    for a in P:
        for b in P:
            DI=[]
            for s in range(0,22):
                DI.append(0)
            PV=PV+1
            F,DI=CallFuncL(a+b,REF,100,DI,100)
            WriteFeatures(F)
            WriteFeatures(DI)
            for c in P:
                TI=[]
                for s in range(0,22):
                    TI.append(0)
                PV=PV+1
                F,TI=CallFuncL(a+b+c,REF,PV,TI,100)
                WriteFeatures(F)
                WriteFeatures(TI)
    F=[]
    F=SimilarityScore(F,REF[0:22],REF[178:200])
    WriteFeatures(F)
    if Arg1=='TP':
        Fe.write('1\n')
    else:
        Fe.write('0\n')
Fe.close()