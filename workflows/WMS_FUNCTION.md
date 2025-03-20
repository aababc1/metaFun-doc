(WMS_FUNCTION_description)=

# <span style="color:#7030A0">WMS_FUNCTION</span>

<img src="../_static/metafun7_purple.png" style="height:200px; width:auto; float:right; margin-left:10px;" />
This module is a part of metaFun pipeline, providing functional analysis of whole metagenome sequencing data using HUMAnN3.

## Overview
The WMS_FUNCTION module performs functional profiling of metagenomic samples to identify the metabolic pathways present in microbial communities. It utilizes HUMAnN3 to map reads to the UniRef90 protein database and MetaCyc pathway database, generating comprehensive functional profiles. The module integrates functional data with sample metadata to perform statistical analyses and visualizations, revealing the functional potential of microbiomes across different conditions.

## Module Execution

```{code-block} bash
# Basic usage with quality-filtered reads
(metafun) metafun -module WMS_FUNCTION -i results/metagenome/RAWREAD_QC/read_filtered -m metadata.csv -s 1

# Include statistical analysis based on metadata column
(metafun) metafun -module WMS_FUNCTION -i results/metagenome/RAWREAD_QC/read_filtered -m metadata.csv -s 1 -a 2

# Specify custom output directory
(metafun) metafun -module WMS_FUNCTION -i results/metagenome/RAWREAD_QC/read_filtered -m metadata.csv -s 1 -a 2 -o custom_output_dir

# Allocate specific CPU resources
(metafun) metafun -module WMS_FUNCTION -i results/metagenome/RAWREAD_QC/read_filtered -m metadata.csv -s 1 -a 2 -p 24
```

## Module Operation Sequence

This module performs the following steps:

1. **HUMAnN3 analysis** on individual samples:
   - Merges paired-end reads for each sample
   - Performs nucleotide and translated searches against ChocoPhlAn and UniRef90 databases
   - Maps reads to MetaCyc pathway database
   - Generates gene family and pathway abundance profiles
   - **Note on human reads**: This module uses the output from RAWREAD_QC, which has already removed human DNA sequences. HUMAnN3 further handles any remaining host reads through its built-in taxonomic filtering using MetaPhlAn

2. **HUMAnN3 output parsing and normalization**:
   - Combines pathway abundance tables from all samples using `humann_join_tables`
   - Normalizes to copies per million (CPM) using `humann_renorm_table` with the `-u cpm` parameter
     - CPM normalization adjusts for sequencing depth by scaling gene abundances to a sum of 1 million, allowing fair comparison between samples with different sequencing depths
     - The calculation is: (pathway_abundance / total_abundance) × 1,000,000
   - Separates stratified (organism-specific) and unstratified (community-level) abundance tables with `humann_split_stratified_table`

3. **Functional analysis and visualization**:
   - Uses the R script `humann3_visualization.R` from scripts directory to perform comprehensive statistical analysis
   - Takes unstratified pathway abundance table (`pathabund_join_renorm_cpm_unstratified.tsv`) and metadata as input
   - Performs statistical analysis based on metadata groupings:
     - Alpha diversity calculations for functional richness and evenness
     - Beta diversity analysis with PERMANOVA tests
     - Differential abundance analysis to identify pathways that differ between groups
   - Creates visualizations including:
     - Stacked barplots of pathway abundances by group (shown in ① of example figure)
     - Alpha and beta diversity boxplots with statistical comparisons (shown in ② of example figure)
     - Heatmaps of differentially abundant pathways (shown in ③ of example figure)
     - Differential abundance boxplots with statistical significance (shown in ④ of example figure)
     - Correlation analyses with numerical metadata variables (shown in ⑤ of example figure)

## Parameters
**`${launchDir}` is the directory where you execute metaFun, and utilized as output base directory.** 

