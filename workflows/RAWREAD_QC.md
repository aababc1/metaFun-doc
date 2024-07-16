(RAWREAD_QC_description)=

# RAWREAD_QC

This Nextflow script implements a workflow for quality control of raw reads from whole metagenome sequencing data.


## Workflow Execution 

```{code-block} bash
:caption: RAWREAD_QC execution

# Activate metafun conda environment
conda activate metafun
# Move to metafun directory where you cloned metafun from the github. 
(metafun) nextflow run nf_scripts/RAWREAD_QC_apptainer.nf  --inputDir ${inputDir}
# In the ${inputDir} of yours, there should be short paired-end metagenomic reads. 
# gzipped format and fastq or fq suffix could be utilized.
```

:::{admonition} Host read filtering out options.
:class: note

There are three options filtering the read, `human` ,`Skip filtering out`,`your custom genome`. 
- Default value is set to human genome. If your dataset is from human genome, you do not need to specify filter. 
- If you would like to skip host read filtering out, specify `--filter none`.
```{code-block} bash
:caption: Skip host read filtering out step and subsequent FastQC step. 

# If you would like to skip any read filtering out using interested genome, use this one.
 ` nextflow run nf_scripts/RAWREAD_QC_apptainer.nf  --inputDir ${inputDir} --filter none`.
 ```

- If you would like to your own genome to filter out reads, index it first and specify that.
```{code-block} bash
:caption: Use your custom genome to filter out.

# Index your genome with specific name of yours. We suppose your named it as mygenome.
(metafun) sh generate_custom_filter_usingyourgenome.sh -i ${your_custom genome} -o mygenome
#Specify the filter name as `mygenome` that you used in indexing your genome(mygenome). 
(metafun) nextflow run nf_scripts/RAWREAD_QC_apptainer.nf  --inputDir ${inputDir} --filter mygenome.
:::



## Workflow Overview
This workflow is used as input data for **[ASSEMBLY_BINNING](ASSEMBLY_BINNING_description)**, **WMS_TAXONOMY** and **WMS_FUNCTION**.
The result of this workflow is **mandatory input** for WMS_TAXONOMY


The workflow performs the following steps:

1. FastQC analysis on raw reads. 
2. Trimming and quality filtering using Fastp
3. Removal of host (e.g., human) reads using Bowtie2 (optional)
4. FastQC analysis on filtered reads 
5. MultiQC report generation

## Inputs and Outputs

**Inputs : The raw paired-end short-read metagenomic reads.`--inputDir ${inputDir} `**
**Outputs : Quality controlled and filtered metagenomic reads and quality visualization results.  Default outdir directory is `${launchDir}/results/metagenome/RAWREAD_QC `.**

**${launchDir} is the directory where you execute nextflow script. This should be git cloned base folder of metaFun(https://github.com/aababc1/metaFun).** 

`${launchDir}/results/metagenome/RAWREAD_QC ` = `${params.outdir}` 

| Process | InputDir | OutputDir | Note |
|---------|----------|-----------|------|
| fastqc_raw | `${params.inputDir}` | `${params.outdir}/fastqc_raw`  | FastQC analysis results for raw reads |
| fastp | `${params.inputDir}` | `${params.outdir}/fastp` | Performs trimming and quality filtering |
| humanread_filter | Output from fastp | `${params.outdir}/read_filtered` | Removes host reads (when params.filter is not 'none') |
| fastqc_filtered | Output from humanread_filter | `${params.outdir}/fastqc_filtered` | FastQC analysis results for filtered reads |
| multiQC | Results from all previous processes | `${params.outdir}/multiqc` | Comprehensive report of all QC results |

```{admonition} Switching input and output directory.
:class: note

