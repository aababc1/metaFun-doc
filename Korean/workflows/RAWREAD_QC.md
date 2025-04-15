(RAWREAD_QC_description)=

# <span style="color:#FF0000">RAWREAD_QC</span>

<img src="../../_static/metafun1_red.png" style="height:200px; width:auto; float:right; margin-left:10px;" />
이 모듈은 전체 메타게놈 시퀀싱 데이터의 원본 리드 품질 제어를 위해 설계된 metaFun 파이프라인의 일부입니다.

## 개요
RAWREAD_QC 모듈은 metaFun 파이프라인의 첫 번째 단계로, 원본 메타게놈 시퀀싱 데이터의 품질 제어를 위해 설계되었습니다. 이 모듈은 품질 평가, 트리밍, 그리고 호스트 리드 필터링을 수행하여 다운스트림 분석을 위한 고품질 리드를 준비합니다. 모든 호스트 리드는 metaFun을 사용하여 인덱싱되고 활용될 수 있으며, 호스트 리드 필터링 과정을 건너뛸 수도 있습니다.

## 모듈 실행

```{code-block} bash
# 기본 사용법
(metafun) metafun -module RAWREAD_QC -i /path/to/raw_reads

# 호스트 필터링 건너뛰기
(metafun) metafun -module RAWREAD_QC -i /path/to/raw_reads --filter none

# 필터링을 위한 사용자 정의 호스트 게놈 사용 (먼저 게놈 준비).
# 게놈을 인덱싱하고 RAWREAD_QC 모듈을 실행합니다.
(metafun) metafun -module PREPARE_CUSTOM_HOST -i yourgenome.fasta -f custom_genome_name
(metafun) metafun -module RAWREAD_QC -i /path/to/raw_reads --filter custom_genome_name
```

:::{admonition} 호스트 리드 필터링 옵션
:class: note

리드를 필터링하는 세 가지 옵션이 있습니다: `human`, `Skip filtering out`, `your custom genome`.
- 기본값은 human genome으로 설정되어 있습니다. 데이터셋이 인간 게놈에서 온 경우, 필터를 지정할 필요가 없습니다.
- 호스트 리드 필터링을 건너뛰려면, `-f none` 또는 `--filter none`을 지정하세요.
```{code-block} bash
:caption: 호스트 리드 필터링 단계와 후속 FastQC 단계를 건너뜁니다.

# 관심 있는 게놈을 사용하여 리드 필터링을 건너뛰려면 이 방법을 사용하세요.
 (metafun) metafun -module RAWREAD_QC -i ${inputDir} -f none
 ```

- 필터링을 위해 자신의 게놈을 사용하려면, 먼저 인덱싱하고 그것을 지정하세요.
```{code-block} bash
:caption: 필터링을 위해 사용자 정의 게놈 사용.

# 특정 이름으로 게놈을 인덱싱합니다. 어떤 이름이든 `-f`와 함께 사용할 수 있지만, RAWREAD_QC 모듈에서 이 단어를 사용해야 합니다.
(metafun) metafun -module PREPARE_CUSTOM_HOST -i yourgenome.fasta -f anyname
# 게놈(mygenome) 인덱싱에 사용한 필터 이름을 `mygenome`으로 지정합니다.
(metafun) metafun -module RAWREAD_QC -i ${inputDir} -f anyname
:::

## 모듈 작동 순서
이 모듈은 다음 단계를 수행합니다:

1. 원본 리드에 대한 FastQC 분석
2. fastp를 사용한 트리밍 및 품질 필터링
3. Bowtie2를 사용한 호스트(예: 인간) 리드 제거(선택 사항)
4. 필터링된 리드에 대한 FastQC 분석
5. MultiQC 보고서 생성

## 매개변수
**`${launchDir}`은 metaFun을 실행하는 디렉토리로, 출력 기본 디렉토리로 활용됩니다.**

| 매개변수 | 설명 | 기본값 | 참고 |
|-----------|-------------|---------------|------|
| `-i, --inputDir` | 원본 리드가 포함된 입력 디렉토리 | **원본 리드가 포함된 디렉토리 경로를 설정해야 합니다.** | **필수** |
| `-o, --outdir` | 출력 디렉토리 | `${launchDir}/results/metagenome/RAWREAD_QC` | 다운스트림 분석을 위해 기본 출력 디렉토리가 권장됩니다. |
| `-f, --filter` | 호스트 게놈 필터링 옵션 | `human` | 옵션: `human`, `none`, 또는 사용자 정의 이름 |
| `-p, --processors` | 사용할 CPU 수 | `4` | |

## **입력 및 출력**

### 입력
* 원본 페어드 엔드 메타게놈 리드(FASTQ 형식, gzip 압축 가능)
* `-i ${inputDir}`로 입력 리드 디렉토리 지정
* 파일 이름 규칙: `*_1.fastq.gz`/`*_2.fastq.gz` 또는 `*_1.fq.gz`/`*_2.fq.gz` 또는 gzip 압축 확장자 없이.

(RAWREAD_QC_output)=

### 출력
* 품질 제어 및 필터링된 메타게놈 리드
* 품질 평가 보고서 및 시각화

### 출력 디렉토리 구조

출력 디렉토리는 ${launchDir} 또는 `-o outdir`로 지정한 디렉토리 경로에 있습니다.

우리는 권장대로 출력 디렉토리를 지정하지 않았다고 가정합니다.

**`${launchDir}`은 metaFun을 실행하는 디렉토리로, 출력 기본 디렉토리로 활용됩니다.**

```{admonition} 입력 및 출력 디렉토리 전환
:class: note