| Parameter | Description | Default Value | Note |
|-----------|-------------|---------------|------|
| `-i, --inputDir` | Input directory containing filtered reads | `"${launchDir}/results/metagenome/RAWREAD_QC/read_filtered"` | **Required**. Output from <span style="color:#FF0000">RAWREAD_QC</span> workflow |
| `-m, --metadata` | Path to metadata file | `"meta.csv"` | **Required**. CSV file with sample information |
| `-s, --sampleIDcolumn` | Column number for sample IDs in metadata | `1` | **Required**. Matches sample IDs in read filenames |
| `-a, --analysiscolumn` | Column number for analysis grouping | `0` | Optional. If set to 0, no statistical analysis is performed |
| `-p, --cpus` | Number of CPUs to use | `36` | Optional. Adjust based on your system capabilities |
| `-o, --outdir` | Output directory | `"${launchDir}/results/metagenome/WMS_FUNCTION"` | Optional. Where results will be saved |

## **Inputs and Outputs**

### Inputs
* Quality-controlled paired-end metagenomic reads (output from <span style="color:#FF0000">RAWREAD_QC</span> workflow)
* Metadata file (CSV format) with sample information and conditions

### Outputs
* HUMAnN3 gene family and pathway abundance profiles for each sample
* Combined and normalized pathway abundance tables
* Statistical analysis results and visualizations (if --analysiscolumn is specified)

### Output directory structure

The output is organized in the following directory structure:

```{code-block} bash
:caption: Output directory structure

${launchDir}/results/metagenome/WMS_FUNCTION/
├── humann3/                          # Individual HUMAnN3 results directories
│   ├── SRR6915091_humann3/            # Sample-specific HUMAnN3 results directory
│   │   ├── SRR6915091_genefamilies.tsv  # Gene family abundances 
│   │   ├── SRR6915091_pathabundance.tsv # Pathway abundances
│   │   ├── SRR6915091_pathcoverage.tsv  # Pathway coverages
│   │   └── SRR6915091_humann_temp/      # Temporary processing files
│   └── ...                            # Results for other samples
├── humann3_combined/                 # Combined HUMAnN3 results
│   └── humann_split_stratified_table/  # Split stratified and unstratified tables
└── WMS_Function_result/              # Statistical analysis results
    ├── alpha_diversity.csv             # Alpha diversity metrics
    ├── beta_group_perMANOVA_stat.csv   # PERMANOVA statistics
    ├── bray.csv                        # Bray-Curtis dissimilarity matrix
    ├── humann_alpha_beta_diversity.pdf # Alpha/beta diversity plots
    ├── humann_alpha_group_diff_stat.csv # Group difference statistics
    ├── humann_beta_group_distance_diff_stat.csv # Beta diversity statistics
    ├── humann_beta_group_distance_raw.csv # Raw distance values
    ├── humann_DAfunction_meta_correlation.pdf # Correlation plots
    ├── humann_group_barplot.pdf        # Pathway abundance barplots
    ├── humann_lefse_heatmap.pdf        # LEfSe heatmap visualization
    ├── humann_lefse_result.pdf         # LEfSe differential pathway analysis
    ├── humann_metadata_autocorrelation.pdf # Metadata correlations
    └── jaccard.csv                     # Jaccard distance matrix
├── humann_analysis_inspect.log       # Analysis log file
└── Rplots.pdf                        # Additional R plots
```

## Visualization Outputs Explained

The WMS_FUNCTION module produces comprehensive visualizations for functional analysis as shown in this example figure comparing Control and CRC (colorectal cancer) groups:

![WMS_FUNCTION outputs example](../images/WMS_FUNCTION_outputs.png)

### <span style="color:#7030A0; font-family:Arial; font-size:20px">①</span> **Pathway Abundance Stacked Barplots**

This visualization shows the relative abundance of metabolic pathways in each sample, grouped by condition:
- Each vertical bar represents a sample
- Different colors represent different metabolic pathways (listed in the legend)
- The y-axis shows the abundance in CPM (Copies Per Million)
- Samples are grouped by metadata categories (in this example, Control vs. CRC)

This visualization helps identify dominant functional capacities across sample groups and reveals potential shifts in metabolic capabilities between conditions. The `humann_group_barplot.pdf` file contains this visualization.

### <span style="color:#7030A0; font-family:Arial; font-size:20px">②</span> **Functional Diversity Analysis**

This panel displays diversity metrics calculated from functional profiles:

