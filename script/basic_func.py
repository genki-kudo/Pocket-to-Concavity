from subprocess import run
import os
import math
import shutil
import numpy as np
import pandas as pd
import argparse
import datetime

bash=lambda x:run(x,shell=True)

#input_discription
def input_process():
    
    input_list=[0 for i in range(9)]

    parser = argparse.ArgumentParser(prog='p2c')
    parser.add_argument('-m', '--method', nargs=1, required=True, help='select mode of P2C (LF, LB)')
    parser.add_argument('-p', '--protein', nargs=1, required=True, help='specify protein file path (format:PDB)')
    parser.add_argument('-l', '--ligand', nargs=1, default=["None"], help='specify ligand file path (format:PDB). Only use this argument when you select "LB" mode.')
    parser.add_argument('-d', '--distance', nargs=1, type=float, default=[1.8], help='specify distance of include pocket. Only use this argument when you select "LB".')
    parser.add_argument('-r', '--rank', nargs=1, type=int, default=[1], help='specify druggability rank by fpocket of include pocket. Only use this argument when you select "LF".')
    parser.add_argument('-c', '--clustering', nargs=1, default=["SINGLE"], help='select "DBSCAN" if you do not use fpocket-clustering-method in empty site identification. Only use this argument when you select "LB".')
    parser.add_argument('-t', '--threshold', nargs=1, type=float, default=[-1], help='threshold of clustering. (order is 1^-10m)')
    parser.add_argument('-o', '--logfilename', nargs=1, default=["p2c.log"], help='specify logfile name (default:p2c.log)')

    args = parser.parse_args()
    
    input_list[0] = str(args.method[0]).upper()#method
    input_list[1] = str(args.protein[0])#protein
    input_list[2] = str(args.ligand[0])#ligand
    input_list[3] = str(args.distance[0])#distance
    input_list[4] = str(args.rank[0])#rank
    input_list[5] = os.path.splitext(input_list[1])[0]#pro_name
    input_list[6] = str(args.clustering[0]).upper()#clustering
    input_list[7] = float(args.threshold[0])
    input_list[8] = str(args.logfilename[0])

    #confirm command input
    if input_list[0]!="LF" and input_list[0]!="LB":
        print("fatal error! method select only LF or LB. ")
        exit()
    if input_list[1][-4:]!='.pdb' :
        print("fatal error! protein select only .pdb format. ")
        exit()
    if input_list[2][-4:]!='.pdb' and input_list[0]=='LB':
        print("fatal error! ligand select only .pdb format. ")
        exit()
    clustering_m = {'DBSCAN':2.0, 'SINGLE':4.5}
    if input_list[6]not in clustering_m.keys():
        print("fatal error! P2C does not have clustering-method["+input_list[6]+"]. ")
        exit()
    if input_list[7]==-1:
        input_list[7]=clustering_m[input_list[6]]

    # output
    s=""
    s+=str(datetime.datetime.now())+"\n"
    s+="Selected Mode\n>> "+input_list[0]+"\n"
    s+="Selected PDB protein file\n>> "+os.path.abspath(input_list[1])+"\n"
    s+="Selected PDB ligand file\n>> "+os.path.abspath(input_list[2])+"\n"
    if input_list[0] == 'LB':
        s+="Distance of include pocket\n>> "+input_list[3]+"\n"
        s+="Clustering method in empty sites identification\n>> "+input_list[5]+"\n"
        s+="Clustering threshold in empty sites identification\n>> "+input_list[6]+"\n"
    if input_list[0] == 'LF':
        s+="Druggability rank of include pocket\n>> "+input_list[4]+"\n"
    print(s)
    input_list.append(s)

    return input_list

#delete dir
def clean_dir(name):
    if (os.path.isdir(name)):
        shutil.rmtree(name)
    return

#atom and xyz dictionary
def dict_pdb_noh(pdbfile):
    dict = {}
    for line in open(pdbfile).readlines():
        if (line[0:6]=="HETATM" or line[0:6]=="ATOM  ") and line[76:78]!=' H':
            dict[str(line[12:16])] = np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])
    return dict

#extract xyz of a atom
def ext_xyz(pdbline):
    if pdbline[0:6]=="HETATM" or pdbline[0:6]=="ATOM  ":
        x = float('{:.3f}'.format(float(pdbline[30:38])))
        y = float('{:.3f}'.format(float(pdbline[38:46])))
        z = float('{:.3f}'.format(float(pdbline[46:54])))
        return x, y, z
    else:
        return 'None'

#calculate vector of a atom
def vec_xyz(pdbline):
    if pdbline[0:6]=="HETATM" or pdbline[0:6]=="ATOM  ":
        x = float('{:.3f}'.format(float(pdbline[30:38])))
        y = float('{:.3f}'.format(float(pdbline[38:46])))
        z = float('{:.3f}'.format(float(pdbline[46:54])))
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
    poc = open(inputname,'r').readlines()
    lat=[]
    for line in poc:
        if line[0:6] == 'ATOM  ' or line[0:6] == 'HETATM':
            p_num += 1
            num_pdb = '{:5}'.format(p_num)
            lxi = math.modf(float(line[30:38]))[1]
            lyi = math.modf(float(line[38:46]))[1]
            lzi = math.modf(float(line[46:54]))[1]
            llx = appr(lxi)
            lly = appr(lyi)
            llz = appr(lzi)
            hetatm='HETATM'+str(num_pdb)+'      PLA A   1   '+str(llx).rjust(8)+str(lly).rjust(8)+str(llz).rjust(8)+'  1.00 10.00           H\n'
            lat.append(hetatm)
    tmp = open('lat.pdb','w').writelines(lat)
    t_file('lat_ex.txt')
    poc = open('lat.pdb','r').readlines()
    for line in poc:
        lat_x = float(line[30:38])
        lat_y = float(line[38:46])
        lat_z = float(line[46:54])
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
    bash('rm lat.pdb')
    bash('rm lat_ex.txt')

def logo():
    print('        PPPPPPPPP/     22222222/      CCCCCCCC/')
    print('       PP/     PP/           22/     CC/       ')
    print('      PPPPPPPPP/     22222222/      CC/')
    print('     PP/            22/            CC/       ')
    print('    PP/            22222222/      CCCCCCCC/')
    print('')
