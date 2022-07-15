import sys
import os
import shutil
import argparse
import subprocess
from script.fpocket import fpoc_lf,fpoc_lb
from script.a_elimination import elim
from script.next_pocket import clst_poc
from script.visual_shapeup import visual_lb, visual_lf
from script.basic_func import dict_pdb_noh, clean_dir

def main_exec(outdir):
    parser = argparse.ArgumentParser(prog='pocket shapeup')
    parser.add_argument('-m', '--method', nargs=1, required=True, help='select mode (LF, LB)')
    parser.add_argument('-p', '--protein', nargs=1, required=True, help='specify protein file (format:PDB)')
    parser.add_argument('-l', '--ligand', nargs=1, default="None", help='specify ligand file (format:PDB). Only use this argument when you select "LB" mode.')
    parser.add_argument('-d', '--distance', nargs=1, type=float, default=[1.8], help='specify distance of include pocket. Only use this argument when you select "LB".')
    parser.add_argument('-r', '--rank', nargs=1, type=int, default=[1], help='specify druggability rank by fpocket of include pocket. Only use this argument when you select "LF".')

    args = parser.parse_args()
    method = str(args.method[0])
    protein = str(args.protein[0])
    ligand = str(args.ligand[0])
    distance = str(args.distance[0])
    rank = str(args.rank[0])
    pro_name = os.path.splitext(protein)[0]

    clean_dir(outdir)
    clean_dir(pro_name+'_out/')
    clean_dir('fpoc_output/')

    if method == 'LF':
        subprocess.call(["mkdir", outdir])
        defpoc = fpoc_lf(protein, pro_name, rank, outdir)
        nshape = elim(defpoc, outdir)
        visual_lf(protein, outdir)
    elif method == 'LB':
        subprocess.call(["mkdir", outdir])
        lig_array = dict_pdb_noh(ligand)
        defpoc = fpoc_lb(protein, pro_name, lig_array, distance, outdir)      
        nshape = elim(defpoc, outdir)
        visual_lf(protein, outdir)
        clst_poc(nshape, ligand, outdir)
        visual_lb(protein, ligand, outdir)
    else:
        sys.exit()
