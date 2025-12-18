# Beginners Guide to metaFun

This guide provides detailed information about metaFun's modules, their inputs, outputs, and how they interact with each other in the workflow.

## Understanding metaFun Modules

metaFun is organized into modules that can be run independently or as part of a workflow. Each module has specific inputs and outputs designed to work seamlessly together.

### Module Relationships and Data Flow

#### Genome-based analysis path:
<span style="color:#FF0000">RAWREAD_QC</span> → <span style="color:#FF9300">ASSEMBLY_BINNING</span> → <span style="color:#00B050">BIN_ASSESSMENT</span> → <span style="color:#00B050">GENOME_</span><span style="color:#4E95D9">SELECTOR</span> → <span style="color:#4E95D9">COMPARATIVE_ANNOTATION</span> → <span style="color:#4E95D9">INTERACTIVE_COMPARATIVE</span>

#### Read-based analysis path:
<span style="color:#FF0000">RAWREAD_QC</span> → <span style="color:#0846FA">WMS_TAXONOMY</span> → <span style="color:#0846FA">INTERACTIVE_TAXONOMY</span>

<span style="color:#FF0000">RAWREAD_QC</span> → <span style="color:#7030A0">WMS_FUNCTION</span>

<span style="color:#FF0000">RAWREAD_QC</span> → <span style="color:#0846FA">WMS_TAXONOMY</span> → <span style="color:#2FA4E7">WMS_STRAIN</span> → <span style="color:#2FA4E7">INTERACTIVE_STRAIN</span>

<span style="color:#0846FA">WMS_TAXONOMY</span> → <span style="color:#2FA4E7">INTERACTIVE_NETWORK</span>

## Module Details

### <span style="color:#FF0000">RAWREAD_QC</span>

**Purpose**: Quality control of raw reads and host genome filtering

**Inputs**:
- Raw paired-end reads (FASTQ format)
- Optional: Custom host genome for filtering

**Outputs**:
- Filtered reads in `read_filtered/` directory
- Quality reports in `qc_reports/` directory

**Key Parameters**:
- `-i, --inputDir`: Directory containing raw read files (required)
- `-f, --filter`: Host genome to filter (default: "human")
- `-o, --output`: Output directory (default: "results/metagenome/RAWREAD_QC")
- `-p, --processors`: Number of CPUs to use (default: 4)

**Workflow Notes**:
- This is the starting point for both genome-based and read-based analyses
- Output files are automatically used by subsequent modules

### <span style="color:#FF9300">ASSEMBLY_BINNING</span>

**Purpose**: Metagenome assembly and binning

**Inputs**:
- Filtered reads from RAWREAD_QC (or specified input directory)

**Outputs**:
- Assembled contigs in `assembly/` directory
- Metagenomic bins in `final_bins/` directory
- Assembly statistics in `stats/` directory

**Key Parameters**:
- `-i, --inputDir`: Input directory (optional if following RAWREAD_QC)
- `-o, --output`: Output directory (default: "results/metagenome/ASSEMBLY_BINNING")
- `-p, --processors`: Number of CPUs to use (default: 8)
- `--megahit_presets`: Preset for MEGAHIT assembler (default: "default")
- `--semibin2_mode`: SemiBin2 binning mode (default: "self")

**Workflow Notes**:
- Takes filtered reads from RAWREAD_QC as input
- Creates metagenomic bins for BIN_ASSESSMENT module

### <span style="color:#00B050">BIN_ASSESSMENT</span>

**Purpose**: Assess genome quality and taxonomy classification

**Inputs**:
- Metagenomic bins from ASSEMBLY_BINNING
- Metadata file with accession information

**Outputs**:
- Quality assessment reports in `quality/` directory
- Taxonomy classification in `taxonomy/` directory
- Combined metadata CSV file with quality and taxonomy information

**Key Parameters**:
- `-m, --metadata`: Metadata file with accession information (required)
- `-c, --accession_column`: Column in metadata containing accession information (required)
- `-i, --inputDir`: Input directory (optional if following ASSEMBLY_BINNING)
- `-o, --output`: Output directory (default: "results/metagenome/BIN_ASSESSMENT")
- `-p, --processors`: Number of CPUs to use (default: 20)

**Workflow Notes**:
- Critical for determining which genomes meet quality standards
- Output is used by GENOME_SELECTOR module

