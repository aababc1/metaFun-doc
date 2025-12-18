(WMS_STRAIN_description_kr)=

# <span style="color:#2FA4E7">WMS_STRAIN</span>

<img src="../../_static/metafun7_purple.png" style="height:200px; width:auto; float:right; margin-left:10px;" />
이 모듈은 InStrain을 사용하여 전장 메타게놈 시퀀싱 데이터의 균주 수준 분석을 제공하는 metaFun 파이프라인의 일부입니다.

## 개요
WMS_STRAIN 모듈은 미생물 집단 내 미세다양성(microdiversity)을 특성화하기 위한 균주 수준 분석을 수행합니다. InStrain을 활용하여 단일 염기 변이(SNV)를 프로파일링하고, 뉴클레오타이드 다양성 지표를 계산하며, 샘플 간 균주 집단을 비교합니다. 이 모듈은 선택압 분석을 위한 pN/pS 비율, 뉴클레오타이드 다양성(π) 값, 샘플 간 균주 공유 패턴을 포함한 종합적인 지표를 생성합니다.

## 모듈 실행

```{code-block} bash
# WMS_TAXONOMY의 phyloseq 객체를 사용한 기본 사용법
(metafun) metafun -module WMS_STRAIN -i results/metagenome/RAWREAD_QC/read_filtered \
    --phyloseq_object results/metagenome/WMS_TAXONOMY/phyloseq/phyloseq_object_sylph.RDS

# 사용자 정의 prevalence 필터링
(metafun) metafun -module WMS_STRAIN -i results/metagenome/RAWREAD_QC/read_filtered \
    --phyloseq_object results/metagenome/WMS_TAXONOMY/phyloseq/phyloseq_object_sylph.RDS \
    --prevalence_threshold 10 --min_abundance 0.001

# 외부 메타데이터 파일 사용
(metafun) metafun -module WMS_STRAIN -i results/metagenome/RAWREAD_QC/read_filtered \
    --phyloseq_object results/metagenome/WMS_TAXONOMY/phyloseq/phyloseq_object_sylph.RDS \
    -m metadata.csv -s 1

# CPU 리소스 지정
(metafun) metafun -module WMS_STRAIN -i results/metagenome/RAWREAD_QC/read_filtered \
    --phyloseq_object results/metagenome/WMS_TAXONOMY/phyloseq/phyloseq_object_sylph.RDS \
    -p 24
```

## 모듈 작동 순서

이 모듈은 다음 단계를 수행합니다:

1. **Prevalence 필터링** (phyloseq 객체로부터):
   - prevalence 임계값 기반 분류군 필터링 (기본값: 샘플의 5%)
   - 최소 풍부도 필터 적용 (기본값: 0.1%)
   - prevalent 분류군을 GTDB 게놈과 매칭
   - phyloseq 또는 외부 파일에서 샘플 메타데이터 추출

2. **게놈 준비**:
   - GTDB 데이터베이스에서 참조 게놈 가져오기
   - 게놈을 결합된 참조 FASTA로 연결
   - Scaffold-to-bin (STB) 매핑 파일 생성
   - 리드 매핑을 위한 Bowtie2 인덱스 구축

3. **유전자 주석**:
   - 개별 게놈에 대해 Prodigal 실행 (병렬화)
   - 유전자 예측 결과 연결 (단백질, 유전자, GFF)
   - 기능 주석을 위한 eggNOG-mapper 실행 (COG 카테고리)

4. **리드 매핑**:
   - Bowtie2를 사용하여 품질 필터링된 리드를 결합된 참조에 매핑
   - 각 샘플에 대해 정렬된 BAM 파일 생성
   - 효율적인 접근을 위한 인덱스 파일 생성

5. **InStrain 프로파일링** (개별 샘플):
   - 각 샘플을 프로파일링하여 균주 수준의 SNV 검출
   - [Nei and Li (1979)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1213565/) 방법으로 뉴클레오타이드 다양성(π) 계산
   - 선택압 평가를 위한 pN/pS 비율 계산
   - 유전자 수준 및 게놈 수준 지표 생성

6. **InStrain 비교** (샘플 간):
   - 모든 샘플 간 균주 집단 비교
   - 샘플 쌍 간 popANI 및 conANI 계산
   - 공유 균주 식별 (기본값: 99.999% popANI 임계값)
   - 다운스트림 분석을 위한 비교 행렬 생성

