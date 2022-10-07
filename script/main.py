import sys
import os
import argparse
import time
from subprocess import run
from script.fpocket import fpoc_lf,fpoc_lb
from script.a_elimination import elim
from script.next_pocket import next_poc, clus_poc
from script.visual_shapeup import visual_lb, visual_lf
from script.basic_func import dict_pdb_noh, clean_dir,input_process

bash=lambda x:run(x,shell=True)

def main_exec():
    
    input_list=input_process()
    
    method,protein,ligand,distance,rank,pro_name,clustering,threshold,logfilename,s = input_list

    outdir = os.path.dirname(os.path.abspath(protein))+"/p2c_output"    

    clean_dir(outdir+"/")
    clean_dir(pro_name+'_out/')
    clean_dir('fpoc_output/')

    bash("mkdir "+outdir)
    tmp=open(outdir+"/"+logfilename,"w").write(s)


    if method == 'LF':
        defpoc = fpoc_lf(protein, pro_name, rank, outdir,logfilename)
        nshape = elim(defpoc, outdir)
        visual_lf(protein, outdir)
    elif method == 'LB':
        lig_array = dict_pdb_noh(ligand)
        defpoc = fpoc_lb(protein, pro_name, lig_array, distance, outdir, logfilename)      
        nshape = elim(defpoc, outdir)
        visual_lf(protein, outdir)
        nextpoc = next_poc(nshape, ligand, outdir)
        clus_poc(clustering, nextpoc, threshold, outdir)
        visual_lb(protein, ligand, outdir)
    else:
        sys.exit()
