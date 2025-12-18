# 빠른 시작 
## metaFun 설치 및 실행
###  1. biocontainer 설치 

시스템에 conda나 mamba가 설치되어 있지 않다면, 안내에 따라 conda나 mamba를 설치하세요. [miniconda](https://docs.anaconda.com/miniconda/miniconda-install/) 또는 [mamba](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html)를 설치하는 것을 권장합니다.

```{code-block} bash
:caption: miniconda 설치
# Linux OS를 사용한다고 가정합니다.
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
# -p $PATH를 대체하여 설치 경로를 지정할 수 있습니다. $PATH는 conda 설치의 기본 디렉토리입니다.
bash miniconda.sh -b -u -p ~/miniconda3
rm  miniconda.sh
```
```{admonition} mamba 설치
빠른 설치를 위해 [miniforge github](https://github.com/conda-forge/miniforge)의 지침에 따라 적합한 mamba를 설치하는 것을 권장합니다. 
```
### 2. Bioconda에서 metaFun 다운로드
```{code-block} bash
# metaFun을 위한 새로운 conda 환경 생성을 권장합니다
conda create -n metafun bioconda::metafun
# mamba가 있다면, mamba로 metaFun을 설치할 수 있습니다
mamba create -n metafun bioconda::metafun

mamba activate metafun
```

### 3. metaFun 활용을 위한 데이터베이스 다운로드
```{code-block} bash
# 데이터베이스 다운로드
conda activate metafun
 (metafun) name $ metafun  -module DOWNLOAD_DB 
```

````{admonition} module DOWNLOAD_DB 실행
:class: note
`metafun -module DOWNLOAD_DB` 실행은 다음 그림과 같습니다. 
```{figure} ../images/DownloadDB_execution_metafun_v011.png
---
width: 100%
figclass: margin-caption
alt: metafun_pipeline
name: download_db_metafun
align: middle
---
```
````

````{admonition} module DOWNLOAD_DB 실행
:class: note
데이터베이스의 크기가 매우 크기 때문에(원시 tar gzip 파일 크기: ~683GB), 네트워크 속도에 따라 다운로드하는 데 시간이 걸릴 수 있습니다.
데이터베이스 정보는 [다운로드 저장소](https://www.microbiome.re.kr/home_design/list_files.php?path=metafun%2Fv0.1%2FmetaFun_db_distribute)에서 확인할 수 있습니다. 

다운로드된 데이터베이스의 무결성은 sha256을 비교하여 자동으로 확인됩니다. 문제가 있다면 데이터베이스를 다시 다운로드해 주세요. 

일반적으로 다음 명령어로 데이터베이스 경로를 찾을 수 있습니다.
```{code-block} bash
ls -d $(find $(dirname $(which metafun)) -type d ! -name 'metafun')/../share/metafun/db
```
````

### 4. metaFun의 모듈 실행  

metaFun은 두 가지 주요 분석 워크플로우를 제공합니다:

#### 게놈 기반 분석 경로:
<span style="color:#FF0000">RAWREAD_QC</span> → <span style="color:#FF9300">ASSEMBLY_BINNING</span> → <span style="color:#00B050">BIN_ASSESSMENT</span> → <span style="color:#00B050">GENOME_</span><span style="color:#4E95D9">SELECTOR</span> → <span style="color:#4E95D9">COMPARATIVE_ANNOTATION</span> → <span style="color:#4E95D9">INTERACTIVE_COMPARATIVE</span>

#### 리드 기반 분석 경로:
  분류학적 구성을 위한 경로

<span style="color:#FF0000">RAWREAD_QC</span> → <span style="color:#0846FA">WMS_TAXONOMY</span> → <span style="color:#0846FA">INTERACTIVE_TAXONOMY</span>

기능 주석을 위한 경로

<span style="color:#FF0000">RAWREAD_QC</span> → <span style="color:#7030A0">WMS_FUNCTION</span>

균주 수준 분석을 위한 경로

<span style="color:#FF0000">RAWREAD_QC</span> → <span style="color:#0846FA">WMS_TAXONOMY</span> → <span style="color:#2FA4E7">WMS_STRAIN</span> → <span style="color:#2FA4E7">INTERACTIVE_STRAIN</span>

네트워크 분석을 위한 경로

<span style="color:#0846FA">WMS_TAXONOMY</span> → <span style="color:#2FA4E7">INTERACTIVE_NETWORK</span>

다음 구문을 사용하여 metaFun의 각 모듈을 실행할 수 있습니다:


```{code-block} bash
metafun -module <module_name> [options]
```

#### 사용 가능한 모듈

```{admonition} 중요 워크플로우 정보
:class: warning

- <span style="color:#FF0000">RAWREAD_QC</span>에 대한 입력 디렉토리를 지정할 때, 명시적으로 재정의하지 않는 한 후속 모듈은 자동으로 이전 단계의 출력을 입력으로 사용합니다.
- 필수 매개변수는 일반적으로 메타데이터 파일과 해당 열(샘플 ID 또는 분석 열)을 지정할 때 필요합니다. 메타데이터가 필요한 각 모듈은 이러한 매개변수를 명시적으로 정의해야 합니다.
- 가장 효율적인 사용을 위해 위에 표시된 색상 코드가 지정된 워크플로우 경로를 따르세요.
```

## <span style="color:#FF0000">RAWREAD_QC</span>: 원시 리드의 품질 제어 및 숙주 게놈 필터링

**필수:** -i <inputDir> (입력 리드 디렉토리)

```{code-block} bash
:caption: 예시
metafun -module RAWREAD_QC -i input_reads/
```

## <span style="color:#FF9300">ASSEMBLY_BINNING</span>: 어셈블리 및 빈닝
**선택 사항:** -i <inputDir> (필터링된 리드 디렉토리)
(출력 매개변수 없이 RAWREAD_QC를 실행한 경우, 이 모듈에서 `-i` 매개변수 없이 실행할 수 있습니다.)

```{code-block} bash
:caption: 예시
metafun -module ASSEMBLY_BINNING -i filtered_reads/ -p 40
```

## <span style="color:#00B050">BIN_ASSESSMENT</span>: 게놈 품질 평가 및 분류학적 분류

**필수:** -m <metadata> -c <accession_column>

```{code-block} bash
:caption: 예시
metafun -module BIN_ASSESSMENT -m metadata.txt -c 2
```

## <span style="color:#00B050">GENOME_</span><span style="color:#4E95D9">SELECTOR</span>: 게놈 선택 인터페이스

**필수:** -i <input_file>

```{code-block} bash
:caption: 예시
metafun -module GENOME_SELECTOR -i combined_metadata.csv
```

## <span style="color:#4E95D9">COMPARATIVE_ANNOTATION</span>: 비교 게놈 분석

**필수:** -i <inputDir> -m <metadata>

```{code-block} bash
:caption: 예시 (INTERACTIVE_COMPARATIVE 모듈을 위한 주석만)
metafun -module COMPARATIVE_ANNOTATION  --metadata metadata.csv --samplecol 1
```


```{code-block} bash
:caption: 예시 (정적 그래프 포함) 이 방법은 더 이상 사용되지 않습니다.
metafun -module COMPARATIVE_ANNOTATION -i genomes/ -m metadata.csv --samplecol 1 --metacol 2
```

## <span style="color:#4E95D9">INTERACTIVE_COMPARATIVE</span>: 대화형 비교 분석

**필수:** -i <inputDir> -m <metadata>

```{code-block} bash
:caption: 예시
metafun -module INTERACTIVE_COMPARATIVE -i results/genomes -m metadata.csv
```

## <span style="color:#0846FA">WMS_TAXONOMY</span>: 메타게놈 리드의 분류학적 프로파일링

**필수:** -m <metadata> -s <sampleIDcolumn> 
```{admonition} 기본 선택은 sylph입니다.
:class: note

kraken2를 사용하려면 kraken2 데이터베이스를 다운로드하고 `--profiler kraken2`를 지정하세요. 

`-s` 옵션은 메타게놈 데이터의 쌍을 이루는 리드 파일의 접근 열 접두사입니다.

`-i` 옵션은 메타게놈 데이터의 입력 디렉토리입니다. <span style="color:#FF0000">RAWREAD_QC</span> 모듈을 실행하지 않았다면 이 옵션을 지정해야 합니다.
```

```{code-block} bash
:caption: 예시
metafun -module WMS_TAXONOMY  -m meta.csv -s 1 
```

## <span style="color:#0846FA">INTERACTIVE_TAXONOMY</span>: 대화형 분류학 분석

**필수:** -i <inputDir>

```{code-block} bash
:caption: 예시
metafun -module INTERACTIVE_TAXONOMY -i results/metagenome/WMS_TAXONOMY
```

## <span style="color:#7030A0">WMS_FUNCTION</span>: 메타게놈 리드의 기능 분석

**필수:** -i <inputDir> -m <metadata> -s <sampleIDcolumn> -a <analysiscolumn>

```{code-block} bash
:caption: 예시
metafun -module WMS_FUNCTION -i filtered_reads/ -m metadata.csv -s 1 -a 2
```

## <span style="color:#2FA4E7">WMS_STRAIN</span>: 균주 수준 미세다양성 분석

**필수:** -i <inputDir> --phyloseq_object <phyloseq_RDS>

```{admonition} WMS_TAXONOMY 출력 필요
:class: note

이 모듈은 균주 수준에서 분석할 우세 분류군을 선택하기 위해 WMS_TAXONOMY의 phyloseq RDS 객체가 필요합니다.
```

```{code-block} bash
:caption: 예시
metafun -module WMS_STRAIN -i results/metagenome/RAWREAD_QC/read_filtered \
    --phyloseq_object results/metagenome/WMS_TAXONOMY/phyloseq/phyloseq_object_sylph.RDS
```

## <span style="color:#2FA4E7">INTERACTIVE_STRAIN</span>: 대화형 균주 다양성 분석

**필수:** -i <inputDir>

```{code-block} bash
:caption: 예시
metafun -module INTERACTIVE_STRAIN -i results/metagenome/WMS_STRAIN
```

## <span style="color:#2FA4E7">INTERACTIVE_NETWORK</span>: 대화형 미생물 네트워크 분석

**필수:** -i <phyloseq_RDS>

```{admonition} WMS_TAXONOMY 출력 필요
:class: note

이 모듈은 공존 네트워크 구축을 위해 WMS_TAXONOMY의 phyloseq RDS 객체가 필요합니다.
```

```{code-block} bash
:caption: 예시
metafun -module INTERACTIVE_NETWORK -i results/metagenome/WMS_TAXONOMY/phyloseq/phyloseq_object_sylph.RDS
```

## DOWNLOAD_DB: 필요한 데이터베이스 다운로드

```{code-block} bash
:caption: 예시
metafun -module DOWNLOAD_DB
```

## PREPARE_CUSTOM_HOST: 사용자 정의 숙주 게놈 인덱스 준비

**필수:** -i <file> -f <n>

```{code-block} bash
:caption: 예시
metafun -module PREPARE_CUSTOM_HOST -i genome.fasta -f mouse
```
```{admonition} 모든 사용자 정의 숙주 게놈을 사용할 수 있습니다.
:class: note

사용자 정의 숙주 게놈을 사용하려면 fasta 파일의 경로와 `-f`로 숙주 게놈의 이름을 지정하세요.

사용자 정의 숙주 게놈을 필터링하기 위해 <span style="color:#FF0000">RAWREAD_QC</span> 모듈에서 `-f` 옵션을 지정해야 합니다.
```


## 공통 옵션

- `-o, --output`: 출력 디렉토리
- `-p, --processors`: 사용할 프로세서 수
- `-h, --help`: 모듈에 대한 자세한 도움말 표시

각 모듈의 자세한 사용법 및 추가 매개변수는 다음을 사용하세요:
```{code-block} bash
metafun -module <module_name> -h
```
