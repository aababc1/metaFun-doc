# metaFun 워크플로우

metaFun은 다양한 분석 모듈로 구성된 메타게놈 분석 파이프라인입니다. 각 모듈은 특정 분석 기능을 수행하며, 서로 연결되어 전체 분석 파이프라인을 형성합니다.

## 분석 모듈 개요

### 1. <span style="color:#FF0000">RAWREAD_QC</span>
- **기능**: 원시 시퀀싱 데이터의 품질 제어 및 호스트 리드 필터링
- **주요 도구**: FastQC, fastp, Bowtie2, MultiQC
- **KBDS 지원**: ✅ 지원됨

### 2. <span style="color:#FF9300">ASSEMBLY_BINNING</span>
- **기능**: 메타게놈 어셈블리 및 메타게놈 어셈블 게놈(MAG) 생성
- **주요 도구**: MEGAHIT, MetaBAT2, SemiBin2, DAS Tool
- **KBDS 지원**: ✅ 지원됨

### 3. <span style="color:#00B050">BIN_ASSESSMENT</span>
- **기능**: 메타게놈 어셈블 게놈의 품질 평가 및 분류
- **주요 도구**: CheckM2, GTDB-Tk, GUNC
- **KBDS 지원**: ✅ 지원됨

### 4. <span style="color:#00B050">GENOME_</span><span style="color:#4E95D9">SELECTOR</span>
- **기능**: 품질 기준에 따른 게놈 선택 및 필터링
- **주요 도구**: R 기반 분석 도구
- **KBDS 지원**: ❌ 지원되지 않음 (로컬 환경에서 사용 권장)

### 5. <span style="color:#4E95D9">COMPARATIVE_ANNOTATION</span>
- **기능**: 게놈 주석 및 비교 분석
- **주요 도구**: Prokka, PPanGGOLiN, KofamScan, VFDB, CARD, dbCAN, skani
- **KBDS 지원**: ✅ 지원됨

### 6. <span style="color:#4E95D9">INTERACTIVE_COMPARATIVE</span>
- **기능**: 비교 게놈 분석 결과의 대화형 시각화
- **주요 도구**: Shiny, R 패키지
- **KBDS 지원**: ❌ 지원되지 않음 (실시간 분석모듈로 개인 환경에서 사용 권장)

### 7. <span style="color:#0846FA">WMS_TAXONOMY</span>
- **기능**: 전체 메타게놈 시퀀싱 데이터의 분류학적 프로파일링
- **주요 도구**: Kraken2, Bracken, Sylph
- **KBDS 지원**: ✅ 지원됨

### 8. <span style="color:#0846FA">INTERACTIVE_TAXONOMY</span>
- **기능**: 분류학적 프로파일의 대화형 분석 및 시각화
- **주요 도구**: Shiny, phyloseq, R 패키지
- **KBDS 지원**: ❌ 지원되지 않음 (실시간 분석모듈로 개인 환경에서 사용 권장)

### 9. <span style="color:#7030A0">WMS_FUNCTION</span>
- **기능**: 메타게놈의 기능적 프로파일링 및 경로 분석
- **주요 도구**: HUMAnN3, MetaPhlAn
- **KBDS 지원**: ✅ 지원됨

### 10. <span style="color:#7030A0">DOWNLOAD_DB</span> (독립 모듈)
- **기능**: 분석에 필요한 데이터베이스 다운로드
- **주요 데이터베이스**: Kraken2, GTDB, HUMAnN3, UniRef90
- **KBDS 지원**: ❌ 지원되지 않음 (KBDS에는 필요한 데이터베이스가 이미 설치됨)

## KBDS 시스템에서의 워크플로우 실행

KBDS 시스템에서는 실시간 분석 모듈 및 일부 모듈이 지원되지 않습니다. KBDS에서 지원되는 모듈은 다음과 같은 순서로 실행할 수 있습니다:

```bash
# 1. 품질 제어
metafun -module RAWREAD_QC -i /path/to/raw_reads

# 2. 어셈블리 및 빈닝
metafun -module ASSEMBLY_BINNING -i /path/to/filtered_reads

# 3. 빈 품질 평가
metafun -module BIN_ASSESSMENT -i /path/to/bins

# 4. 비교 주석
metafun -module COMPARATIVE_ANNOTATION -i /path/to/quality_bins -m metadata.csv --samplecol 1

# 5. 분류학적 프로파일링
metafun -module WMS_TAXONOMY -i /path/to/filtered_reads -m metadata.csv -c 1 -a 2

# 6. 기능적 프로파일링
metafun -module WMS_FUNCTION -i /path/to/filtered_reads -m metadata.csv -s 1 -a 2
```

## 대화형 분석 모듈

대화형 분석 모듈(<span style="color:#4E95D9">INTERACTIVE_COMPARATIVE</span> 및 <span style="color:#0846FA">INTERACTIVE_TAXONOMY</span>)은 KBDS 시스템에서 직접 실행할 수 없으며, 개인 환경에서 실행해야 합니다. 이러한 모듈은 KBDS에서 생성된 결과 파일을 로컬 환경으로 다운로드한 후 사용할 수 있습니다:

```bash
# 로컬 환경에서 대화형 분류 분석 실행
metafun -module INTERACTIVE_TAXONOMY -i /path/to/downloaded/wms_taxonomy_results

# 로컬 환경에서 대화형 비교 분석 실행
metafun -module INTERACTIVE_COMPARATIVE -i /path/to/downloaded/comparative_annotation_results
```

## 모듈 간 데이터 흐름

아래는 metaFun 워크플로우의 데이터 흐름을 보여줍니다:

```
RAWREAD_QC → ASSEMBLY_BINNING → BIN_ASSESSMENT → GENOME_SELECTOR → COMPARATIVE_ANNOTATION → INTERACTIVE_COMPARATIVE
                              ↘                                   ↗
                 RAWREAD_QC → WMS_TAXONOMY → INTERACTIVE_TAXONOMY
                 RAWREAD_QC → WMS_FUNCTION
```

KBDS 시스템에서는 GENOME_SELECTOR, INTERACTIVE_COMPARATIVE, INTERACTIVE_TAXONOMY 모듈을 제외한 나머지 모듈을 순차적으로 실행할 수 있습니다.