### <span style="color:#00B050">GENOME_</span><span style="color:#4E95D9">SELECTOR</span>

**Purpose**: Interactive genome selection interface

**Inputs**:
- Combined metadata CSV file from BIN_ASSESSMENT

**Outputs**:
- Selected genome list in `genome_selector_result.csv`

**Key Parameters**:
- `-i, --input`: Input metadata file (default: most recent BIN_ASSESSMENT output)
- `--port`: Port for web interface (default: 8050)

**Workflow Notes**:
- Interactive web interface for selecting genomes
- Output is used by COMPARATIVE_ANNOTATION module

### <span style="color:#4E95D9">COMPARATIVE_ANNOTATION</span>

**Purpose**: Comparative genomic analysis and annotation

**Inputs**:
- Selected genomes from GENOME_SELECTOR
- Metadata file with sample and analysis information

**Outputs**:
- Pangenome analysis results in `pangenome/` directory
- Functional annotations (KO, CAZy, VFDB, etc.) in respective directories
- Visualization data for interactive analysis

**Key Parameters**:
- `-m, --metadata`: Metadata file (required)
- `--samplecol`: Column in metadata containing sample IDs (required)
- `-i, --inputDir`: Input directory with genomes (optional)
- `-o, --output`: Output directory (default: based on run date/time)
- `--metacol`: Column for analysis grouping (optional for static plots)
- `-p, --processors`: Number of CPUs to use (default: 40)

**Workflow Notes**:
- Comprehensive comparative genomics pipeline
- Two main modes: annotation-only or annotation with static plots
- Prepares data for INTERACTIVE_COMPARATIVE module

### <span style="color:#4E95D9">INTERACTIVE_COMPARATIVE</span>

**Purpose**: Interactive visualization of comparative genomics data

**Inputs**:
- Annotation results from COMPARATIVE_ANNOTATION

**Outputs**:
- Interactive visualization through Shiny web interface

**Key Parameters**:
- `-i, --inputDir`: Input directory with COMPARATIVE_ANNOTATION results (required)
- `-m, --metadata`: Metadata file (required)
- `-o, --output`: Output directory for any saved results (default: "results/interactive_comparative")

**Workflow Notes**:
- Provides interactive dashboards for exploring comparative genomics data
- No further modules depend on its output

### <span style="color:#0846FA">WMS_TAXONOMY</span>

**Purpose**: Taxonomic profiling of metagenomic reads

**Inputs**:
- Filtered reads from RAWREAD_QC (or specified input directory)
- Metadata file with sample information

**Outputs**:
- Taxonomic profiles in `profiles/` directory
- Visualization data in `visualization/` directory
- Phyloseq objects for statistical analysis in `phyloseq/` directory

**Key Parameters**:
- `-m, --metadata`: Metadata file (required)
- `-s, --sampleIDcolumn`: Column in metadata with sample IDs (required)
- `-i, --inputDir`: Input directory (optional if following RAWREAD_QC)
- `--profiler`: Taxonomic profiler to use, either "sylph" or "kraken2" (default: "sylph")
- `-a, --analysiscolumn`: Column for analysis grouping (optional)
- `-o, --output`: Output directory (default: "results/metagenome/WMS_TAXONOMY")
- `-p, --processors`: Number of CPUs to use (default: 4)

**Workflow Notes**:
- Takes filtered reads from RAWREAD_QC as input
- Output is used by INTERACTIVE_TAXONOMY module

### <span style="color:#0846FA">INTERACTIVE_TAXONOMY</span>

**Purpose**: Interactive exploration of taxonomic profiles

**Inputs**:
- Phyloseq objects from WMS_TAXONOMY

**Outputs**:
- Interactive visualization through Shiny web interface

**Key Parameters**:
- `-i, --inputDir`: Input directory with phyloseq objects (required)
- `-o, --output`: Output directory for any saved results (default: "results/interactive_taxonomy")

**Workflow Notes**:
- Provides interactive dashboards for exploring taxonomic data
- No further modules depend on its output

### <span style="color:#7030A0">WMS_FUNCTION</span>

**Purpose**: Functional analysis of metagenomic reads

**Inputs**:
- Filtered reads from RAWREAD_QC (or specified input directory)
- Metadata file with sample information

