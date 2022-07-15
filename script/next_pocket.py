import subprocess
import math
from sklearn.cluster import DBSCAN
from script.basic_func import appr, lat_gen, t_file

def clst_poc(nshape, ligand, outdir):
    lat_gen(nshape, 'ATOM  ', './'+outdir+'/poc_lat.pdb')
    lat_gen(ligand, 'HETATM', './'+outdir+'/lig_lat.pdb')
    poclat = './'+outdir+'/poc_lat.pdb'
    liglat = './'+outdir+'/lig_lat.pdb'
    subprocess.call(['mkdir', outdir+'/cluster'])
    t_file('./'+outdir+'/poc_surp.pdb')
    surp = './'+outdir+'/poc_surp.pdb'
    t_file('./'+outdir+'/poc_next.pqr')
    t_file('./'+outdir+'/cluster/cluster_all.pqr')
    t_file('./'+outdir+'/cluster/clus.pqr')
    with open(surp,'a')as sur:
        with open(poclat,'r')as pla:
            for pline in pla:
                px, py, pz = float(pline[31:38]), float(pline[39:46]), float(pline[47:54])
                dupl = 0
                with open(liglat,'r')as lla:
                    for lline in lla:
                        lx, ly, lz = float(lline[31:38]), float(lline[39:46]), float(lline[47:54])
                        if px==lx and py==ly and pz==lz:
                            dupl += 1
                            break
                    if dupl==0:
                        print(pline, end='', file=sur)
    num = 0
    with open(nshape,'r')as poc:
        for l in poc:
            llx = appr(math.modf(float(l[31:38]))[1])
            lly = appr(math.modf(float(l[39:46]))[1])
            llz = appr(math.modf(float(l[47:54]))[1])
            check = 0
            with open(liglat,'r')as lla:
                for lline in lla:
                    llax, llay, llaz = float(lline[31:38]), float(lline[39:46]), float(lline[47:54])
                    if float(llx)==llax and float(lly)==llay and float(llz)==llaz:
                        check += 1
                        break
            if check == 0:
                num += 1
                with open('./'+outdir+'/poc_next.pqr','a')as pro:
                    print(l, end='', file=pro)
    data =[]
    with open('./'+outdir+'/poc_next.pqr','r')as pro:
        for l in pro:
            lst = [float(l[31:38]), float(l[39:46]), float(l[47:54])]
            data.append(lst)
    db = DBSCAN(eps=2, min_samples=1).fit(data)
    labels = list(db.labels_)
    for i in range(len(data)):
        with open('./'+outdir+'/poc_next.pqr','r')as pro:
            p = pro.readlines()[i]
            if str(labels[i]) != str(-1) and labels.count(int(labels[i])) >= 5:
                with open('./'+outdir+'/cluster/clus.pqr','a')as cls:
                    print(p[0:20], str('{:5}'.format(labels[i])), p[27:], end='', file=cls)
    with open('./'+outdir+'/cluster/clus.pqr','r')as cls:
        data = cls.readlines()
        data.sort(key=lambda data: data[21:26])
    with open('./'+outdir+'/cluster/cluster_all.pqr','a')as cls:
        for i in range(len(data)):
            print(data[i], end='', file=cls)

    with open('./'+outdir+'/cluster/cluster_all.pqr','r')as cls:
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
    subprocess.call(['rm', './'+outdir+'/cluster/clus.pqr'])
    subprocess.call(['rm', './'+outdir+'/cluster/cluster_all.pqr'])
    