from subprocess import run
import numpy as np
from script.basic_func import t_file, vec_xyz

bash=lambda x:run(x,shell=True)

def fpoc_lf(protein, pro_name, rank, outdir,logfile):
    bash('/home/user01/software/fpocket2/bin/fpocket -f '+protein+' >> '+outdir+"/"+logfile)
    bash('mv '+pro_name+'_out/ fpoc_output/')
    inipoc = 'fpoc_output/'+pro_name.split("/")[-1]+'_pockets.pqr'
    defpoc = outdir+'/default_pocket.pqr'
    t_file(defpoc)
    inp  = open(inipoc,'r').readlines()
    dpoc=[]
    for line in inp:
        if line[0:6]!="ATOM  ":continue
        if int(line[22:28])<=int(rank):
            dpoc.append(line)
        elif int(line[22:28])>int(rank):
            break
    tmp = open(defpoc,'w').writelines(dpoc)
    return defpoc

def fpoc_lb(protein, pro_name, ligand, distance, outdir, logfile):
    bash('/home/user01/software/fpocket2/bin/fpocket -f '+protein+' -i 1 >> '+outdir+"/"+logfile)
    bash('mv '+pro_name+'_out/ fpoc_output/')
    inipoc = 'fpoc_output/'+pro_name.split("/")[-1]+'_pockets.pqr'
    defpoc = outdir+'/default_pocket.pqr'
    t_file(defpoc)
    near = []
    poc = open(inipoc,'r').readlines()
    for line in poc:
        if str(vec_xyz(line))=='None':continue
        dislist = []
        for lig_ar in ligand.values():
            dislist.append(float(np.linalg.norm(vec_xyz(line) - lig_ar)))
        if float(min(dislist))<=float(distance):
            near.append(line[22:28])
    near_list = set(near)
    dpoc = []
    for line in poc:
        if (line[22:28]) in near_list:
            dpoc.append(line)
    tmp = open(defpoc,'w').writelines(dpoc)
    return defpoc
