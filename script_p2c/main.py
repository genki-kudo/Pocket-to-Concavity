import sys
import os
import argparse
import time
from subprocess import run
from script_p2c.fpocket import fpoc_lf,fpoc_lb
from script_p2c.a_elimination import elim
from script_p2c.next_pocket import next_poc, clus_poc
from script_p2c.visual_shapeup import visual_lb, visual_lf
from script_p2c.basic_func import dict_pdb_noh, clean_dir,input_process

bash=lambda x:run(x,shell=True)

def main_exec():
    
    input_list=input_process()
    
    method,protein,ligand,distance,rank,pro_name,clustering,threshold,logfilename, pockets_file, number, s = input_list

    outdir = os.path.dirname(os.path.abspath(protein))+"/p2c_output"    

    clean_dir(outdir+"/")
    clean_dir(pro_name+'_out/')
    clean_dir('asphere_output/')

    bash("mkdir "+outdir)
    tmp=open(outdir+"/"+logfilename,"w").write(s)
    
    tmp = open(outdir+"/"+logfilename,"a").write("###fpocket location###\n")
    bash("which fpocket >> "+outdir+"/"+logfilename)
    tmp = open(outdir+"/"+logfilename,"a").write("###fpocket location###\n")


    if method == 'LF':
        if pockets_file == 'default':
            defpoc = fpoc_lf(protein, pro_name, rank, outdir,logfilename)
        else:
            defpoc = pockets_file
        nshape = elim(defpoc, outdir, number)
        visual_lf(protein, outdir)
    elif method == 'LB':
        lig_array = dict_pdb_noh(ligand)
        if pockets_file == 'default':
            defpoc = fpoc_lb(protein, pro_name, lig_array, distance, outdir,logfilename)
        else:
            defpoc = pockets_file    
        nshape = elim(defpoc, outdir, number)
        visual_lf(protein, outdir)
        nextpoc = next_poc(nshape, ligand, outdir)
        clus_poc(clustering, nextpoc, threshold, outdir)
        visual_lb(protein, ligand, outdir)
    else:
        sys.exit()
