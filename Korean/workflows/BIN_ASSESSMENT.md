(BIN_ASSESSMENT_description)=

# <span style="color:#00B050">BIN_ASSESSMENT</span>

<img src="../../_static/metafun4_green.png" style="height:200px; width:auto; float:right; margin-left:10px;" />
이 모듈은 메타게놈 어셈블 게놈(MAG)의 품질 평가 및 분류학적 분류를 위해 설계된 metaFun 파이프라인의 일부입니다.

## 개요
BIN_ASSESSMENT 모듈은 메타게놈 어셈블 게놈(MAG)의 포괄적인 평가를 위해 설계된 metaFun 파이프라인의 세 번째 단계입니다. 이 모듈은 CheckM2를 사용한 품질 평가, GUNC를 사용한 오염도 평가, GTDB-Tk를 사용한 분류학적 분류를 수행하고, 다운스트림 분석을 위해 결과를 결합합니다. 이 모듈은 비교 유전체 분석에 적합한 고품질 게놈을 식별하는 데 도움이 됩니다.

## 모듈 작동 순서

이 모듈은 다음 단계를 수행합니다:

1. 입력 게놈 빈 준비
2. CheckM2를 사용한 게놈 품질 평가
3. GUNC를 사용한 게놈 오염도 평가
4. CheckM2 및 GUNC 결과 결합 및 품질 기반 게놈 필터링
5. GTDB-Tk를 사용한 품질 필터링된 게놈의 분류학적 분류
6. 품질 평가 및 분류학적 분류를 결합한 최종 보고서 작성
7. (선택 사항) 사용자 제공 메타데이터와 결과 결합

## 매개변수
**`${launchDir}`은 metaFun을 실행하는 디렉토리로, 출력 기본 디렉토리로 활용됩니다.** 

| 매개변수 | 설명 | 기본값 | 참고 |
|-----------|-------------|---------------|------|
| `-i, --inputDir` | 게놈 빈이 있는 입력 디렉토리 | `${launchDir}/results/metagenome/ASSEMBLY_BINNING/final_bins` | <span style="color:#FF9300">ASSEMBLY_BINNING</span> 모듈의 출력 또는 게놈 빈이 포함된 자체 디렉토리를 지정합니다. |
| `-o, --outdir` | 출력 디렉토리 | `${launchDir}/results/metagenome/BIN_ASSESSMENT` | 다운스트림 분석을 위해 기본값 권장 |
| `-m, --metadata` | 메타데이터 파일 경로 | null | 선택 사항이지만 권장됩니다. 다운스트림 분석을 위해 품질/분류학 결과를 샘플 메타데이터와 결합하는 데 사용됩니다. |
| `-c, --accession_column` | 메타데이터의 열 인덱스 | 1 | 메타데이터 파일에서 게놈 빈 이름과 일치하는 샘플 식별자가 포함된 열을 지정합니다. |
| `--pass_quality` | 게놈 선택을 위한 품질 필터 | `QS50.pass` | 옵션: `medium_quality.pass`, `high_quality.pass`, `medium_quality_gunc.pass`, `high_quality_gunc.pass`, `QS50.pass`, `QS50_gunc.pass`, `all` |
| `-p, --processors` | 사용할 CPU 수 | 20 | 시스템 기능에 따라 조정 |
| `--run_id` | 고유 실행 식별자 | Timestamp_workflowName | "yyyyMMddHHmmss_number" 형식(예: "20250306135829_2996")으로 자동 생성됩니다. 필요한 경우 사용자 정의할 수 있습니다. |

:::{admonition} 품질 필터링 및 메타데이터 매개변수에 대한 정보
:class: note

**품질 필터링 구현:**

Nextflow 스크립트는 `--pass_quality` 매개변수를 기반으로 품질 필터링을 구현합니다. 게놈이 처리될 때:

- 매개변수는 지정된 품질 기준에 따라 후속 단계로 전달될 게놈을 선택합니다.
- `--pass_quality`가 `all`로 설정된 경우, 모든 게놈 빈이 필터링 없이 포함됩니다.
- 다른 옵션(`QS50.pass`, `medium_quality.pass` 등)의 경우, 스크립트는 선택된 품질 기준에 대해 "True"로 표시된 게놈만 포함하도록 결합된 품질 보고서의 해당 열에 따라 게놈을 필터링합니다.

