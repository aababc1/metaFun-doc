# Quick start 
## metaFun install and run
###  1. Install biocontainer 

If there is no conda or mamba in your system, follow the instructions and install conda or mamba. We reommend to install [miniconda](https://docs.anaconda.com/miniconda/miniconda-install/) or [mamba](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html). 

```{code-block} bash
:caption: Install miniconda
# Suppose you are using Linux OS.
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
# you can indicate the installation path by replacing -p $PATH. $PATH is the base directory of your conda installation.
bash miniconda.sh -b -u -p ~/miniconda3
rm  miniconda.sh
```
```{admonition} Install mamba
We recommend to install mamba suitable for quick installation following instruction from [miniforge github](https://github.com/conda-forge/miniforge). 
```
### 2. Download metaFun from Bioconda
```{code-block} bash
# we recommend create a new conda environment for metaFun
conda create -n metafun bioconda::metafun
# If you have mamba, you can install metaFun with mamba
mamba create -n metafun bioconda::metafun

mamba activate metafun
```

### 3. Download databases to utilize metaFun
```{code-block} bash
# download databases
conda activate metafun
 (metafun) name $ metafun  -module DOWNLOAD_DB 
```

````{admonition} module DOWNLOAD_DB execution
:class: note
Execution of `metafun -module DOWNLOAD_DB` is shown in the following figure. 
```{figure} ../images/DownloadDB_execution_metafun_v011.png
---
width: 100%
figclass: margin-caption
alt: metafun_pipeline
name: download_db_metafun
align: middle
---
```
````

````{admonition} module DOWNLOAD_DB execution
:class: note
Due to the huge size of databases (File size of raw tar gzipped files : ~683GB),  it may take a while to download databasese depending on your network speed.
Database information is available at [download repository](https://www.microbiome.re.kr/home_design/list_files.php?path=metafun%2Fv0.1%2FmetaFun_db_distribute). 

The integrity of downloaded databases is automatically checked by comparing  sha256.  If there are problems, please redonwload the datases. 

Typically you can find the database path by the following command.
```{code-block} bash
ls -d $(find $(dirname $(which metafun)) -type d ! -name 'metafun')/../share/metafun/db
```
````

### 4. Run Modules of metaFun  

metaFun provides two main analysis workflows:

#### Genome-based analysis path:
<span style="color:#FF0000">RAWREAD_QC</span> → <span style="color:#FF9300">ASSEMBLY_BINNING</span> → <span style="color:#00B050">BIN_ASSESSMENT</span> → <span style="color:#00B050">GENOME_</span><span style="color:#4E95D9">SELECTOR</span> → <span style="color:#4E95D9">COMPARATIVE_ANNOTATION</span> → <span style="color:#4E95D9">INTERACTIVE_COMPARATIVE</span>

#### Read-based analysis path:
  For taxonomic composition

<span style="color:#FF0000">RAWREAD_QC</span> → <span style="color:#0846FA">WMS_TAXONOMY</span> → <span style="color:#0846FA">INTERACTIVE_TAXONOMY</span>

For functional annotation

<span style="color:#FF0000">RAWREAD_QC</span> → <span style="color:#7030A0">WMS_FUNCTION</span>

For strain-level analysis

<span style="color:#FF0000">RAWREAD_QC</span> → <span style="color:#0846FA">WMS_TAXONOMY</span> → <span style="color:#2FA4E7">WMS_STRAIN</span> → <span style="color:#2FA4E7">INTERACTIVE_STRAIN</span>

For network analysis

<span style="color:#0846FA">WMS_TAXONOMY</span> → <span style="color:#2FA4E7">INTERACTIVE_NETWORK</span>

You can execute each module of metaFun using the following syntax:


```{code-block} bash
metafun -module <module_name> [options]
```

#### Available Modules

```{admonition} Important Workflow Information
:class: warning

- When specifying an input directory for <span style="color:#FF0000">RAWREAD_QC</span>, subsequent modules  will automatically use the output from previous steps as their input unless explicitly overridden.
- Mandatory parameters are typically needed when specifying metadata files and their columns (sample ID or analysis columns). Each module that requires metadata will need these parameters explicitly defined.
- For the most efficient usage, follow the color-coded workflow paths shown above.
```

## <span style="color:#FF0000">RAWREAD_QC</span>: Quality control of raw reads and host genome filtering

**Required:** -i <inputDir> (input reads directory)

```{code-block} bash
:caption: Example
metafun -module RAWREAD_QC -i input_reads/
```

## <span style="color:#FF9300">ASSEMBLY_BINNING</span>: Assembly and binning
**Optional:** -i <inputDir> (filtered reads directory)
(If you run RAWREAD_QC without output parameter, you can run it this module without `-i` parameter in this module.)

```{code-block} bash
:caption: Example
metafun -module ASSEMBLY_BINNING -i filtered_reads/ -p 40
```

## <span style="color:#00B050">BIN_ASSESSMENT</span>: Assess genome quality and taxonomy classification

**Required:** -m <metadata> -c <accession_column>

```{code-block} bash
:caption: Example
metafun -module BIN_ASSESSMENT -m metadata.txt -c 2
```

## <span style="color:#00B050">GENOME_</span><span style="color:#4E95D9">SELECTOR</span>: Genome selection interface

**Required:** -i <input_file>

```{code-block} bash
:caption: Example
metafun -module GENOME_SELECTOR -i combined_metadata.csv
```

## <span style="color:#4E95D9">COMPARATIVE_ANNOTATION</span>: Comparative genomic analysis

**Required:** -i <inputDir> -m <metadata>

```{code-block} bash
:caption: Example (annotation only for INTERACTIVE_COMPARATIVE module)
metafun -module COMPARATIVE_ANNOTATION  --metadata metadata.csv --samplecol 1
```


```{code-block} bash
:caption: Example (with static plots) This is deprecated.
metafun -module COMPARATIVE_ANNOTATION -i genomes/ -m metadata.csv --samplecol 1 --metacol 2
```

## <span style="color:#4E95D9">INTERACTIVE_COMPARATIVE</span>: Interactive comparative analysis

**Required:** -i <inputDir> -m <metadata>

```{code-block} bash
:caption: Example
metafun -module INTERACTIVE_COMPARATIVE -i results/genomes -m metadata.csv
```

## <span style="color:#0846FA">WMS_TAXONOMY</span>: Taxonomic profiling of metagenomic reads

**Required:** -m <metadata> -s <sampleIDcolumn> 
```{admonition} Default selection is sylph.
:class: note

If you would like to utilize kraken2, please download kraken2 database and specify `--profiler kraken2`. 

`-s` option is accession column prefix of paired reads files of metagenomic data.

`-i` option is input directory of metagenomic data. You need to specify this option if you did not run <span style="color:#FF0000">RAWREAD_QC</span> module.
```

```{code-block} bash
:caption: Example
metafun -module WMS_TAXONOMY  -m meta.csv -s 1 
```

## <span style="color:#0846FA">INTERACTIVE_TAXONOMY</span>: Interactive taxonomy analysis

**Required:** -i <inputDir>

```{code-block} bash
:caption: Example
metafun -module INTERACTIVE_TAXONOMY -i results/metagenome/WMS_TAXONOMY
```

## <span style="color:#7030A0">WMS_FUNCTION</span>: Functional analysis of metagenomic reads

**Required:** -i <inputDir> -m <metadata> -s <sampleIDcolumn> -a <analysiscolumn>

```{code-block} bash
:caption: Example
metafun -module WMS_FUNCTION -i filtered_reads/ -m metadata.csv -s 1 -a 2
```

## <span style="color:#2FA4E7">WMS_STRAIN</span>: Strain-level microdiversity analysis

**Required:** -i <inputDir> --phyloseq_object <phyloseq_RDS>

```{admonition} Requires WMS_TAXONOMY output
:class: note

This module requires a phyloseq RDS object from WMS_TAXONOMY for selecting prevalent taxa to analyze at strain level.
```

```{code-block} bash
:caption: Example
metafun -module WMS_STRAIN -i results/metagenome/RAWREAD_QC/read_filtered \
    --phyloseq_object results/metagenome/WMS_TAXONOMY/phyloseq/phyloseq_object_sylph.RDS
```

## <span style="color:#2FA4E7">INTERACTIVE_STRAIN</span>: Interactive strain diversity analysis

**Required:** -i <inputDir>

```{code-block} bash
:caption: Example
metafun -module INTERACTIVE_STRAIN -i results/metagenome/WMS_STRAIN
```

## <span style="color:#2FA4E7">INTERACTIVE_NETWORK</span>: Interactive microbial network analysis

**Required:** -i <phyloseq_RDS>

```{admonition} Requires WMS_TAXONOMY output
:class: note

This module requires a phyloseq RDS object from WMS_TAXONOMY for constructing co-occurrence networks.
```

```{code-block} bash
:caption: Example
metafun -module INTERACTIVE_NETWORK -i results/metagenome/WMS_TAXONOMY/phyloseq/phyloseq_object_sylph.RDS
```

## DOWNLOAD_DB: Download required databases

```{code-block} bash
:caption: Example
metafun -module DOWNLOAD_DB
```

## PREPARE_CUSTOM_HOST: Prepare custom host genome index

**Required:** -i <file> -f <name>

```{code-block} bash
:caption: Example
metafun -module PREPARE_CUSTOM_HOST -i genome.fasta -f mouse
```
```{admonition} Any custom host genome can be used.
:class: note

If you would like to use custom host genome, please specify the path of fasta file and name of the host genome by `-f`.

You need to specify `-f` option in <span style="color:#FF0000">RAWREAD_QC</span> module to filter out your custom host  genome.
```


## Common Options

- `-o, --output`: Output directory
- `-p, --processors`: Number of processors to use
- `-h, --help`: Show detailed help for a module

For detailed usage and additional parameters for each module, use:
```{code-block} bash
metafun -module <module_name> -h
``` 

