# Quick start 
## metaFun install and run
###  Install biocontainer 

1. If there is no conda or mamba in your system, follow the instructions and install conda or mamba. We reommend to install [miniconda](https://docs.anaconda.com/miniconda/miniconda-install/) or [mamba](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html). 

```{code-block} bash
:caption: Install miniconda

# Suppose you are using Linux OS.
# This install miniconda at your $HOME directory. 
#!/bin/bash
$ mkdir -p ~/miniconda3
$ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
$ bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
$ rm -rf ~/miniconda3/miniconda.sh
$ echo ${PWD}
```
```{admonition} Install mamba
We recommend to install mamba suitable for your OS following instruction from [miniforge github](https://github.com/conda-forge/miniforge). 
```
### Setup program execution environment
2. Create a metaFun execution conda environment. Nextflow and Apptainer (former Singularity) will be utilized for this pipeline

conda env create -f metafun.yml -n
conda activate metafun

### Clone the code repository and download databases 
3. All envronemnts are enclosed into apptainer imgage to prohibit version incompatability. Detailed  programs and versions are denoted into # inlink reference. 

```{code-block} bash
:caption: Install and activate metaFun environment
# If you installed mamba, use mamba instead of conda
conda create -n metafun -c conda-forge -c bioconda apptainer nextflow git requests python
conda activate metafun
git clone https://github.com/aababc1/metaFun.git
sh download_db_setup.sh
```
Because of the huge size of databases,  it may take a while to download databasese. 

The integrity of databases is checked by md5sum value. If there are problems, please redonwload the datases. 
You can launch metaFun from now on. 