**Top Section:**
- **Alpha Diversity:** Shannon diversity boxplots comparing functional diversity between groups
- **Beta Diversity:** Bray-Curtis distance boxplots showing similarity within and between groups
- Statistical significance is indicated (in this example, "ns" for not significant)

**Bottom Section:**
- **PCoA Plot:** Principal Coordinates Analysis showing sample relationships based on functional profiles
- Samples are colored by group with confidence ellipses
- Statistical metrics are displayed (Pr(>F), Pseudo-F statistic, R²)
- Axes show percent variance explained by each principal coordinate

This visualization is found in the `humann_alpha_beta_diversity.pdf` file, with corresponding statistics in the `alpha_diversity.csv`, `bray.csv`, and `beta_group_perMANOVA_stat.csv` files.

### <span style="color:#7030A0; font-family:Arial; font-size:20px">③</span> **Differential Abundance Heatmap**

This visualization shows the results of LEfSe (Linear discriminant analysis Effect Size) analysis:
- Each row represents a specific metabolic pathway
- Each column represents a sample, grouped by condition
- Color intensity indicates relative abundance (red=high, blue=low)
- Pathways are selected based on statistical significance between groups

The heatmap allows identification of pathways that are consistently more abundant in one group compared to the other, providing potential functional biomarkers. This visualization is saved as `humann_lefse_heatmap.pdf`.

### <span style="color:#7030A0; font-family:Arial; font-size:20px">④</span> **LEfSe Differential Abundance Boxplots**

This panel shows statistical comparison of specific pathways identified by LEfSe analysis:
- Each row shows a differential abundant pathway
- Bars represent abundance in different groups
- The x-axis shows LDA score (Effect size)
- Asterisks indicate statistical significance levels
- Direction and length of bars indicate which group has higher abundance

This visualization highlights the most significantly different pathways between groups and is saved as `humann_lefse_result.pdf`.

### <span style="color:#7030A0; font-family:Arial; font-size:20px">⑤</span> **Metadata Correlation Analysis**

This comprehensive panel analyzes relationships between metadata variables:

**Top Row:**
- Distribution of categorical and numerical metadata variables

**Middle Row:**
- Distribution of a numerical variable (e.g., host_age) by group
- Correlation coefficients between variables, overall and by group

**Bottom Row:**
- Distribution of another numerical variable (e.g., BMI) by group
- Scatterplot showing relationship between numerical variables, colored by group
- Density plots comparing distributions between groups

This analysis helps identify potential confounding variables or correlations between metadata that might influence functional profiles. This visualization is saved as `humann_metadata_autocorrelation.pdf` and `humann_DAfunction_meta_correlation.pdf`.

Together, these visualizations provide a comprehensive analysis of functional metagenomics data, from high-level pathway abundance patterns to specific differential pathways and their relationship with metadata variables.

## Nextflow Processes in <span style="color:#7030A0">WMS_FUNCTION</span> Module

| Process | InputDir | OutputDir | Note |
|---------|----------|-----------|------|
| humann3_run | `${params.inputDir}` | `${params.outdir}/humann3` | Performs HUMAnN3 analysis on individual samples |
| humann3_parsing | Output from humann3_run | `${params.outdir}/humann3_combined` | Combines and normalizes HUMAnN3 outputs |
| function_analysis | Output from humann3_parsing | `${params.outdir}/WMS_Function_result` | Performs statistical analysis and visualization |

## Descriptions of Processes in <span style="color:#7030A0">WMS_FUNCTION</span> Workflow

1. **humann3_run**: Executes HUMAnN3 on each sample's paired-end reads.
   - Input: Paired-end quality-filtered metagenomic reads
   - Output: Gene family and pathway profiles for each sample
   - Merges paired reads for processing
   - Uses UniRef90 protein database and MetaCyc pathway database
   - Performs both nucleotide and translated searches

2. **humann3_parsing**: Combines and normalizes the HUMAnN3 outputs from all samples.
   - Input: HUMAnN3 output files from all samples
   - Output: Combined and normalized pathway abundance tables
   - Joins tables across all samples
   - Normalizes to copies per million (CPM)
   - Separates stratified (organism-specific) and unstratified (community-level) tables