If you switch input or output directory by specifying `--inputDir ${your input directory}` and `--outdir ${output directory}`, you should have to modify those parameters in other workflows.
The default directory is `results/metagenome/RAWREAD_QC.`
```

We suppose you only specify input directory by set `--inputDir ${inputDir}` or switching it in params.file. The defulat base output directory is `results/metagenome/RAWREAD_QC`. 

## Parameters in RAWREAD_QC Nextflow Script 

| Parameter | Description | Default Value | Note | 
|-----------|-------------|---------------|-------------------|
| `db_baseDir` | Base directory for databases | `/opt/database` in apptainer env. `${git base directory}/database` in your server. | This is mounted path in apptainer environment. We do not recommend switching it to another value. |
| `scripts_baseDir` | Base directory for scripts | `"/scratch/tools/microbiome_analysis/scripts"` in apptainer env. `${git base directory}/scripts` in your server. | This is mounted path in apptainer environment. We do not recommend switching it to another value. |
| `filter` | Type of read filtering to perform | `'human'`| This is parameter for filtering host read. Default value is human (GRCh38_p12.dna.primary_assembly). You could skip this step by using `--filter none` in command line or  modify this value in params file. If you would like to  filter out another host genome reads, you could index genome using  `sh generate_custom_filter_usingyourgenome.sh -i $yourgenome -o $output`.  | 
| `human_index` | Path to human genome index | `"${params.db_baseDir}/host_genome/GRCh38/GRCh38_p12.dna.primary_assembly.fa"` | This is default set value for RAWREAD_QC filtering option. If you need to switch or use other genome, please specify `--filter none` or `--filter ${your genome index}`.| 
| `custom_index` | Path to custom genome index | It is automatically set by `--filter ${value}`. `${params.db_baseDir}/host_genome/${value}/${value}`| You can utilize any genome that you want to filter out read in metagenome. First, you need to index your genome with provided script using `sh generate_custom_filter_usingyourgenome.sh -i $yourgenome -o ${value}`. Then, use it to  nextflow run by designating `--filter value` or  setting `value` in `params.file` |  
| `outdir` | Output directory | `"${launchDir}/results/metagenome/RAWREAD_QC"` | Once you designated the `outdir`, You should designate 'inputDir' in other workflows to be same. |
| `cpus` | Number of CPUs to use | `4` | Number of cpus to be utilized in each program.|
| `inputDir` | Input directory containing raw reads | `'raw_reads'` | The location of folder containing short paired-end metagenomic reads. The files could be gzipped and suffix of file could be fastq or fq such as `*1.fastq,*2.fastq`,`*1.fastq.gz,*2.fastq.gz`,`*1.fq,*2.fq`,`*1.fq.gz,*2.fq.gz` |

## Descriptions of Processes in RAWREAD_QC Workflow 

1. **FastQC on Raw Reads**: Performs FastQC analysis on the raw input metagenomic reads specified by `--inputDir ${your input directory}`.
2. **Fastp Processing**: Trims and filters the metagenomic reads using Fastp.
3. **Host Read Filtering** (optional): Removes host reads using Bowtie2. if `params.filter` is not set to "none". `human` is default genome.  If your metagenomes do not need to be filtered out any host contamination, specify `--filter none` to nextflow execution in command line or switch the value in `parameter.file`. Otherwise If you want to use your own genome of interest, you could index your genome with  `sh generate_custom_filter_usingyourgenome.sh -i $yourgenome -o ${value}` in the metafun directory. 
4. **FastQC on Filtered Reads**: Performs FastQC analysis on the filtered reads.
5. **MultiQC Report**: Generates a MultiQC report combining all QC results.

## Tools Used in RAWREAD_QC


| Tool | Purpose | Version | Default paramters | Parameters that can be selected  |
|------|---------|------------|------------|------------|
| FastQC | Quality control checks on raw sequence data |  v0.12.1 | default | you could select only cpus by `--cpus ${number}` |
| fastp | Trimming and filtering of raw metagenomic reads |  0.23.4 | default |  you could select only cpus by `--cpus ${number}` |
| Bowtie2 | Alignment of reads to remove host contamination | 2.5.2 |`--very-sensitive`: sensitivity preset, `--un-conc-gz`: gzipped metagenomic reads, unaligned to host genome , `end-to-end`  | null |
| MultiQC | Aggregate results from bioinformatics analyses | v1.18 | No specific parameters in this script | null |

## Usage Notes

- Custom index could be utilized by s by specifying `--custom_index` in command shell or modify the parameter in the  `params.file`. 
- The script checks for the existence and non-emptiness of the input directory before proceeding.

## Output file details and examples

If you did not designate output, default output directory is at 
The workflow generates the following outputs in the specified `outdir`:

- FastQC reports for raw and filtered reads
- Fastp filtered reads and JSON report
- Host-filtered reads (if applicable)
- MultiQC report summarizing all QC steps