`-o ${output directory}`를 지정하여 출력 디렉토리를 정의한 경우, 다른 모듈에서도 이러한 매개변수를 수정해야 합니다.
기본 출력 디렉토리는 ${launchDir}에 있는 `results/metagenome/RAWREAD_QC.`입니다.
```

```{code-block} bash
:caption: 출력 디렉토리 구조
 # 입력 샘플은 ${inputDir}에 있으며, 입력 fastq 파일 이름은 ${sample_id}_{1,2}.fastq.gz 또는 ${sample_id}_{1,2}.fq.gz 또는 gzip 압축 확장자 없이 될 수 있습니다.

${launchDir}/results/metagenome/RAWREAD_QC/
├── fastqc_raw/                      # 원본 리드에 대한 FastQC 결과
│   ├── ${sample_id}_1_fastqc.html
│   ├── ${sample_id}_1_fastqc.zip 
│   ├── ${sample_id}_2_fastqc.html
│   ├── ${sample_id}_2_fastqc.zip
│   ├── ...
├── read_filtered/                   # 호스트 필터링된 리드
│   ├── ${sample_id}_fastp_hg38_1.fastq.gz
│   └── ${sample_id}_fastp_hg38_2.fastq.gz
├── fastqc_filtered/                 # 필터링된 리드에 대한 FastQC 결과
│   ├── ${sample_id}_fastp_hg38_fastqc_filtered/
│   │   ├── ${sample_id}_fastp_hg38_1_fastqc.html
│   │   ├── ${sample_id}_fastp_hg38_1_fastqc.zip
│   │   ├── ${sample_id}_fastp_hg38_2_fastqc.html
│   │   ├── ${sample_id}_fastp_hg38_2_fastqc.zip
│   ├── ...
└── multiqc/                         # MultiQC 보고서
    ├── multiqc_report.html
    └── multiqc_data/
        └── ...