7. **데이터 집계** (시각화용):
   - 모든 샘플의 프로파일 결과 결합
   - GTDB 분류 및 샘플 메타데이터와 통합
   - INTERACTIVE_STRAIN 모듈용 RDS 파일 준비

## 매개변수
**`${launchDir}`은 metaFun을 실행하는 디렉토리로, 출력 기본 디렉토리로 활용됩니다.**

| 매개변수 | 설명 | 기본값 | 참고 |
|-----------|-------------|---------------|------|
| `-i, --input_dir` | 필터링된 리드가 포함된 입력 디렉토리 | 필수 | <span style="color:#FF0000">RAWREAD_QC</span> 워크플로우의 출력 |
| `--phyloseq_object` | WMS_TAXONOMY의 Phyloseq RDS 파일 | 필수 | prevalence 필터링을 위한 phyloseq 객체 경로 |
| `-m, --metadata` | 메타데이터 파일 경로 | 선택 사항 | CSV 파일; 제공하지 않으면 phyloseq에서 추출 |
| `-s, --sampleIDcolumn` | 메타데이터의 샘플 ID 열 번호 | `1` | 리드 파일 이름의 샘플 ID와 일치 |
| `--prevalence_threshold` | prevalence 최소 샘플 % | `5` | 분류군이 이 % 이상의 샘플에 존재해야 함 |
| `--min_abundance` | 최소 상대적 풍부도 임계값 | `0.001` | 0.1% 미만 풍부도의 분류군 필터링 |
| `--min_coverage` | InStrain 최소 커버리지 | `5` | 높을수록 더 신뢰성 있는 결과 |
| `--min_freq` | 최소 SNP 빈도 임계값 | `0.05` | 저빈도 변이 필터링 |
| `--min_read_ani` | 리드 할당을 위한 ANI 임계값 | `0.92` | 0.92=균주, 0.95=종, 0.99=클론 |
| `-p, --cpus` | 사용할 CPU 수 | 자동 감지 | 시스템 기능에 따라 조정 |
| `-o, --outdir` | 출력 디렉토리 | `"${launchDir}/results/metagenome/WMS_STRAIN"` | 결과가 저장될 위치 |

## **입력 및 출력**

### 입력
* 품질 제어된 페어드 엔드 메타게놈 리드 (<span style="color:#FF0000">RAWREAD_QC</span> 워크플로우의 출력)
* <span style="color:#2FA4E7">WMS_TAXONOMY</span>의 Phyloseq 객체 (분류 및 샘플 메타데이터 포함)
* 선택 사항: phyloseq 메타데이터를 대체할 외부 메타데이터 파일 (CSV 형식)

### 출력
* GTDB 게놈 매칭이 포함된 prevalent 분류군 목록
* 각 샘플에 대한 InStrain 프로파일 결과
* 게놈별 뉴클레오타이드 다양성 지표
* pN/pS 비율 테이블 (유전자 수준 및 게놈 전체)
* 균주 비교 행렬 (popANI, conANI)
* INTERACTIVE_STRAIN 시각화를 위한 전처리된 RDS 파일

### 출력 디렉토리 구조

출력은 다음 디렉토리 구조로 구성됩니다:

