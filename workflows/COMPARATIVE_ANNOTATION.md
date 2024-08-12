(COMPARATIVE_ANNOTATION_description)=


# COMPARATIVE_ANNOTATION

<img src="../_static/metafun5_sky.png" style="height:200px; width:auto; float:right; margin-left:10px;" />
This Nextflow script implements a workflow for comparative annotation of metagenome-assembled genomes (MAGs).

# COMPARATIVE_ANNOTATION Workflow

## Overview

This Nextflow script implements a comprehensive and flexible comparative genomic analysis workflow. It performs various analyses including pangenome analysis, functional annotation, and visualization of results, with the ability to skip steps based on existing results.

## Key Features

- Dynamic execution based on existing results
- Pangenome analysis using PPanGGOLiN
- Functional annotations: KEGG (KofamScan), virulence factors (VFDB), antibiotic resistance (CARD), CAZymes (dbCAN)
- Genome similarity analysis using Skani
- Protein function prediction using eggNOG-mapper
- Gene-trait association analysis using Scoary2
- Flexible visualization for both gene presence/absence and gene count data

## Inputs

- Quality-controlled genome assemblies (FASTAs)
- Metadata file with sample information

## Outputs

- Annotation results for each analysis tool
- Visualization results including interactive plots and heatmaps
- Separate visualizations for gene presence/absence and gene count data

## Main Parameters

| Parameter | Description | Default Value |
|-----------|-------------|---------------|
| `inputDir` | Input directory for genome files | `"${launchDir}/results/metagenome/BIN_ASSESSMENT/bins_quality_passed"` |
| `metadata` | Path to metadata file | `"${launchDir}/selected_metadata.csv"` |
| `metacol` | Column number in metadata to use | Required (no default) |
| `outdir` | Output directory | `"${launchDir}/results/metagenome/COMPARATIVE_ANNOTATION/${current_time}"` |
| `cpus` | Number of CPUs to use | 40 |
| `pan_identity` | PPanGGOLiN identity threshold | 0.8 |
| `pan_coverage` | PPanGGOLiN coverage threshold | 0.8 |
| `module_completeness` | KEGG module completeness threshold | 0.5 |
| `kofamscan_eval` | KEGG KO e-value threshold | 0.00001 |
| `VFDB_identity` | VFDB identity threshold | 50 |
| `VFDB_coverage` | VFDB coverage threshold | 80 |
| `VFDB_e_value` | VFDB e-value threshold | 1e-10 |
| `CAZyme_hmm_eval` | CAZyme HMM e-value threshold | 1e-15 |
| `CAZyme_hmm_cov` | CAZyme HMM coverage threshold | 0.35 |

## Workflow Structure

The workflow dynamically determines which steps to run based on the existence of previous results:

1. **Genome Preparation**: Selects and prepares input genomes based on metadata.
2. **Annotation**:
   - Prokka for gene prediction (if not already run)
   - PPanGGOLiN for pangenome analysis (if not already run)
   - KofamScan for KEGG annotation
   - VFDB for virulence factor annotation
   - CARD for antibiotic resistance gene detection
   - dbCAN for CAZyme annotation
   - Skani for genome similarity analysis
   - eggNOG for protein function prediction
3. **Visualization**:
   - Creates visualizations for both gene presence/absence and gene count data
   - Includes heatmaps and interactive plots for each annotation type
4. **Additional Analyses**:
   - Scoary2 for gene-trait association analysis
   - Metadata summary creation

## Key Processes and Their Outputs

| Process | Output |
|---------|--------|
| `run_prokka` | Prokka annotation files |
| `run_ppanggolin` | Pangenome analysis results |
| `run_kofamscan_annotation` | KO matrix |
| `run_VFDB_annotation` | VFDB annotation results (PA and count) |
| `run_rgi_CARD_annotation` | CARD annotation results (PA and count) |
| `run_dbCAN_annotation` | CAZyme annotation results (PA and count) |
| `run_skani_annotation` | Genome similarity matrix |
| `run_eggNOG` | eggNOG annotation results |

## Visualization Processes

Each visualization process creates separate outputs for gene presence/absence (PA) and gene count data:

- `run_kofamscan_visualization`
- `run_VFDB_visualization`
- `run_rgi_CARD_visualization`
- `run_dbCAN_visualization`
- `run_skani_visualization`

## Usage

```bash
nextflow run COMPARATIVE_ANNOTATION_apptainer.nf --metadata [path_to_metadata] --metacol [metadata_column] [additional_options]
```

## Requirements

- Nextflow
- Apptainer/Singularity containers with required tools
- Input genomes and metadata file

For detailed information on parameters and usage, run the script with the `--help` flag.

## Notes

- The workflow uses Apptainer (formerly Singularity) containers for tool execution.
- Results are organized in a structured output directory for easy navigation.
- The script includes error checking for critical parameters and input files.
- Visualization results are designed to be interactive and easily interpretable.
- The workflow is flexible and can resume from partial runs, optimizing resource usage.
## Output Files Details
[Check out the HTML Content!](/_static/pcoa_plot_interactive.html)

(pcoa_plot_permanova)=
[COMPARATIVE_ANNOTATION result viewer](http://165.132.36.43/shiny/).
<iframe src="http://165.132.36.43/shiny/" style="border: 2px solid gray"; width="1100px" ; height="900px"></iframe>
