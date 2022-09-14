import sys
import os
import argparse
import subprocess
from script.fpocket import fpoc_lf,fpoc_lb
from script.a_elimination import elim
from script.next_pocket import next_poc, clus_poc
from script.visual_shapeup import visual_lb, visual_lf
from script.basic_func import dict_pdb_noh, clean_dir

def main_exec(outdir):
    parser = argparse.ArgumentParser(prog='pocket shapeup')
    parser.add_argument('-m', '--method', nargs=1, required=True, help='select mode of P2C (LF, LB)')
    parser.add_argument('-p', '--protein', nargs=1, required=True, help='specify protein file (format:PDB)')
    parser.add_argument('-l', '--ligand', nargs=1, default="None", help='specify ligand file (format:PDB). Only use this argument when you select "LB" mode.')
    parser.add_argument('-d', '--distance', nargs=1, type=float, default=[1.8], help='specify distance of include pocket. Only use this argument when you select "LB".')
    parser.add_argument('-r', '--rank', nargs=1, type=int, default=[1], help='specify druggability rank by fpocket of include pocket. Only use this argument when you select "LF".')
    parser.add_argument('-c', '--clustering', nargs=1, default="None", help='select "DBSCAN" if you do not use fpocket-clustering-method in empty site identification. Only use this argument when you select "LB".')

    args = parser.parse_args()
    method = str(args.method[0])
    protein = str(args.protein[0])
    ligand = str(args.ligand[0])
    distance = str(args.distance[0])
    rank = str(args.rank[0])
    pro_name = os.path.splitext(protein)[0]
    clustering = str(args.clustering[0])

    clean_dir(outdir)
    clean_dir(pro_name+'_out/')
    clean_dir('fpoc_output/')

    if method == 'LF':
        print("")
        print("#### Ligand Free mode selected####")
        print("")
        subprocess.call(["mkdir", outdir])
        print(">> fpocket calculation started")
        defpoc = fpoc_lf(protein, pro_name, rank, outdir)
        print("")
        print(">> alpha-spheres elimination started")
        nshape = elim(defpoc, outdir)
        visual_lf(protein, outdir)
    elif method == 'LB':
        print("")
        print("#### Ligand Bound mode selected ####")
        print("")
        subprocess.call(["mkdir", outdir])
        lig_array = dict_pdb_noh(ligand)
        print(">> fpocket calculation started")
        defpoc = fpoc_lb(protein, pro_name, lig_array, distance, outdir)      
        print("")
        print(">> alpha-spheres elimination started")
        nshape = elim(defpoc, outdir)
        visual_lf(protein, outdir)
        nextpoc = next_poc(nshape, ligand, outdir)
        print("")
        print(">> empty site identification started")
        clus_poc(clustering, nextpoc, outdir)
        visual_lb(protein, ligand, outdir)
    else:
        sys.exit()
