(COMPARATIVE_ANNOTATION_description)=


# COMPARATIVE_ANNOTATION

This Nextflow script implements a workflow for comparative annotation of metagenome-assembled genomes (MAGs).

## Workflow Execution

```{code-block} bash
:caption: COMPARATIVE_ANNOTATION execution

# Activate metafun conda environment
conda activate metafun
# Move to metafun directory where you cloned metafun from GitHub
# Run the COMPARATIVE_ANNOTATION workflow
nextflow run nf_scripts/COMPARATIVE_ANNOTATION_apptainer.nf --metadata "${your metadata}" --metacol "${your metacolumn}"
```

## Workflow Overview

This workflow performs the following steps:

1. Genome similarity analysis using Skani
2. Gene annotation using Prokka
3. Pangenome analysis using Panaroo and PPanGGOLiN
4. Functional annotation using KofamScan (KEGG)
5. Virulence factor annotation using VFDB
6. Antibiotic resistance gene annotation using RGI (CARD)

## Inputs and Outputs

**Inputs**: 
- High-quality MAGs (`.fa` files) from the BIN_ASSESSMENT workflow
- Metadata file (CSV format) from the BIN_ASSESSMENT workflow

**Outputs**: 
- Skani genome similarity results and visualizations
- Prokka gene annotations
- Panaroo and PPanGGOLiN pangenome analysis results
- KofamScan KEGG annotations and visualizations
- VFDB virulence factor annotations and visualizations
- CARD antibiotic resistance gene annotations and visualizations

Default input directory: `${params.outdir_Base}/results/metagenome/BIN_ASSESSMENT/bins_quality_passedFinal`
Default output directory: `${params.outdir_Base}/results/metagenome/COMPARATIVE_ANNOTATION`

## Parameters in COMPARATIVE_ANNOTATION Nextflow Script

| Parameter | Description | Default Value | Note |
|-----------|-------------|---------------|------|
| `db_baseDir` | Base directory for databases | `/scratch/tools/microbiome_analysis/database` | Mounted path in apptainer environment |
| `scripts_baseDir` | Base directory for scripts | `/scratch/tools/microbiome_analysis/scripts` | Mounted path in apptainer environment |
| `inputDir` | Input directory | `${params.outdir_Base}/results/metagenome/BIN_ASSESSMENT/bins_quality_passedFinal` | Contains high-quality MAGs |
| `outdir` | Output directory | `${params.outdir_Base}/results/metagenome/COMPARATIVE_ANNOTATION` | Where results will be stored |
| `metadata` | Path to metadata file | `${params.inputDir}/../final_report/quality_taxonomy_combined_final.csv` | Metadata file from BIN_ASSESSMENT |
| `metacol` | Column name for metadata grouping | `""` | Used for visualization grouping |
| `module_completeness` | KEGG module completeness threshold | 0.5 | Used in KofamScan analysis |
| `cpus` | Number of CPUs to use | 64 | Used for parallel processing |
| `pan_identity` | Pangenome identity threshold | 0.8 | Used in pangenome analysis |
| `pan_coverage` | Pangenome coverage threshold | 0.8 | Used in pangenome analysis |

## Descriptions of Processes in COMPARATIVE_ANNOTATION Workflow

1. **run_skani**: Performs genome similarity analysis using Skani.
   - Input: High-quality MAGs
   - Output: Skani similarity matrix and visualizations
   - Key parameters: `-t 32`, `--full-matrix`

2. **run_prokka**: Performs gene annotation using Prokka.
   - Input: Individual MAGs
   - Output: Prokka annotations (GFF files)
   - Key parameters: `--noanno`, `--cpus ${params.cpus}`, `--centre MGSSB`, `--compliant`

3. **run_panaroo**: Performs pangenome analysis using Panaroo.
   - Input: Prokka GFF files
   - Output: Panaroo pangenome results
   - Key parameters: `--clean-mode moderate`, `--remove-invalid-genes`, `-c 0.9`, `-f 0.5`, `--merge_paralogs`

4. **run_ppanggolin**: Performs pangenome analysis using PPanGGOLiN.
   - Input: Prokka GFF files
   - Output: PPanGGOLiN pangenome results
   - Key parameters: `--coverage ${params.pan_identity}`, `--identity ${params.pan_coverage}`, `--kingdom bacteria`, `--rarefaction`

