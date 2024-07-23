(ASSEMBLY_BINNING_description)=

# ASSEMBLY_BINNING

This Nextflow script implements a workflow for de novo assembly, binning, and binning refinement of metagenomic data.

## Workflow Execution

```{code-block} bash
:caption: ASSEMBLY_BINNING execution

# Activate metafun conda environment
conda activate metafun
# Move to metafun directory where you cloned metafun from GitHub
# Suppose you executed RAWREAD_QC_apptainer.nf in previous step, you could simply type this to get assembled contigs and MAGs.  
(metafun) nextflow run nf_scripts/ASSEMBLY_BINNING_apptainer.nf 
```

## Workflow Overview

This workflow performs the following steps:

1. *De novo* assembly using MEGAHIT 
2. Contig renaming
3. Building Bowtie2 index of each sample
4. Metagenomic read mapping to contig
5. Metagenomic binning using MetaBAT2 and SemiBin2
6. Bin refinement using DAS Tool

## Inputs and Outputs

**Inputs**: Quality-controlled paired-end metagenomic reads from **[RAWREAD_QC](RAWREAD_QC_description)** workflow, or you could provide your short paired-end metagenomic data. We highly recommned to run `RAWREAD_QC` workflow.

**Outputs**: *De novo* assembled contigs, metagenome-assembled genomes(MAGs) of MetaBAT2 and SemiBin2, and refined MAGs using DAS Tool. In this workflow, only genomic contents are created without statistical reports.  

Detailes and examples of output files are described at [Output file details and examples](ASSEMBLY_BINNING_output).

Default output directory: `${launchDir}/results/metagenome/ASSEMBLY_BINNING`

| <div style="width:100px">Process</div> |<div style="width:150px">InputDir</div>  | <div style="width:250px">OutputDir</div> | <div style="width:300px"> Note </div> |
|---------|----------|-----------|---------|
| AssemblyAndRename | `${params.inputDir}` | `${params.outdir}/assembled_contigs` | MEGAHIT assembly and contig renaming |
| Bowtie2IndexBuild | Output from AssemblyAndRename | Intermediate result <br> (not separately stored)| Builds Bowtie2 index for contigs |
| MHcontig2sortedbam | Reads and Bowtie2 index | Intermediate result <br> (not separately stored)| Maps reads to contigs and creates sorted BAM |
| MB2_binning | Sorted BAM and contigs | `${params.outdir}/metabat2_bins` | MetaBAT2 binning |
| SB2_binning | Sorted BAM and contigs | `${params.outdir}/semibin2_bins` | SemiBin2 binning |
| Dastool | MetaBAT2 and SemiBin2 bins, contigs | `${params.outdir}/dastool_bins` | DAS Tool bin refinement |

## Parameters in ASSEMBLY_BINNING Nextflow Script

| <div style="width:100px">Parameter</div> |<div style="width:150px">Description</div>  | <div style="width:250px">Default Value</div> | <div style="width:400px"> Note </div> |
|-----------------|--------------------------|------------------------|---------------------| 
|`db_baseDir`|Base directory for databases | `/opt/database` in apptainer env. `${git base directory}/database` in your server. | This is mounted path in apptainer environment. We do not recommend switching it to another value. |
| `scripts_baseDir` | Base directory for scripts | `"/scratch/tools/microbiome_analysis/scripts"` in apptainer env. `${git base directory}/scripts` in your server. | This is mounted path in apptainer environment. We do not recommend switching it to another value. |
| `inputDir` | Input directory | `"${launchDir}/results/metagenome/RAWREAD_QC/read_filtered"` | The folder contains quality-controlled reads. |
| `outdir` | Output directory | `"${launchDir}/results/metagenome/ASSEMBLY_BINNING"` | Where results will be stored. |
| `semibin2_mode` | SemiBin2 environment mode | `"human_gut"` | For self-trained model : use `--semibin2_mode self`. For pretrained model : use `--semibin2_mode ${one of Available modes}`:  Available modes: human_gut, dog_gut, ocean, soil, cat_gut, human_oral, mouse_gut, pig_gut, built_environment, wastewater, chicken_caecum, global |
| `megahit_presets` | MEGAHIT assembly preset | `"default"` | Available presets: default, meta-large, meta-sensitive |
| `cpus` | Number of CPUs to use | `8` | Used for parallel processing |




## Descriptions of Processes in ASSEMBLY_BINNING Workflow

1. **AssemblyAndRename**: Performs de novo assembly using MEGAHIT and renames contigs.
2. **Bowtie2IndexBuild**: Builds Bowtie2 index for the assembled contigs.
3. **MHcontig2sortedbam**: Maps reads to contigs using Bowtie2 and creates sorted BAM files.
4. **MB2_binning**: Performs metagenomic binning using MetaBAT2.
5. **SB2_binning**: Performs metagenomic binning using SemiBin2.
6. **Contigs2bin_prep_mb2** and **Contigs2bin_prep_sb2**: Prepare contig-to-bin files for DAS Tool.
7. **Dastool**: Refines bins using DAS Tool.

## Tools Used in ASSEMBLY_BINNING

| Tool | Purpose | Version | Default parameters | Parameters that can be selected |
|------|---------|---------|---------------------|--------------------------------|
| MEGAHIT | De novo assembly | v1.2.9 | Varies based on `megahit_presets` | `--presets ${params.megahit_presets}` |
| Bowtie2 | Read mapping | 2.5.2. | `--sensitive` | Not specified in this script |
| MetaBAT2 | Metagenomic binning | 2.15 | `-m 1500` | Not specified in this script |
| SemiBin2 | Metagenomic binning | 2.1.0 | `single_easy_bin` mode with pretrained human gut model `--environment  human_gut`|`--semibin2_mode ${mode}` | 
| DAS Tool | Bin refinement | 1.1.7 | `--score_threshold=0` | Not specified in this script |

## Usage Notes

- The script checks for the existence and non-emptiness of the input directory before proceeding.
- SemiBin2 can be run in self-supervised mode or with premade environments models by setting proper `--semibin2_mode ${mode}`. The name of `${mode}` should be vaild. `self` represents self-supervised mode without any reference information that would be proper for novel environmental metagenome data. Available `${mode}` for `--semibin2_mode` : `self`, `human_gut`, `dog_gut`, `ocean`, `soil`, `cat_gut`, `human_oral`, `mouse_gut`, `pig_gut`, `built_environment`, `wastewater`, `chicken_caecum` and `global`. More detailed information is available at SemiBin documentation (https://semibin.readthedocs.io/en/latest/usage/#easy-single-binning-mode)
- The **ASSEMBLY_BINNING** workflow is designed to work with the output from the RAWREAD_QC workflow.
- This pipeline generates MAGs and *de novo* assembled contigs.

(ASSEMBLY_BINNING_output)=
## Output file details and examples