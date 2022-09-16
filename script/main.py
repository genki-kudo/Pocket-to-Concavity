import sys
import os
import argparse
from subprocess import run
from script.fpocket import fpoc_lf,fpoc_lb
from script.a_elimination import elim
from script.next_pocket import next_poc, clus_poc
from script.visual_shapeup import visual_lb, visual_lf
from script.basic_func import dict_pdb_noh, clean_dir,input_process

bash=lambda x:run(x,shell=True)

def main_exec(outdir):
    
    input_list=input_process()
    
    method,protein,ligand,distance,rank,pro_name,clustering = input_list

    clean_dir(outdir)
    clean_dir(pro_name+'_out/')
    clean_dir('fpoc_output/')

    if method == 'LF':
        print("\n#### Ligand Free mode selected####\n")
        bash("mkdir "+outdir)
        print(">> fpocket calculation started")
        defpoc = fpoc_lf(protein, pro_name, rank, outdir)
        print("\n>> alpha-spheres elimination started")
        nshape = elim(defpoc, outdir)
        visual_lf(protein, outdir)
    elif method == 'LB':
        print("\n#### Ligand Bound mode selected ####\n")
        bash("mkdir "+outdir)
        lig_array = dict_pdb_noh(ligand)
        print(">> fpocket calculation started")
        defpoc = fpoc_lb(protein, pro_name, lig_array, distance, outdir)      
        print("\n>> alpha-spheres elimination started")
        nshape = elim(defpoc, outdir)
        visual_lf(protein, outdir)
        nextpoc = next_poc(nshape, ligand, outdir)
        print("\n>> empty site identification started")
        clus_poc(clustering, nextpoc, outdir)
        visual_lb(protein, ligand, outdir)
    else:
        sys.exit()
