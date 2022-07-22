# Pocket-to-Concavity(P2C)
![図1](https://user-images.githubusercontent.com/96423408/180365403-939d72f2-3268-4398-8ec7-b33bd0732c14.png)
P2C is a tool to accurately detect concavity that bind to the active compound in the pocket predicted by fpocket. 
There are two main modes, Ligand-Free(LF) mode and Ligand-Bound(LB) mode. 

* **Ligand-Free(LF) mode**  
  For the hit compound identification process, this mode can use to correct pockets more clearly.  
  
* **Ligand-Bound(LB) mode**  
  For lead optimization of known compounds, this mode can guide the direction of functional group expansion.  
  
You can use P2C if you have protein structure file(.pdb) or complex structure file(.pdb). 

## Requirements
* fpocket  
  You can install it according to fpocket github.(https://github.com/Discngine/fpocket)  
  We tested P2C on fpocket2.

* python  
  We tested P2C on python3.7.10  
  Several modules are needed.
  * numpy(1.21.2)
  * pandas(2.8.2)
  * sklearn(1.0.2)
  * pymol(2.5.2)

## Installation
Download this source code from github, and set PATH in this directory.  
~~~
git clone https://github.com/genki-kudo/Pocket-to-Concavity  
export P2C=/path/to/source/directory
~~~

## Preparation of input files
* **Ligand-Free(LF) mode**  
  In the LF mode of P2C, you need to prepare **protein 3D structure file (pdb format)**. If the PDB file contains substrates such as DNA, RNA, ligands, etc., I recommend removing them so that fpocket can work properly.
  
* **Ligand-Bound(LB) mode**  
  In the LB mode of P2C, you need to prepare **protein 3D structure file (pdb format)** as in LF mode. In addition to this, **ligand structure file (pdb format)** is required. the ligand file is used to obtain coordinate information during pocket selection and empty site identification stages, so please prepare the file that contain coordinates in the protein-bound state.

## Running

~~~
python ${P2C}/pocket_shapeup.py -h
~~~




