(WMS_STRAIN_description)=

# <span style="color:#2FA4E7">WMS_STRAIN</span>

<img src="../_static/metafun7_purple.png" style="height:200px; width:auto; float:right; margin-left:10px;" />
This module is a part of metaFun pipeline, providing strain-level analysis of whole metagenome sequencing data using InStrain.

## Overview
The WMS_STRAIN module performs strain-level analysis of metagenomic samples to characterize microdiversity within microbial populations. It utilizes InStrain to profile single nucleotide variants (SNVs), calculate nucleotide diversity metrics, and compare strain populations across samples. The module generates comprehensive metrics including pN/pS ratios for selection pressure analysis, nucleotide diversity (π) values, and strain sharing patterns between samples.

## Module Execution

```{code-block} bash
# Basic usage with phyloseq object from WMS_TAXONOMY
(metafun) metafun -module WMS_STRAIN -i results/metagenome/RAWREAD_QC/read_filtered \
    --phyloseq_object results/metagenome/WMS_TAXONOMY/phyloseq/phyloseq_object_sylph.RDS

# With custom prevalence filtering
(metafun) metafun -module WMS_STRAIN -i results/metagenome/RAWREAD_QC/read_filtered \
    --phyloseq_object results/metagenome/WMS_TAXONOMY/phyloseq/phyloseq_object_sylph.RDS \
    --prevalence_threshold 10 --min_abundance 0.001

# With external metadata file
(metafun) metafun -module WMS_STRAIN -i results/metagenome/RAWREAD_QC/read_filtered \
    --phyloseq_object results/metagenome/WMS_TAXONOMY/phyloseq/phyloseq_object_sylph.RDS \
    -m metadata.csv -s 1

# Allocate specific CPU resources
(metafun) metafun -module WMS_STRAIN -i results/metagenome/RAWREAD_QC/read_filtered \
    --phyloseq_object results/metagenome/WMS_TAXONOMY/phyloseq/phyloseq_object_sylph.RDS \
    -p 24
```

## Module Operation Sequence

This module performs the following steps:

1. **Prevalence filtering** from phyloseq object:
   - Filters taxa based on prevalence threshold (default: 5% of samples)
   - Applies minimum abundance filter (default: 0.1%)
   - Matches prevalent taxa to GTDB genomes
   - Extracts sample metadata from phyloseq or external file

2. **Genome preparation**:
   - Fetches reference genomes from GTDB database
   - Concatenates genomes into combined reference FASTA
   - Generates scaffold-to-bin (STB) mapping file
   - Builds Bowtie2 index for read mapping

3. **Gene annotation**:
   - Runs Prodigal on individual genomes (parallelized)
   - Concatenates gene predictions (proteins, genes, GFF)
   - Runs eggNOG-mapper for functional annotation (COG categories)

4. **Read mapping** to reference genomes:
   - Maps quality-filtered reads to combined reference using Bowtie2
   - Generates sorted BAM files for each sample
   - Creates index files for efficient access

5. **InStrain profiling** on individual samples:
   - Profiles each sample to detect SNVs at strain-level resolution
   - Calculates nucleotide diversity (π) using [Nei and Li (1979)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1213565/) method
   - Computes pN/pS ratios to assess selection pressure
   - Generates gene-level and genome-level metrics

6. **InStrain comparison** across samples:
   - Compares strain populations across all samples
   - Calculates popANI and conANI between sample pairs
   - Identifies shared strains (default: 99.999% popANI threshold)
   - Generates comparison matrices for downstream analysis

7. **Data aggregation** for visualization:
   - Combines profile results from all samples
   - Integrates with GTDB taxonomy and sample metadata
   - Prepares RDS files for INTERACTIVE_STRAIN module

## Parameters
**`${launchDir}` is the directory where you execute metaFun, and utilized as output base directory.**

| Parameter | Description | Default Value | Note |
|-----------|-------------|---------------|------|
| `-i, --input_dir` | Input directory containing filtered reads | Required | Output from <span style="color:#FF0000">RAWREAD_QC</span> workflow |
| `--phyloseq_object` | Phyloseq RDS file from WMS_TAXONOMY | Required | Path to phyloseq object for prevalence filtering |
| `-m, --metadata` | Path to metadata file | Optional | CSV file; if not provided, extracts from phyloseq |
| `-s, --sampleIDcolumn` | Column number for sample IDs in metadata | `1` | Matches sample IDs in read filenames |
| `--prevalence_threshold` | Minimum % of samples for prevalence | `5` | Taxa must be present in this % of samples |
| `--min_abundance` | Minimum relative abundance threshold | `0.001` | Filter taxa below 0.1% abundance |
| `--min_coverage` | Minimum coverage for InStrain | `5` | Higher values = more confident calls |
| `--min_freq` | Minimum SNP frequency threshold | `0.05` | Filter low-frequency variants |
| `--min_read_ani` | ANI threshold for read assignment | `0.92` | 0.92=strain, 0.95=species, 0.99=clonal |
| `-p, --cpus` | Number of CPUs to use | Auto-detected | Adjust based on your system capabilities |
| `-o, --outdir` | Output directory | `"${launchDir}/results/metagenome/WMS_STRAIN"` | Where results will be saved |