5. **run_kofamscan**: Performs KEGG functional annotation using KofamScan.
   - Input: Pangenome reference sequences
   - Output: KEGG annotations and visualizations
   - Key parameters: `--cpu ${params.cpus}`, `-c ${params.db_baseDir}/kofam/27Nov2023/config-template.yml`

6. **run_VFDB**: Performs virulence factor annotation using VFDB.
   - Input: Pangenome reference sequences
   - Output: VFDB annotations and visualizations
   - Key parameters: `--max-target-seqs 1`, `--id 50`, `--subject-cover 80`, `-e 1e-10`

7. **run_rgi_CARD**: Performs antibiotic resistance gene annotation using RGI (CARD).
   - Input: Pangenome reference sequences
   - Output: CARD annotations and visualizations
   - Key parameters: `--include_nudge`, `--local`

## Tools and Databases Used in COMPARATIVE_ANNOTATION

| Tool | Purpose | Tool Version | Database | Database Version | Default parameters | Parameters that can be selected |
|------|---------|--------------|----------|------------------|---------------------|--------------------------------|
| Skani | Genome similarity analysis | Not specified | N/A | N/A | `skani triangle *.fa -t 32 --full-matrix` | `-t` |
| Prokka | Gene annotation | Not specified | N/A | N/A | `--noanno --cpus ${params.cpus} --centre MGSSB --compliant` | `--cpus` |
| Panaroo | Pangenome analysis | Not specified | N/A | N/A | `--clean-mode moderate --remove-invalid-genes -c 0.9 -f 0.5 --merge_paralogs` | `--threads` |
| PPanGGOLiN | Pangenome analysis | Not specified | N/A | N/A | `--coverage ${params.pan_identity} --identity ${params.pan_coverage} --kingdom bacteria --rarefaction` | `--cpu` |
| KofamScan | KEGG functional annotation | 1.3.0 | KEGG | 27Nov2023 | `-c ${params.db_baseDir}/kofam/27Nov2023/config-template.yml` | `--cpu` |
| VFDB | Virulence factor annotation | Not specified | VFDB | Aug2023 | `--max-target-seqs 1 --id 50 --subject-cover 80 -e 1e-10` | Not specified |
| RGI (CARD) | Antibiotic resistance gene annotation | 6.0.3 | CARD | Not specified | `--include_nudge --local` | `-t`, `-n` |

## Usage Notes

- The script checks for the existence and non-emptiness of the input directory before proceeding.
- The workflow is designed to work with the output from the BIN_ASSESSMENT workflow.
- The script uses conda environments for tool execution, ensuring reproducibility across different computational environments.
- Visualization scripts are included for Skani, KEGG, VFDB, and CARD results.

## Output Files Details

1. Skani results:
   - Location: `${params.outdir}/ani/`
   - Key files: `skani_fullmatrix`, `heatmap_skani.pdf`, `skani_interactive`

2. Prokka results:
   - Location: `${params.outdir}/prokka/`
   - Key files: Individual genome annotation files

3. Panaroo results:
   - Location: `${params.outdir}/panaroo_result/`
   - Key files: Pangenome analysis output files

4. PPanGGOLiN results:
   - Location: `${params.outdir}/ppanggolin_result/`
   - Key files: Pangenome analysis output files

5. KofamScan results:
   - Location: `${params.outdir}/kofamscan/`
   - Key files: `ko_matrix.csv`, `KEGG_module_visualization_shiny`, `KEGG_module_completeness.csv`, `heatmap_KEGG.pdf`

6. VFDB results:
   - Location: `${params.outdir}/VFDB/`
   - Key files: `pangene_vfdb_result.txt`, `gene_PA_VFDB_added.csv`, `heatmap_VFDB.pdf`, `VFDB_interactive`

7. CARD results:
   - Location: `${params.outdir}/CARD/`
   - Key files: `pangene_rgi_CARD_result.txt`, `gene_PA_CARD_added.csv`, `heatmap_CARD.pdf`, `CARD_interactive`

For more detailed information about this workflow, please visit the COMPARATIVE_ANNOTATION documentation (link to be added).

## Output Files Details
[Check out the HTML Content!](/_static/pcoa_plot_interactive.html)

(pcoa_plot_permanova)=

<iframe src="/_static/pcoa_plot_interactive.html" style="border: 2px solid gray"; width="1000px" ; height="800px"></iframe>