**Accession Column 예시:**

메타데이터 파일과 함께 `--accession_column`이 작동하는 방식의 예:

메타데이터 파일(sample_metadata.csv):
```
run_accession,sample_id,location,disease_status,age
SRR6915091,P001,USA,Healthy,35
SRR6915092,P002,Canada,Disease,42
SRR6915093,P003,UK,Healthy,28
```

게놈 빈 이름은 다음과 같을 것입니다:
- SRR6915091_bin.1.fa
- SRR6915091_bin.2.fa
- SRR6915092_bin.1.fa
...

이러한 빈 이름을 메타데이터와 일치시키려면 다음을 사용합니다:
```
metafun -module BIN_ASSESSMENT -m sample_metadata.csv -c 1
```

열 1(`run_accession`)에 게놈 빈 이름의 접두사와 일치하는 샘플 식별자(SRR6915091, SRR6915092)가 포함되어 있기 때문입니다.
:::

## **입력 및 출력**

### 입력
* FASTA 형식의 게놈 빈(`.fa`, `.fna`, 또는 `.fasta` 확장자)
* <span style="color:#FF9300">ASSEMBLY_BINNING</span> 워크플로우에서 나온 고품질 빈이어야 함
* 기본 입력 디렉토리: `${launchDir}/results/metagenome/ASSEMBLY_BINNING/final_bins`
* 선택 사항: CSV 또는 TSV 형식의 샘플 정보가 포함된 메타데이터 파일

(BIN_ASSESSMENT_output)=

### 출력
* CheckM2 품질 평가 결과
* GUNC 오염도 평가 결과
* GTDB-Tk 분류학적 분류
* 품질 필터링된 게놈 빈
* 결합된 품질 및 분류학 보고서
* 선택 사항: 품질/분류학 정보가 포함된 결합 메타데이터

### 출력 디렉토리 구조

출력 디렉토리는 `${launchDir}/results/metagenome/BIN_ASSESSMENT` 또는 `-o outdir`로 지정한 디렉토리 경로에 있습니다.

```{admonition} 입력 및 출력 디렉토리 전환
:class: note

`-o ${output directory}`로 사용자 정의 출력 디렉토리를 정의한 경우, 다운스트림 워크플로우에서 입력 매개변수를 적절히 수정해야 합니다.
기본 출력 디렉토리는 ${launchDir}에 있는 `results/metagenome/BIN_ASSESSMENT`입니다.
```

```{code-block} bash
:caption: 출력 디렉토리 구조

${launchDir}/results/metagenome/BIN_ASSESSMENT/
├── prepared_bins_${run_id}/              # 준비되고 이름이 변경된 입력 빈
│   └── renamed_bins/
│       ├── ${sample_id}_bin.1.fa
│       ├── ${sample_id}_bin.2.fa
│       └── ...
├── checkm2_${run_id}/                    # CheckM2 품질 평가 결과
│   └── ${outputDirCheckM2}/
│       ├── quality_report.tsv            # 주요 품질 평가 보고서
│       ├── protein_files/                # 게놈에서 예측된 단백질
│       │   ├── ${genome_name}.faa
│       │   └── ...
│       └── ...
├── gunc_${run_id}/                       # GUNC 오염도 평가 결과
│   └── ${outputDirGUNC}/
│       ├── GUNC.progenomes_2.1.maxCSS_level.tsv  # 주요 오염도 보고서
│       └── ...
├── checkm_gunc_combined_${run_id}/       # 결합된 품질/오염도 결과
│   └── combined_report.tsv               # 결합된 CheckM2 및 GUNC 결과
├── bins_quality_passed/                  # 품질 필터링된 게놈 빈
│   ├── ${sample_id}_bin.1.fa             # 품질 필터를 통과한 빈만 포함
│   └── ...
├── gtdb_outdir_${run_id}/                # GTDB-Tk 분류학 분류 결과
│   ├── gtdbtk.bac120.summary.tsv         # 박테리아 게놈 분류
│   ├── gtdbtk.ar53.summary.tsv           # 고세균 게놈 분류
│   ├── quality_taxonomy_combined.csv     # 결합된 품질 및 분류학
│   └── ...
└── quality_taxonomy_combined_final.csv   # 다운스트림 분석을 위한 최종 보고서
```

