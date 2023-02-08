# **Pocket to Concavity (P2C)**
![図1](https://user-images.githubusercontent.com/96423408/180365403-939d72f2-3268-4398-8ec7-b33bd0732c14.png)

**P2C is a tool for the refinement of Protein-Ligand binding site shape from alpha-spheres.**  
There are two main modes, **Ligand-Free(LF) mode** and **Ligand-Bound(LB) mode**.

* ### Ligand-Free (LF) mode
  LF mode provides the shape of the deep and druggable concavity where the core scaffold can bind.
* ### Ligand-Bound (LB) mode
  LB mode searches deep concavity around the bound ligand.

# INSTALLATION
**You can use P2C in Linux OS.** (We tested on the Ubuntu20.04LTS.)

## Requirements

* **Python**  
  We tested P2C on python3.7.10.  
  Several modules are needed in addition to default modules.
  * numpy(1.21.5)
  * pandas(1.3.5)
  * scikit-learn(1.0.2)
  * scipy(1.7.0)
  * pymol(open-source)

  This exvironment is built as following commands if you have anaconda in the OS.  
  (you can download and install Anaconda in the URL-> https://www.anaconda.com/download/ )
  ```
  conda create -n p2c_env python==3.7.10
  conda activate p2c_env
  
  conda numpy==1.21.5
  conda pandas==1.3.5
  conda scikit-learn==1.0.2
  conda scipy==1.7.3
  conda install -c conda-forge pymol-open-source
  ```

* **Fpocket2**  
  You can get fpocket2.tar.gz in the following URL.
  https://sourceforge.net/projects/fpocket/files/latest/download.  
  And then, you unzip this file and make install. Set PATH in this fpocket directory.
  ```
  tar -xvf fpocket2.tar.gz
  cd fpocket2/
  make
  make install
  
  #set PATH in this fpocket directory.
  echo "export PATH=\$PATH:`pwd`/bin" >> ~/.bashrc
  source ~/.bashrc
  ```
  If you try to install fpocket in new linux distributions, you can have an error during ```make```.  
  In that case, change ```$(LINKER) $(LFLAGS) $^ -o $@``` the makefile to ```$(LINKER) $^ -o $@ $(LFLAGS)```.  
  More detail of the error is referred in https://sourceforge.net/p/fpocket/mailman/message/28785185/. 

* **P2C**  
  Download this source code, and set PATH in this directory.  
  ```
  git clone https://github.com/genki-kudo/Pocket-to-Concavity  
  cd Pocket-to-Concavity/
  echo "export PATH=\$PATH:`pwd`/bin" >> ~/.bashrc
  source ~/.bashrc
  ```

# Preparation of input files
## **Ligand-Free(LF) mode**  
  In the LF mode of P2C, **protein 3D structure file (PDB format)** need to be prepared. If the PDB file contains substrates such as DNA, RNA, ligands, etc., I recommend removing them so that fpocket can work properly.
  
## **Ligand-Bound(LB) mode**  
  In the LB mode of P2C, **protein 3D structure file (PDB format)** needs to be prepared, as in LF mode. In addition, a **ligand 3D structure file (PDB format)** is required. the ligand file is used to obtain coordinate information during pocket selection and empty sites identification stages; therefore, prepare the file that contains coordinates in the protein-bound state.

## Running
To view options of P2C:
~~~
$ p2c -h
usage: p2c [-h] -m METHOD -p PROTEIN [-l LIGAND] [-d DISTANCE] [-r RANK]
           [-c CLUSTERING] [-t THRESHOLD] [-o LOGFILENAME]

optional arguments:
  -h, --help            show this help message and exit
  -m METHOD, --method METHOD
                        select mode (LF, LB)
  -p PROTEIN, --protein PROTEIN
                        specify protein file (format:PDB)
  -l LIGAND, --ligand LIGAND
                        specify ligand file (format:PDB). Use this argument
                        only when you select "LB" mode.
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

### **example of LF mode**
~~~
$ p2c -m LF -p protein.pdb -r 1
~~~

### **example of LB mode**
~~~
$ p2c -m LB -p protein.pdb -l ligand.pdb -d 5.0
~~~

## Output files
All output files are stored in ```fpoc_output/``` and ```p2c_output/```.  
```fpoc_output``` contains the results of fpocket calculation.  
```p2c_output``` contains the files as follows.  
* **default_pocket.pqr**: alpha-spheres of selected pocket in pocket selection (before elimination process)
* **newshape_pocket.pqr**: alpha-spheres after elimination process
* **visual_lf.pse**: PYMOL session file of LF mode results
* **p2c.log**: log file

In LB mode, additional output files are stored in this directory.  
* **lig_lat.pdb**: lattice representation of the ligand
* **poc_lat.pdb**: lattice representation of the newshape_pocket
* **poc_surp.pdb**: lattice of "(poc_lat.pdb)-(lig_lat.pdb)"
* **poc_next.pqr**: alpha-spheres that did not overlap with the ligand
* **cluster/**: clustering results of "poc_next.pqr"
* **visual_lb.pse**: pymol session file of LB mode results 

## visualization
You can view the results of P2C if the process terminated successfully.  
~~~
$ pymol ./p2c_output/visual_lf.pse
~~~
or
~~~
$ pymol ./p2c_output/visual_lb.pse
~~~



## others
In the present P2C(2022/12), fpocket is used as the generation tool of alpha-spheres because this tool is free licence software. In ideal, P2C is applicable to other tools that utilize alpha-spheres algorithms (ex. SiteFinder). Actually, our usecase in supplementary materials describes the application results of Sitefinder's alpha-spheres. Note that the parameters in P2C is needed to tune for application to other tools. 
We will update P2C and the options.



