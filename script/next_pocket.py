from subprocess import run
import math
import sys
from sklearn.cluster import DBSCAN
from scipy.cluster.hierarchy import linkage, fcluster
from script.basic_func import appr, lat_gen, t_file

bash = lambda x:run(x,shell=True)

def next_poc(nshape, ligand, outdir):
    lat_gen(nshape, outdir+'/poc_lat.pdb')
    lat_gen(ligand, outdir+'/lig_lat.pdb')
    poclat = outdir+'/poc_lat.pdb'
    liglat = outdir+'/lig_lat.pdb'
    t_file(outdir+'/poc_surp.pdb')
    surp = outdir+'/poc_surp.pdb'
    t_file(outdir+'/poc_next.pqr')
    next = outdir+'/poc_next.pqr'
    sur=[]
    pla = open(poclat,"r").readlines()
    lla = open(liglat,"r").readlines()
    for pline in pla:
        px, py, pz = float(pline[30:38]), float(pline[38:46]), float(pline[46:54])
        dupl = 0
        for lline in lla:
            lx, ly, lz = float(lline[30:38]), float(lline[38:46]), float(lline[46:54])
            if px==lx and py==ly and pz==lz:
                dupl += 1
                break
        if dupl==0:
            sur.append(pline)
    tmp=open(surp,"w").writelines(sur)
    num = 0
    poc = open(nshape,"r").readlines()
    pro=[]
    for l in poc:
        llx = appr(math.modf(float(l[30:38]))[1])
        lly = appr(math.modf(float(l[38:46]))[1])
        llz = appr(math.modf(float(l[46:54]))[1])
        check = 0
        for lline in lla:
            llax, llay, llaz = float(lline[30:38]), float(lline[38:46]), float(lline[46:54])
            if float(llx)==llax and float(lly)==llay and float(llz)==llaz:
                check += 1
                break
        if check == 0:
            num += 1
            pro.append(l)
    tmp=open(next,"w").writelines(pro)
    return next

def clus_poc(clustering, next,threshold, outdir):
    bash('mkdir '+outdir+'/cluster')
    if clustering == 'DBSCAN':
        print("DBSCAN start")
        t_file(outdir+'/cluster/cluster_all.pqr')
        t_file(outdir+'/cluster/clus.pqr')
        pro = open(next,"r").readlines()
        data =[[float(i[30:38]), float(i[38:46]), float(i[46:54])] for i in pro]
        db = DBSCAN(eps=threshold, min_samples=1).fit(data)
        labels = list(db.labels_)
        cls = open(outdir+'/cluster/clus.pqr',"r").readlines()
        for i in range(len(data)):
            p = pro[i]
            if str(labels[i]) != str(-1) and labels.count(int(labels[i])) >= 5:
                cls.append(p[0:20]+str('{:5}'.format(labels[i]))+p[27:])
        tmp=open(outdir+'/cluster/clus.pqr',"w").writelines(cls)
        data = open(outdir+'/cluster/clus.pqr',"r").readlines()
        data.sort(key=lambda data: data[21:26])
        
        cls = open(outdir+'/cluster/cluster_all.pqr','r').readlines()
        for i in range(len(data)):
            cls.append(data[i])
        tmp=open(outdir+'/cluster/cluster_all.pqr',"w").writelines(cls)        
        id = -1
        for line in cls:
            if int(line[21:26])==id:
                with open(outdir+"/cluster/cluster"+str(id)+".pqr",'a')as tmp:
                    print(line, end='', file=tmp)
            else:
                id += 1
                t_file(outdir+"/cluster/cluster"+str(id)+".pqr")
                with open(outdir+"/cluster/cluster"+str(id)+".pqr",'a')as tmp:
                    print(line, end='', file=tmp)
        bash('rm '+outdir+'/cluster/clus.pqr')
        bash('rm '+outdir+'/cluster/cluster_all.pqr')

    elif clustering == 'SINGLE':
        #choose the second clustering of fpocket-clustering-method
        #it is the cnetroid linkage clustering
        #print("fpoc-clustering start")
        second_thre = threshold
        POINTS = []
        for line in open(next,'r').readlines():
            POINTS.append([float(line[30:38]),float(line[38:46]),float(line[46:54])])
        Z = linkage(POINTS, method="centroid", metric="euclidean")
        c = fcluster(Z, second_thre, criterion="distance")
        num = 0
        for line in open(next,'r').readlines():
            with open(outdir+"/cluster/cluster"+str(c[num])+".pqr",'a')as out:
                print(line, end='', file=out)
            num += 1

    else:
        sys.exit()
    