또한, 메타데이터가 제공될 때:
```{code-block} bash
:caption: 메타데이터 관련 출력 파일(launchDir에 있음)

${launchDir}/
├── combined_metadata_quality_taxonomy_${run_id}.csv  # 결합된 메타데이터 및 품질/분류학
└── metadata_column_BIN_ASSESSMENT_summary.tsv        # 메타데이터 열 요약
```

## 모듈 실행

```{code-block} bash
# 기본 사용법
(metafun) metafun -module BIN_ASSESSMENT

# ASSEMBLY_BINNING에서 사용자 지정 출력 경로를 사용한 경우 입력 디렉토리 지정
(metafun) metafun -module BIN_ASSESSMENT -i /path/to/bins

# 품질/분류 결과와 결합할 메타데이터 파일 제공(권장)
(metafun) metafun -module BIN_ASSESSMENT -m your_metadata.csv -c 2

# 게놈 선택을 위한 품질 필터 지정
(metafun) metafun -module BIN_ASSESSMENT --pass_quality medium_quality.pass
```

:::{admonition} 품질 필터링 옵션
:class: note

품질 메트릭에 기반하여 게놈을 필터링하는 여러 옵션이 있습니다:

- 기본 품질 필터링을 위해 `medium_quality.pass` 사용:
```{code-block} bash
:caption: 중간 품질 필터 적용

(metafun) metafun -module BIN_ASSESSMENT --pass_quality medium_quality.pass
```

- 더 엄격한 품질 요구 사항을 위해 `high_quality.pass` 사용:
```{code-block} bash
:caption: 고품질 필터 적용

(metafun) metafun -module BIN_ASSESSMENT --pass_quality high_quality.pass
```

- 품질 및 GUNC 검사를 모두 통과하는 게놈 포함:
```{code-block} bash
:caption: 품질 및 GUNC 필터 적용

(metafun) metafun -module BIN_ASSESSMENT --pass_quality QS50_gunc.pass
```

- 사용 가능한 품질 필터 옵션:
  - `medium_quality.pass`: 완전성 ≥ 50%, 오염도 < 10%
  - `high_quality.pass`: 완전성 > 90%, 오염도 < 5%
  - `medium_quality_gunc.pass`: medium_quality + GUNC 통과
  - `high_quality_gunc.pass`: high_quality + GUNC 통과
  - `QS50.pass`: QS50 점수 ≥ 50
  - `QS50_gunc.pass`: QS50 통과 + GUNC 통과
  - `all`: 품질 필터링 없음(모든 게놈 포함)
::: 

## 실행 예제 및 결과

### metaFun 명령줄 실행 예제

```{figure} ../../images/BIN_ASSESSMENT_command.png
---
width: 100%
figclass: margin-caption
alt: metafun_pipeline
name: BIN_ASSESSMENT_command
align: middle
---
```

::::{admonition} 메타데이터와 품질/분류학 결과 결합하기
:class: note

결합된 메타데이터 파일(combined_metadata_quality_taxonomy_${run_id}.csv)은 <span style="color:#00B050">GENOME_</span><span style="color:#4E95D9">SELECTOR</span> 모듈의 다운스트림 분석에 필수적입니다. 이는 게놈 품질 및 분류학을 샘플 메타데이터와 연결합니다. 이 프로세스에서 선택된 빈은 <span style="color:#4E95D9">COMPARATIVE_ANNOTATION</span> 모듈에서 추가 분석에 사용됩니다.

메타데이터 파일을 효과적으로 사용하려면:

1. 먼저 메타데이터 열 요약을 확인하여 열 구조를 식별합니다:
```{code-block} bash
:caption: 메타데이터 열 요약 보기

cat yourmetadata.csv
```
메타데이터에 대한 접근 열을 식별해야 합니다


