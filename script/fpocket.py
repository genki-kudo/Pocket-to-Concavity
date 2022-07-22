import subprocess
import numpy as np
from script.basic_func import t_file, vec_xyz, dist_cf

def fpoc_lf(protein, pro_name, rank, outdir):
    subprocess.call(['fpocket', '-f', protein])
    subprocess.call(["mv", './'+pro_name+'_out/', 'fpoc_output/'])
    inipoc = 'fpoc_output/'+pro_name+'_pockets.pqr'
    defpoc = './'+outdir+'/default_pocket.pqr'
    t_file(defpoc)
    with open(defpoc,'a')as dpoc:
        with open(inipoc, 'r')as inp:
            for line in inp:
                if line[0:6]=="ATOM  ":
                    if int(line[22:28])<=int(rank):
                        print(line, end='', file=dpoc)
                    elif int(line[22:28])>int(rank):
                        break
    return defpoc

def fpoc_lb(protein, pro_name, ligand, distance, outdir):
    subprocess.call(['fpocket', '-f', protein, '-i', '1'])
    subprocess.call(["mv", './'+pro_name+'_out/', 'fpoc_output/'])
    inipoc = 'fpoc_output/'+pro_name+'_pockets.pqr'
    defpoc = './'+outdir+'/default_pocket.pqr'
    t_file(defpoc)
    near = []
    with open(inipoc,'r')as poc:
        for line in poc:
            if str(vec_xyz(line))!='None':
                dislist = []
                for lig_ar in ligand.values():
                    dislist.append(float(np.linalg.norm(vec_xyz(line) - lig_ar)))
                if float(min(dislist))<=float(distance):
                    near.append(line[22:28])
    near_list = set(near)
    with open(defpoc,'a')as dpoc:
        with open(inipoc,'r')as poc:
            for line in poc:
                if (line[22:28]) in near_list:
                    print(line, end='', file=dpoc)
    return defpoc
