(BIN_ASSESSMENT_description)=

# BIN_ASSESSMENT

<img src="../_static/metafun4_green.png" style="height:200px; width:auto; float:right; margin-left:10px;" />
This Nextflow script implements a workflow for assessing genome quality and assigning taxonomy to metagenome-assembled genomes (MAGs).

## Workflow Execution

```{code-block} bash
:caption: BIN_ASSESSMENT execution

# Activate metafun conda environment
conda activate metafun
# Move to metafun directory where you cloned metafun from GitHub
# Run the BIN_ASSESSMENT workflow
nextflow run nf_scripts/BIN_ASSESSMENT_apptainer.nf \
--metadata "${your metadata}" --accession_column "${your accessioncolumn}"
```

## Workflow Overview

This workflow performs the following steps:

1. Genome quality assessment using CheckM2
2. Genome contamination assessment using GUNC
3. Combining CheckM2 and GUNC results and filtering **medium-quality genomes [^1]**
4. Taxonomic classification using GTDB-Tk
5. Combining quality assessment and taxonomic classification results
6. Combining results with user-provided metadata **(Optional, highly recommended)**

[^1]: The standards about Minimum information about metagenome-assembled genome **(MIMAG)** was proposed by the Genomic Standards Consortium **(GSC)** in 2017 ([MIMAG paper](https://www.nature.com/articles/nbt.3893)). Medium-quality represents Completeness >= 50% and Contamination < 10% assessed by marker genes by [CheckM2](https://www.nature.com/articles/s41592-023-01940-w).

## Inputs and Outputs

(BIN_ASSESSMENT_combine_metadata)=

- **Inputs**: 
    - Assembled genomic fasta files (`.fa`) from the ASSEMBLY_BINNING workflow.
    - Optional: User-provided metadata file.  
<span style="color:red">We highly recommend specifying **metagenome metadata** during running the **BIN_ASSESSMENT** workflow.</span> See below note. 
:::{admonition} Combining Metadata from Metagenomic and Genomic Analyses
:class: note, dropdown

The metadata should contain `common basename` of paired-end read metagenomic files in `csv format`. 
For example, the base name of a pair of paired-end metagenomic fastq files would be like this.  
`SRR6915091_1.fastq`, `SRR6915091_2fastq` --> **basename** : `SRR6915091`

#### Metadata of Metagenomes

**Example table content of metadata csv file.**
- You need to prepare metada file in csv format of your own. 
- For your reference, download metadata of bioproject [PRJNA447983](https://www.nature.com/articles/s41591-019-0405-7) in csv format.  
{download}`CRC_Control113_PRJNA447983_metadata.csv </_static/CRC_Control113_PRJNA447983_metadata.txt>`

| bioproject_accession | accession_used_in_analysis | country | continent | host_age | host_body_mass_index | host_sex | disease_group | AJCC_stage | age_group |
|:---------------------|:---------------------------|:--------|:----------|:---------|:---------------------|:---------|:--------------|:-----------|:----------|
| PRJNA447983          | SRR6915092                 | Italy   | Europe    | 60       | 20                   | Female   | Control       | Control    | Old       |
| PRJNA447983          | SRR6915097                 | Italy   | Europe    | 80       | 32                   | Female   | Control       | Control    | Old       |
| PRJNA447983          | SRR6915108                 | Italy   | Europe    | 67       | 20.43816558          | Female   | Control       | Control    | Old       |
| PRJNA447983          | SRR6915113                 | Italy   | Europe    | 77       | NA                   | Female   | Control       | Control    | Old       |

- Some lines of metadata of metagenomes are represented. In this table, second column`accession_used_in_analysis` is the base name of generated MAGs.  


#### Metadata of MAGs
- Upon successful execution of the  `BIN_ASSESSMENT`, several output files are created, including  `MAGs` and `metadata file` containing **genome quality** and **taxonomy classification** information.
- For your reference, we povide metadata of MAGs at least **medium quality** generated using `BIN_ASSESSMENT` workflow. 
{download}`quality_taxonomy_combined_final.csv </_static/quality_taxonomy_combined_final.csv>`

| Genome                | Completeness | Contamination | medium_quality.pass | near_complete.pass | medium_quality_gunc.pass | near_complete_gunc.pass | QS50  | QS50.pass | pass.GUNC | QS50_gunc.pass | classification                                                                                                                                             |
|-----------------------|--------------|---------------|---------------------|--------------------|--------------------------|-------------------------|-------|-----------|-----------|----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| SRR6915091_MB2.14     | 91.77        | 0.55          | True                | True               | True                     | True                    | 89.02 | True      | True      | True           | d__Bacteria;p__Bacillota_C;c__Negativicutes;o__Acidaminococcales;f__Acidaminococcaceae;g__Acidaminococcus;s__Acidaminococcus intestini                      |
| SRR6915091_MB2.16     | 93.32        | 6.58          | True                | False              | False                    | False                   | 60.42 | True      | False     | False          | d__Bacteria;p__Bacteroidota;c__Bacteroidia;o__Bacteroidales;f__Bacteroidaceae;g__Phocaeicola;s__Phocaeicola dorei                                           |
| SRR6915091_MB2.17     | 70.82        | 2.2           | True                | False              | True                     | False                   | 59.82 | True      | True      | True           | d__Bacteria;p__Bacillota_A;c__Clostridia;o__Lachnospirales;f__Lachnospiraceae;g__Fusicatenibacter;s__Fusicatenibacter saccharivorans                        |
| SRR6915091_MB2.18_sub | 64.01        | 9.25          | True                | False              | False                    | False                   | 17.76 | True      | False     | False          | d__Bacteria;p__Bacillota_A;c__Clostridia;o__Oscillospirales;f__Oscillospiraceae;g__Flavonifractor;s__Flavonifractor plautii                                  |

- The above file is **automatically generated** in **[ASSEMBLY_BINNING](ASSEMBLY_BINNING_description)** workflow, and name of the file is `quality_taxonomy_combined_final.csv`.

#### Generate combined metadata file contains genome statistics and metagenome metadata of every MAG

- In this example, the second column of metagenome metadata is the basename of the MAGs.  Users need to specify **the column number index of metagenome metadata** file in command line such as `--accession_column 2`.  
- `nextflow run nf_scripts/BIN_ASSESSMENT_apptainer.nf  --metadata CRC_Control113_PRJNA447983_metadata.csv  --accession_column 2`
- For the output file, `combined_metadata_quality_taxonomy.csv` is generated by above command.  

{download}`combined_metadata_quality_taxonomy.csv </_static/combined_metadata_quality_taxonomy.csv>`

| Genome                | Completeness | Contamination | medium_quality.pass | near_complete.pass | medium_quality_gunc.pass | near_complete_gunc.pass | QS50  | QS50.pass | pass.GUNC | QS50_gunc.pass | classification                                                                                                                                             | Analysis_accession | bioproject_accession | accession_used_in_analysis | country | continent | host_age | host_body_mass_index | host_sex | disease_group | AJCC_stage | age_group |
|-----------------------|--------------|---------------|---------------------|--------------------|--------------------------|-------------------------|-------|-----------|-----------|----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------|----------------------|----------------------------|---------|-----------|----------|----------------------|----------|---------------|------------|-----------|
| SRR6915091_MB2.14     | 91.77        | 0.55          | True                | True               | True                     | True                    | 89.02 | True      | True      | True           | d__Bacteria;p__Bacillota_C;c__Negativicutes;o__Acidaminococcales;f__Acidaminococcaceae;g__Acidaminococcus;s__Acidaminococcus intestini                      | SRR6915091         | PRJNA447983          | SRR6915091                 | Italy   | Europe    | 77.0     | 23.0                 | Male     | CRC           |            | Old       |
| SRR6915091_MB2.16     | 93.32        | 6.58          | True                | False              | False                    | False                   | 60.42 | True      | False     | False          | d__Bacteria;p__Bacteroidota;c__Bacteroidia;o__Bacteroidales;f__Bacteroidaceae;g__Phocaeicola;s__Phocaeicola dorei                                           | SRR6915091         | PRJNA447983          | SRR6915091                 | Italy   | Europe    | 77.0     | 23.0                 | Male     | CRC           |            | Old       |
| SRR6915091_MB2.17     | 70.82        | 2.2           | True                | False              | True                     | False                   | 59.82 | True      | True      | True           | d__Bacteria;p__Bacillota_A;c__Clostridia;o__Lachnospirales;f__Lachnospiraceae;g__Fusicatenibacter;s__Fusicatenibacter saccharivorans                        | SRR6915091         | PRJNA447983          | SRR6915091                 | Italy   | Europe    | 77.0     | 23.0                 | Male     | CRC           |            | Old       |
| SRR6915091_MB2.18_sub | 64.01        | 9.25          | True                | False              | False                    | False                   | 17.76 | True      | False     | False          | d__Bacteria;p__Bacillota_A;c__Clostridia;o__Oscillospirales;f__Oscillospiraceae;g__Flavonifractor;s__Flavonifractor plautii                                  | SRR6915091         | PRJNA447983          | SRR6915091                 | Italy   | Europe    | 77.0     | 23.0                 | Male     | CRC           |            | Old       |


- <span style="color:red">We highly recommend specifying **metagenome metadata** during running the **BIN_ASSESSMENT** workflow.</span>

:::

- **Outputs**: 
    - CheckM2 quality assessment results
    - GUNC contamination assessment results
    - GTDB-Tk taxonomic classification results
    - Genome fasta files at least medium quality
    - Quality and taxonomy combined report : `quality_taxonomy_combined_final.csv`
    - **(Optional)** Combined metadata and quality/taxonomy report : `combined_metadata_quality_taxonomy.csv`

* Default input directory:  `${launchDir}/results/metagenome/ASSEMBLY_BINNING/final_bins`
* Default output directory:  `${launchDir}/results/metagenome/BIN_ASSESSMENT`

| Process | InputDir | OutputDir | Note |
|---------|----------|-----------|------|
| runCheckM2 | `${params.inputDir}` | `${params.outdir}/checkm2_${params.run_id}` | CheckM2 quality assessment |
| runGUNC | Output from runCheckM2 | `${params.outdir}/gunc_${params.run_id}` | GUNC contamination assessment |
| combineFiles | Outputs from runCheckM2 and runGUNC | `${params.outdir}/checkm_gunc_combined_${params.run_id}` | Combines and filters results |
| gtdbtk |  Genomes from combineFiles at leaset medium quality | `${params.outdir}/gtdb_outdir_${params.run_id}` | GTDB-Tk taxonomic classification |
| createFinalFile | Outputs from gtdbtk | `${params.outdir}` | Creates final combined report |
| combineMetadata | Final report and user metadata | `${launchDir}` | Optional: Combines with user metadata |

## Parameters in BIN_ASSESSMENT Nextflow Script
| <div style="width:100px">Parameter</div> |<div style="width:150px">Description</div>  | <div style="width:250px">Default Value</div> | <div style="width:400px"> Note </div> |
|-----------|-------------|---------------|------|
| `db_baseDir` | Base directory for databases | `/opt/database` | This is mounted path in apptainer environment.<br> We do not recommend switching it to another value. |
| `scripts_baseDir` | Base directory for scripts | `/scratch/tools/microbiome_analysis/scripts` | This is mounted path in apptainer environment.<br> We do not recommend switching it to another value. |
| `inputDir` | Input directory | `${params.outdir_Base}/results/metagenome/ASSEMBLY_BINNING/final_bins` | Contains assembled genomic fasta files. |
| `outdir` | Output directory | `${params.outdir_Base}/results/metagenome/BIN_ASSESSMENT` | Where results will be stored. |
| `GUNCdb` | GUNC database file | `${params.db_baseDir}/gunc/gunc_db_progenomes2.1.dmnd` | GUNC database file |
| `checkm2db` | CheckM2 database file | `${params.db_baseDir}/checkm2/CheckM2_database/uniref100.KO.1.dmnd` | CheckM2 database file |
| `cpus` | Number of CPUs to use | 76 | Used for parallel processing |
| `metadata` | Path to metadata file | null | Optional: User-provided metadata file [refer this section](BIN_ASSESSMENT_combine_metadata).  **We highly recommend use this option.**|
| `accession_column` | Column index for accession in metadata | 1 | Used when combining with metadata. Use with above metadata option `--metadata ${your metadata}`. |
| `run_id` | Unique identifier for the run | Generated based on date and workflow name | Used to distinguish between different runs. It enables parallel processing of this workflow. It is automatically generated, but you can specify this. |

## Descriptions of Processes in BIN_ASSESSMENT Workflow

1. **runCheckM2**: Performs genome quality assessment using CheckM2.
   - Input: Directory containing genome fasta files
   - Output: CheckM2 quality report
   - Key parameters: `--threads ${params.cpus}`, `--database_path ${params.checkm2db}`

2. **runGUNC**: Assesses genome contamination using GUNC.
   - Input: Protein files generated by CheckM2
   - Output: GUNC contamination report
   - Key parameters: `-t ${task.cpus}`, `--db_file ${params.GUNCdb}`

3. **combineFiles**: Combines CheckM2 and GUNC results, filters high-quality genomes.
   - Input: CheckM2 and GUNC reports
   - Output: Combined quality report, high-quality genome fasta files
   - Uses custom Python script: `Checkm2_GUNC_combine_quality_pass.py`

4. **gtdbtk**: Performs taxonomic classification using GTDB-Tk.
   - Input: High-quality genome fasta files
   - Output: GTDB-Tk classification results
   - Key parameters: `--mash_db ${params.db_baseDir}/gtdb/release220/mash_220.db.msh`, `--cpus ${task.cpus}`

5. **createFinalFile**: Creates a final combined report of quality assessment and taxonomic classification.
   - Input: Combined quality report and GTDB-Tk results
   - Output: Final quality and taxonomy report

6. **combineMetadata**: Optional step to combine results with user-provided metadata.
   - Input: Final quality and taxonomy report, user metadata file
   - Output: Combined metadata and quality/taxonomy report
   - Uses custom Python script: `combine_metadata_WMS_genome.py`

## Tools and Databases Used in BIN_ASSESSMENT
| <div style="width:70px">Tool</div> |<div style="width:150px">Purpose</div>  | <div style="width:60px">Tool Version</div> | <div style="width:150px"> Database </div> | <div style="width:60px"> Database Version </div> | <div style="width:450px"> Default parameters </div> | <div style="width:300px"> Parameters that can be selected for only this tool </div> |
|------|---------|--------------|----------|------------------|---------------------|--------------------------------|
| CheckM2 | Genome quality assessment | 1.0.2 | CheckM2 Database | 1.0.2 |`checkm2 predict --threads ${task.cpus} --input ${params.inputDir} --output-directory ${params.outputDirCheckM2} -x fa --database_path ${params.checkm2db} `| `${params.outputDirCheckM2}` |
| GUNC | Genome contamination assessment | 1.0.6 | GUNC Database | progenomes2.1 |   `gunc run -d ${checkm2faa_dir}/protein_files -g -t ${task.cpus} -o ${params.outputDirGUNC} --db_file ${params.GUNCdb} -e .faa `| `--outputDirGUNC ${gunc outdir}`  |
| GTDB-Tk | Genome taxonomy classification | v2.4.0 | GTDB | r220 |  `time gtdbtk classify_wf --mash_db ${params.db_baseDir}/gtdb/release220/mash_220.db.msh --genome_dir ${bins_quality_passed}  -x fa  --cpus ${task.cpus} --pplacer_cpus ${task.cpus} --out_dir gtdb_outdir` | No specific parameters could be adjusted for this pipeline except parameters regarding input and output files. |

This table provides a comprehensive overview of the tools used in the BIN_ASSESSMENT workflow, including their associated databases and versions. It ensures that users have a clear understanding of both the software and reference data being utilized in their analysis.

## Custom scripts and internal conversion of files.
 - `Checkm2_GUNC_combine_quality_pass.py` : Combine results files of CheckM2 and GUNC file, and select genomes at least medium quality ([MIMAG ](https://www.nature.com/articles/nbt.3893)). This script create `combined_report.tsv`. 
 - `GTDB_add2_check2gunc.py` : This script creates genome quality and taxonomy combined metadata file named **`quality_taxonomy_combined.csv`**. This file contains CheckM2 result, GUNC result, and taxonomy classification by GTDB-Tk. 
 - `combine_metadata_WMS_genome.py` : This script generate combined metadata file named **`combined_metadata_quality_taxonomy.csv`** by combining user's metadata and `quality_taxonomy_combined.csv`. This file is optionally generated, but is essential file for downstream statistical analysis in **[COMPARATIVE_ANNOTATION](COMPARATIVE_ANNOTATION_description)** workflow. 

## Usage Notes

- The script checks for the existence and non-emptiness of the input directory before proceeding.
- To generate a genome metadata table for use in COMPARATIVE_ANNOTATION, specify the `--metadata` option and the `--accession_column`.
- The final metadata file (when using the `--metadata` option) will be named `quality_taxonomy_combined_${params.run_id}.csv`.
- This workflow is designed to work with the output from the ASSEMBLY_BINNING workflow.
- The script uses Apptainer (formerly Singularity) containers for tool execution, ensuring reproducibility across different computational environments.

## Output Files Details

1. CheckM2 results: 
   - Location: `${params.outdir}/checkm2_${params.run_id}/`
   - Key file: `quality_report.tsv`

2. GUNC results: 
   - Location: `${params.outdir}/gunc_${params.run_id}/`
   - Key file: `GUNC.progenomes_2.1.maxCSS_level.tsv`

3. Combined CheckM2 and GUNC report: 
   - Location: `${params.outdir}/checkm_gunc_combined_${params.run_id}/`
   - Key file: `combined_report.tsv`

4. GTDB-Tk results: 
   - Location: `${params.outdir}/gtdb_outdir_${params.run_id}/`
   - Key files: `gtdbtk.bac120.summary.tsv`, `gtdbtk.ar53.summary.tsv`

5. Final quality and taxonomy report: 
   - Location: `${params.outdir}/`
   - File: `quality_taxonomy_combined_final.csv`

6. Optional combined metadata and quality/taxonomy report: 
   - Location: `${launchDir}/`
   - File: `combined_metadata_quality_taxonomy.csv`

For more detailed information about this workflow, please visit the [BIN_ASSESSMENT documentation](https://metafun-doc.readthedocs.io/en/latest/workflows/BIN_ASSESSMENT.html).