이것은 게놈 선택 및 추가 분석을 진행하기 전에 데이터 구조를 이해하는 데 도움이 됩니다.
::::

### 품질 평가 결과 예시

```{code-block} bash
:caption: CheckM2 품질 보고서 예시

$ head -n 5 ${launchDir}/results/metagenome/BIN_ASSESSMENT/checkm2_*/quality_report.tsv

Name    Completeness    Contamination    Completeness_Model_Used  Translation_Table_Used    Coding_Density    Contig_N50    Average_Gene_Length    Genome_Size    GC_Content    Total_Coding_Sequences    Total_Contigs    Max_Contig_Length    Additional_Notes
SRR6915091_bin.1    98.2    1.3    Neural Network (Specific Model)    11    0.877    278453    899.8    2758979    0.474    2698    823    32542    None
SRR6915091_bin.2    87.6    3.2    Neural Network (Specific Model)    11    0.863    129876    891.2    3104325    0.418    3077    945    28754    None
SRR6915091_bin.3    62.4    5.1    Gradient Boost (General Model)    11    0.901    87542    911.5    2198765    0.562    2154    752    18923    None
```

CheckM2 품질 보고서에는 다음과 같은 주요 열이 포함됩니다:
- **Name**: 게놈 빈 식별자
- **Completeness**: 추정된 게놈 완전성 백분율(0-100%)
- **Contamination**: 추정된 오염도 백분율(0-100%)
- **Completeness_Model_Used**: 완전성 추정에 사용된 모델(예: "Neural Network (Specific Model)", "Gradient Boost (General Model)")
- **Translation_Table_Used**: 번역에 사용된 유전 코드
- **Coding_Density**: 단백질을 코딩하는 게놈의 비율
- **Contig_N50**: 컨티그의 N50 값(이 크기 이상의 컨티그에 게놈의 50%가 포함된 길이)
- **Average_Gene_Length**: 예측된 유전자의 평균 길이
- **Genome_Size**: 염기쌍 단위의 게놈 총 크기
- **GC_Content**: 게놈의 GC 함량(0-1)
- **Total_Coding_Sequences**: 예측된 코딩 시퀀스 수
- **Total_Contigs**: 게놈 어셈블리의 컨티그 수
- **Max_Contig_Length**: 가장 큰 컨티그의 길이

### 분류학적 분류 결과 예시

```{code-block} bash
:caption: GTDB-Tk 분류학적 분류 예시

$ head -n 5 ${launchDir}/results/metagenome/BIN_ASSESSMENT/gtdb_outdir_*/gtdbtk.bac120.summary.tsv

| Genome                | Completeness | Contamination | medium_quality.pass | near_complete.pass | medium_quality_gunc.pass | near_complete_gunc.pass | QS50  | QS50.pass | pass.GUNC | QS50_gunc.pass | classification                                                                                                                                             | Analysis_accession | bioproject_accession | accession_used_in_analysis | country | continent | host_age | host_body_mass_index | host_sex | disease_group | AJCC_stage | age_group |
|-----------------------|--------------|---------------|---------------------|--------------------|--------------------------|-------------------------|-------|-----------|-----------|----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------|----------------------|----------------------------|---------|-----------|----------|----------------------|----------|---------------|------------|-----------|
| SRR6915091_MB2.14     | 91.77        | 0.55          | True                | True               | True                     | True                    | 89.02 | True      | True      | True           | d__Bacteria;p__Bacillota_C;c__Negativicutes;o__Acidaminococcales;f__Acidaminococcaceae;g__Acidaminococcus;s__Acidaminococcus intestini                      | SRR6915091         | PRJNA447983          | SRR6915091                 | Italy   | Europe    | 77.0     | 23.0                 | Male     | CRC           |            | Old       |
| SRR6915091_MB2.16     | 93.32        | 6.58          | True                | False              | False                    | False                   | 60.42 | True      | False     | False          | d__Bacteria;p__Bacteroidota;c__Bacteroidia;o__Bacteroidales;f__Bacteroidaceae;g__Phocaeicola;s__Phocaeicola dorei                                           | SRR6915091         | PRJNA447983          | SRR6915091                 | Italy   | Europe    | 77.0     | 23.0                 | Male     | CRC           |            | Old       |
| SRR6915091_MB2.17     | 70.82        | 2.2           | True                | False              | True                     | False                   | 59.82 | True      | True      | True           | d__Bacteria;p__Bacillota_A;c__Clostridia;o__Lachnospirales;f__Lachnospiraceae;g__Fusicatenibacter;s__Fusicatenibacter saccharivorans                        | SRR6915091         | PRJNA447983          | SRR6915091                 | Italy   | Europe    | 77.0     | 23.0                 | Male     | CRC           |            | Old       |
| SRR6915091_MB2.18_sub | 64.01        | 9.25          | True                | False              | False                    | False                   | 17.76 | True      | False     | False          | d__Bacteria;p__Bacillota_A;c__Clostridia;o__Oscillospirales;f__Oscillospiraceae;g__Flavonifractor;s__Flavonifractor plautii                                  | SRR6915091         | PRJNA447983          | SRR6915091                 | Italy   | Europe    | 77.0     | 23.0                 | Male     | CRC           |            | Old       |


```{code-block} bash
:caption: 결합된 품질 및 분류학 보고서 예시