3. **function_analysis**: Performs statistical analysis and creates visualizations.
   - Input: Normalized pathway abundance tables and metadata
   - Output: Statistical results and visualizations
   - Identifies differentially abundant pathways between conditions
   - Creates heatmaps, PCA plots, and boxplots
   - Only runs if --analysiscolumn is specified

## Tools Used in <span style="color:#7030A0">WMS_FUNCTION</span>

| Tool | Purpose | Version | Default parameters | Parameters that can be selected |
|------|---------|---------|---------------------|--------------------------------|
| HUMAnN3 | Functional profiling | 3.0.0 | `--search-mode uniref90`, `--pathways metacyc` | `--threads ${task.cpus}` |
| MetaPhlAn | Taxonomic profiling (used by HUMAnN3) | 4.0.6 | `--index mpa_vOct22_CHOCOPhlAnSGB_202212` | None specific to this workflow |
| R | Statistical analysis and visualization | 4.3.2 | N/A | N/A |

## Usage Notes

- The **<span style="color:#7030A0">WMS_FUNCTION</span>** module is designed to work with the output from the <span style="color:#FF0000">RAWREAD_QC</span> module.
- Metadata file should be in CSV format with at least one column containing sample IDs that match the prefixes of your read filenames.
- HUMAnN3 requires significant computational resources, especially for large datasets. Consider adjusting the CPU allocation with the `-p` parameter.
- HUMAnN3 databases (ChocoPhlAn and UniRef90) must be properly installed and configured.
- The statistical analysis component only runs when the `-a/--analysiscolumn` parameter is specified with a valid column number.
- For optimal results, ensure your reads have been properly quality filtered and host DNA has been removed.
- HUMAnN3 provides both stratified (organism-specific) and unstratified (community-level) functional profiles, allowing for detailed analysis of which organisms contribute to specific pathways.

### Understanding CPM Normalization

The Copies Per Million (CPM) normalization used in this module is crucial for accurate comparison of pathway abundances between samples:

- **What is CPM?** CPM normalizes read counts by dividing each value by the total abundance in a sample, then multiplying by 1 million.

- **Why use CPM?** Different samples often have different sequencing depths. Without normalization, samples with more sequencing would appear to have higher pathway abundances simply due to more reads. CPM allows fair comparison by accounting for these differences.

- **Implementation**: The normalization is performed by the `humann_renorm_table` utility with the command:
  ```
  humann_renorm_table -i pathabund_join.tsv -o pathabund_join_renorm_cpm.tsv -u cpm
  ```

### Processing Scripts

The WMS_FUNCTION module uses several scripts to process and analyze data:

1. **humann3_visualization.R**: The main R script that performs:
   - Statistical analysis of pathway abundances
   - Creation of visualization plots
   - Differential abundance testing
   - Alpha and beta diversity calculations
   - Correlation analysis with metadata
   
   Input parameters:
   - `-i`: Input file (normalized pathway abundance table)
   - `-out`: Output directory name
   - `-m`: Metadata file
   - `-mc`: Metadata column for analysis
   - `-sc`: Sample ID column in metadata

2. **HUMAnN3 utility scripts**:
   - `humann_join_tables`: Combines individual sample results
   - `humann_renorm_table`: Performs CPM normalization
   - `humann_split_stratified_table`: Separates organism-specific and community-level profiles

The execution of these scripts can be seen in the Nextflow processes defined in `WMS_FUNCTION_apptainer.nf`.

## Next Steps

After running <span style="color:#7030A0">WMS_FUNCTION</span>, you can:

Explore taxonomic profiles with the **<span style="color:#0846FA">WMS_TAXONOMY</span>** module to complement your functional analysis:
   ```bash
   (metafun) metafun -module WMS_TAXONOMY -i results/metagenome/RAWREAD_QC/read_filtered -m metadata.csv -c 1 -a 2
   ```


2. Perform deeper analysis by:
   - Examining specific metabolic pathways of interest
   - Comparing functional profiles across different conditions
   - Correlating pathway abundances with metadata variables or taxonomic profiles
   - Identifying functional biomarkers for specific conditions

The <span style="color:#7030A0">WMS_FUNCTION</span> module provides comprehensive insights into the metabolic potential of microbial communities, complementing taxonomic analysis to reveal not just who is present in your samples, but what they can do.