# Pocket-to-Concavity(P2C)
![図1](https://user-images.githubusercontent.com/96423408/180365403-939d72f2-3268-4398-8ec7-b33bd0732c14.png)

P2C is a tool to accurately detect concavity that bind to the active compound in the pocket predicted by fpocket. 
There are two main modes, Ligand-Free(LF) mode and Ligand-Bound(LB) mode. 

### **Ligand-Free(LF) mode**  
  For the hit compound identification process, this mode can use to correct pockets more clearly.  
  
### **Ligand-Bound(LB) mode**  
  For lead optimization of known compounds, this mode can guide the direction of functional group expansion.  
  
You can use P2C if you have protein structure file(.pdb) or complex structure file(.pdb). 

## Requirements
* **fpocket**  
  You can install it according to fpocket github.(https://github.com/Discngine/fpocket)  
  ~~~
  $ git clone https://github.com/Discngine/fpocket.git
  $ cd fpocket
  $ make
  $ sudo make install
  ~~~
  If you try to install fpocket in new linux distributions, you can have an error during ```make```. In that case, change ```$(LINKER) $(LFLAGS) $^ -o $@``` the makefile to ```$(LINKER) $^ -o $@ $(LFLAGS)```. More detail of the error is referred in https://sourceforge.net/p/fpocket/mailman/message/28785185/.  
  
  set PATH in this fpocket directory.  
  ~~~
  $ export PATH=$PATH:/path/to/fpocket/directory
  ~~~
  
  We tested P2C on fpocket2.

* **python**  
  We tested P2C on python3.7.10  
  Several modules are needed.
  * numpy(1.21.2)
  * pandas(2.8.2)
  * sklearn(1.0.2)
  * pymol(2.5.2)

## Installation
Download this source code from github, and set PATH in this directory.  
~~~
$ git clone https://github.com/genki-kudo/Pocket-to-Concavity  
$ export PATH=$PATH:/path/to/source/directory
~~~

## Preparation of input files
* **Ligand-Free(LF) mode**  
  In the LF mode of P2C, you need to prepare **protein 3D structure file (pdb format)**. If the PDB file contains substrates such as DNA, RNA, ligands, etc., I recommend removing them so that fpocket can work properly.
  
* **Ligand-Bound(LB) mode**  
  In the LB mode of P2C, you need to prepare **protein 3D structure file (pdb format)** as in LF mode. In addition to this, **ligand structure file (pdb format)** is required. the ligand file is used to obtain coordinate information during pocket selection and empty site identification stages, so please prepare the file that contain coordinates in the protein-bound state.

## Running
To view options of P2C:
~~~
$ p2c -h
usage: pocket shapeup [-h] -m METHOD -p PROTEIN [-l LIGAND] [-d DISTANCE]
                      [-r RANK]

optional arguments:
  -h, --help            show this help message and exit
  -m METHOD, --method METHOD
                        select mode (LF, LB)
  -p PROTEIN, --protein PROTEIN
                        specify protein file (format:PDB)
  -l LIGAND, --ligand LIGAND
                        specify ligand file (format:PDB). Only use this
                        argument when you select "LB" mode.
  -d DISTANCE, --distance DISTANCE
                        specify distance of include pocket. Only use this
                        argument when you select "LB".
  -r RANK, --rank RANK  specify druggability rank by fpocket of include
                        pocket. Only use this argument when you select "LF".
~~~

### **example of LF mode**
~~~
$ p2c -m LF -p protein.pdb -r 1
~~~

### **example of LB mode**
~~~
$ p2c -m LB -p protein.pdb -l ligand.pdb -d 3.0
~~~

## Output files
All output files are stored in ```./fpoc_output/``` or ```./p2c_output/```.  
```fpoc_output``` contains the results of fpocket calculation.  
```p2c_output``` contains the files in follows.  
* **default_pocket.pqr**: alpha-spheres before elimination process
* **newshape_pocket.pqr**: alpha-spheres after elimination process
* **visual_lf.pse**: pymol session file of LF mode results  

In LB mode, additional output files are stored in this directory.  
* **lig_lat.pdb**: lattice representation of the ligand
* **poc_lat.pdb**: lattice representation of the newshape_pocket
* **poc_surp.pdb**: lattice of "(poc_lat.pdb)-(lig_lat.pdb)"
* **poc_next.pqr**: alpha-spheres that not overlapped to the ligand
* **cluster/**: DBSCAN clustering results of "poc_next.pqr"
* **visual_lb.pse**: pymol session file of LB mode results 

## visualization
You can view the results of P2C if the process terminated successfully.  
~~~
$ pymol visual_lf.pse
~~~
or
~~~
$ pymol visual_lb.pse
~~~