## **Inputs and Outputs**

### Inputs
* Quality-controlled paired-end metagenomic reads (output from <span style="color:#FF0000">RAWREAD_QC</span> workflow)
* Phyloseq object from <span style="color:#2FA4E7">WMS_TAXONOMY</span> (contains taxonomy and sample metadata)
* Optional: External metadata file (CSV format) to replace phyloseq metadata

### Outputs
* Prevalent taxa list with GTDB genome matches
* InStrain profile results for each sample
* Nucleotide diversity metrics per genome
* pN/pS ratio tables (gene-level and genome-wide)
* Strain comparison matrices (popANI, conANI)
* Preprocessed RDS files for INTERACTIVE_STRAIN visualization

### Output directory structure

The output is organized in the following directory structure:

```{code-block} bash
:caption: Output directory structure

${launchDir}/results/metagenome/WMS_STRAIN/
├── 01_prevalent_taxa/                    # Prevalence filtering results
│   ├── prevalent_taxa_taxonomy_ids.txt   # Filtered taxa IDs
│   ├── prevalent_taxa_metadata.tsv       # GTDB metadata for prevalent taxa
│   ├── prevalent_taxa_genome_paths.txt   # Paths to GTDB genomes
│   ├── prevalence_summary.tsv            # Prevalence statistics
│   └── sample_metadata.csv               # Extracted/provided sample metadata
├── 02_genome_prep/                       # Genome preparation
│   ├── all_genomes_combined.fa           # Concatenated reference genomes
│   ├── prevalent_taxa.stb               # Scaffold-to-bin mapping
│   └── bowtie2_index/                    # Bowtie2 index files
├── 03_gene_annotation/                   # Gene predictions and annotations
│   ├── genes.faa                         # Protein sequences
│   ├── genes.fna                         # Gene sequences
│   ├── genes.gff                         # Gene annotations (GFF format)
│   └── eggnog_results.emapper.annotations # eggNOG functional annotations
├── 04_bam_files/                         # Read mapping results
│   ├── ${sample_id}.sorted.bam           # Sorted BAM files
│   └── ${sample_id}.sorted.bam.bai       # BAM index files
├── 05_instrain_profiles/                 # InStrain profile results
│   ├── ${sample_id}_instrain_profile/    # Sample-specific profile directory
│   │   ├── output/                       # Main output files
│   │   │   ├── ${sample_id}_genome_info.tsv    # Genome-level metrics
│   │   │   ├── ${sample_id}_gene_info.tsv      # Gene-level metrics
│   │   │   └── ${sample_id}_scaffold_info.tsv  # Scaffold metrics
│   │   └── raw_data/
│   │       └── genes_SNP_count.csv.gz    # SNP counts for pN/pS calculation
│   └── validation_summary.txt            # Profile validation results
├── 06_instrain_compare/                  # InStrain comparison results
│   └── instrainComparer_output/
│       └── output/
│           ├── comparisonsTable.tsv      # Pairwise sample comparisons
│           └── genomeWide_compare.tsv    # popANI/conANI metrics
└── 07_shiny_data/                        # Preprocessed data for visualization
    ├── integrated_microbiome_data.rds    # Combined R data object
    ├── pN_pS_gene_level.rds              # Gene-level pN/pS data
    ├── pN_pS_genome_wide.rds             # Genome-wide pN/pS data
    └── eggnog_annotations_subset.rds     # Filtered eggNOG annotations
```

## Key Metrics Explained

### Nucleotide Diversity (π)
Nucleotide diversity measures within-population genetic variation using the [Nei and Li (1979)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1213565/) method:

**Formula**: π = 1 - Σ(frequency of each base)²

InStrain calculates π at every genomic position with sufficient coverage (≥5x by default) and averages across genes/genomes. This metric is robust to coverage differences between samples.

- **High π**: Indicates diverse strain population with many SNVs
- **Low π**: Indicates homogeneous population or recent selective sweep

