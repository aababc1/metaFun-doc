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
> 1. [<span style="color:#0846FA">INTERACTIVE_TAXONOMY</span>](INTERACTIVE_WMS_TAXONOMY)
> 1. [<span style="color:#7030A0">WMS_FUNCTION</span>](WMS_FUNCTION)

```{raw} html
<iframe src="https://dash-mag.onrender.com" width="100%" height="1200px"></iframe>
```

## FAQ & Troubleshooting

### Storage Management

- **Reducing Disk Usage**: After verifying your results, you can safely delete the Nextflow `work/` directory to free up significant disk space:
  ```bash
  # Remove work directory after successful run
  rm -rf work/
  ```
  
- **Temporary Files**: Several modules create large temporary files during processing that can be deleted after successful runs:
  - HUMAnN3 (`*_humann_temp` directories in WMS_FUNCTION results)
  - Assembly files (ASSEMBLY_BINNING intermediates)
  - MetaPhlAn bowtie2 indices (in WMS_TAXONOMY)

- **Selective Results Retention**: For large metagenomic studies, consider keeping only essential outputs:
  - Save final tables and visualization files
  - Compress large text outputs with `gzip`
  - Archive raw binning results after successful bin refinement

### Common Issues

- **Metadata Formatting**: The most common errors come from metadata file issues:
  - Ensure your sample IDs in the metadata CSV file exactly match the prefixes of your read filenames
  - Verify that the column numbers specified in parameters (`-s/-c`, `-a`) are correct
  - Check that your CSV file uses comma (,) separators and not tabs or semicolons
  - For interactive modules, ensure consistent metadata across analysis stages
  
- **Database Installation**: If you encounter database-related errors, you may need to reinstall the required databases:
  ```bash
  # Reinstall specific databases
  (metafun) metafun -module DOWNLOAD_DB -d humann3     # For WMS_FUNCTION
  (metafun) metafun -module DOWNLOAD_DB -d kraken2     # For WMS_TAXONOMY

  
  # For complete reinstallation of all databases
  (metafun) metafun -module DOWNLOAD_DB
  ```

- **Memory Requirements**: Several modules require significant memory:
  - **ASSEMBLY_BINNING**: Lower `-m` parameter for metaSPAdes if OOM errors occur
  - **WMS_FUNCTION**: Adjust threads with `-p` parameter for HUMAnN3
  - For low-memory environments, process samples in smaller batches

### Module-Specific Troubleshooting

- **RAWREAD_QC**:
  - If human read filtering fails, check that the human genome database is properly installed
  - For samples with unusual quality distributions, adjust fastp parameters directly
  
- **ASSEMBLY_BINNING**:
  - Low-coverage samples may produce fragmented assemblies; consider co-assembly of related samples
  - If binning produces too few bins, try adjusting the minimum contig length parameters
  
- **WMS_TAXONOMY**:
  - If Kraken2 results show high "unclassified" percentages, try updating to the latest database
  - When switching between profilers (sylph/kraken2), remember to use the correct phyloseq object

- **WMS_FUNCTION**:
  - For pathway analysis issues, check that both ChocoPhlAn and UniRef90 databases are installed
  - Stratified outputs may be large; use unstratified tables for overview analyses
  
- **Interactive Modules**:
  - If web interfaces fail to load, check for port conflicts and use the `-p` parameter
  - For visualization export issues, verify that required R packages are properly installed

### Performance Optimization

- **Parallelize Efficiently**:
  - Adjust CPU allocation based on available resources and module needs:
    ```bash
    # Example optimized parameters for high-performance systems
    (metafun) metafun -module ASSEMBLY_BINNING -p 24 -m 128
    (metafun) metafun -module WMS_FUNCTION -p 16
    ```
  
- **Staged Analysis**:
  - For large datasets, run modules sequentially on subsets of samples
  - Process taxonomic analysis (fast) before resource-intensive assembly or functional analysis
  
- **Resume Functionality**:
  - Utilize Nextflow's resume feature to continue interrupted workflows:
    ```bash
    # Example restarting a failed run
    (metafun) metafun -module ASSEMBLY_BINNING -resume
    ```

### Getting Support

- **GitHub Issues**: For bug reports, feature requests, or support:
  - Visit the [metaFun GitHub repository](https://github.com/aababc1/metaFun)
  - Create a new issue describing your problem or request
  - Include details about your environment, command used, and error messages
  
- **Documentation**: Refer to the specific module documentation for detailed parameter descriptions and usage examples

- **Citing metaFun**: If you use metaFun in your research, please cite:
  ```
  [Citation information to be added upon publication]
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
workflows/INTERACTIVE_TAXONOMY.md
workflows/WMS_FUNCTION.md
```

```{toctree}
:maxdepth: 2
:caption: Guide for interactive visualization 

```