$ head -n 5 ${launchDir}/results/metagenome/BIN_ASSESSMENT/quality_taxonomy_combined_final.csv

Genome,Completeness,Contamination,medium_quality.pass,high_quality.pass,medium_quality_gunc.pass,high_quality_gunc.pass,QS50,QS50.pass,pass.GUNC,QS50_gunc.pass,classification
SRR6915091_bin.1,98.2,1.3,True,True,True,True,89.02,True,True,True,d__Bacteria;p__Bacteroidota;c__Bacteroidia;o__Bacteroidales;f__Bacteroidaceae;g__Bacteroides;s__Bacteroides vulgatus
SRR6915091_bin.2,87.6,3.2,True,False,True,False,72.76,True,True,True,d__Bacteria;p__Firmicutes_A;c__Clostridia;o__Lachnospirales;f__Lachnospiraceae;g__Blautia;s__Blautia obeum
SRR6915091_bin.3,62.4,5.1,True,False,False,False,47.05,False,False,False,d__Bacteria;p__Firmicutes_A;c__Clostridia;o__Oscillospirales;f__Ruminococcaceae;g__Faecalibacterium;s__Faecalibacterium prausnitzii
```

## <span style="color:#00B050">BIN_ASSESSMENT</span> 모듈의 Nextflow 프로세스

| 프로세스 | InputDir | OutputDir | 참고 |
|---------|----------|-----------|------|
| prepareInputFiles | `${params.inputDir}` | `${params.outdir}/prepared_bins_${params.run_id}` | 입력 게놈 빈 준비 및 이름 변경 |
| runCheckM2 | prepareInputFiles의 출력 | `${params.outdir}/checkm2_${params.run_id}` | CheckM2 품질 평가 |
| runGUNC | runCheckM2의 출력 | `${params.outdir}/gunc_${params.run_id}` | GUNC 오염도 평가 |
| combineFiles | runCheckM2 및 runGUNC의 출력 | `${params.outdir}/checkm_gunc_combined_${params.run_id}` 및 `${params.outdir}/bins_quality_passed` | 결과 결합 및 게놈 필터링 |
| gtdbtk | combineFiles의 출력 | `${params.outdir}/gtdb_outdir_${params.run_id}` | GTDB-Tk 분류학적 분류 |
| createFinalFile | gtdbtk의 출력 | `${params.outdir}` | 최종 결합 보고서 생성 |
| combineMetadata | 최종 보고서 및 사용자 메타데이터 | `${launchDir}` | 선택 사항: 사용자 메타데이터와 결합 |
| create_metadata_summary | 결합된 메타데이터 파일 | `${launchDir}` | 메타데이터 열 요약 생성 |

## <span style="color:#00B050">BIN_ASSESSMENT</span> 워크플로우의 프로세스 설명

1. **prepareInputFiles**: 파일 확장자를 표준화하고 압축된 파일을 처리하여 입력 게놈 빈을 준비합니다.
   - 입력: 게놈 빈이 포함된 디렉토리
   - 출력: `.fa` 형식의 표준화된 게놈 빈이 있는 디렉토리

2. **runCheckM2**: 계통 특이적 마커 유전자를 기반으로 완전성과 오염도를 추정하는 CheckM2를 사용하여 게놈 품질을 평가합니다.
   - 입력: 표준화된 게놈 빈
   - 출력: CheckM2 품질 보고서 및 단백질 파일
   - 마커 유전자 식별을 위한 CheckM2 데이터베이스 사용

3. **runGUNC**: 게놈 일관성을 기반으로 오염을 감지하는 GUNC를 사용하여 게놈 오염도를 평가합니다.
   - 입력: CheckM2의 단백질 파일
   - 출력: GUNC 오염도 보고서
   - 참조 기반 오염 감지를 위한 GUNC 데이터베이스 사용

4. **combineFiles**: CheckM2 및 GUNC 결과를 결합하고, 품질 점수를 계산하며, 품질 임계값에 따라 게놈을 필터링합니다.
   - 입력: CheckM2 및 GUNC 보고서
   - 출력: 결합된 품질 보고서 및 필터링된 게놈 빈
   - 선택된 품질 매개변수에 기반한 품질 필터링 구현

5. **gtdbtk**: Genome Taxonomy Database를 기반으로 분류를 할당하는 GTDB-Tk를 사용하여 품질 필터링된 게놈의 분류학적 분류를 수행합니다.
   - 입력: 품질 필터링된 게놈 빈
   - 출력: 박테리아 및 고세균 게놈에 대한 GTDB-Tk 분류 결과
   - 분류를 위한 GTDB-r220 데이터베이스 활용

6. **createFinalFile**: 품질 평가 및 분류학적 분류를 결합한 포괄적인 최종 보고서를 생성합니다.
   - 입력: 결합된 품질 보고서 및 GTDB-Tk 결과
   - 출력: 품질 메트릭 및 분류가 포함된 최종 보고서
   - 가능한 경우 이전 실행 결과 병합

7. **combineMetadata**: (선택 사항) 최종 품질/분류학 보고서를 사용자 제공 메타데이터와 결합합니다.
   - 입력: 최종 보고서 및 사용자 메타데이터 파일
   - 출력: 품질, 분류학 및 샘플 정보가 포함된 결합된 메타데이터 파일
   - 다운스트림 분석을 위해 게놈 정보를 샘플 메타데이터와 연결

8. **create_metadata_summary**: 후속 분석을 지원하기 위한 메타데이터 열 요약을 생성합니다.
   - 입력: 결합된 메타데이터 파일
   - 출력: 인덱스와 이름이 있는 메타데이터 열 요약
   - 다운스트림 분석을 위한 관련 열 식별 지원

## <span style="color:#00B050">BIN_ASSESSMENT</span>에서 사용되는 도구

| 도구 | 목적 | 버전 | 데이터베이스 | 데이터베이스 버전 | 기본 매개변수 | 선택할 수 있는 매개변수 |
|------|---------|------------|------------|------------------|---------------------|--------------------------------|
| CheckM2 | 게놈 품질 평가 | 1.0.2 | CheckM2 Database | 1.0.2 | `--threads ${task.cpus} --output-directory ${params.outputDirCheckM2} -x fa` | 출력 디렉토리 이름 |
| GUNC | 게놈 오염도 평가 | 1.0.6 | GUNC Database | progenomes2.1 | `-g -t ${task.cpus} -o ${params.outputDirGUNC} -e .faa` | 출력 디렉토리 이름 |
| GTDB-Tk | 게놈 분류학 분류 | 2.4.0 | GTDB | r220 | `--mash_db mash_220.db.msh --cpus ${task.cpus} --pplacer_cpus ${task.cpus}` | 이 워크플로우에 특정한 것 없음 |

## <span style="color:#00B050">BIN_ASSESSMENT</span>의 사용자 정의 스크립트

| 스크립트 | 목적 | 입력 | 출력 | 참고 |
|--------|---------|-------|--------|------|
| Checkm2_GUNC_combine_quality_pass.py | CheckM2 및 GUNC 결과 결합 | CheckM2 및 GUNC 보고서 | 결합된 품질 보고서 | 품질 점수 및 플래그 계산 |
| GTDB_add2_check2gunc.py | 품질 및 분류학 데이터 결합 | 품질 보고서 및 GTDB-Tk 결과 | 결합된 품질/분류학 보고서 | 포괄적인 게놈 보고서 생성 |
| combine_metadata_WMS_genome.py | 게놈 데이터를 샘플 메타데이터와 결합 | 게놈 보고서 및 사용자 메타데이터 | 결합된 메타데이터 파일 | 게놈 데이터를 샘플 컨텍스트와 연결 |

## 사용 참고 사항

- **<span style="color:#00B050">BIN_ASSESSMENT</span>** 워크플로우는 <span style="color:#FF9300">ASSEMBLY_BINNING</span> 워크플로우의 출력과 함께 작동하도록 설계되었습니다.
- **<span style="color:#4E95D9">COMPARATIVE_ANNOTATION</span>** 모듈의 다운스트림 분석을 위해 `--metadata` 옵션을 사용하여 메타데이터 제공을 강력히 권장합니다.
- 기본 품질 필터(`QS50.pass`)는 QS50 품질 점수 ≥ 50인 게놈을 선택하지만, 연구 필요에 따라 다른 필터를 선택할 수 있습니다.
- 스크립트는 진행하기 전에 입력 디렉토리의 존재 및 비어 있지 않은지 확인합니다.
- 여러 샘플의 병렬 처리를 위해 다른 `--run_id` 값으로 워크플로우를 실행할 수 있습니다.
- 최종 품질/분류학 보고서 및 선택적 결합 메타데이터 파일은 **<span style="color:#4E95D9">COMPARATIVE_ANNOTATION</span>** 모듈의 주요 입력입니다.

## 다음 단계

이 모듈로 게놈 품질 및 분류학을 평가한 후, **<span style="color:#00B050">GENOME_</span><span style="color:#4E95D9">SELECTOR</span>**로 진행하여 관심 있는 게놈을 선택합니다. 그런 다음 **<span style="color:#4E95D9">COMPARATIVE_ANNOTATION</span>**에서 결과 csv 파일을 사용하여:
- 유전자 예측 및 주석 수행
- 비교 유전체 분석 수행
- 기능적 프로필 생성
- 다양한 샘플이나 조건에 걸쳐 게놈 비교

(BIN_ASSESSMENT_combine_metadata)=

## 메타데이터와 품질/분류학 결과 결합하기

:::{admonition} 샘플 메타데이터와 게놈 정보 결합하기
:class: note, dropdown

메타데이터는 CSV 형식의 페어드 엔드 리드 메타게놈 파일의 공통 기본 이름을 포함해야 합니다. 
예를 들어, 페어드 엔드 메타게놈 fastq 파일 쌍의 기본 이름은 다음과 같습니다:  
`SRR6915091_1.fastq`, `SRR6915091_2fastq` --> **basename**: `SRR6915091`

### 메타게놈의 메타데이터

**메타데이터 csv 파일의 예시 테이블 내용:**
- 자신만의 csv 형식의 메타데이터 파일을 준비해야 합니다. 
- 참고용으로 생물정보 프로젝트 [PRJNA447983](https://www.nature.com/articles/s41591-019-0405-7)의 메타데이터를 csv 형식으로 다운로드하세요.  
{download}`CRC_Control113_PRJNA447983_metadata.csv </_static/CRC_Control113_PRJNA447983_metadata.txt>`

| bioproject_accession | accession_used_in_analysis | country | continent | host_age | host_body_mass_index | host_sex | disease_group | AJCC_stage | age_group |
|:---------------------|:---------------------------|:--------|:----------|:---------|:---------------------|:---------|:--------------|:-----------|:----------|
| PRJNA447983          | SRR6915092                 | Italy   | Europe    | 60       | 20                   | Female   | Control       | Control    | Old       |
| PRJNA447983          | SRR6915097                 | Italy   | Europe    | 80       | 32                   | Female   | Control       | Control    | Old       |
| PRJNA447983          | SRR6915108                 | Italy   | Europe    | 67       | 20.43816558          | Female   | Control       | Control    | Old       |
| PRJNA447983          | SRR6915113                 | Italy   | Europe    | 77       | NA                   | Female   | Control       | Control    | Old       |

이 테이블에서 두 번째 열 `accession_used_in_analysis`는 생성된 MAG의 기본 이름입니다.

### MAG의 메타데이터

- `BIN_ASSESSMENT` 모듈을 성공적으로 실행하면 게놈 품질, 분류학 및 상세 메트릭 정보가 포함된 `quality_taxonomy_combined_final.csv` 파일이 생성됩니다:

```
Genome,Completeness,Contamination,medium_quality.pass,high_quality.pass,medium_quality_gunc.pass,high_quality_gunc.pass,QS50,QS50.pass,pass.GUNC,QS50_gunc.pass,Completeness_Model_Used,Translation_Table_Used,Coding_Density,Contig_N50,Average_Gene_Length,Genome_Size,GC_Content,Total_Coding_Sequences,Total_Contigs,Max_Contig_Length,classification
ERR1018185qced_headed_MB2.1,62.18,0.38,True,False,True,False,60.28,True,True,True,Neural Network (Specific Model),11,0.886,3309,254.5395019981556,2799002,0.51,3253,900,18216,d__Bacteria;p__Pseudomonadota;c__Gammaproteobacteria;o__Enterobacterales;f__Enterobacteriaceae;g__Escherichia;s__Escherichia coli
```

### 결합된 메타데이터 파일

- `--metadata` 옵션을 `--accession_column`과 함께 사용할 때, `combined_metadata_quality_taxonomy_${run_id}.csv` 파일이 생성됩니다:

| Genome                | Completeness | Contamination | medium_quality.pass | high_quality.pass | classification | bioproject_accession | accession_used_in_analysis | country | host_age | disease_group |
|-----------------------|--------------|---------------|---------------------|-------------------|----------------|----------------------|----------------------------|---------|----------|---------------|
| SRR6915091_bin.1     | 91.77        | 0.55          | True                | True              | d__Bacteria;p__Bacillota_C;c__Negativicutes;o__Acidaminococcales;f__Acidaminococcaceae;g__Acidaminococcus;s__Acidaminococcus intestini | PRJNA447983 | SRR6915091 | Italy | 77 | CRC |
| SRR6915091_bin.2     | 93.32        | 6.58          | True                | False             | d__Bacteria;p__Bacteroidota;c__Bacteroidia;o__Bacteroidales;f__Bacteroidaceae;g__Phocaeicola;s__Phocaeicola dorei | PRJNA447983 | SRR6915091 | Italy | 77 | CRC |

이 결합된 파일은 게놈 품질 및 분류학을 샘플 메타데이터와 연결하여 <span style="color:#7FBDFF">COMPARATIVE_ANNOTATION</span> 모듈의 다운스트림 분석을 위한 가치 있는 컨텍스트를 제공합니다.

이 결합된 파일을 생성하려면 다음을 사용하세요:
```{code-block} bash
(metafun) metafun -module BIN_ASSESSMENT -m your_metadata.csv -c 2
```

여기서 `2`는 게놈 빈 이름과 일치하는 샘플 식별자가 포함된 메타데이터의 열 인덱스를 나타냅니다.

출력 파일의 이름은 타임스탬프와 워크플로우 식별자(예: `combined_metadata_quality_taxonomy_20250306135829_2996.csv`)로 지정됩니다. 여기서:
- `20250306135829`는 yyyyMMddHHmmss 형식의 타임스탬프입니다
- `2996`은 고유한 워크플로우 식별자입니다
:::

<span style="color:#00B050">BIN_ASSESSMENT</span>는 게놈 복구와 기능 분석 사이의 간극을 연결하는 중요한 단계로, 다운스트림 비교 연구에 고품질 게놈만 사용되도록 보장합니다.
