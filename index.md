# Welcome to  metaFun
## 

::::{grid}
:reverse:
:gutter: 2 1 1 1
:margin: 4 4 1 1

:::{grid-item}
:columns: 4

```{image} ./_static/ref_picture.jpg
:width: 150px
```
:::

:::{grid-item}
:columns: 8
:class: sd-fs-3

A Sphinx theme with a clean design, support for interactive content, and a modern book-like look and feel.
:::

::::

### metaFun : An analysis pipeline for **meta**genomic big data with fast and unified **Fun**ctional searches 

metaFun is implemented in Nextflow with apptainer. You can easily run this pipeline with easy installation using conda or mamba.  This package is deposited in Bioconda channel (https://anaconda.org/bioconda/metafun) 

## Introduction   
metaFun is aimed at agile and scalable generation of metagenome assembled genomes and taxonomic profiling with statistical analysis. Using user interested genomes with metadata, this pipeline enables fast comprative genomic analysis and functional annotation. 

```{figure} images/Picture1.png
---
width: 100%
figclass: margin-caption
alt: metafun_pipeline
name: myfig5
align: middle
---
Birdeye view of metaFun pipeline. This pipeline is comprised of six analytical modules and two interactive modules. 
```

## Quick Start 

1. **Install Prerequisites (conda, miniconda, or mamba)**
   ```bash
   # Install miniconda or mamba
   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
   bash Miniconda3-latest-Linux-x86_64.sh
   ```

2. **Install metaFun**
   ```bash
   # make  metafun environment
   git clone https://github.com/aababc1/metaFun.git
   cd metaFun
   
   # Create environment
   conda create -n metafun bioconda::metafun
   conda activate metafun
   ```

3. **Download Databases**
   ```bash
   (metafun)  metafun  -module DOWNLOAD_DB 
   # get help 
   (metafun)  metafun  -help
   ```

> 1. [<span style="color:#FF0000">RAWREAD_QC</span>](RAWREAD_QC)
> 1. [<span style="color:#FF9300">ASSEMBLY_BINNING</span>](ASSEMBLY_BINNING)
> 1. [<span style="color:#00B050">BIN_ASSESSMENT</span>](BIN_ASSESSMENT)
> 1. [<span style="color:#00B050">GENOME_</span><span style="color:#4E95D9">SELECTOR</span>](GENOME_SELECTOR)
> 1. [<span style="color:#4E95D9">COMPARATIVE_ANNOTATION</span>](COMPARATIVE_ANNOTATION)
> 1. [<span style="color:#4E95D9">INTERACTIVE_COMPARATIVE</span>](INTERACTIVE_COMPARATIVE)
> 1. [<span style="color:#0846FA">WMS_TAXONOMY</span>](WMS_TAXONOMY)
> 1. [<span style="color:#0846FA">INTERACTIVE_WMS_TAXONOMY</span>](INTERACTIVE_WMS_TAXONOMY)
> 1. [<span style="color:#7030A0">WMS_FUNCTION</span>](WMS_FUNCTION)

```{raw} html
<iframe src="https://dash-mag.onrender.com" width="100%" height="1200px"></iframe>
```


```{toctree}
:maxdepth: 2
:caption: Getting Started
:numbered:

Getstart/Getstart.md
Beginners/Beginners.md
Getstart/Input_preparation.md
```

```{toctree}
:maxdepth: 2
:caption: metaFun workflows

workflows/workflow_list.md
workflows/RAWREAD_QC.md
workflows/ASSEMBLY_BINNING.md
workflows/BIN_ASSESSMENT.md
workflows/GENOME_SELECTOR.md
workflows/COMPARATIVE_ANNOTATION.md
workflows/INTERACTIVE_COMPARATIVE.md
workflows/WMS_TAXONOMY.md
workflows/WMS_FUNCTION.md



```

```{toctree}
:maxdepth: 2
:caption: Guide for interactive visualization 

```