### pN/pS Ratio
The ratio of nonsynonymous to synonymous substitutions, indicating selection pressure:
- **pN/pS < 1**: Purifying (negative) selection - deleterious mutations removed
- **pN/pS ≈ 1**: Neutral evolution - no selective pressure
- **pN/pS > 1**: Positive selection - beneficial mutations favored

### Population ANI (popANI) and Consensus ANI (conANI)
InStrain calculates two ANI metrics for strain comparison:

- **popANI** (population-level ANI): Considers both major and minor alleles, accounting for within-sample microdiversity. A popANI substitution is called only when no alleles are shared between samples.
- **conANI** (consensus ANI): Compares only consensus (major) alleles between samples. A conANI substitution is called when samples have different major alleles.

The default threshold of **99.999% popANI** is recommended for identifying shared strains. For more details, see the [InStrain documentation](https://instrain.readthedocs.io/en/latest/important_concepts.html).

## Nextflow Processes in <span style="color:#2FA4E7">WMS_STRAIN</span> Module

| Process | InputDir | OutputDir | Note |
|---------|----------|-----------|------|
| prevalence_filter_phyloseq | Phyloseq RDS | `01_prevalent_taxa` | Filters taxa by prevalence |
| concat_genomes | GTDB genome paths | `02_genome_prep` | Concatenates reference genomes |
| generate_stb | GTDB genome paths | `02_genome_prep` | Creates scaffold-to-bin mapping |
| bowtie2_build | Combined FASTA | `02_genome_prep/bowtie2_index` | Builds Bowtie2 index |
| prodigal_per_genome | Individual genomes | Work directory | Predicts genes (parallelized) |
| concat_gene_predictions | Prodigal outputs | `03_gene_annotation` | Concatenates gene predictions |
| eggnog_mapper | Protein sequences | `03_gene_annotation` | Functional annotation |
| bowtie2_mapping | Filtered reads | `04_bam_files` | Maps reads to reference |
| instrain_profile | BAM files | `05_instrain_profiles` | Profiles strain-level variation |
| validate_instrain_profiles | Profile directories | `05_instrain_profiles` | Validates profiles |
| instrain_compare | Valid profiles | `06_instrain_compare` | Compares strains across samples |
| aggregate_for_shiny | All outputs | `07_shiny_data` | Prepares data for visualization |

## Tools Used in <span style="color:#2FA4E7">WMS_STRAIN</span>

| Tool | Purpose | Version | Default parameters | Parameters that can be selected |
|------|---------|---------|---------------------|--------------------------------|
| Bowtie2 | Read mapping | 2.5+ | `--sensitive-local --no-unal` | `--threads ${task.cpus}` |
| InStrain | Strain profiling | 1.8+ | `--min_cov 5`, `--database_mode` | `-p ${task.cpus}`, `--min_read_ani` |
| Prodigal | Gene prediction | 2.6.3 | `-p single` (per genome) | N/A |
| eggNOG-mapper | Functional annotation | 2.1+ | `-m mmseqs` | `--cpu ${task.cpus}` |
| samtools | BAM processing | 1.17+ | `-@ ${task.cpus}` | N/A |

## Usage Notes

- The **<span style="color:#2FA4E7">WMS_STRAIN</span>** module requires a phyloseq object from <span style="color:#2FA4E7">WMS_TAXONOMY</span> for prevalence filtering.
- Prevalent taxa are automatically matched to GTDB genomes for reference-based analysis.
- Metadata can be extracted from the phyloseq object or provided separately via `-m` parameter.
- InStrain requires significant computational resources. CPU allocation is auto-detected but can be adjusted with `-p`.
- Higher coverage samples provide more reliable strain-level metrics. Samples with average coverage < 5x may have limited strain resolution.
- The module automatically validates InStrain profiles and skips comparison if fewer than 2 valid profiles exist.
- For optimal results, use appropriate `--prevalence_threshold` to focus on abundant, prevalent taxa.

## Next Steps

After running <span style="color:#2FA4E7">WMS_STRAIN</span>, you can:

1. Explore the results interactively using the **<span style="color:#2FA4E7">INTERACTIVE_STRAIN</span>** module:
   ```bash
   (metafun) metafun -module INTERACTIVE_STRAIN -i results/metagenome/WMS_STRAIN/07_shiny_data
   ```

2. Perform deeper analysis by:
   - Examining nucleotide diversity patterns across conditions
   - Analyzing pN/pS ratios to identify genes under selection (COG functional categories)
   - Comparing strain populations between sample groups using popANI thresholds
   - Correlating strain-level metrics with metadata variables

The <span style="color:#2FA4E7">WMS_STRAIN</span> module provides comprehensive insights into strain-level diversity within microbial communities, enabling researchers to understand not just which species are present, but the genetic variation within those species.
