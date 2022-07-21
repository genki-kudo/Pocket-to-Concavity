from script.basic_func import vec_xyz
from script.basic_func import t_file
import numpy as np

def elim(defpoc, outdir):
    nshape = './'+outdir+'/newshape_pocket.pqr'
    t_file(nshape)
    dictionary={}
    with open(defpoc,'r')as poc1:
        num = 0
        for a in poc1:
            num+=1
            plist=[]
            with open(defpoc,'r')as poc2:
                target = 0
                for b in poc2:
                    target += 1
                    distance = float(np.linalg.norm(vec_xyz(a)- vec_xyz(b)))
                    if distance <= 1.53 and distance != 0:
                        plist.append(target)
            dictionary[num] = plist
    dout = {0:[]}
    while len(dout)!=0:
        dout = {k: v for k, v in dictionary.items() if len(v)<=3}
        dsafe = {k: v for k, v in dictionary.items() if len(v)>=4}
        for i in dout.keys():
            for j in dsafe.values():
                if i in j:
                    j.remove(i)
        dictionary = dsafe
    n=0
    with open(nshape,'a')as nsh:
        with open(defpoc,'r')as dep:
            for line in dep:
                n+=1
                if n in dictionary.keys():
                    print(line,end='',file=nsh)
    return nshape
