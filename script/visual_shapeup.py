from pymol import cmd
import glob
import os

def visual_lb(protein, ligand, outdir):
    cmd.load(ligand)
    cmd.load(protein)

    clsname = glob.glob('./'+outdir+'/cluster/*.pqr')
    for cls in clsname:
        cmd.load(cls)
        with open(cls,'r')as clfi:
            number = os.path.splitext(os.path.basename(cls))[0][7:]
            cmd.color(int(number)+2, os.path.splitext(os.path.basename(cls))[0]) 

    cmd.set("sphere_scale", "0.3")
    cmd.bg_color("white")
    #cmd.zoom("cluster")

    cmd.save("./"+outdir+"/visual_lb.pse")
    cmd.delete("all")

def visual_lf(protein, outdir):
    cmd.load('./'+outdir+'/newshape_pocket.pqr')
    cmd.color("red", "newshape_pocket")
    cmd.show("mesh", "newshape_pocket")
    cmd.load('./'+outdir+'/default_pocket.pqr')
    cmd.color("gray70", "default_pocket")
    cmd.show("mesh", "default_pocket")
    cmd.load(protein)
    cmd.set("sphere_scale", "0.3")
    cmd.bg_color("white")
    cmd.zoom("default_pocket")
    
    cmd.save("./"+outdir+"/visual_lf.pse")
    cmd.delete("all")
