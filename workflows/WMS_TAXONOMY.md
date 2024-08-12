(# WMS_TAXONOMY_description)=

# WMS_TAXONOMY

<img src="../_static/metafun6_ocean.png" style="height:200px; width:auto; float:right; margin-left:10px;" />
This Nextflow script implements a workflow for taxonomic analysis of whole metagenome sequencing data using Kraken2 and Bracken.

## Workflow Execution

```{code-block} bash
:caption: WMS_TAXONOMY execution

# Activate metafun conda environment
conda activate metafun
# Move to metafun directory where you cloned metafun from GitHub
(metafun) nextflow run nf_scripts/WMS_TAXONOMY_apptainer.nf --inputDir ${inputDir} --metadata ${metadata} --sampleIDcolumn ${column_number} --analysiscolumn ${column_number}
```

## Workflow Overview
The workflow performs the following steps:

1. Kraken2 taxonomic classification
2. Bracken abundance estimation
3. Phyloseq object creation from Bracken outputs
4. Statistical analysis and visualization based on metadata

Result of this workflow provides taxonomic profiles of metagenomic samples, which can be used for downstream comparative analyses.

## Inputs and Outputs

**Inputs**: Quality-controlled paired-end metagenomic reads (output from RAWREAD_QC workflow), metadata file.
**Outputs**: Kraken2 reports, Bracken abundance estimates, Phyloseq object, statistical analysis results and visualizations.

Default output directory is `${launchDir}/results/metagenome/WMS_TAXONOMY`.

| Process | InputDir | OutputDir | Note |
|---------|----------|-----------|------|
| kraken2_run | `${params.inputDir}` | `${params.outdir}/kraken2` | Kraken2 classification results |
| bracken_run | Output from kraken2_run | `${params.outdir}/bracken` | Bracken abundance estimates |
| phyloseq_creation | Output from bracken_run | `${params.outdir}/phyloseq` | Phyloseq object creation |
| statistical_analysis | Phyloseq object | `${params.outdir}/stats_analysis` | Statistical analysis and visualizations |

## Parameters in WMS_TAXONOMY Nextflow Script

| Parameter | Description | Default Value | Note |
|-----------|-------------|---------------|------|
| `db_baseDir` | Base directory for databases | `/opt/database` | Mounted path in apptainer environment |
| `scripts_baseDir` | Base directory for scripts | `/scratch/tools/microbiome_analysis/scripts` | Mounted path in apptainer environment |
| `inputDir` | Input directory containing filtered reads | `"${launchDir}/results/metagenome/RAWREAD_QC/read_filtered"` | Output from RAWREAD_QC workflow |
| `outdir` | Output directory | `"${launchDir}/results/metagenome/WMS_TAXONOMY"` | |
| `metadata` | Path to metadata file | Required input | |
| `sampleIDcolumn` | Column number for sample IDs in metadata | `1` | |
| `analysiscolumn` | Column number for analysis grouping | `0` | |
| `relab_filter` | Relative abundance filter for Bracken results | `0.000001` | |
| `cpus` | Number of CPUs to use | `15` | |
| `kraken_method` | Kraken2 method ('default' or 'memory-mapping') | `'default'` | |

## Descriptions of Processes in WMS_TAXONOMY Workflow

1. **Kraken2 Run**: Performs taxonomic classification on each sample's paired-end reads using Kraken2.
2. **Bracken Run**: Estimates abundances at the species level using Bracken, based on Kraken2 results.
3. **Phyloseq Creation**: Creates a Phyloseq object from Bracken outputs and metadata for downstream analysis.
4. **Statistical Analysis**: Conducts statistical analyses and creates visualizations based on the Phyloseq object and metadata.

## Tools Used in WMS_TAXONOMY

| Tool | Purpose | Version | Default parameters | Parameters that can be selected |
|------|---------|---------|---------------------|--------------------------------|
| Kraken2 | Taxonomic classification | 2.1.2 | `--confidence 0.25`, `--paired` | `--memory-mapping` |
| Bracken | Abundance estimation | 2.7 | `-l S` (species level) | `-r ${read_length}` |
| R (phyloseq) | Statistical analysis and visualization | 4.3.2 | N/A | N/A |

## Usage Notes

- The input directory should contain paired-end read files processed by the RAWREAD_QC workflow.
- Metadata file should be in CSV format with at least two columns: sample IDs and grouping information for analysis.
- The script checks for the existence and non-emptiness of the input directory before proceeding.
- Kraken2 and Bracken databases should be properly set up in the specified database directory.
- The `kraken_method` parameter allows for memory-mapping, which can improve performance on systems with sufficient RAM.

## Output file details and examples

The workflow generates the following outputs in the specified `outdir`:

- Kraken2 classification reports for each sample
- Bracken abundance estimates at the species level
- Phyloseq object (RDS file) containing taxonomic profiles and metadata
- Statistical analysis results and visualizations (e.g., alpha diversity plots, beta diversity ordinations, differential abundance analyses)