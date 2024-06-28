# Quick start 
## metaFun install and run
###  1. Install biocontainer 

If there is no conda or mamba in your system, follow the instructions and install conda or mamba. We reommend to install [miniconda](https://docs.anaconda.com/miniconda/miniconda-install/) or [mamba](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html). 

```{code-block} bash
:caption: Install miniconda
# Suppose you are using Linux OS.
# This install miniconda at your $HOME directory. 
#!/bin/bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
echo ${PWD}
```
```{admonition} Install mamba
We recommend to install mamba suitable for your OS following instruction from [miniforge github](https://github.com/conda-forge/miniforge). 
```
### 2. Setup program execution environment
Create a metaFun execution conda environment. All you should  do is running below code.  
Nextflow and Apptainer (former Singularity) will be utilized for entire pipeline execution with provided conda environment. 

:::{note}
If there is no git in your system, install git using conda  
```{code-block} bash
conda activate
conda install git 
```
:::
```{code-block} bash
:caption: Install and activate metaFun environment

# Clone the metaFun repository
git clone https://github.com/aababc1/metaFun.git

# Create metaFun environment 
# conda environemnt name is metafun 
conda env create -f metafun.yaml -n metafun
conda activate metafun

# Because of large size of databases (It will take around 683 GB.), it will take some time.
python download_db_metafun.py

```
:::{caution}
Due to the huge size of databases (After download and preparation : ~683GB),  it may take a while to download databasese depending on your network speed. 
:::

The integrity of downloaded databases is automatically checked by comparing  sha256 value provided in the [download repository](http://www.microbiome.re.kr/home_design/Database.html). It there are unzigged folders and hash file in the `databases/{CARD,checkm2,dbCAN,eggNOG5,gtdb,gunc,hashes.json,host_genome,humann3,KEGG_modules,kofam,kraken2_GTDBr220,VFDB}` the databases prepation is completed.  If there are problems, please redonwload the datases. 
You can launch metaFun from now on. 


