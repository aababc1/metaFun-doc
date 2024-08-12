(WMS_FUNCTION_description)=

# WMS_FUNCTION

<img src="../_static/metafun7_purple.png" style="height:200px; width:auto; float:right; margin-left:10px;" />
This Nextflow script implements a workflow for functional analysis of whole metagenome sequencing data using HUMAnN3.

## Workflow Execution

```{code-block} bash
:caption: WMS_FUNCTION execution

# Activate metafun conda environment
conda activate metafun
# Move to metafun directory where you cloned metafun from GitHub
(metafun) nextflow run nf_scripts/WMS_FUNCTION_apptainer.nf --inputDir ${inputDir} --metadata ${metadata} --sampleIDcolumn ${column_number} --analysiscolumn ${column_number}
```

## Workflow Overview
The workflow performs the following steps:

1. HUMAnN3 analysis on individual samples
2. Parsing and normalization of HUMAnN3 outputs
3. Functional analysis and visualization based on metadata

Result of this workflow provides functional profiles of metagenomic samples, which can be used for downstream comparative analyses.

## Inputs and Outputs

**Inputs**: Quality-controlled paired-end metagenomic reads (output from RAWREAD_QC workflow), metadata file.
**Outputs**: HUMAnN3 results, normalized pathway abundance tables, functional analysis visualizations.

Default output directory is `${launchDir}/results/metagenome/WMS_FUNCTION`.

| Process | InputDir | OutputDir | Note |
|---------|----------|-----------|------|
| humann3_run | `${params.inputDir}` | `${params.outdir}/humann3` | HUMAnN3 analysis results for each sample |
| humann3_parsing | Output from humann3_run | `${params.outdir}/humann3_combined` | Combined and normalized HUMAnN3 results |
| function_analysis | Output from humann3_parsing | `${params.outdir}` | Functional analysis visualizations |

## Parameters in WMS_FUNCTION Nextflow Script

| Parameter | Description | Default Value | Note |
|-----------|-------------|---------------|------|
| `db_baseDir` | Base directory for databases | `/opt/database` | Mounted path in apptainer environment |
| `scripts_baseDir` | Base directory for scripts | `/scratch/tools/microbiome_analysis/scripts` | Mounted path in apptainer environment |
| `inputDir` | Input directory containing filtered reads | `"${launchDir}/results/metagenome/RAWREAD_QC/read_filtered"` | Output from RAWREAD_QC workflow |
| `outdir` | Output directory | `"${launchDir}/results/metagenome/WMS_FUNCTION"` | |
| `metadata` | Path to metadata file | `"meta.csv"` | |
| `sampleIDcolumn` | Column number for sample IDs in metadata | `1` | |
| `analysiscolumn` | Column number for analysis grouping | `0` | |
| `cpus` | Number of CPUs to use | `36` | |

## Descriptions of Processes in WMS_FUNCTION Workflow

1. **HUMAnN3 Run**: Executes HUMAnN3 on each sample's paired-end reads.
2. **HUMAnN3 Parsing**: Combines and normalizes the HUMAnN3 outputs from all samples.
3. **Function Analysis**: Performs statistical analysis and creates visualizations based on the normalized HUMAnN3 results and metadata.

## Tools Used in WMS_FUNCTION

| Tool | Purpose | Version | Default parameters | Parameters that can be selected |
|------|---------|---------|---------------------|--------------------------------|
| HUMAnN3 | Functional profiling of microbial communities | 3.0.0 | `--search-mode uniref90`, `--pathways metacyc` | `--threads ${task.cpus}` |
| R | Statistical analysis and visualization | 4.3.2 | N/A | N/A |

## Usage Notes

- The input directory should contain paired-end read files processed by the RAWREAD_QC workflow.
- Metadata file should be in CSV format with at least two columns: sample IDs and grouping information for analysis.
- The script checks for the existence and non-emptiness of the input directory before proceeding.
- HUMAnN3 databases (ChocoPhlAn and UniRef90) should be properly set up in the specified database directory.

## Output file details and examples

The workflow generates the following outputs in the specified `outdir`:

- HUMAnN3 output files for each sample (gene families, pathway abundances, pathway coverages)
- Combined and normalized pathway abundance tables
- Functional analysis visualizations (e.g., heatmaps, PCA plots)
- Statistical analysis results based on the metadata groupings