```{code-block} bash
:caption: 출력 디렉토리 구조

${launchDir}/results/metagenome/WMS_STRAIN/
├── 01_prevalent_taxa/                    # Prevalence 필터링 결과
│   ├── prevalent_taxa_taxonomy_ids.txt   # 필터링된 분류군 ID
│   ├── prevalent_taxa_metadata.tsv       # prevalent 분류군의 GTDB 메타데이터
│   ├── prevalent_taxa_genome_paths.txt   # GTDB 게놈 경로
│   ├── prevalence_summary.tsv            # Prevalence 통계
│   └── sample_metadata.csv               # 추출/제공된 샘플 메타데이터
├── 02_genome_prep/                       # 게놈 준비
│   ├── all_genomes_combined.fa           # 연결된 참조 게놈
│   ├── prevalent_taxa.stb               # Scaffold-to-bin 매핑
│   └── bowtie2_index/                    # Bowtie2 인덱스 파일
├── 03_gene_annotation/                   # 유전자 예측 및 주석
│   ├── genes.faa                         # 단백질 서열
│   ├── genes.fna                         # 유전자 서열
│   ├── genes.gff                         # 유전자 주석 (GFF 형식)
│   └── eggnog_results.emapper.annotations # eggNOG 기능 주석
├── 04_bam_files/                         # 리드 매핑 결과
│   ├── ${sample_id}.sorted.bam           # 정렬된 BAM 파일
│   └── ${sample_id}.sorted.bam.bai       # BAM 인덱스 파일
├── 05_instrain_profiles/                 # InStrain 프로파일 결과
│   ├── ${sample_id}_instrain_profile/    # 샘플별 프로파일 디렉토리
│   │   ├── output/                       # 주요 출력 파일
│   │   │   ├── ${sample_id}_genome_info.tsv    # 게놈 수준 지표
│   │   │   ├── ${sample_id}_gene_info.tsv      # 유전자 수준 지표
│   │   │   └── ${sample_id}_scaffold_info.tsv  # Scaffold 지표
│   │   └── raw_data/
│   │       └── genes_SNP_count.csv.gz    # pN/pS 계산을 위한 SNP 카운트
│   └── validation_summary.txt            # 프로파일 검증 결과
├── 06_instrain_compare/                  # InStrain 비교 결과
│   └── instrainComparer_output/
│       └── output/
│           ├── comparisonsTable.tsv      # 페어와이즈 샘플 비교
│           └── genomeWide_compare.tsv    # popANI/conANI 지표
└── 07_shiny_data/                        # 시각화를 위한 전처리된 데이터
    ├── integrated_microbiome_data.rds    # 결합된 R 데이터 객체
    ├── pN_pS_gene_level.rds              # 유전자 수준 pN/pS 데이터
    ├── pN_pS_genome_wide.rds             # 게놈 전체 pN/pS 데이터
    └── eggnog_annotations_subset.rds     # 필터링된 eggNOG 주석
```

## 주요 지표 설명

### 뉴클레오타이드 다양성 (π)
뉴클레오타이드 다양성은 [Nei and Li (1979)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1213565/) 방법을 사용하여 집단 내 유전적 변이를 측정합니다:

**공식**: π = 1 - Σ(각 염기의 빈도)²

InStrain은 충분한 커버리지(기본값 ≥5x)를 가진 모든 게놈 위치에서 π를 계산하고 유전자/게놈 전체의 평균을 구합니다. 이 지표는 샘플 간 커버리지 차이에 강건합니다.

- **높은 π**: 많은 SNV를 가진 다양한 균주 집단을 나타냄
- **낮은 π**: 균질한 집단 또는 최근의 선택적 스윕을 나타냄

### pN/pS 비율
비동의 치환과 동의 치환의 비율로, 선택압을 나타냅니다:
- **pN/pS < 1**: 정화 (음성) 선택 - 유해한 돌연변이 제거
- **pN/pS ≈ 1**: 중립 진화 - 선택압 없음
- **pN/pS > 1**: 양성 선택 - 유익한 돌연변이 선호

### Population ANI (popANI) 및 Consensus ANI (conANI)
InStrain은 균주 비교를 위해 두 가지 ANI 지표를 계산합니다:

- **popANI** (집단 수준 ANI): 주요 및 소수 대립유전자를 모두 고려하여 샘플 내 미세다양성을 설명합니다. popANI 치환은 샘플 간 공유 대립유전자가 없을 때만 호출됩니다.
- **conANI** (합의 ANI): 샘플 간 합의(주요) 대립유전자만 비교합니다. conANI 치환은 샘플의 주요 대립유전자가 다를 때 호출됩니다.

