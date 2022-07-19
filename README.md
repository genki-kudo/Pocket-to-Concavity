# Pocket-to-Concavity(P2C)
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
Download this source code from github, and set PATH in This directory.
``` git clone https://github.com/genki-kudo/Pocket-to-Concavity ```  




