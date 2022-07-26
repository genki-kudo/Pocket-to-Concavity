import subprocess
import os
import math
import shutil
import numpy as np
import pandas as pd

#delete dir
def clean_dir(name):
    if (os.path.isdir(name)):
        shutil.rmtree(name)
    return

#atom and xyz dictionary
def dict_pdb_noh(pdbfile):
    dict = {}
    with open(pdbfile, 'r')as pdb:
        for line in pdb:
            if (line[0:6]=="HETATM" or line[0:6]=="ATOM  ") and line[76:78]!=' H':
                dict[str(line[12:16])] = np.array([float(line[31:38]), float(line[39:46]), float(line[47:54])])
    return dict

#extract xyz of a atom
def ext_xyz(pdbline):
    if pdbline[0:6]=="HETATM" or pdbline[0:6]=="ATOM  ":
        x = float('{:.3f}'.format(float(pdbline[31:38])))
        y = float('{:.3f}'.format(float(pdbline[39:46])))
        z = float('{:.3f}'.format(float(pdbline[47:54])))
        return x, y, z
    else:
        return 'None'

#calculate vector of a atom
def vec_xyz(pdbline):
    if pdbline[0:6]=="HETATM" or pdbline[0:6]=="ATOM  ":
        x = float('{:.3f}'.format(float(pdbline[31:38])))
        y = float('{:.3f}'.format(float(pdbline[39:46])))
        z = float('{:.3f}'.format(float(pdbline[47:54])))
        xyz = [x, y, z]
        vec_xyz = np.array(xyz)
        return vec_xyz
    else:
        return 'None'
    
def dist_cf(vec_a, vec_b, d_min):
    distance = float(np.linalg.norm(vec_a - vec_b))
    if distance <= d_min:
        return distance
    else:
        return d_min

#truncated file  
def t_file(filename):
    with open(filename,'w')as file:
        file.truncate(0)


def appr(xxx):
    if xxx < 0:
        return '{:7.03f}'.format(xxx - 0.5)
    else:
        return '{:7.03f}'.format(xxx + 0.5)
        
def lat_gen(inputname, outputname):
    t_file('lat.pdb')
    p_num = 0
    with open(inputname,'r')as poc:
        for line in poc:
            if line[0:6] == 'ATOM  ' or line[0:6] == 'HETATM':
                p_num += 1
                num_pdb = '{:5}'.format(p_num)
                lxi = math.modf(float(line[31:38]))[1]
                lyi = math.modf(float(line[39:46]))[1]
                lzi = math.modf(float(line[47:54]))[1]
                llx = appr(lxi)
                lly = appr(lyi)
                llz = appr(lzi)
                with open('lat.pdb','a')as lat:
                    print('HETATM'+str(num_pdb)+'      PLA A   1      '+str(llx)+' '+str(lly)+' '+str(llz)+'  1.00 10.00           H', file=lat)
    t_file('lat_ex.txt')
    with open('lat.pdb','r')as poc:
        for line in poc:
            lat_x = float(line[31:38])
            lat_y = float(line[39:46])
            lat_z = float(line[47:54])
            for j in range(3):
                x = round(float(j-1.0),1)
                for k in range(3):
                    y = round(float(k-1.0),1)
                    for l in range(3):
                        z = round(float(l-1.0),1)
                        with open('lat_ex.txt','a')as exp:
                            print(lat_x+x, lat_y+y, lat_z+z, file=exp)
    df = pd.read_csv('lat_ex.txt', sep=" ",header=None)
    dup = df.drop_duplicates()
    t_file(outputname)
    p_num = 0
    for item in zip(dup[0],dup[1],dup[2]):
        p_num += 1
        num_pdb = '{:5}'.format(p_num)
        one_x = '{:7.03f}'.format(float(item[0]))
        one_y = '{:7.03f}'.format(float(item[1]))
        one_z = '{:7.03f}'.format(float(item[2]))
        with open (outputname,'a')as poc:
            print('HETATM'+num_pdb+'      PLA A   1     '+one_x+' '+one_y+' '+one_z+'  1.00 10.00           H', file=poc)
    subprocess.call(['rm', 'lat.pdb'])
    subprocess.call(['rm', 'lat_ex.txt'])
