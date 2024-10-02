# **Pocket to Concavity (P2C)**
![図1](https://user-images.githubusercontent.com/96423408/180365403-939d72f2-3268-4398-8ec7-b33bd0732c14.png)

**P2C is a tool for refining the of Protein-Ligand binding site shape from alpha-spheres.**  
There are two main modes, **Ligand-Free(LF) mode** and **Ligand-Bound(LB) mode**.

* ### LF mode
  LF mode provides the shape of the deep and druggable concavity where the core scaffold can bind.
* ### LB mode
  LB mode searches the deep concavity around the bound ligand.

# INSTALLATION
**P2C can be used in Linux OS.** (tested on Ubuntu20.04LTS).

## Requirements

* **Python**  
  P2C was tested on python3.7.10.  
  Several modules are needed in addition to the default modules:
  * numpy(1.21.5)
  * pandas(1.3.5)
  * scikit-learn(1.0.2)
  * scipy(1.7.0)
  * pymol(open-source)

  This environment is built by the following commands if using anaconda (download and install Anaconda here: https://www.anaconda.com/download/) in OS.
  ```
  conda create -n p2c_env python==3.7.10
  conda activate p2c_env
  
  conda install numpy==1.21.5
  conda install pandas==1.3.5
  conda install scikit-learn==1.0.2
  conda install scipy==1.7.3
  conda install -c conda-forge pymol-open-source
  ```

* **Fpocket4**  
  Refer to https://github.com/Discngine/fpocket
  After fpocket installation, check to be available fpocket using CUI(run ```fpocket```).
  
  (P2C <= v1.0.3 used fpocket2 as alpha-spheres generator, however; >=v1.1.0 recommends fpocket4.)

* **P2C**  
  Download this source code, and set PATH in this directory.  
  ```
  git clone https://github.com/genki-kudo/Pocket-to-Concavity  
  cd Pocket-to-Concavity/
  echo "export PATH=\$PATH:`pwd`" >> ~/.bashrc
  source ~/.bashrc
  ```

# Preparation of input files
### **LF mode**  
  In the LF mode of P2C, a **protein 3D structure file (PDB format)** must be prepared. If the PDB file contains substrates, such as DNA, RNA, and ligands, it is recommended that they be removed so fpocket can function properly.
  
### **Ligand-Bound(LB) mode**  
  In the LB mode of P2C, a **protein 3D structure file (PDB format)** must be prepared, as in the LF mode. In addition, a **ligand 3D structure file (PDB format)** is required. The ligand file obtains coordinate information during the pocket selection and empty sites identification stages. Therefore, the file that contains coordinates in the protein-bound state must be prepared.

# Running
To view options of P2C:
~~~
$ p2c -h

optional arguments:
  -h, --help            show this help message and exit
  -m METHOD, --method METHOD
                        select mode (LF, LB)
  -p PROTEIN, --protein PROTEIN
                        specify protein file (format:PDB)
  -l LIGAND, --ligand LIGAND
                        specify ligand file (format:PDB). Use this argument
                        only when you select "LB" mode.
  -a ALPHASPHERE, --alphasphere ALPHASPHERE
                        specify alpha-spheres coordinetes file (format:PQR).
                        Use this argument if you does not require alpha-
                        spheres generation in P2C.
  -n NUMBER, --number NUMBER
                        specify the parameter in the alpha-spheres elimination
                        process
  -d DISTANCE, --distance DISTANCE
                        specify the distance of included pocket. Use this
                        argument only when you select "LB" mode.
  -r RANK, --rank RANK  specify the druggability rank of included pocket
                        predicted. Use this argument only when you select "LF"
                        mode.
  -c CLUSTERING, --clustering CLUSTERING
                        default clustering is single-linkage
                        clustering(threshold 4.5A). You can select clustering
                        methods; single-linkage, DBSCAN. (Other clustering
                        methods will be available.) Use this argument only
                        when you select "LB" mode.
  -t THRESHOLD, --threshold THRESHOLD
                        specify threshold of clustering. (order is 1^-10m)
                        default threshold of single-linkage is 4.5A and that
                        of DBSCAN is 2.0A.
  -o LOGFILENAME, --logfilename LOGFILENAME
                        specify logfile name (default:p2c.log)
~~~

### **(A) default LF mode**
The default LF mode can be used if the binding site and the deep concavity where the core scaffold can bind are accurately predicted.  
The command to run this case is as follows:
~~~
$ p2c -m LF -p protein.pdb -r 1
~~~
The optional argument “-r 1” specifies the number of pockets (sorted druggability score) that executes the P2C processes. 

### **(B) LF mode without alpha-spheres generation**
The LF mode can be performed to refine alpha-spheres from other software (e.g., output by SiteFiner).  
The command to run the LF mode, in this case, is as follows:
~~~
$ p2c -m LF -p protein.pdb -a pockets.pqr -n 4
~~~
“pockets.pqr” is the alpha-spheres coordinate file from other settings or alpha sphere-based software.  
Note that the re-optimized parameter should be used if the default settings are not used for the pocket file. The re-optimized parameter can be specified in the optional argument “-n”.

### **(C) default LB mode**
The deep concavity around the active ligand can be searched with the LB mode in P2C.  
The command to run the LB mode with alpha-spheres generation is as follows:
~~~
$ p2c -m LB -p protein.pdb -l ligand.pdb -d 10
~~~
The range of search is specified by “-d”. “-d 10” means the LB mode searches unoccupied pockets within 10 Å from the ligand.

### **(D) LB mode without alpha-spheres generation**
The LB mode can be performed to refine for the refinement of alpha-spheres from other software, the same as the LF mode.  
The command to run the LB mode, in this case, is as follows:
~~~
$ p2c -m LB -p protein.pdb -l ligand.pdb -a pockets.pqr -n 4
~~~
“-a” is the same as the LF mode without alpha-spheres generation.  
Note that the re-optimized parameter should be used if the default settings are not used for the pocket file. 

# Output files
All output files are stored in ```asphere_output/``` and ```p2c_output/```.  
```asphere_output``` contains the results of the alpha-spheres generation (The default generator is Fpocket).  
```p2c_output``` contains the following files: 
* **default_pocket.pqr**: alpha-spheres of a selected pocket in the pocket selection (before the elimination process).
* **newshape_pocket.pqr**: alpha-spheres after the elimination process.
* **visual_lf.pse**: the PYMOL session file of the LF mode results.
* **p2c.log**: the log file

In the LB mode, additional output files are stored in this directory.  
* **lig_lat.pdb**: the lattice representation of the ligand.
* **poc_lat.pdb**: the lattice representation of the newshape_pocket.
* **poc_surp.pdb**: the lattice of "(poc_lat.pdb)-(lig_lat.pdb)".
* **poc_next.pqr**: alpha-spheres that did not overlap with the ligand.
* **cluster/**: the clustering results of "poc_next.pqr".
* **visual_lb.pse**: the pymol session file of the LB mode results .

# Visualization
The results of P2C can be viewed if the process was successful by the following code:  
~~~
$ pymol ./p2c_output/visual_lf.pse
~~~
or
~~~
$ pymol ./p2c_output/visual_lb.pse
~~~



# Others
The default alpha-spheres generator is fpocket because this tool is a free license software. However, P2C applies to other tools that utilize alpha-sphere algorithms (e.g., SiteFinder). The use case in The Supplementary Information describes the application results of Sitefinder's alpha-spheres. Note that the parameters in P2C are needed to tune the application in other tools. 