```

## 실행 예제 및 결과

### metaFun 명령줄 실행 예제

```{figure} ../../images/RAWREAD_QC_command.png
---
width: 100%
figclass: margin-caption
alt: metafun_pipeline
name: RAWREAD_QC_command
align: middle
---
```

### MultiQC 보고서 예제

MultiQC 보고서는 모든 샘플에 걸쳐 원본 리드 및 필터링된 리드 품질 통계를 통합합니다.

```{figure} ../../images/multiqc.png
---
width: 100%
figclass: margin-caption
alt: metafun_pipeline
name: multiqc
align: middle
---
```

[HTML multiQC 보고서 예제!](/_static/multiqc_report.html)

## <span style="color:#FF0000">RAWREAD_QC</span> 모듈의 Nextflow 프로세스

| 프로세스 | InputDir | OutputDir | 참고 |
|---------|----------|-----------|------|
| fastqc_raw | `${params.inputDir}` | `${params.outdir}/fastqc_raw`  | 원본 리드에 대한 FastQC 분석 결과 |
| fastp | `${params.inputDir}` | None | 트리밍 및 품질 필터링 수행 |
| humanread_filter | fastp의 출력 | `${params.outdir}/read_filtered` | 호스트 리드 제거(params.filter가 'none'이 아닐 때) |
| fastqc_filtered | humanread_filter의 출력 | `${params.outdir}/fastqc_filtered` | 필터링된 리드에 대한 FastQC 분석 결과 |
| multiQC | 모든 이전 프로세스의 결과 | `${params.outdir}/multiqc` | 모든 QC 결과의 종합 보고서 |

## <span style="color:#FF0000">RAWREAD_QC</span> 모듈의 프로세스 설명

1. **원본 리드에 대한 FastQC**: `--inputDir ${your input directory}`로 지정된 원본 입력 메타게놈 리드에 대해 FastQC 분석을 수행합니다.
2. **fastp 처리**: fastp를 사용하여 메타게놈 리드를 트리밍하고 필터링합니다.
3. **호스트 리드 필터링**(선택 사항): Bowtie2를 사용하여 호스트 리드를 제거합니다. 기본 입력 게놈은 GRCh38_p12.dna.primary_assembly입니다(`-f human`). **호스트 리드를 필터링하지 않으려면**, 명령줄에서 `-f none`을 지정하세요. 그렇지 않고 **관심 있는 자신의 게놈을 필터링하려면**, `(metafun) metafun -module PREPARE_CUSTOM_HOST -i $yourgenome -f${value}`로 게놈을 인덱싱할 수 있습니다.
4. **필터링된 리드에 대한 FastQC**: 필터링된 리드에 대해 FastQC 분석을 수행합니다.
5. **MultiQC 보고서**: 모든 QC 결과를 결합한 MultiQC 보고서를 생성합니다.

## <span style="color:#FF0000">RAWREAD_QC</span>에서 사용되는 도구

| 도구 | 목적 | 버전 | 기본 매개변수 | 선택할 수 있는 매개변수 |
|------|---------|------------|------------|------------|
| FastQC | 원본 시퀀스 데이터에 대한 품질 제어 검사 |  v0.12.1 | 기본값 | `--cpus ${number}`로만 CPU 선택 가능 |
| fastp | 원본 메타게놈 리드의 트리밍 및 필터링 |  0.23.4 | 기본값 | `--cpus ${number}`로만 CPU 선택 가능 |
| Bowtie2 | 호스트 오염을 제거하기 위한 리드 정렬 | 2.5.2 | `--very-sensitive`: 감도 프리셋, `--un-conc-gz`: gzip 압축된 메타게놈 리드, 호스트 게놈에 비정렬, `end-to-end` | null |
| MultiQC | 생물정보학 분석 결과 집계 | v1.18 | 이 스크립트에 특정 매개변수 없음 | null |

## 사용 참고 사항

- `metafun -module PREPARE_CUSTOM_HOST -i yourgenome.fasta -f name`을 사용하여 `-f name`을 지정하여 사용자 정의 인덱스를 생성할 수 있습니다.
- 스크립트는 진행하기 전에 입력 디렉토리의 존재 및 비어 있지 않은지 확인합니다.
- 이 모듈의 결과는 **[<span style="color:#FF9300">ASSEMBLY_BINNING</span>](ASSEMBLY_BINNING_description)**, **[<span style="color:#0846FA">WMS_TAXONOMY</span>](WMS_TAXONOMY_description)** 및 **[<span style="color:#7030A0">WMS_FUNCTION</span>](WMS_FUNCTION_description)**의 입력 데이터로 사용됩니다.
이 모듈의 결과는 Bracken과 함께 Kraken2를 위한 <span style="color:#0846FA">WMS_TAXONOMY</span>에 **필수 입력**입니다. 