공유 균주 식별에는 **99.999% popANI** 기본 임계값이 권장됩니다. 자세한 내용은 [InStrain 문서](https://instrain.readthedocs.io/en/latest/important_concepts.html)를 참조하세요.

## <span style="color:#2FA4E7">WMS_STRAIN</span> 모듈의 Nextflow 프로세스

| 프로세스 | 입력 | 출력 | 참고 |
|---------|----------|-----------|------|
| prevalence_filter_phyloseq | Phyloseq RDS | `01_prevalent_taxa` | prevalence로 분류군 필터링 |
| concat_genomes | GTDB 게놈 경로 | `02_genome_prep` | 참조 게놈 연결 |
| generate_stb | GTDB 게놈 경로 | `02_genome_prep` | scaffold-to-bin 매핑 생성 |
| bowtie2_build | 결합된 FASTA | `02_genome_prep/bowtie2_index` | Bowtie2 인덱스 구축 |
| prodigal_per_genome | 개별 게놈 | 작업 디렉토리 | 유전자 예측 (병렬화) |
| concat_gene_predictions | Prodigal 출력 | `03_gene_annotation` | 유전자 예측 연결 |
| eggnog_mapper | 단백질 서열 | `03_gene_annotation` | 기능 주석 |
| bowtie2_mapping | 필터링된 리드 | `04_bam_files` | 참조에 리드 매핑 |
| instrain_profile | BAM 파일 | `05_instrain_profiles` | 균주 수준 변이 프로파일링 |
| validate_instrain_profiles | 프로파일 디렉토리 | `05_instrain_profiles` | 프로파일 검증 |
| instrain_compare | 유효한 프로파일 | `06_instrain_compare` | 샘플 간 균주 비교 |
| aggregate_for_shiny | 모든 출력 | `07_shiny_data` | 시각화 데이터 준비 |

## <span style="color:#2FA4E7">WMS_STRAIN</span>에서 사용된 도구

| 도구 | 목적 | 버전 | 기본 매개변수 | 선택 가능한 매개변수 |
|------|---------|---------|---------------------|--------------------------------|
| Bowtie2 | 리드 매핑 | 2.5+ | `--sensitive-local --no-unal` | `--threads ${task.cpus}` |
| InStrain | 균주 프로파일링 | 1.8+ | `--min_cov 5`, `--database_mode` | `-p ${task.cpus}`, `--min_read_ani` |
| Prodigal | 유전자 예측 | 2.6.3 | `-p single` (게놈별) | N/A |
| eggNOG-mapper | 기능 주석 | 2.1+ | `-m mmseqs` | `--cpu ${task.cpus}` |
| samtools | BAM 처리 | 1.17+ | `-@ ${task.cpus}` | N/A |

## 사용 참고 사항

- **<span style="color:#2FA4E7">WMS_STRAIN</span>** 모듈은 prevalence 필터링을 위해 <span style="color:#2FA4E7">WMS_TAXONOMY</span>의 phyloseq 객체가 필요합니다.
- Prevalent 분류군은 참조 기반 분석을 위해 자동으로 GTDB 게놈과 매칭됩니다.
- 메타데이터는 phyloseq 객체에서 추출하거나 `-m` 매개변수를 통해 별도로 제공할 수 있습니다.
- InStrain은 상당한 계산 리소스가 필요합니다. CPU 할당은 자동 감지되지만 `-p`로 조정할 수 있습니다.
- 높은 커버리지 샘플이 더 신뢰성 있는 균주 수준 지표를 제공합니다. 평균 커버리지 < 5x인 샘플은 균주 해상도가 제한될 수 있습니다.
- 모듈은 자동으로 InStrain 프로파일을 검증하고 유효한 프로파일이 2개 미만이면 비교를 건너뜁니다.
- 최적의 결과를 위해 풍부하고 prevalent한 분류군에 집중하도록 적절한 `--prevalence_threshold`를 사용하세요.

## 다음 단계

<span style="color:#2FA4E7">WMS_STRAIN</span> 실행 후:

1. **<span style="color:#2FA4E7">INTERACTIVE_STRAIN</span>** 모듈을 사용하여 결과를 대화형으로 탐색:
   ```bash
   (metafun) metafun -module INTERACTIVE_STRAIN -i results/metagenome/WMS_STRAIN/07_shiny_data
   ```

2. 심층 분석 수행:
   - 조건에 따른 뉴클레오타이드 다양성 패턴 조사
   - 선택을 받는 유전자 식별을 위한 pN/pS 비율 분석 (COG 기능 카테고리)
   - popANI 임계값을 사용한 샘플 그룹 간 균주 집단 비교
   - 균주 수준 지표와 메타데이터 변수의 상관관계 분석

<span style="color:#2FA4E7">WMS_STRAIN</span> 모듈은 미생물 군집 내 균주 수준 다양성에 대한 종합적인 통찰을 제공하여, 연구자들이 어떤 종이 존재하는지뿐만 아니라 해당 종 내의 유전적 변이를 이해할 수 있게 합니다.