**Outputs**:
- Functional annotations in `annotations/` directory
- Pathway analysis in `pathways/` directory
- Visualization data in `visualization/` directory

**Key Parameters**:
- `-m, --metadata`: Metadata file (required)
- `-s, --sampleIDcolumn`: Column in metadata with sample IDs (required)
- `-a, --analysiscolumn`: Column for analysis grouping (required)
- `-i, --inputDir`: Input directory (optional if following RAWREAD_QC)
- `-o, --output`: Output directory (default: "results/metagenome/WMS_FUNCTION")
- `-p, --processors`: Number of CPUs to use (default: 36)

**Workflow Notes**:
- Takes filtered reads from RAWREAD_QC as input
- Final module in the read-based functional analysis path

### <span style="color:#2FA4E7">WMS_STRAIN</span>

**Purpose**: Strain-level microdiversity analysis using InStrain

**Inputs**:
- Filtered reads from RAWREAD_QC
- Phyloseq object from WMS_TAXONOMY (for selecting prevalent taxa)

**Outputs**:
- Nucleotide diversity metrics per genome in `instrain_profiles/` directory
- pN/pS ratio tables for selection pressure analysis
- Strain comparison matrices (popANI, conANI)
- Preprocessed RDS files for INTERACTIVE_STRAIN

**Key Parameters**:
- `-i, --input_dir`: Input directory containing filtered reads (required)
- `--phyloseq_object`: Phyloseq RDS file from WMS_TAXONOMY (required)
- `-m, --metadata`: Path to metadata file (optional, extracted from phyloseq if not provided)
- `-s, --sampleIDcolumn`: Column number for sample IDs (default: 1)
- `--prevalence_threshold`: Minimum % of samples for prevalence filtering (default: 5)
- `--min_abundance`: Minimum relative abundance threshold (default: 0.001)
- `-p, --cpus`: Number of CPUs to use

**Workflow Notes**:
- Requires phyloseq output from WMS_TAXONOMY for selecting prevalent taxa
- Output is used by INTERACTIVE_STRAIN module

### <span style="color:#2FA4E7">INTERACTIVE_STRAIN</span>

**Purpose**: Interactive exploration of strain-level diversity results

**Inputs**:
- Results directory from WMS_STRAIN containing InStrain profiles

**Outputs**:
- Interactive visualization through Shiny web interface
- Exported figures and statistical analysis results

**Key Parameters**:
- `-i, --input`: Input directory with WMS_STRAIN results (required)
- `-m, --metadata`: Additional metadata file (optional)
- `-p, --port`: Port number for web interface (default: 8050)

**Workflow Notes**:
- Provides interactive dashboards for exploring nucleotide diversity, pN/pS ratios, and strain sharing
- No further modules depend on its output

### <span style="color:#2FA4E7">INTERACTIVE_NETWORK</span>

**Purpose**: Interactive microbial co-occurrence network analysis

**Inputs**:
- Phyloseq RDS object from WMS_TAXONOMY

**Outputs**:
- Interactive network visualizations
- Network comparison statistics across sample groups
- Node centrality and influential taxa rankings
- Exportable figures and data tables

**Key Parameters**:
- `-i, --input`: Phyloseq RDS file from WMS_TAXONOMY (required)
- `-p, --port`: Port number for web interface (default: 8050)

**Workflow Notes**:
- Supports network inference using FastSpar (SparCC) or FlashWeave
- Enables group-wise network comparison for different conditions
- No further modules depend on its output

## Tips for Beginners

1. **Start with RAWREAD_QC**: This is the foundation for all workflows.

2. **Follow a single path**: Choose either the genome-based or read-based path based on your research question:
   - Genome-based: For comparative genomics, pangenome analysis, and functional annotation of genomes
   - Read-based: For direct taxonomic and functional profiling of metagenomic data

3. **Understand data dependencies**: 
   - Each module automatically looks for output from previous module
   - You only need to specify input directory if you're not following the standard workflow
   - Metadata files must be manually specified for each module that requires them

4. **Resource management**:
   - Adjust `-p` parameter to match your system's capabilities
   - Large datasets may require more memory, especially for assembly and annotation

5. **Troubleshooting**:
   - Check log files in each module's output directory
   - Use `-h` option to get detailed help for each module
   - Resume interrupted workflows with the same parameters 